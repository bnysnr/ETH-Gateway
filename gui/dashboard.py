from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from .window_settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, EGOMOTION_DEFAULT_VALUES, RADAR_STATUS_DEFAULT_VALUES, SIGNALE_INFORMATION_NOT_CONNECTED
from .functions import load_custom_font
from .widgets import (
    TitleBox,
    Egomotion_SRR_FL,
    Egomotion_SRR_FR,
    SignalStatus_SRR_FL,
    SignalStatus_SRR_FR,
    Pointcloud_SRR_FL,
    Pointcloud_SRR_FR,
    SensorInformationTable_SRR_FL,
    SensorInformationTable_SRR_FR,
)
from .data_binding import DataBinding
from publisher.radar_status_reader import radar_status_reader
from publisher.can_msg_sender import can_msg_sender
from publisher.sensor_information_reader import SensorInformationReader
from gui.available_sensors_checker import available_sensors
import socket
import struct
import time
import concurrent.futures


class Dashboard(QWidget):
    """Hauptfenster des Dashboards"""

    radar_status_updated = pyqtSignal(str, list)       # sensor_id, values
    egomotion_values_updated = pyqtSignal(str, list)  # sensor_id, values
    sensor_information_updated = pyqtSignal(str, list)  # sensor_id, values

    def __init__(self):
        super().__init__()

        # GUI-Font laden
        self.gui_font = load_custom_font()
        QApplication.instance().setFont(self.gui_font)

        # Fenster Einstellungen
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Widgets erstellen
        self._create_widgets()
        self._setup_data_binding()

        # Sensor-Objekte
        self.radar_obj = radar_status_reader()
        self.can_egomotion_obj = can_msg_sender()
        self.sensor_information_obj = SensorInformationReader()
        self.available_sensors_checker_obj = available_sensors()
        

        self.available_sensors_checker_obj.start()

        # Netzwerk
        self.SOURCE_IP = "127.0.0.1"
        self.SOURCE_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Thread Flag
        self.thread_running = True

        # Signale verbinden
        self.radar_status_updated.connect(self.update_signal_status_values)
        self.egomotion_values_updated.connect(self.update_egomotion_values)
        self.sensor_information_updated.connect(self.update_sensor_information)

        # Mapping IP -> Sensor
        self.IP_TO_SENSOR = {
            "srr_fl": "192.168.16.12",
            "srr_fr": "192.168.16.13"
        }

        self.available_ip_addresses = []

    def _create_widgets(self):
        self.title_box = TitleBox(self, self.gui_font)

        # Egomotion
        self.egomotion_box_srr_fl = Egomotion_SRR_FL(self, self.gui_font)
        self.egomotion_box_srr_fr = Egomotion_SRR_FR(self, self.gui_font)

        # Signal Status
        self.signalstatus_box_srr_fl = SignalStatus_SRR_FL(self, self.gui_font)
        self.signalstatus_box_srr_fr = SignalStatus_SRR_FR(self, self.gui_font)

        # Pointcloud Checkbox
        self.checkbox_srr_fl = Pointcloud_SRR_FL(self, self.gui_font, self.signalstatus_box_srr_fl)
        self.checkbox_srr_fr = Pointcloud_SRR_FR(self, self.gui_font, self.signalstatus_box_srr_fr)

        # Sensorinformation
        self.sensor_information_table_srr_fl = SensorInformationTable_SRR_FL(self, self.gui_font)
        self.sensor_information_table_srr_fr = SensorInformationTable_SRR_FR(self, self.gui_font)

   
    def _setup_data_binding(self):
        self.data_binding = DataBinding(
            sensor_config_tables={
                "192.168.16.12": self.signalstatus_box_srr_fl.table,
                "192.168.16.13": self.signalstatus_box_srr_fr.table,
            },
            egomotion_tables={
                "192.168.16.12": self.egomotion_box_srr_fl.table,
                "192.168.16.13": self.egomotion_box_srr_fr.table,
            },
            sensor_information_tables={
                "192.168.16.12": self.sensor_information_table_srr_fl.table,
                "192.168.16.13": self.sensor_information_table_srr_fr.table,
            },
            gui_font=self.gui_font,
        )


    def resizeEvent(self, event):
        super().resizeEvent(event)

        ego_width = self.egomotion_box_srr_fl.table.viewport().width()
        for box in (self.egomotion_box_srr_fl, self.egomotion_box_srr_fr):
            box.table.setColumnWidth(0, int(ego_width * 0.55))
            box.table.setColumnWidth(1, int(ego_width * 0.15))
            box.table.setColumnWidth(2, int(ego_width * 0.30))

        signal_width = self.signalstatus_box_srr_fl.table.viewport().width()
        for box in (self.signalstatus_box_srr_fl, self.signalstatus_box_srr_fr):
            box.table.setColumnWidth(0, int(signal_width * 0.4))
            box.table.setColumnWidth(1, int(signal_width * 0.2))
            box.table.setColumnWidth(2, int(signal_width * 0.4))

        sensor_width = self.sensor_information_table_srr_fl.table.viewport().width()
        for table in (self.sensor_information_table_srr_fl.table, self.sensor_information_table_srr_fr.table):
            table.setColumnWidth(0, int(sensor_width * 0.4))
            table.setColumnWidth(1, int(sensor_width * 0.25))
            table.setColumnWidth(2, int(sensor_width * 0.35))

    def showEvent(self, event):
        super().showEvent(event)
        self.resizeEvent(None)

    # Funktion zum prüfen der aktuell verfügbaren Sensoren
    def check_available_sensors(self):
        pass
  
    def update_signal_status_values(self, sensor_id: str, values: list):
        if self.data_binding:
            self.data_binding.update_signal_status_values(sensor_id, values)
   
    def update_egomotion_values(self, sensor_id, values):
        if self.data_binding:
            self.data_binding.update_egomotion_values(sensor_id, values)

    def update_sensor_information(self, sensor_id: str, values: list):
        if self.data_binding:
            self.data_binding.update_sensor_information_values(sensor_id, values)

  
    def update_radar_status_thread(self):
        while self.thread_running:
            try:
                current_available_sensors = self.available_sensors_checker_obj.get_available()
                not_available = self.available_sensors_checker_obj.get_not_available()

                # Jeden verfügbaren Sensor EINZELN verarbeiten (nicht alle auf einmal)
                for sensor_ip in current_available_sensors:
                    try:
                        gen = self.radar_obj.run([sensor_ip], "0007", 1231, 56)  # Nur EINEN Sensor!
                        response_ip, values = next(gen)
                        self.radar_status_updated.emit(response_ip, values)
            #            print(f"AVAILABLE SENSORS: {response_ip} - {values}")
                    except StopIteration:
                        print(f"No response from {sensor_ip}")
                    except Exception as e:
                        print(f"Error reading {sensor_ip}: {e}")

                # Nicht verfügbare Sensoren verarbeiten
                for not_available_sensor_ip in not_available:
                    self.radar_status_updated.emit(not_available_sensor_ip, RADAR_STATUS_DEFAULT_VALUES)
           

                time.sleep(0.2)

            except Exception as e:
                print("THREAD ERROR:", repr(e))
                import traceback
                traceback.print_exc()
                time.sleep(1)


    def update_egomotion_value_thread(self):
        self.sock.bind((self.SOURCE_IP, self.SOURCE_PORT))
        self.sock.settimeout(0.1)
        last_update_time = 0
        latest_values = None

        while self.thread_running:
            try:
                data, _ = self.sock.recvfrom(1024)
                num_floats = len(data) // 4
                latest_values = struct.unpack("<" + "f" * num_floats, data)
                current_available_sensors = self.available_sensors_checker_obj.get_available()
                not_available = self.available_sensors_checker_obj.get_not_available()
            except socket.timeout:
                pass

            current_time = time.time()
            if latest_values and current_time - last_update_time >= 0.5:
                for sensor_ip in current_available_sensors:
                    self.egomotion_values_updated.emit(sensor_ip, list(latest_values))
                    last_update_time = current_time

                for not_available_sensor_ip in not_available:
                    self.egomotion_values_updated.emit(not_available_sensor_ip, EGOMOTION_DEFAULT_VALUES)
                   

                
    

    def update_radar_signal_information_thread(self):
        required_signal_data_arr = [
            ["0007", "1000", 199, 32],
            ["0009", "1000", 191, 8],
            ["0001", "1000", 575, 16],
            ["0001", "1000", 591, 16],
            ["0007", "1000", 1311, 8],
            ["0001", "1000", 479, 16],
        ]

        while self.thread_running:
            try:
                current_available_sensors = self.available_sensors_checker_obj.get_available()
                not_available = self.available_sensors_checker_obj.get_not_available()

                #print(f"Ausgabe in Sensor Information: {current_available_sensors} - {not_available}")

                # Jeden verfügbaren Sensor EINZELN verarbeiten
                for sensor_ip in current_available_sensors:
                    buffer = []

                    # Alle 6 Anfragen PARALLEL ausführen
                    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                        futures = []
                        
                        for service_id, method_id, bit_pos, bit_size in required_signal_data_arr:
                            future = executor.submit(
                                self._fetch_sensor_value, 
                                sensor_ip, 
                                service_id, 
                                method_id, 
                                bit_pos, 
                                bit_size
                            )
                            futures.append(future)
                        
                        # Ergebnisse in der gleichen Reihenfolge sammeln
                        for future in futures:
                            try:
                                value = future.result(timeout=2.5)
                                buffer.append(value)
                            except concurrent.futures.TimeoutError:
                                print(f"Timeout for {sensor_ip}")
                                buffer.append(None)
                            except Exception as e:
                                print(f"Error reading {sensor_ip}: {e}")
                                buffer.append(None)
                    
                    # Abfrage für die Sensorkalibrierung
                    if((buffer[1]) == 3 and buffer[2] is not None):
                        buffer.append(True) # Index 6: Kalibrierung
                        print("Sensor ist kalibriert")
                    else:    
                        buffer.append(False) # Index 6: Kalibrierung
                        print("Sensor ist nicht kalibriert")

                    # Signal emitten für den spezifischen Sensor (IP-basiert)
                    self.format_sensor_information_arr(buffer)
                    buffer.append("Connected") # Index 7: Connection
                    self.sensor_information_updated.emit(sensor_ip, buffer)
                    print(f"{sensor_ip}: {buffer}")
                    

                # Nicht verfügbare Sensoren mit Default-Werten verarbeiten
                for not_available_sensor_ip in not_available:
                    self.sensor_information_updated.emit(not_available_sensor_ip, SIGNALE_INFORMATION_NOT_CONNECTED)
                    self.radar_status_updated.emit(not_available_sensor_ip, RADAR_STATUS_DEFAULT_VALUES)

                time.sleep(0.2)

            except Exception as e:
                print(f"SENSOR INFORMATION THREAD ERROR: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(1)

    # Hilfsfunktion zur besseren Anzeige der Sensorinformationen
    def format_sensor_information_arr(self, arr):
        arr[0] = arr[0][::-1]  # Bytes umdrehen
        software_version_number = [int(x, 16) for x in arr[0]]  # Umwandlung von Hex in Int
        software_version_final = '.'.join(str(x) for x in software_version_number)  # Formattierung als Softwareversion mit .
        arr[0] = software_version_final
        arr[1] = int(arr[1])
        arr[5] = arr[5][0]
        arr[2] = arr[2][::-1]
        arr[2] = ' '.join(str(x) for x in arr[2])
        arr[3] = arr[3][::-1]
        arr[3] = ' '.join(str(x) for x in arr[3])
        arr[4] = ' '.join(str(arr[4]))
        print(arr[4])

    def _fetch_sensor_value(self, sensor_ip, service_id, method_id, bit_pos, bit_size):
        """Hilfsfunktion für parallele Sensor-Abfragen"""
        try:
            gen = self.sensor_information_obj.run(
                sensor_ip,
                service_id, 
                method_id, 
                bit_pos, 
                bit_size
            )
            value = next(gen)

            if isinstance(value, list):
                value = value[0] if len(value) == 1 else value

            return value
        except StopIteration:
            print(f"No response from {sensor_ip} - Service: {service_id}")
            return None
        except Exception as e:
            print(f"Error reading from {sensor_ip} - Service: {service_id}, Method: {method_id}: {e}")
            return None

  
    def closeEvent(self, event):
        self.thread_running = False
        try:
            self.sock.close()
        except Exception:
            pass
        super().closeEvent(event)
