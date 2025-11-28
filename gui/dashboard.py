# gui/dashboard.py
"""Hauptfenster des Signal State Dashboards"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from .window_settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from .functions import load_custom_font, apply_font_to_table
from .widgets import TitleBox, EgomotionBox, SensorConfigBox, PointcloudCheckbox
from .data_binding import DataBinding


class Dashboard(QWidget):
    """Hauptfenster des Dashboards"""
    
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
    
    def update_signal_status_values(self, values):
        """
        Öffentliche Methode für externe Updates der Sensor-Werte
        
        Args:
            values: Liste von Sensor-Werten
        """
        self.data_binding.update_signal_status_values(values)
    
    def update_egomotion_values(self, values):
        """
        Öffentliche Methode für externe Updates der Egomotion-Werte
        
        Args:
            values: Liste von Egomotion-Werten
        """
        self.data_binding.update_egomotion_values(values)