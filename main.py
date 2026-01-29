import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from gui.dashboard import SQCQ_DASHBOARD, SRR_FRONT, SRR_REAR, ARS_FRONT_REAR, BaseDashboard
from publisher.can_msg_sender import can_msg_sender
import threading
import socket
import struct
import time


class EgomotionDistributor:
    """Verteilt Egomotion-Daten von einem Socket an alle Dashboards"""
    def __init__(self):
        self.dashboards = []
        self.thread_running = True
        self.SOURCE_IP = "127.0.0.1"
        self.SOURCE_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def register_dashboard(self, dashboard):
        """Registriert ein Dashboard für Egomotion-Updates"""
        if dashboard not in self.dashboards:
            self.dashboards.append(dashboard)
    
    def run(self):
        """Hauptloop - empfängt Daten und verteilt an alle Dashboards"""
        self.sock.bind((self.SOURCE_IP, self.SOURCE_PORT))
        self.sock.settimeout(0.1)
        last_update_time = 0
        latest_values = None
        
        print(f"EgomotionDistributor läuft auf {self.SOURCE_IP}:{self.SOURCE_PORT}")
        
        while self.thread_running:
            try:
                data, _ = self.sock.recvfrom(1024)
                num_floats = len(data) // 4
                latest_values = struct.unpack("<" + "f" * num_floats, data)
            except socket.timeout:
                pass
            
            current_time = time.time()
            if latest_values and current_time - last_update_time >= 0.5:
                for dashboard in self.dashboards:
                    if hasattr(dashboard, 'distribute_egomotion_data'):
                        dashboard.distribute_egomotion_data(list(latest_values))
                last_update_time = current_time
    
    def stop(self):
        """Stoppt den Distributor"""
        self.thread_running = False
        try:
            self.sock.close()
        except:
            pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Zentral-Widget für MainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hauptlayout (vertikal)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # StackedWidget (nimmt den verfügbaren Platz ein)
        self.stacked_widget = QStackedWidget()
        
        # Seiten erstellen
        self.pages = [
            SQCQ_DASHBOARD(),       # Index 0
            SRR_FRONT(),            # Index 1
            SRR_REAR(),             # Index 2
            ARS_FRONT_REAR()        # Index 3
        ]
        
        for page in self.pages:
            self.stacked_widget.addWidget(page)
        
        main_layout.addWidget(self.stacked_widget)
        
        # Navigation-Bar UNTEN
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(10)
        
        # Stretch VOR den Buttons für Zentrierung
        nav_layout.addStretch()
        
        # Navigation-Buttons
        self.btn_sqcq = QPushButton("SQCQ")
        self.btn_srr_front = QPushButton("SRR Front Sensors")
        self.btn_srr_rear = QPushButton("SRR Rear Sensors")
        self.btn_ars_front_rear = QPushButton("ARS Sensors")
        
        button_style = "QPushButton { padding: 8px 15px; font-weight: bold; }"
        for btn in [self.btn_sqcq, self.btn_srr_front, self.btn_srr_rear, self.btn_ars_front_rear]:
            btn.setStyleSheet(button_style)
        
        nav_layout.addWidget(self.btn_sqcq)
        nav_layout.addWidget(self.btn_srr_front)
        nav_layout.addWidget(self.btn_srr_rear)
        nav_layout.addWidget(self.btn_ars_front_rear)
        
        # Stretch NACH den Buttons für Zentrierung
        nav_layout.addStretch()
        
        # Navigation-Layout zum Hauptlayout hinzufügen (UNTEN)
        main_layout.addLayout(nav_layout)
        
        # Button-Signale verbinden
        self.btn_sqcq.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_srr_front.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_srr_rear.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_ars_front_rear.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        
        # MainWindow-Einstellungen
        self.setWindowTitle(self.pages[1].windowTitle())
        self.setFixedSize(self.pages[1].width(), self.pages[1].height() + 50)
        
        # Egomotion Distributor erstellen
        self.egomotion_distributor = EgomotionDistributor()
        
        # Threads initialisieren
        self._start_threads()

    def _start_threads(self):
        """Startet alle Threads für alle Dashboard-Seiten"""
        # CAN Message Sender (global für alle Sensoren)
        can_sender = can_msg_sender()
        can_thread = threading.Thread(target=can_sender.start, daemon=True)
        can_thread.start()
        
        # Registriere alle BaseDashboard-Seiten beim Distributor
        for page in self.pages:
            if isinstance(page, BaseDashboard):
                self.egomotion_distributor.register_dashboard(page)
        
        # Starte Egomotion Distributor Thread (nur EINMAL!)
        egomotion_thread = threading.Thread(target=self.egomotion_distributor.run, daemon=True)
        egomotion_thread.start()
        
        # Starte andere Threads für jede BaseDashboard-Seite
        for page in self.pages:
            if isinstance(page, BaseDashboard):
                self._start_page_threads(page)

    def _start_page_threads(self, page: BaseDashboard):
        """Startet Threads für eine spezifische Dashboard-Seite (OHNE Egomotion)"""
        threads = [
            threading.Thread(target=page.update_radar_status_thread, daemon=True),
            threading.Thread(target=page.update_radar_signal_information_thread, daemon=True)
        ]
        
        for thread in threads:
            thread.start()


def main():
    """Startet die Anwendung"""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()