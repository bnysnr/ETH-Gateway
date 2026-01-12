# Script welches die UDP nachrichten auswertet und die gewünschten Sensorinformationen speichert

import socket
import struct
import sys
import time


MCAST_GRP = '239.22.0.3'
UDP_PORT = 40000
INTERFACE_IP = '192.168.16.5'

SENSOR_TIMEOUT = 2  # Sekunden ohne Daten = Fehler


class SensorInformationReader():
    def __init__(self):
        super().__init__()

        # An die Socket binden, um per Eth Schnittstelle die UDP Nachrichten zu empfangen
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', UDP_PORT))
        self.sock.settimeout(SENSOR_TIMEOUT)  # Timeout setzen!

        mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(INTERFACE_IP))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            
    
    def run(self, sensor_ip_adress, service_id, method_id, bitposition, bitsize):
        
        try:
            while True:
                try:
                    data, addr = self.sock.recvfrom(4096)
                    
                    # Nur Pakete vom gewünschten Sensor akzeptieren
                    #if addr[0] != sensor_ip_adress:
                    #    continue

                    self.last_any_data = time.time()

                    raw = data.hex()
                    
                    if not raw.startswith(service_id + method_id):
                        continue
                    
                    array_start_pos = round(bitposition / 8)                
                    array_offset = bitposition % 8                          
                    array_length = bitsize // 8                             
        
                    values = self.decode_values(raw)                        
                    start = array_start_pos + array_offset                  
                    end = start + array_length                              
                    yield values[start: end]
                    
                    # Nach erfolgreichem Yield die Schleife beenden (ein Wert pro Aufruf)
                    break
                    
                except socket.timeout:
                    # Timeout: Kein Paket vom Sensor erhalten
                    print(f"Timeout for sensor {sensor_ip_adress}")
                    raise StopIteration

        except Exception as e:
            print(f"Fehler im UDP Thread für {sensor_ip_adress}: {e}")
            raise StopIteration

    

    def decode_values(self, hexstring):
        return [hexstring[i:i+2] for i in range(0, len(hexstring), 2)]