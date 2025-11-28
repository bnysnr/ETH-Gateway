# gui/data_binding.py
"""Daten-Binding und Live-Updates"""

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from .functions import create_table_item, get_status_description


class DataBinding:
    """Verwaltet die Verbindung zwischen Daten und GUI-Elementen"""
    
    def __init__(self, sensor_config_table, egomotion_table, gui_font):
        self.sensor_config_table = sensor_config_table
        self.egomotion_table = egomotion_table
        self.gui_font = gui_font
    
    def update_signal_status_values(self, values):
        """
        Aktualisiert die Sensor-Config-Tabelle mit neuen Werten
        
        Args:
            values: Liste von Werten (String oder Int)
        """
        for i, val in enumerate(values):
            if i >= self.sensor_config_table.rowCount():
                break
            
            # Status-Spalte
            status_item = create_table_item(
                str(val), 
                self.gui_font, 
                is_status=True,
                status_value=str(val)
            )
            self.sensor_config_table.setItem(i, 1, status_item)
            
            # Description-Spalte
            desc_text = get_status_description(int(val) if isinstance(val, str) and val.isdigit() else 0)
            desc_item = QTableWidgetItem(desc_text)
            desc_item.setFont(self.gui_font)
            desc_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.sensor_config_table.setItem(i, 2, desc_item)
    
    def update_egomotion_values(self, values):
        """
        Aktualisiert die Egomotion-Tabelle mit neuen Werten
        
        Args:
            values: Liste von Werten (als Strings)
        """
        for i, val in enumerate(values):
            if i >= self.egomotion_table.rowCount():
                break
            
            value_item = QTableWidgetItem(str(val))
            value_item.setFont(self.gui_font)
            value_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
