# gui/dashboard.py


"""Hauptfenster des Signal State Dashboards"""
"""
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from .window_settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from .functions import load_custom_font, apply_font_to_table
from .widgets import TitleBox, EgomotionBox, SensorConfigBox, PointcloudCheckbox
from .data_binding import DataBinding
from publisher.radar_status_reader import radar_status_reader
from publisher.can_msg_sender import can_msg_sender
import socket
import struct
import time


class Dashboard(QWidget):

    
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

        

        self.SOURCE_IP = "127.0.0.1"
        self.SOURCE_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def _create_widgets(self):
   
        # Titel
        self.title_box = TitleBox(self, self.gui_font)
        
        # Egomotion-Box
        self.egomotion_box = EgomotionBox(self, self.gui_font)
        
        # Sensor-Config-Box
        self.sensor_config_box = SensorConfigBox(self, self.gui_font)
        
        # Pointcloud-Checkbox
        self.checkbox = PointcloudCheckbox(self, self.gui_font, self.sensor_config_box)
    
    def _setup_data_binding(self):
     
        self.data_binding = DataBinding(
            self.sensor_config_box.table,
            self.egomotion_box.table,
            self.gui_font
        )
    
    def resizeEvent(self, event):
      
        super().resizeEvent(event)
        
        # Egomotion-Tabelle: 70% / 30%
        ego_width = self.egomotion_box.table.viewport().width()
        self.egomotion_box.table.setColumnWidth(0, int(ego_width * 0.7))
        self.egomotion_box.table.setColumnWidth(1, int(ego_width * 0.3))
        
        # Sensor-Config-Tabelle: 40% / 20% / 40%
        cfg_width = self.sensor_config_box.table.viewport().width()
        self.sensor_config_box.table.setColumnWidth(0, int(cfg_width * 0.4))
        self.sensor_config_box.table.setColumnWidth(1, int(cfg_width * 0.2))
        self.sensor_config_box.table.setColumnWidth(2, int(cfg_width * 0.4))
    
    def showEvent(self, event):
   
        super().showEvent(event)
        # Spaltenbreiten beim ersten Anzeigen setzen
        self.resizeEvent(None)
    
    def update_signal_status_values(self, values):
        if self.data_binding is not None:
            print(f"Val: {values}")
            self.data_binding.update_signal_status_values(values)
        
    
    def update_egomotion_values(self, values):
        if self.data_binding is not None:
            self.data_binding.update_egomotion_values(values)


    def update_radar_status_thread(self):
        arr = self.radar_obj.run()
        for radar_status in arr:
            self.update_signal_status_values(radar_status)

    def update_egomotion_value_thread(self):
        self.sock.bind((self.SOURCE_IP, self.SOURCE_PORT))

        print(f"Listening on {self.SOURCE_IP}:{self.SOURCE_PORT}")

        while True:
            data, addr = self.sock.recvfrom(1024)
            
            # 4 Bytes pro Float -> Little Endian
            num_floats = len(data) // 4
            egomotion_val_arr = struct.unpack("<" + "f"*num_floats, data)
            print(f"Egomotion Val Arr: {egomotion_val_arr}")
            self.update_egomotion_values(egomotion_val_arr)
"""


# gui/dashboard.py
"""Hauptfenster des Signal State Dashboards"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from .window_settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from .functions import load_custom_font, apply_font_to_table
from .widgets import TitleBox, EgomotionBox, SensorConfigBox, PointcloudCheckbox
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
        self.egomotion_box = EgomotionBox(self, self.gui_font)
        
        # Sensor-Config-Box
        self.sensor_config_box = SensorConfigBox(self, self.gui_font)
        
        # Pointcloud-Checkbox
        self.checkbox = PointcloudCheckbox(self, self.gui_font, self.sensor_config_box)
    
    def _setup_data_binding(self):
        """Initialisiert das Daten-Binding"""
        self.data_binding = DataBinding(
            self.sensor_config_box.table,
            self.egomotion_box.table,
            self.gui_font
        )
    
    def resizeEvent(self, event):
        """Passt Spaltenbreiten bei Größenänderung an"""
        super().resizeEvent(event)
        
        # Egomotion-Tabelle: 70% / 30%
        ego_width = self.egomotion_box.table.viewport().width()
        self.egomotion_box.table.setColumnWidth(0, int(ego_width * 0.7))
        self.egomotion_box.table.setColumnWidth(1, int(ego_width * 0.3))
        
        # Sensor-Config-Tabelle: 40% / 20% / 40%
        cfg_width = self.sensor_config_box.table.viewport().width()
        self.sensor_config_box.table.setColumnWidth(0, int(cfg_width * 0.4))
        self.sensor_config_box.table.setColumnWidth(1, int(cfg_width * 0.2))
        self.sensor_config_box.table.setColumnWidth(2, int(cfg_width * 0.4))
    
    def showEvent(self, event):
        """Wird aufgerufen, wenn das Fenster angezeigt wird"""
        super().showEvent(event)
        # Spaltenbreiten beim ersten Anzeigen setzen
        self.resizeEvent(None)
    
    # ================== GUI-Update Methoden ==================
    def update_signal_status_values(self, values):
        if self.data_binding is not None:
            self.data_binding.update_signal_status_values(values)
        
    def update_egomotion_values(self, values):
        if self.data_binding is not None:
            self.data_binding.update_egomotion_values(values)

    # ================== Thread-Methoden ==================
    def update_radar_status_thread(self):
        """Thread für Radar-Status"""
        while self.thread_running:
            arr = self.radar_obj.run()
            for radar_status in arr:
                # Thread-sicher: Signal emitten
                self.radar_status_updated.emit(radar_status)
            time.sleep(0.01)  # kleines Delay, um CPU-Last zu reduzieren

    def update_egomotion_value_thread(self):
        """Thread für Egomotion-Daten"""
        self.sock.bind((self.SOURCE_IP, self.SOURCE_PORT))
        print(f"Listening on {self.SOURCE_IP}:{self.SOURCE_PORT}")

        while self.thread_running:
            try:
                data, addr = self.sock.recvfrom(1024)
            except OSError:
                # Socket wurde möglicherweise geschlossen
                break

            # 4 Bytes pro Float -> Little Endian
            num_floats = len(data) // 4
            egomotion_val_tuple = struct.unpack("<" + "f"*num_floats, data)
            
            # Thread-sicher: Signal emitten, Typ muss Liste sein
            self.egomotion_values_updated.emit(list(egomotion_val_tuple))
            
            # Optional: kurze Pause, um CPU-Last zu reduzieren
            time.sleep(0.001)


    # ================== Fenster schließen ==================
    def closeEvent(self, event):
        """Stoppt Threads beim Schließen"""
        self.thread_running = False
        # Socket schließen
        try:
            self.sock.close()
        except:
            pass
        super().closeEvent(event)
