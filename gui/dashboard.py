from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from .window_parameter import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    EGOMOTION_DEFAULT_VALUES, RADAR_STATUS_DEFAULT_VALUES,
    SIGNALE_INFORMATION_NOT_CONNECTED
)
from .functions import load_custom_font
from .widgets import TitleBox
from .data_binding import DataBinding
from publisher.radar_status_reader import radar_status_reader
from publisher.can_msg_sender import can_msg_sender
from publisher.sensor_information_reader import SensorInformationReader
from gui.available_sensors_checker import available_sensors

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

import math
import time

# Konkrete Dashboard-Implementierungen mit Widget-Imports
from .widgets import (
    SQCQ,
    Egomotion_SRR_FL, Egomotion_SRR_FR, Egomotion_SRR_RL, Egomotion_SRR_RR, Egomotion_ARS_FRONT, Egomotion_ARS_REAR,
    SignalStatus_SRR_FL, SignalStatus_SRR_FR, SignalStatus_SRR_RL, SignalStatus_SRR_RR, SignalStatus_ARS_FRONT, SignalStatus_ARS_REAR,
    Pointcloud_SRR_FL, Pointcloud_SRR_FR, Pointcloud_SRR_RL, Pointcloud_SRR_RR, Pointcloud_ARS_FRONT, Pointcloud_ARS_REAR, 
    SensorInformationTable_SRR_FL, SensorInformationTable_SRR_FR, SensorInformationTable_SRR_RL, SensorInformationTable_SRR_RR, SensorInformationTable_ARS_FRONT, SensorInformationTable_ARS_REAR
)

AZIMUTH_ELEVATION_MISALIGNMENT_MIN = -6 * (math.pi / 180)
AZIMUTH_ELEVATION_MISALIGNMENT_MAX = 6 * (math.pi / 180)
AZIMUTH_ELEVATION_OFFSET = -0.2095
AZIMUTH_ELEVATION_RESOLUTION = 0.0000063935301747158

# Globale Referenz für SQCQ Dashboard
_sqcq_dashboard_instance = None

def set_sqcq_dashboard(instance):
    """Setzt die globale SQCQ Dashboard Referenz"""
    global _sqcq_dashboard_instance
    _sqcq_dashboard_instance = instance

def get_sqcq_dashboard():
    """Holt die globale SQCQ Dashboard Referenz"""
    return _sqcq_dashboard_instance


