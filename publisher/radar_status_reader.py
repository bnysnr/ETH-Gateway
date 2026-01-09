import socket
import struct
import sys
import time
from collections import defaultdict
from gui.window_settings import RADAR_STATUS_DEFAULT_VALUES


ALLOWED_IPS = {"192.168.16.15", "192.168.16.12", "192.168.16.13", "192.168.16.14", "192.168.16.11", "192.168.16.16"}

MCAST_GRP = '239.22.0.3'
UDP_PORT = 40000
INTERFACE_IP = '192.168.16.5'


SENSOR_TIMEOUT = 1  # Sekunden ohne Daten = Fehler


class radar_status_reader():
    def __init__(self):
        super().__init__()
        self.active_sensors = defaultdict(lambda: {"last_seen": 0, "warned": False})

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', UDP_PORT))

        mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(INTERFACE_IP))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock.settimeout(0.5)

    def run(self, service_id, bitposition, bitsize):
        """Liefert den genauen Wert aus der UDP Nachricht und extrahiert diesen"""
        print(f"Listening on multicast {MCAST_GRP}:{UDP_PORT} ...")
        print(f"Überwache nur folgende IP-Adressen: {ALLOWED_IPS}")
        
        # Initialisiere alle Sensoren mit last_seen
        for ip in ALLOWED_IPS:
            self.active_sensors[ip]["last_seen"] = time.time()
        
        try:
            while True:
                try:
                    data, addr = self.sock.recvfrom(4096)
                except socket.timeout:
                    # Überprüfe inaktive Sensoren und gebe Default-Werte zurück
                    for result in self.check_inactive_sensors():
                        yield result
                    continue
                
                sensor_ip = addr[0]
                
                # Nur erlaubte IPs verarbeiten
                if sensor_ip not in ALLOWED_IPS:
                    continue

                self.active_sensors[sensor_ip]["last_seen"] = time.time()
                self.active_sensors[sensor_ip]["warned"] = False  # Reset warning flag

                raw = data.hex()
                
                if not raw.startswith(service_id):
                    continue
                
                array_start_pos = round(bitposition / 8)
                array_offset = bitposition % 8
                array_length = bitsize // 8
    
                values = self.decode_values(raw)
                start = array_start_pos + array_offset
                end = start + array_length
                
                # Yield gibt IP-Adresse und Werte zurück
                yield (sensor_ip, values[start:end])

        except Exception as e:
            print(f"Fehler im UDP Thread: {e}")

    def check_inactive_sensors(self):
        """Überprüft inaktive Sensoren und gibt Default-Werte zurück"""
        current_time = time.time()
        yielded = False
        
        for ip in ALLOWED_IPS:
            info = self.active_sensors[ip]
            if (current_time - info["last_seen"]) > SENSOR_TIMEOUT:
                # Nur einmal warnen
                if not info["warned"]:
                    print(f"[{ip}] FEHLER: Sensor inaktiv (timeout) - verwende Default-Werte")
                    self.active_sensors[ip]["warned"] = True
                
                # Gebe Default-Werte zurück
                yield (ip, RADAR_STATUS_DEFAULT_VALUES)
                yielded = True

    def decode_values(self, hexstring):
        return [hexstring[i:i+2] for i in range(0, len(hexstring), 2)]


if __name__ == "__main__":
    radar_obj = radar_status_reader()
    
    # Generator konsumieren und Daten verarbeiten
  #  for sensor_ip, values in radar_obj.run("0007", 1231, 56):
  #      print(f"[{sensor_ip}] Empfangene Werte: {values}")