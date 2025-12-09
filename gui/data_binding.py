"""Daten-Binding und Live-Updates"""

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from .functions import create_table_item, get_status_description
from .window_settings import EGO_SIGNAL_UNITS


class DataBinding:
    """Verwaltet die Verbindung zwischen Daten und GUI-Elementen"""
    
    def __init__(self, sensor_config_tables, egomotion_tables, sensor_information_table, gui_font):
        self.sensor_config_tables = sensor_config_tables   # dict
        self.egomotion_tables = egomotion_tables           # dict
        self.sensor_information_table = sensor_information_table # dict
        self.gui_font = gui_font
    
    def update_signal_status_values(self, values):

        for key, table in self.sensor_config_tables.items():
            # jede Tabelle durchlaufen
            for i, val in enumerate(values):
                if i >= table.rowCount():
                    break
                
                # Status-Spalte
                status_item = create_table_item(
                    str(val), 
                    self.gui_font, 
                    status_value=str(val),
                    is_status=True
                )
                table.setItem(i, 1, status_item)

                # Farbe
                if int(val) != 0:
                    status_item.setForeground(QColor('red'))
                else:
                    status_item.setForeground(QColor('green'))
                
                # Description
                desc_val = int(val) if isinstance(val, (int, float, str)) else 0
                desc_text = get_status_description(desc_val)

                desc_item = QTableWidgetItem(desc_text)
                desc_item.setFont(self.gui_font)
                desc_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table.setItem(i, 2, desc_item)

    def update_egomotion_values(self, values):
        """Update für Ego-Motion Tabellen (beide Seiten)."""
        ego_signal_units_arr = EGO_SIGNAL_UNITS
        

        for key, table in self.egomotion_tables.items():
            for i, val in enumerate(values):
                if i >= table.rowCount():
                    break

                formatted_val = f"{val:.4f}"

                # Egomotion Item
                egomotion_value_item = create_table_item(
                    formatted_val,
                    self.gui_font,
                    status_value=str(val),
                    is_status=False
                )
                table.setItem(i, 2, egomotion_value_item)
                
                # Unit Item
                unit_item = create_table_item(
                    ego_signal_units_arr[i],
                    self.gui_font,
                    status_value=str(val),
                    is_status=False
                )
                table.setItem(i, 1, unit_item)

    def update_sensor_information_values(self, values):
        for key, table in self.sensor_information_table.items():
            for index, value in enumerate(values):
                    
                # Status-Spalte
                status_item = create_table_item(
                    str(value), 
                    self.gui_font, 
                    status_value=str(value),
                    is_status=True
                    )
                table.setItem(index, 1, status_item)
        
