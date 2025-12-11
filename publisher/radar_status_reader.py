import socket
import struct
import sys
import time


sensor_ips = {"192.168.16.15", "192.168.16.12", "192.168.16.13", "192.168.16.14"}

MCAST_GRP = '239.22.0.3'
UDP_PORT = 40000
INTERFACE_IP = '192.168.16.5'

SENSOR_TIMEOUT = 2  # Sekunden ohne Daten = Fehler


class radar_status_reader():
    def __init__(self):
        super().__init__()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', UDP_PORT))

        mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(INTERFACE_IP))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

                

    def run(self, service_id, bitposition, bitsize):
        # Liefert den genauen Wert aus der UDP Nachricht und extrahiert diesen
        print(f"Listening on multicast {MCAST_GRP}:{UDP_PORT} ...")
        try:
            while True:
                data, addr = self.sock.recvfrom(4096)
                if addr[0] not in sensor_ips:
                    continue

                self.last_any_data = time.time()

                raw = data.hex()
                
                if not raw.startswith(service_id):
                    continue
                array_start_pos = round(bitposition / 8)
                array_offset = bitposition % 8
                array_length = bitsize // 8
    
                values = self.decode_values(raw)
                start = array_start_pos + array_offset
                end = start + array_length
                yield values[start: end] 

        except Exception as e:
            print(f"Fehler im UDP Thread: {e}")

    def decode_values(self, hexstring):
        return [hexstring[i:i+2] for i in range(0, len(hexstring), 2)]


if __name__ == "__main__":
    radar_obj = radar_status_reader()
    radar_obj.run()


