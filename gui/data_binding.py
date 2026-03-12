"""Daten-Binding und Live-Updates"""

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from .functions import create_table_item, get_signal_status_description, get_sensor_operation_mode_description, get_blockage_state_description, get_blockage_state_selftest_description
from .window_parameter import EGO_SIGNAL_UNITS, SENSOR_SIGNAL_INFORMATION, EGO_SIGNALS, SENSOR_CONFIG_SIGNALS, SENSOR_OPERATION_MODE, BLOCKAGE_STATE, BLOCKAGE_STATE_SELFTEST

AZIMUTH_ELEVATION_RESOLUTION = 0.0000063935301747158
AZIMUTH_ELEVATION_OFFSET = -0.21


class DataBinding:
    # Schnittstelle zwischen Daten und GUI-Elementen
    
    def __init__(
        self,
        sensor_config_tables: dict,
        egomotion_tables: dict,
        sensor_information_tables: dict,
        gui_font
    ):

        self.sensor_config_tables = sensor_config_tables        
        self.egomotion_tables = egomotion_tables                
        self.sensor_information_tables = sensor_information_tables
        self.gui_font = gui_font


    # Signal Status Werte
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
            desc_text = get_signal_status_description(desc_val)

            desc_item = QTableWidgetItem(desc_text)
            desc_item.setFont(self.gui_font)
            desc_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table.setItem(i, 2, desc_item)


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


    def format_sensor_information_arr(self, arr):
        """Formatiert Sensor-Informations-Array mit Fehlerbehandlung"""
        try:
            # Index 0: Software Version
            if arr[0] is not None:
                arr[0] = arr[0][::-1]  # Bytes umdrehen
                software_version_number = [int(x, 16) for x in arr[0]]
                software_version_final = '.'.join(str(x) for x in software_version_number)
                arr[0] = software_version_final
            else:
                arr[0] = "UNKNOWN"
            
            # Index 1: Operation Mode
            if arr[1] is not None:
                arr[1] = int(arr[1])
            else:
                arr[1] = "UNKNOWN"
            
            # Index 2: Azimuth (Hex-Wert)
            if arr[2] is not None and isinstance(arr[2], str):
                arr[2] = arr[2][::-1]
                arr[2] = ' '.join(str(x) for x in arr[2])
            else:
                arr[2] = "UNKNOWN"
            
            # Index 3: Elevation (Hex-Wert)
            if arr[3] is not None and isinstance(arr[3], str):
                arr[3] = arr[3][::-1]
                arr[3] = ' '.join(str(x) for x in arr[3])
            else:
                arr[3] = "UNKNOWN"
            
            # Index 4: Blockage State
            if arr[4] is not None:
                arr[4] = ' '.join(str(arr[4]))
            else:
                arr[4] = "UNKNOWN"
            
            # Index 5: Sicherer Zugriff auf Element
            if arr[5] is not None and len(arr[5]) > 0:
                arr[5] = arr[5][0]
            else:
                arr[5] = "UNKNOWN"
            
            
        except (IndexError, TypeError, ValueError) as e:
            print(f"Fehler beim Formatieren der Sensor-Information: {e}")
            # Setze alle auf UNKNOWN bei Fehler
            for i in range(len(arr)):
                arr[i] = "UNKNOWN"


    def format_sensor_information_arr(self, arr):
        """Formatiert Sensor-Informations-Array mit Fehlerbehandlung"""
        try:
            # Index 0: Software Version
            if arr[0] is not None:
                arr[0] = arr[0][::-1]  # Bytes umdrehen
                software_version_number = [int(x, 16) for x in arr[0]]
                software_version_final = '.'.join(str(x) for x in software_version_number)
                arr[0] = software_version_final
            else:
                arr[0] = "UNKNOWN"
            
            # Index 1: Operation Mode
            if arr[1] is not None:
                arr[1] = int(arr[1])
            else:
                arr[1] = "UNKNOWN"
            
            # Index 2: Azimuth (Hex-Wert)
            if arr[2] is not None and isinstance(arr[2], str):
                arr[2] = arr[2][::-1]
                arr[2] = ' '.join(str(x) for x in arr[2])
            else:
                arr[2] = "UNKNOWN"
            
            # Index 3: Elevation (Hex-Wert)
            if arr[3] is not None and isinstance(arr[3], str):
                arr[3] = arr[3][::-1]
                arr[3] = ' '.join(str(x) for x in arr[3])
            else:
                arr[3] = "UNKNOWN"
            
            # Index 4: Blockage State
            if arr[4] is not None:
                arr[4] = ' '.join(str(arr[4]))
            else:
                arr[4] = "UNKNOWN"
            
            # Index 5: Sicherer Zugriff auf Element
            if arr[5] is not None and len(arr[5]) > 0:
                arr[5] = arr[5][0]
            else:
                arr[5] = "UNKNOWN"
            
            
        except (IndexError, TypeError, ValueError) as e:
            print(f"Fehler beim Formatieren der Sensor-Information: {e}")
            # Setze alle auf UNKNOWN bei Fehler
            for i in range(len(arr)):
                arr[i] = "UNKNOWN"


    def update_sensor_information_values(self, sensor_id: str, values: list):
        table = self.sensor_information_tables.get(sensor_id)
        if table is None:
            print(f"Keine Sensor-Information-Tabelle für '{sensor_id}'")
            return

        table.setRowCount(len(SENSOR_SIGNAL_INFORMATION)) 
        for index, value in enumerate(values):
            status_item = create_table_item(
                str(value) if value is not None else "UNKNOWN",
                self.gui_font,
                status_value=str(value) if value is not None else "UNKNOWN",
                is_status=True
            )
                
            # Beschreibung für die Sensorinformation - Statuswert abhängig 
            if index == 1:
                description = self._safe_dict_lookup(SENSOR_OPERATION_MODE, value, "UNKNOWN")
                table.setItem(index, 2, create_table_item(
                    description,
                    self.gui_font,
                    status_value=str(value) if value is not None else "UNKNOWN",
                    is_status=False
                ))

            elif index == 2:
                # Azimuth: Hex zu Float mit Berechnung
                final_int_val, is_valid = self._safe_hex_to_float(value, AZIMUTH_ELEVATION_RESOLUTION, AZIMUTH_ELEVATION_OFFSET)
                display_val = str(f"{final_int_val:.10f}") if is_valid else "UNKNOWN"
                table.setItem(index, 2, create_table_item(
                    display_val,
                    self.gui_font,
                    status_value=display_val,
                    is_status=True
                ))

            elif index == 3:
                # Elevation: Hex zu Float mit Berechnung
                final_int_val, is_valid = self._safe_hex_to_float(value, AZIMUTH_ELEVATION_RESOLUTION, AZIMUTH_ELEVATION_OFFSET)
                display_val = str(f"{final_int_val:.10f}") if is_valid else "UNKNOWN"
                table.setItem(index, 2, create_table_item(
                    display_val,
                    self.gui_font,
                    status_value=display_val,
                    is_status=True
                ))
                
            elif index == 4:
                # Blockage State
                if value is not None and value != "UNKNOWN":
                    parts = str(value).split()
                    if len(parts) >= 2:
                        try:
                            desc1 = self._safe_dict_lookup(BLOCKAGE_STATE_SELFTEST, int(parts[0]), "UNKNOWN")
                            desc2 = self._safe_dict_lookup(BLOCKAGE_STATE, int(parts[1]), "UNKNOWN")
                            description = f"{desc1} {desc2}"
                        except (ValueError, IndexError):
                            description = "UNKNOWN"
                    else:
                        description = "UNKNOWN"
                else:
                    description = "UNKNOWN"
                    
                table.setItem(index, 2, create_table_item(
                    description,
                    self.gui_font,
                    status_value=str(value) if value is not None else "UNKNOWN",
                    is_status=False
                ))
            
            table.setItem(index, 1, status_item)

            # Farbe für Kalibrierung
            if index == 7:
                status_item.setForeground(QColor('green') if str(value) == "Connected" else QColor('red'))


    def _safe_dict_lookup(self, dictionary: dict, key, default: str = "UNKNOWN") -> str:
        """Sicherer Zugriff auf Dictionary mit Default-Wert"""
        try:
            if key is None:
                return default
            value = dictionary.get(key, default)
            return str(value) if value is not None else default
        except (TypeError, AttributeError, ValueError):
            return default


    def _safe_hex_to_float(self, value, resolution, offset) -> tuple:
        """Konvertiert Hex-String zu Float mit Berechnung
        Rückghabeform (float_value, is_valid_bool)"""
        try:
            if value is None or value == "UNKNOWN":
                return 0.0, False
            
            # Entferne Leerzeichen aus Hex-String
            hex_value = str(value).replace(" ", "")
            
            # Prüfe ob es gültiges Hex ist
            if not all(c in '0123456789abcdefABCDEF' for c in hex_value):
                return 0.0, False
            
            hex_to_int_val = int(hex_value, 16)
            final_val = (hex_to_int_val * resolution) + offset
            return final_val, True
            
        except (ValueError, TypeError, AttributeError):
            return 0.0, False