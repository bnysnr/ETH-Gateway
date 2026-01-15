import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from gui.dashboard import Dashboard, Page2, Page3, BaseDashboard
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
            print(f"Dashboard {dashboard.__class__.__name__} registriert für Egomotion-Updates")
    
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
                # Verteile Daten an ALLE registrierten Dashboards
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
        
        # Hauptlayout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Navigation-Bar
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(2, 2, 2, 2)
        nav_layout.setSpacing(5)
        
        # Navigation-Buttons
        self.btn_page1 = QPushButton("SRR Front Sensors")
        self.btn_page2 = QPushButton("SRR Rear Sensors")
        self.btn_page3 = QPushButton("ARS Sensors")
        
        button_style = "QPushButton { padding: 8px 15px; font-weight: bold; }"
        for btn in [self.btn_page1, self.btn_page2, self.btn_page3]:
            btn.setStyleSheet(button_style)
        
        nav_layout.addWidget(self.btn_page1)
        nav_layout.addWidget(self.btn_page2)
        nav_layout.addWidget(self.btn_page3)
        nav_layout.addStretch()
        
        main_layout.addLayout(nav_layout)
        
        # StackedWidget
        self.stacked_widget = QStackedWidget()
        
        # Seiten erstellen
        self.pages = [
            Dashboard(),  # Index 0
            Page2(),      # Index 1
            Page3()       # Index 2
        ]
        
        for page in self.pages:
            self.stacked_widget.addWidget(page)
        
        main_layout.addWidget(self.stacked_widget)
        
        # Button-Signale verbinden
        self.btn_page1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_page2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_page3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        # MainWindow-Einstellungen
        self.setWindowTitle(self.pages[0].windowTitle())
        self.setFixedSize(self.pages[0].width(), self.pages[0].height() + 50)
        
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
            # KEIN Egomotion Thread mehr - wird zentral verwaltet!
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