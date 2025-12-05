from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from .window_settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from .functions import load_custom_font, apply_font_to_table
from .widgets import TitleBox, Egomotion_SRR_FL, Egomotion_SRR_FR, SignalStatus_SRR_FL, SignalStatus_SRR_FR, Pointcloud_SRR_FL, Pointcloud_SRR_FR, SensorInformationTable_SRR_FL, SensorInformationTable_SRR_FR
from .data_binding import DataBinding
from publisher.radar_status_reader import radar_status_reader
from publisher.can_msg_sender import can_msg_sender
import socket
import struct
import time


class Dashboard(QWidget):
    """Hauptfenster des Dashboards"""
    
    # Signale für thread-sichere Updates
    radar_status_updated = pyqtSignal(list)
    egomotion_values_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        
        # Schriftart laden
        self.gui_font = load_custom_font()
        QApplication.instance().setFont(self.gui_font)
        
        # Fenster-Einstellungen
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # GUI aufbauen
        self._create_widgets()
        self._setup_data_binding()
        self.radar_obj = radar_status_reader()
        self.can_egomotion_obj = can_msg_sender() 

        # Netzwerk-Einstellungen
        self.SOURCE_IP = "127.0.0.1"
        self.SOURCE_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Threads-Flags
        self.thread_running = True

        # Signale verbinden
        self.radar_status_updated.connect(self.update_signal_status_values)
        self.egomotion_values_updated.connect(self.update_egomotion_values)
    
    def _create_widgets(self):
        """Erstellt alle GUI-Komponenten"""
        # Titel
        self.title_box = TitleBox(self, self.gui_font)
        
        # Egomotion-Box
        self.egomotion_box_srr_fl = Egomotion_SRR_FL(self, self.gui_font)
        self.egomotion_box_srr_fr = Egomotion_SRR_FR(self, self.gui_font)

        
        # Sensor-Config-Box
        self.signalstatus_box_srr_fl = SignalStatus_SRR_FL(self, self.gui_font)
        self.signalstatus_box_srr_fr = SignalStatus_SRR_FR(self, self.gui_font)
        
        # Pointcloud-Checkbox
        # Pointcloud-Checkboxen korrekt erzeugen
        self.checkbox_srr_fl = Pointcloud_SRR_FL(self, self.gui_font, self.signalstatus_box_srr_fl)
        self.checkbox_srr_fr = Pointcloud_SRR_FR(self, self.gui_font, self.signalstatus_box_srr_fr)

        # Sensorinformation Tabelle
        self.sensor_information_table_srr_fl = SensorInformationTable_SRR_FL(self, self.gui_font)
        self.sensor_information_table_srr_fr = SensorInformationTable_SRR_FR(self, self.gui_font)

    # Data Bindiung für die Sensor Information Tabelle noch implementieren
    def _setup_data_binding(self):
        """Initialisiert das Daten-Binding"""
        self.data_binding = DataBinding(
        {
            "signal_status_srr_fl": self.signalstatus_box_srr_fl.table,
            "signal_status_srr_fr": self.signalstatus_box_srr_fr.table,
        },
        {
            "egomotion_srr_fl": self.egomotion_box_srr_fl.table,
            "egomotion_srr_fr": self.egomotion_box_srr_fr.table,
        },
        {
            "sensor_information_srr_fl": self.sensor_information_table_srr_fl,
            "sensor_information_srr_fr" : self.sensor_information_table_srr_fr,
        },
        self.gui_font
        )
    
    def resizeEvent(self, event):
        """Passt Spaltenbreiten bei Größenänderung an"""
        super().resizeEvent(event)
        
        # Egomotion-Tabelle (Spaltenverhältnisse)
        # SRR - FL
        ego_width = self.egomotion_box_srr_fl.table.viewport().width()
        self.egomotion_box_srr_fl.table.setColumnWidth(0, int(ego_width * 0.6))
        self.egomotion_box_srr_fl.table.setColumnWidth(1, int(ego_width * 0.4))

        # SRR - FR
        self.egomotion_box_srr_fr.table.setColumnWidth(0, int(ego_width * 0.6))
        self.egomotion_box_srr_fr.table.setColumnWidth(1, int(ego_width * 0.4))
        

        # Signal Status Tabelle (Spaltenverhältnisse)
        # SRR - FL
        signal_status_width = self.signalstatus_box_srr_fl.table.viewport().width()
        self.signalstatus_box_srr_fl.table.setColumnWidth(0, int(signal_status_width * 0.4))
        self.signalstatus_box_srr_fl.table.setColumnWidth(1, int(signal_status_width * 0.2))
        self.signalstatus_box_srr_fl.table.setColumnWidth(2, int(signal_status_width * 0.4))

        # SRR - FR
        self.signalstatus_box_srr_fr.table.setColumnWidth(0, int(signal_status_width * 0.4))
        self.signalstatus_box_srr_fr.table.setColumnWidth(1, int(signal_status_width * 0.2))
        self.signalstatus_box_srr_fr.table.setColumnWidth(2, int(signal_status_width * 0.4))

        # Sensorinformation Tabelle (Spaltenverhätltnisse)
        sensor_information_width = self.sensor_information_table_srr_fr.table.viewport().width()
        self.sensor_information_table_srr_fl.table.setColumnWidth(0, int(sensor_information_width * 0.6))
        self.sensor_information_table_srr_fl.table.setColumnWidth(1, int(sensor_information_width * 0.4))

        self.sensor_information_table_srr_fr.table.setColumnWidth(0, int(sensor_information_width * 0.6))
        self.sensor_information_table_srr_fr.table.setColumnWidth(1, int(sensor_information_width * 0.4))

                   


        
    def showEvent(self, event):
        """Wird aufgerufen, wenn das Fenster angezeigt wird"""
        super().showEvent(event)
        # Spaltenbreiten beim ersten Anzeigen setzen
        self.resizeEvent(None)
    
    # GUI-Update Methoden
    def update_signal_status_values(self, values):
        if self.data_binding is not None:
            self.data_binding.update_signal_status_values(values)
        
    def update_egomotion_values(self, values):
        if self.data_binding is not None:
            self.data_binding.update_egomotion_values(values)


    def update_radar_status_thread(self):
        """Thread für Radar-Status"""
        while self.thread_running:
            arr = self.radar_obj.run()
            for radar_status in arr:
                # Signal emitten
                self.radar_status_updated.emit(radar_status)
            time.sleep(0.2)  


    def update_egomotion_value_thread(self):
        self.sock.bind((self.SOURCE_IP, self.SOURCE_PORT))
        self.sock.settimeout(0.1)  # kurzes Timeout, um Thread nicht zu blockieren

        last_update_time = 0
        latest_values = None

        while self.thread_running:
            try:
                data, addr = self.sock.recvfrom(1024)
                num_floats = len(data) // 4
                latest_values = struct.unpack("<" + "f"*num_floats, data)
            except socket.timeout:
                pass  # keine Nachricht, weiter zum Timer-Check

            current_time = time.time()
            if latest_values and (current_time - last_update_time >= 0.5):
                self.egomotion_values_updated.emit(list(latest_values))
                last_update_time = current_time


    # Fenster schließen
    def closeEvent(self, event):
        """Stoppt Threads beim Schließen"""
        self.thread_running = False

        try:
            self.sock.close()
        except:
            pass
        super().closeEvent(event)
