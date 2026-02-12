import cantools
import can
import socket
import struct
import time
import threading


# Singleton-Instanz
_can_sender_instance = None
_instance_lock = threading.Lock()

def get_can_msg_sender():
    """Gibt die globale Singleton-Instanz zurück"""
    global _can_sender_instance
    if _can_sender_instance is None:
        with _instance_lock:
            if _can_sender_instance is None:
                _can_sender_instance = can_msg_sender()
    return _can_sender_instance


class AvailableSensors:
    """Multicast-basierter Radar-IP-Scanner"""
    
    ALLOWED_IPS = {"192.168.16.11", "192.168.16.12", "192.168.16.13", "192.168.16.14", "192.168.16.15", "192.168.16.16"}
    MCAST_GRP = '239.22.0.3'
    UDP_PORT = 40000
    INTERFACE_IP = '192.168.16.5'
    
    def __init__(self):
        self.sensors = {}
        self.available_ips = []
        self.not_available_ips = []
        self._running = False
        self._listener_thread = None
        self._checker_thread = None
       

    def listen(self):
        """Empfängt Multicast-Heartbeats von Radar-Sensoren"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.UDP_PORT))
        
        mreq = struct.pack("4s4s", socket.inet_aton(self.MCAST_GRP), socket.inet_aton(self.INTERFACE_IP))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        print(f"Radar IP-Scanner aktiv (Multicast {self.MCAST_GRP}:{self.UDP_PORT})")
        
        while self._running:
            try:
                sock.settimeout(0.5)
                data, addr = sock.recvfrom(4096)
                ip = addr[0]
                if ip in self.ALLOWED_IPS:
                    self.sensors[ip] = time.time()
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    print(f"Listener Fehler: {e}")
        
        sock.close()

    def check_available(self):
        """Prüft kontinuierlich, welche Sensoren verfügbar sind"""
        while self._running:
            time.sleep(0.1)
            now = time.time()
            available = sorted([ip for ip in self.ALLOWED_IPS if (now - self.sensors.get(ip, 0)) < 1.5])
            
            if available != self.available_ips:
                # Neue offline IPs
                for ip in self.available_ips:
                    if ip not in available and ip not in self.not_available_ips:
                        self.not_available_ips.append(ip)
                        print(f"Radar {ip} offline")
                
                # Wieder online IPs
                for ip in available:
                    if ip in self.not_available_ips:
                        self.not_available_ips.remove(ip)
                        print(f"Radar {ip} wieder online")
                    elif ip not in self.available_ips:
                        print(f"Radar {ip} gefunden")
                
                self.available_ips = available

    def get_available(self):
        """Gibt Liste der verfügbaren Radar-IPs zurück"""
        return self.available_ips.copy()
    
    def get_not_available(self):
        """Gibt Liste der nicht verfügbaren Radar-IPs zurück"""
        return self.not_available_ips.copy()

    def start(self):
        """Startet den IP-Scanner"""
        if self._running:
            return
        
        self._running = True
        self._listener_thread = threading.Thread(target=self.listen, daemon=True)
        self._checker_thread = threading.Thread(target=self.check_available, daemon=True)
        self._listener_thread.start()
        self._checker_thread.start()

    def stop(self):
        """Stoppt den IP-Scanner"""
        self._running = False
        if self._listener_thread:
            self._listener_thread.join(timeout=2)
        if self._checker_thread:
            self._checker_thread.join(timeout=2)

    def wait_for_radars(self, timeout=5):
        """Wartet bis mindestens ein Radar gefunden wurde"""
        print(f"Warte auf Radar-Heartbeats (max. {timeout}s)...")
        start = time.time()
        while time.time() - start < timeout:
            if self.available_ips:
                print(f"{len(self.available_ips)} Radare gefunden: {self.available_ips}")
                return True
            time.sleep(0.2)
        print(" Keine Radare gefunden!")
        return False


class can_msg_sender():

    def __init__(self):
        super().__init__()
        self.vhc_can_val_arr = []
        self.running = False
        self.radar_ips = []
        self.lock = threading.Lock()
        
        # Radar IP-Scanner
        self.ip_scanner = AvailableSensors()

        # Konstanten
        self.SOURCE_IP = "192.168.16.5"
        self.SOURCE_PORT = 2001
        self.DEST_PORT = 60000
        self.INTERFACE = b"eth0.34\0"  # VLAN 34

        self.SERVICE_ID_EGOMOTION = 0x0002
        self.SERVICE_ID_SENSOR_CONFIG_MSG_STATUS = 0x0007
        self.METHOD_ID = 0x1000
        self.CLIENT_ID = 0x0000
        self.SESSION_ID = 0x0000
        self.PROTOCOL_VERSION = 0x01
        self.INTERFACE_VERSION = 0x01
        self.MESSAGE_TYPE = 0x02
        self.RETURN_CODE = 0x00
        self.DATA_ID = 0x03E8
        self.E2E_PAYLOAD_LENGTH = 73

        self.DBC_PATH = '/home/admin/ETH-Gateway/assets/dbc/J1939_MAN_1.dbc'
        self.SIGNALS_FILE = '/home/admin/ETH-Gateway/assets/signals/required_signals.txt'
        self.CAN_CHANNEL = 'can0'

        self.UDP_OUT_IP = "127.0.0.1"     
        self.UDP_OUT_PORT = 5005          
        self.udp_sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.vdy_ethernet_parameter_arr = [0]
        
        # NEU: Sendeintervall 20ms (50 Hz)
        self.SEND_INTERVAL = 0.020  # 20ms

    # CRC16 Algorithmus
    def calc_crc16(self, data: bytes) -> int:
        crc = 0xFFFF
        for byte in data:
            crc ^= byte << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = ((crc << 1) ^ 0x1021) & 0xFFFF
                else:
                    crc = (crc << 1) & 0xFFFF
        return crc

    def float_to_uint32_le(self, value: float) -> int:
        """Float -> 4 Byte Little Endian (uint32)"""
        return struct.unpack("<I", struct.pack("<f", value))[0]

    def get_available_radar_ips(self):
        """Gibt aktuell verfügbare Radar-IPs zurück"""
        return self.ip_scanner.get_available()

    # -------------------- Initialisierung --------------------
    def load_dbc_and_signals(self):
        """Lädt DBC und ermittelt relevante CAN-IDs"""
        db = cantools.database.load_file(self.DBC_PATH)
        print(f"DBC geladen: {len(db.messages)} Messages\n")

        with open(self.SIGNALS_FILE, 'r') as f:
            required_signals = [line.strip() for line in f if line.strip()]

        print(f"Required Signals: {required_signals}\n")

        relevant_message_ids = set()
        signal_info = {}

        for signal_name in required_signals:
            for message in db.messages:
                for signal in message.signals:
                    if signal.name == signal_name:
                        relevant_message_ids.add(message.frame_id)
                        signal_info[signal_name] = {
                            'message_id': message.frame_id,
                            'message_name': message.name,
                            'unit': signal.unit or ''
                        }
                        break

        return db, relevant_message_ids, signal_info, required_signals

    def init_can_bus(self):
        """Initialisiert die CAN-Schnittstelle"""
        return can.interface.Bus(channel=self.CAN_CHANNEL, interface='socketcan')

    def init_udp_socket(self):
        """Erzeugt und bindet den UDP-Socket"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, 25, self.INTERFACE)      # zum Anzeigen der Egomotion Daten per Ethernet-Vektor Box die Zeile auskommentieren
        sock.bind((self.SOURCE_IP, self.SOURCE_PORT))
        return sock

    # -------------------- SOME/IP Aufbau --------------------
    def build_someip_payload(self, signal_names, vdy_signal_parameters, qf_signals_list, sqc):
        """Erstellt SOME/IP Payload dynamisch basierend auf signal_names"""
        float_signals_list = [self.float_to_uint32_le(v) for v in vdy_signal_parameters]
        E2E_PAYLOAD_RAW = b''.join(struct.pack("<I", v) for v in float_signals_list)
        E2E_PAYLOAD_RAW += b''.join(struct.pack("B", qf) for qf in qf_signals_list)

        if len(E2E_PAYLOAD_RAW) < self.E2E_PAYLOAD_LENGTH:
            E2E_PAYLOAD_RAW += bytes(self.E2E_PAYLOAD_LENGTH - len(E2E_PAYLOAD_RAW))
        elif len(E2E_PAYLOAD_RAW) > self.E2E_PAYLOAD_LENGTH:
            print(f"E2E payload länger ({len(E2E_PAYLOAD_RAW)}) als erwartet ({self.E2E_PAYLOAD_LENGTH})")

        header_part2 = struct.pack("!HHBBBB",
                                self.CLIENT_ID, self.SESSION_ID,
                                self.PROTOCOL_VERSION, self.INTERFACE_VERSION,
                                self.MESSAGE_TYPE, self.RETURN_CODE)

        crc_input = (
            header_part2 +
            struct.pack("<H", len(E2E_PAYLOAD_RAW)) +
            struct.pack("B", sqc) +
            E2E_PAYLOAD_RAW +
            struct.pack("<H", self.DATA_ID)
        )

        crc = self.calc_crc16(crc_input)
        e2e_header = struct.pack(">HHB", crc, self.E2E_PAYLOAD_LENGTH, sqc)
        someip_payload = e2e_header + E2E_PAYLOAD_RAW

        message_id = (self.SERVICE_ID_EGOMOTION << 16) | self.METHOD_ID
        someip_length = len(header_part2) + len(someip_payload)
        header_part1 = struct.pack("!II", message_id, someip_length)

        for name, val in zip(signal_names, vdy_signal_parameters):
            print(f" {name:30s}: {val:10.3f}")
        print('*' * 40)
        print(f"Geschwindigkeit: {vdy_signal_parameters[7]}")

        vdy_signal_parameters[3] += self.vdy_ethernet_parameter_arr[0]
        vdy_signal_parameters[4] += self.vdy_ethernet_parameter_arr[0]
        vdy_signal_parameters[5] += self.vdy_ethernet_parameter_arr[0]
        vdy_signal_parameters[6] += self.vdy_ethernet_parameter_arr[0]

        return header_part1 + header_part2 + someip_payload

    # -------------------- Sender --------------------
    def send_udp_to_all(self, sock, payload):
        """Sendet Payload direkt an alle verfügbaren Radar-IPs ohne Threading"""
        current_radars = self.ip_scanner.get_available()
        
        if not current_radars:
            return
        
        # Direkt senden ohne Thread-Overhead
        for radar_ip in current_radars:
            try:
                sock.sendto(payload, (radar_ip, self.DEST_PORT))
            except Exception as e:
                print(f"Fehler beim Senden an {radar_ip}: {e}")

    # -------------------- NEU: CAN-Empfänger Thread --------------------
    def can_receiver_thread(self, db, bus, relevant_message_ids, signal_names):
        """Separater Thread: Empfängt CAN-Nachrichten und aktualisiert Werte"""
        vdy_signal_parameters = [0.0] * len(signal_names)
        
        try:
            while self.running:
                msg = bus.recv(timeout=0.1)
                if msg is None:
                    continue

                if msg.arbitration_id not in relevant_message_ids:
                    continue

                decoded = db.decode_message(msg.arbitration_id, msg.data)

                # Dynamisch über alle Signale iterieren
                for idx, signal_name in enumerate(signal_names):
                    if signal_name in decoded:
                        value = decoded[signal_name]
                        
                        # Geschwindigkeit direkt beim Empfang umrechnen (Index 7)
                        if idx == 7:
                            print(f"Speed vom CAN (km/h): {value}")
                            value = value / 3.6  # km/h -> m/s
                            print(f"Speed umgerechnet (m/s): {value}")
                        
                        if idx == 3 or idx == 4 or idx == 5 or idx == 6:
                            print(f"Wheel Velocity (m/s): {value}")
                            value = value / 3.6  # km/h -> m/s
                            value += vdy_signal_parameters[7]
                            print(f"Speed umgerechnet (m/s) nach addition: {value}")

                        vdy_signal_parameters[idx] = value

                # Thread-sicher aktualisieren
                with self.lock:
                    self.vhc_can_val_arr = vdy_signal_parameters.copy()

        except Exception as e:
            print(f"CAN Receiver Fehler: {e}")
        finally:
            bus.shutdown()

    # -------------------- NEU: 20ms Sender Thread --------------------
    def periodic_sender_thread(self, sock, signal_names):
        """Separater Thread: Sendet alle 20ms die aktuellen Werte"""
        qf_signals_list = [0x00] * len(signal_names)
        sqc = 0
        
        try:
            while self.running:
                start_time = time.time()
                
                # Aktuelle Werte holen (thread-safe)
                with self.lock:
                    vdy_signal_parameters = self.vhc_can_val_arr.copy() if self.vhc_can_val_arr else [0.0] * len(signal_names)
                
                # SOME/IP Nachricht aufbauen
                udp_payload = self.build_someip_payload(signal_names, vdy_signal_parameters, qf_signals_list, sqc)
                print(f"UDP PAYLOAD Ausgabe: {vdy_signal_parameters}")
                
                # An lokalen UDP-Port senden
                float_payload = b''.join(struct.pack("<f", v) for v in vdy_signal_parameters)
                self.udp_sender_sock.sendto(float_payload, (self.UDP_OUT_IP, self.UDP_OUT_PORT))
                
                # An alle Radars senden
                self.send_udp_to_all(sock, udp_payload)
                
                sqc = (sqc + 1) % 256
                
                # Präzises Timing: Wartet genau bis 20ms vergangen sind
                elapsed = time.time() - start_time
                sleep_time = self.SEND_INTERVAL - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    print(f"⚠️ Warnung: Sendezyklen überschritten um {-sleep_time*1000:.1f}ms")

        except Exception as e:
            print(f"Periodic Sender Fehler: {e}")
        finally:
            sock.close()

    def get_vhc_can_val_arr(self):
        """Gibt aktuelle CAN-Werte zurück"""
        with self.lock:
            return self.vhc_can_val_arr.copy()

    def set_vhc_can_val_arr(self, arr):
        """Setzt CAN-Werte"""
        with self.lock:
            self.vhc_can_val_arr = arr

    def start(self):
        """Startet den CAN-Sender in separaten Threads"""
        if self.running:
            print("Already running!")
            return
        
        # IP-Scanner starten
        print("=" * 60)
        self.ip_scanner.start()
        
        # Auf Radars warten (mit Timeout)
        if not self.ip_scanner.wait_for_radars(timeout=2):
            print("Fahre ohne Radars fort (werden im Betrieb erkannt)")
        
        print("=" * 60)
        
        # DBC und Signale laden
        db, relevant_message_ids, signal_info, signal_names = self.load_dbc_and_signals()
        
        # Bus und Socket initialisieren
        bus = self.init_can_bus()
        sock = self.init_udp_socket()
        
        self.running = True
        
        # NEU: Zwei separate Threads
        # Thread 1: CAN-Empfänger (liest CAN-Bus und aktualisiert Werte)
        can_thread = threading.Thread(
            target=self.can_receiver_thread,
            args=(db, bus, relevant_message_ids, signal_names),
            daemon=False
        )
        can_thread.start()
        print("CAN-Receiver Thread gestartet")
        
        # Thread 2: Periodischer Sender (sendet alle 20ms)
        sender_thread = threading.Thread(
            target=self.periodic_sender_thread,
            args=(sock, signal_names),
            daemon=False
        )
        sender_thread.start()
        print("Periodic Sender Thread gestartet (20ms Intervall / 50 Hz)")

    def stop(self):
        """Stoppt den CAN-Sender"""
        self.running = False
        self.ip_scanner.stop()
        print("Wird beendet...")


if __name__ == "__main__":
    obj = get_can_msg_sender()
    obj.start()
    try:
        while True:
            time.sleep(5)
            available = obj.get_available_radar_ips()
            print(f"\n[Status] Aktive Radars: {len(available)} - {available}")
    except KeyboardInterrupt:
        obj.stop()