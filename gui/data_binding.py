"""Daten-Binding und Live-Updates"""

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from .functions import create_table_item, get_status_description
from .window_settings import EGO_SIGNAL_UNITS, SENSOR_SIGNAL_INFORMATION, EGO_SIGNALS, SENSOR_CONFIG_SIGNALS


class DataBinding:
    """Verwaltet die Verbindung zwischen Daten und GUI-Elementen"""
    
    def __init__(
        self,
        sensor_config_tables: dict,
        egomotion_tables: dict,
        sensor_information_tables: dict,
        gui_font
    ):
        self.sensor_config_tables = sensor_config_tables        # dict[str, QTableWidget]
        self.egomotion_tables = egomotion_tables                # dict[str, QTableWidget]
        self.sensor_information_tables = sensor_information_tables  # dict[str, QTableWidget]
        self.gui_font = gui_font

    # ----------------------------
    # Signal Status Werte
    # ----------------------------
    def update_signal_status_values(self, sensor_id: str, values: list):
        table = self.sensor_config_tables.get(sensor_id)
        if table is None:
            print(f"Keine Sensor-Config-Tabelle für '{sensor_id}'")
            return

        table.setRowCount(len(SENSOR_CONFIG_SIGNALS))  
        for i, val in enumerate(values):
            # Status Item
            status_item = create_table_item(
                str(val),
                self.gui_font,
                status_value=str(val),
                is_status=True
            )
            table.setItem(i, 1, status_item)

            # Farbe
            status_item.setForeground(QColor('red') if int(val) != 0 else QColor('green'))

            # Beschreibung
            desc_val = int(val) if isinstance(val, (int, float, str)) else 0
            desc_text = get_status_description(desc_val)

            desc_item = QTableWidgetItem(desc_text)
            desc_item.setFont(self.gui_font)
            desc_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table.setItem(i, 2, desc_item)

    # ----------------------------
    # Egomotion Werte 
    def update_egomotion_values(self, sensor_id: str, values: list):
        table = self.egomotion_tables.get(sensor_id)
        if table is None:
            print(f"Keine Egomotion-Tabelle für '{sensor_id}'")
            return

        # Tabelle immer auf 9 Zeilen setzen
        table.setRowCount(len(EGO_SIGNALS))

        for i in range(len(EGO_SIGNALS)):
            # Prüfe ob Index existiert
            if i >= len(values):
                val = None
            else:
                val = values[i]
            
            # Formatiere Wert oder zeige "None"
            if val == 'None' or val is None:
                formatted_val = "None"
            else:
                try:
                    formatted_val = f"{float(val):.4f}"
                except (ValueError, TypeError):
                    formatted_val = "None"

            # Wert Item
            value_item = create_table_item(
                formatted_val,
                self.gui_font,
                status_value=str(val),
                is_status=False
            )
            table.setItem(i, 2, value_item)

            # Einheit Item
            unit_item = create_table_item(
                EGO_SIGNAL_UNITS[i],
                self.gui_font,
                status_value=EGO_SIGNAL_UNITS[i],
                is_status=False
            )
            table.setItem(i, 1, unit_item)

    # ----------------------------
    # Sensorinformationen pro Sensor
    # ----------------------------
    def update_sensor_information_values(self, sensor_id: str, values: list):
        table = self.sensor_information_tables.get(sensor_id)
        if table is None:
            print(f"Keine Sensor-Information-Tabelle für '{sensor_id}'")
            return

        table.setRowCount(len(SENSOR_SIGNAL_INFORMATION)) 
        for index, value in enumerate(values):
            status_item = create_table_item(
                str(value),
                self.gui_font,
                status_value=str(value),
                is_status=True
            )
            table.setItem(index, 1, status_item)

            # Farbe für Kalibrierung
            if index == 7:
                status_item.setForeground(QColor('green') if str(value) == "Connected" else QColor('red'))
