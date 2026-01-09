import socket
import struct
import time
import threading

ALLOWED_IPS = {"192.168.16.15", "192.168.16.12", "192.168.16.13"}
MCAST_GRP = '239.22.0.3'
UDP_PORT = 40000
INTERFACE_IP = '192.168.16.5'

class available_sensors():
    def __init__(self):
        self.sensors = {}
        self.available_ips = []
        self.not_available_ips = []

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', UDP_PORT))
        
        mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(INTERFACE_IP))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        print("UDP Listener aktiv")
        
        while True:
            data, addr = sock.recvfrom(4096)
            ip = addr[0]
            if ip in ALLOWED_IPS:
                self.sensors[ip] = time.time()

    def check_available(self):
        while True:
            time.sleep(0.1)
            now = time.time()
            available = sorted([ip for ip in ALLOWED_IPS if (now - self.sensors.get(ip, 0)) < 1])
            
            if available != self.available_ips:
                # Finde neue offline IPs
                for ip in self.available_ips:
                    if ip not in available and ip not in self.not_available_ips:
                        self.not_available_ips.append(ip)
                
                # Entferne wieder online IPs aus not_available
                for ip in available:
                    if ip in self.not_available_ips:
                        self.not_available_ips.remove(ip)
                
                self.available_ips = available

    def get_available(self):
        return self.available_ips
    
    def get_not_available(self):
        return self.not_available_ips

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.check_available, daemon=True).start()

if __name__ == "__main__":
    sensor_obj = available_sensors()
    sensor_obj.start()
    
    while True:
        ips = sensor_obj.get_available()
        not_available = sensor_obj.get_not_available()
        print(f"Verfügbar: {ips}")
        print(f"Nicht mehr verfügbar: {not_available}")
        time.sleep(0.5)