class BaseDashboard(QWidget):
    """Basis-Klasse für alle Dashboard-Pages mit gemeinsamer Logik"""
    
    radar_status_updated = pyqtSignal(str, list)
    egomotion_values_updated = pyqtSignal(str, list)
    sensor_information_updated = pyqtSignal(str, list)

    def __init__(self, sensor_config):

        super().__init__()
        self.sensor_config = sensor_config
        
        # GUI-Font laden
        self.gui_font = load_custom_font()
        QApplication.instance().setFont(self.gui_font)
        
        # Fenster Einstellungen
        self.setWindowTitle(WINDOW_TITLE)
        #self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        
        
        # Widget-Container
        self.egomotion_boxes = []
        self.signalstatus_boxes = []
        self.checkboxes = []
        self.sensor_information_tables = []
        
        # Widgets erstellen
        self._create_widgets()
        self._setup_layout()
        self._setup_data_binding()
        
        # Sensor-Objekte
        self.radar_obj = radar_status_reader()
        self.can_egomotion_obj = can_msg_sender()
        self.sensor_information_obj = SensorInformationReader()
        self.available_sensors_checker_obj = available_sensors()
        self.available_sensors_checker_obj.start()


        
        # Thread Flag
        self.thread_running = True
        
        # Signale verbinden
        self.radar_status_updated.connect(self.update_signal_status_values)
        self.egomotion_values_updated.connect(self.update_egomotion_values)
        self.sensor_information_updated.connect(self.update_sensor_information)

    def _create_widgets(self):
        """Erstellt alle Widget-Komponenten dynamisch"""
        self.title_box = TitleBox(self, self.gui_font)
        
        widget_classes = self.sensor_config['widget_classes']


        # Egomotion Widgets
        for widget_class in widget_classes['egomotion']:
            widget = widget_class(self, self.gui_font)
            self.egomotion_boxes.append(widget)
        
        # Signal Status Widgets
        for widget_class in widget_classes['signal_status']:
            widget = widget_class(self, self.gui_font)
            self.signalstatus_boxes.append(widget)
        
        # Pointcloud Checkboxes (benötigen Signal Status Box als Referenz)
        for i, widget_class in enumerate(widget_classes['pointcloud']):
            widget = widget_class(self, self.gui_font, self.signalstatus_boxes[i])
            self.checkboxes.append(widget)
        
        # Sensor Information Tables
        for widget_class in widget_classes['sensor_info']:
            widget = widget_class(self, self.gui_font)
            self.sensor_information_tables.append(widget)

    def _setup_layout(self):
        """Setzt Layout auf"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def _setup_data_binding(self):
        """Setzt Data Binding auf - FIXED: Richtige Zuordnung der IPs"""
        sensor_ips = list(self.sensor_config['sensors'].values())
        
        # Debug-Ausgabe
        print(f"\n=== Data Binding Setup für {self.__class__.__name__} ===")
        print(f"Sensor IPs: {sensor_ips}")
        print(f"Anzahl Egomotion Boxes: {len(self.egomotion_boxes)}")
        print(f"Anzahl Signal Status Boxes: {len(self.signalstatus_boxes)}")
        print(f"Anzahl Sensor Info Tables: {len(self.sensor_information_tables)}")
        
        # Mapping erstellen
        egomotion_mapping = {}
        signal_status_mapping = {}
        sensor_info_mapping = {}
        
        for i, ip in enumerate(sensor_ips):
            if i < len(self.egomotion_boxes):
                egomotion_mapping[ip] = self.egomotion_boxes[i].table
                print(f"Egomotion: {ip} -> {self.egomotion_boxes[i].__class__.__name__}")
            
            if i < len(self.signalstatus_boxes):
                signal_status_mapping[ip] = self.signalstatus_boxes[i].table
                print(f"Signal Status: {ip} -> {self.signalstatus_boxes[i].__class__.__name__}")
            
            if i < len(self.sensor_information_tables):
                sensor_info_mapping[ip] = self.sensor_information_tables[i].table
                print(f"Sensor Info: {ip} -> {self.sensor_information_tables[i].__class__.__name__}")
        
        print("="*50 + "\n")
        
        self.data_binding = DataBinding(
            sensor_config_tables=signal_status_mapping,
            egomotion_tables=egomotion_mapping,
            sensor_information_tables=sensor_info_mapping,
            gui_font=self.gui_font,
        )

    def resizeEvent(self, event):
        """Definiert Spaltenverhältnisse"""
        super().resizeEvent(event)
        
        # Egomotion Spalten
        if self.egomotion_boxes:
            ego_width = self.egomotion_boxes[0].table.viewport().width()
            for box in self.egomotion_boxes:
                box.table.setColumnWidth(0, int(ego_width * 0.55))
                box.table.setColumnWidth(1, int(ego_width * 0.15))
                box.table.setColumnWidth(2, int(ego_width * 0.30))
        
        # Signal Status Spalten
        if self.signalstatus_boxes:
            signal_width = self.signalstatus_boxes[0].table.viewport().width()
            for box in self.signalstatus_boxes:
                box.table.setColumnWidth(0, int(signal_width * 0.4))
                box.table.setColumnWidth(1, int(signal_width * 0.15))
                box.table.setColumnWidth(2, int(signal_width * 0.45))
        
        # Sensor Information Spalten
        if self.sensor_information_tables:
            sensor_width = self.sensor_information_tables[0].table.viewport().width()
            for table in self.sensor_information_tables:
                table.table.setColumnWidth(0, int(sensor_width * 0.34))
                table.table.setColumnWidth(1, int(sensor_width * 0.23))
                table.table.setColumnWidth(2, int(sensor_width * 0.43))

    def showEvent(self, event):
        super().showEvent(event)
        self.update()

    def safe_hex_to_float(self, value: str):
        try:
            value = value.replace(" ", "")
            return (int(value, 16) * AZIMUTH_ELEVATION_RESOLUTION) + AZIMUTH_ELEVATION_OFFSET
        except (ValueError, AttributeError):
            return None


    # SQCQ Funktionen
    def sqcq_sensor_signal_status(self, sensor_id: str, values: list):
        """SQCQ for Signal Status - sendet an globales SQCQ Dashboard"""
        result = "Valid"
        for val in values:
            if val == '02':
                result = "Invalid"
                break    
        #print(f"SQCQ Sensor Signal Status for: {sensor_id} - Result: {result}")
        
        # Sende an globales SQCQ Dashboard
        sqcq_dashboard = get_sqcq_dashboard()
        if sqcq_dashboard:
            sqcq_dashboard._fill_test_data(sensor_id, result)
        else:
            print("WARNING: SQCQ Dashboard nicht verfügbar!")
        

    def sqcq_sensor_information_status(self, sensor_id: str, values: list):
        """SQCQ for Sensor Information"""
        result = "Valid"

        # Azimuth / Elevation sicher konvertieren
        azimuth = self.safe_hex_to_float(values[2])
        elevation = self.safe_hex_to_float(values[3])

        # Wenn keine gültigen Werte → sofort False
        if azimuth is None or elevation is None:
            #print(f"DEBUG Sensor {sensor_id}: Invalid Azimuth/Elevation ({values[2]}, {values[3]})")
            #print(f"SQCQ Sensor Information for: {sensor_id} - Result: {result}")
            result = "Invalid"
            # Sende trotzdem an SQCQ Dashboard
            sqcq_dashboard = get_sqcq_dashboard()
            if sqcq_dashboard:
                sqcq_dashboard._fill_sensor_information_data(sensor_id, result)
                self
            return

        values[2] = azimuth
        values[3] = elevation

        # Blockage Status
        try:
            values[4] = [int(x) for x in values[4].split()]
        except Exception:
            #print(f"DEBUG Sensor {sensor_id}: Invalid Blockage Status ({values[4]})")
            result = "Invalid"

        # Valid Detections
        try:
            values[5] = int(values[5], 16)
        except Exception:
            result = "Invalid"

        if not (
            values[1] == 3 and
            AZIMUTH_ELEVATION_MISALIGNMENT_MIN <= values[2] <= AZIMUTH_ELEVATION_MISALIGNMENT_MAX and
            AZIMUTH_ELEVATION_MISALIGNMENT_MIN <= values[3] <= AZIMUTH_ELEVATION_MISALIGNMENT_MAX and
            len(values[4]) >= 2 and
            values[4][0] == 1 and
            values[4][1] == 4 and
            values[5] > 0 and
            values[6] is True and
            values[7] == 'Connected'
        ):
            result = "Invalid"

        #print(f"SQCQ Sensor Information for: {sensor_id} - Result: {result}")
        
        # Sende an globales SQCQ Dashboard
        sqcq_dashboard = get_sqcq_dashboard()
        if sqcq_dashboard:
            sqcq_dashboard._fill_sensor_information_data(sensor_id, result)
        
        else:
            print("WARNING: SQCQ Dashboard nicht verfügbar!")
        

    # Update Funktionen
    def update_signal_status_values(self, sensor_id: str, values: list):
        if self.data_binding:
            self.data_binding.update_signal_status_values(sensor_id, values)
            self.sqcq_sensor_signal_status(sensor_id, values)

    def update_egomotion_values(self, sensor_id, values):
        if self.data_binding:
            self.data_binding.update_egomotion_values(sensor_id, values)
        else:
            print(f"[{self.__class__.__name__}] WARNUNG: data_binding ist None!")

    def update_sensor_information(self, sensor_id: str, values: list):
        if self.data_binding:
            self.data_binding.update_sensor_information_values(sensor_id, values)
            self.sqcq_sensor_information_status(sensor_id, values)

    def distribute_egomotion_data(self, values: list):
        """Empfängt Egomotion-Daten vom zentralen Distributor und verteilt sie an eigene Sensoren"""
        current_available_sensors = self.available_sensors_checker_obj.get_available()
        not_available = self.available_sensors_checker_obj.get_not_available()
        
        # Aktualisiere nur die Sensoren, die zu DIESEM Dashboard gehören
        for sensor_ip in current_available_sensors:
            if sensor_ip in self.sensor_config['sensors'].values():
                self.egomotion_values_updated.emit(sensor_ip, values)
        
        for not_available_sensor_ip in not_available:
            if not_available_sensor_ip in self.sensor_config['sensors'].values():
                self.egomotion_values_updated.emit(not_available_sensor_ip, EGOMOTION_DEFAULT_VALUES)


    def update_radar_status_thread(self):
        """Thread für Radar-Status-Updates"""
        while self.thread_running:
            try:
                current_available_sensors = self.available_sensors_checker_obj.get_available()
                not_available = self.available_sensors_checker_obj.get_not_available()

                for sensor_ip in current_available_sensors:
                    # Prüfe ob dieser Sensor zu DIESEM Dashboard gehört
                    if sensor_ip not in self.sensor_config['sensors'].values():
                        continue
                    
                    try:
                        gen = self.radar_obj.run([sensor_ip], "0007", 1231, 56)
                        response_ip, values = next(gen)
                        self.radar_status_updated.emit(response_ip, values)
                    except StopIteration:
                        print(f"No response from {sensor_ip}")
                    except Exception as e:
                        print(f"Error reading {sensor_ip}: {e}")

                for not_available_sensor_ip in not_available:
                    # Prüfe ob dieser Sensor zu DIESEM Dashboard gehört
                    if not_available_sensor_ip in self.sensor_config['sensors'].values():
                        self.radar_status_updated.emit(not_available_sensor_ip, RADAR_STATUS_DEFAULT_VALUES)
                        self.sensor_information_updated.emit(not_available_sensor_ip, SIGNALE_INFORMATION_NOT_CONNECTED)

                time.sleep(0.2)

            except Exception as e:
                print("THREAD ERROR:", repr(e))
                import traceback
                traceback.print_exc()
                time.sleep(1)

    def update_radar_signal_information_thread(self):
        """Thread für Sensor-Information-Updates"""
        required_signal_data_arr = [
            ["0007", "1000", 199, 32],   # Software Version
            ["0009", "1000", 191, 8],    # Sensor Operation Mode
            ["0001", "1000", 575, 16],   # Azimuth Misalignment
            ["0001", "1000", 591, 16],   # Elevation Misalignment
            ["0007", "1000", 1311, 8],   # Blockage Status
            ["0001", "1000", 479, 16],   # Valid Detections
        ]

        while self.thread_running:
            try:
                current_available_sensors = self.available_sensors_checker_obj.get_available()
                not_available = self.available_sensors_checker_obj.get_not_available()

                for sensor_ip in current_available_sensors:
                    # Prüfe ob dieser Sensor zu DIESEM Dashboard gehört
                    if sensor_ip not in self.sensor_config['sensors'].values():
                        continue
                    
                    buffer = []
                    response_ip = None

                    try:
                        for service_id, method_id, bitposition, bitsize in required_signal_data_arr:
                            gen = self.sensor_information_obj.run(sensor_ip, service_id, method_id, bitposition, bitsize)
                            for response_ip, value in gen:
                                buffer.append(value)

                        buffer_2_formatted = ''.join(buffer[2][::-1]) 
                        buffer_2_formatted_decimal = int(buffer_2_formatted, 16)

                        # interne Abfrage ob der Sensor kalibriert ist
                        if len(buffer) == 6:
                            buffer_1_decimal = int(buffer[1][0], 16)
                            if buffer_1_decimal == 3 and buffer_2_formatted_decimal is not None:
                                buffer.append(True)
                            else:
                                buffer.append(False)

                            self.format_sensor_information_arr(buffer)
                            buffer.append("Connected")
                            self.sensor_information_updated.emit(response_ip, buffer)
                        else:
                            print(f"Unvollständige Daten für {sensor_ip}: {len(buffer)}/6")

                    except StopIteration:
                        print(f"No response from {sensor_ip}")
                    except Exception as e:
                        print(f"Error processing {sensor_ip}: {e}")
                        import traceback
                        traceback.print_exc()

                for not_available_sensor_ip in not_available:
                    # Prüfe ob dieser Sensor zu DIESEM Dashboard gehört
                    if not_available_sensor_ip in self.sensor_config['sensors'].values():
                        self.sensor_information_updated.emit(not_available_sensor_ip, SIGNALE_INFORMATION_NOT_CONNECTED)
                        self.radar_status_updated.emit(not_available_sensor_ip, RADAR_STATUS_DEFAULT_VALUES)

                time.sleep(0.2)

            except Exception as e:
                print(f"SENSOR INFORMATION THREAD ERROR: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(1)

    def format_sensor_information_arr(self, arr):
        """Formatiert Sensor-Informations-Array für Anzeige"""
        arr[0] = arr[0][::-1]
        software_version_number = [int(x, 16) for x in arr[0]]
        software_version_final = '.'.join(str(x) for x in software_version_number)
        arr[0] = software_version_final

        arr[1] = int(arr[1][0], 16)

        arr[2] = arr[2][::-1]
        arr[2] = ' '.join(str(x) for x in arr[2])

        arr[3] = arr[3][::-1]
        arr[3] = ' '.join(str(x) for x in arr[3])

        arr[4] = ' '.join(''.join(arr[4]))
        arr[5] = arr[5][0]
        return arr

    def closeEvent(self, event):
        """Cleanup beim Schließen"""
        self.thread_running = False
        super().closeEvent(event)



 

class SRR_FRONT(BaseDashboard):
    """Dashboard für Front-Sensoren (FL, FR)"""
    def __init__(self):
        config = {
            'sensors': {
                'srr_fl': "192.168.16.12",
                'srr_fr': "192.168.16.13"
            },
            'widget_classes': {
                'egomotion': [Egomotion_SRR_FL, Egomotion_SRR_FR],
                'signal_status': [SignalStatus_SRR_FL, SignalStatus_SRR_FR],
                'pointcloud': [],                                                               # [Pointcloud_SRR_FL, Pointcloud_SRR_FR],
                'sensor_info': [SensorInformationTable_SRR_FL, SensorInformationTable_SRR_FR]
            }
        }
        super().__init__(config)


class SRR_REAR(BaseDashboard):
    """Dashboard für Rear-Sensoren (RL, RR)"""
    def __init__(self):
        config = {
            'sensors': {
                'srr_rl': "192.168.16.14",
                'srr_rr': "192.168.16.15"
            },
            'widget_classes': {
                'egomotion': [Egomotion_SRR_RL, Egomotion_SRR_RR],
                'signal_status': [SignalStatus_SRR_RL, SignalStatus_SRR_RR],
                'pointcloud': [],                                                               # [Pointcloud_SRR_RL, Pointcloud_SRR_RR],
                'sensor_info': [SensorInformationTable_SRR_RL, SensorInformationTable_SRR_RR]
            }
        }
        super().__init__(config)


class ARS_FRONT_REAR(BaseDashboard):
    """Dashboard für ARS Sensoren"""
    def __init__(self):
        config = {
            'sensors': {
                'ars_front': "192.168.16.11",
                'ars_rear': "192.168.16.16"
            },
            'widget_classes': {
                'egomotion': [Egomotion_ARS_FRONT, Egomotion_ARS_REAR],
                'signal_status': [SignalStatus_ARS_FRONT, SignalStatus_ARS_REAR],
                'pointcloud': [],                                                           # [Pointcloud_ARS_FRONT, Pointcloud_ARS_REAR],
                'sensor_info': [SensorInformationTable_ARS_FRONT, SensorInformationTable_ARS_REAR]
            }
        }
        super().__init__(config)


class SQCQ_DASHBOARD(BaseDashboard):
    """Dashboard fürs SQCQ (nur Logo + eine Tabelle)"""

    def __init__(self):
        config = {
            'sensors': {
                'srr_fl': "192.168.16.12",
                'srr_fr': "192.168.16.13",
                'srr_rl': "192.168.16.14",
                'srr_rr': "192.168.16.15",
                'ars_front': "192.168.16.11",
                'ars_rear': "192.168.16.16"
            },  
            'widget_classes': {
                'sqcq': [SQCQ],
                'egomotion': [],
                'signal_status': [],
                'pointcloud': [],
                'sensor_info': []
            }
        }
        super().__init__(config)
        
        # Mapping: IP -> Tabellenzeile
        self.ip_to_row = {
            "192.168.16.12": 0,  # SRR Front Left
            "192.168.16.13": 1,  # SRR Front Right
            "192.168.16.14": 2,  # SRR Rear Left
            "192.168.16.15": 3,  # SRR Rear Right
            "192.168.16.11": 4,  # ARS Front
            "192.168.16.16": 5   # ARS Rear
        }
        
        # Registriere diese Instanz als globales SQCQ Dashboard
        set_sqcq_dashboard(self)

    def _create_widgets(self):
        """Nur TitleBox + SQCQ Tabelle"""
        self.title_box = TitleBox(self, self.gui_font)
        self.egomotion_boxes = []
        self.signalstatus_boxes = []
        self.checkboxes = []
        self.sensor_information_tables = []
        self.sqcq_table = SQCQ(self, self.gui_font)

    def _setup_data_binding(self):
        """Kein Data Binding nötig"""
        self.data_binding = None

    def _fill_test_data(self, sensor_id, values):
        """Füllt Tabelle mit Werten basierend auf Sensor IP"""
    
        
        # Prüfe ob sqcq_table existiert
        if not hasattr(self, 'sqcq_table'):
            print("ERROR: sqcq_table existiert nicht!")
            return
        
        if not hasattr(self.sqcq_table, 'table'):
            print("ERROR: sqcq_table.table existiert nicht!")
            return
        
        # Hole die entsprechende Zeile für die IP
        if sensor_id not in self.ip_to_row:
            print(f"WARNING: Unknown sensor IP {sensor_id}")
            return
        
        row = self.ip_to_row[sensor_id]
    
        
        # Erstelle QTableWidgetItem mit dem Wert
        item = QTableWidgetItem(str(values))
        
        # Setze Hintergrundfarbe basierend auf Wert
        if values is "Valid":
            item.setForeground(QColor('green'))  # Grün für True
        else:
            item.setForeground(QColor('red'))  # Rot für False
        
        # Zentriere den Text
        item.setTextAlignment(Qt.AlignCenter)
        
        # Schreibe in die Tabelle (Zeile basierend auf IP, Spalte 1)
        self.sqcq_table.table.setItem(row, 1, item)
        print(f"Wert '{values}' erfolgreich in Zeile {row}, Spalte 1 geschrieben")

    def _fill_sensor_information_data(self, sensor_id, values):
        """Füllt Tabelle mit Sensor Information Werten in Spalte 2"""
    
        
        # Prüfe ob sqcq_table existiert
        if not hasattr(self, 'sqcq_table'):
            print("ERROR: sqcq_table existiert nicht!")
            return
        
        if not hasattr(self.sqcq_table, 'table'):
            print("ERROR: sqcq_table.table existiert nicht!")
            return
        
        # Hole die entsprechende Zeile für die IP
        if sensor_id not in self.ip_to_row:
            print(f"WARNING: Unknown sensor IP {sensor_id}")
            return
        
        row = self.ip_to_row[sensor_id]
        
        # Erstelle QTableWidgetItem mit dem Wert
        item = QTableWidgetItem(str(values))
        
        # Setze Hintergrundfarbe basierend auf Wert
        if values is "Valid":
            item.setForeground(QColor('green'))  
        else:
            item.setForeground(QColor('red'))  # Rot für False
        
        # Zentriere den Text
        item.setTextAlignment(Qt.AlignCenter)
        
        # Schreibe in die Tabelle (Zeile basierend auf IP, Spalte 2)
        self.sqcq_table.table.setItem(row, 2, item)
    
    def sqcq_sensor_signal_status(self, sensor_id: str, values: list):
        """Überschreibe die Methode - nicht nötig für SQCQ Dashboard"""
        pass

    def sqcq_sensor_information_status(self, sensor_id: str, values: list):
        """Überschreibe die Methode - nicht nötig für SQCQ Dashboard"""
        pass

    def update_radar_status_thread(self):
        """Überschreibe die Methode - nicht nötig für SQCQ Dashboard"""
        pass

    def update_radar_signal_information_thread(self):
        """Überschreibe die Methode - nicht nötig für SQCQ Dashboard"""
        pass

    def distribute_egomotion_data(self, values: list):
        """Überschreibe die Methode - nicht nötig für SQCQ Dashboard"""
        pass
    
    def closeEvent(self, event):
        """Cleanup beim Schließen"""
        # Entferne globale Referenz
        global _sqcq_dashboard_instance
        if _sqcq_dashboard_instance == self:
            _sqcq_dashboard_instance = None
        super().closeEvent(event)