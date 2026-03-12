# gui/widgets.py
"""Widget-Komponenten des Dashboards"""

from PyQt5.QtWidgets import QFrame, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from .window_parameter import LOGO_PATH, EGO_SIGNALS, SENSOR_CONFIG_SIGNALS, SENSOR_SIGNAL_INFORMATION, SQCQ_SENSOR_NAMES
from .functions import apply_font_to_table, create_table_item
from .generic_egomotion_table import GenericEgomotionTable
from .generic_status_config_table import GenericSignalStatus
from .generic_pointcloud_checkbox import PointcloudCheckbox


class TitleBox(QFrame):
    """Titel-Box mit Logo und Überschrift"""
    def __init__(self, parent, gui_font):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)
        
        box_height = int(parent.height() * 0.2)
        self.setGeometry(0, 0, parent.width(), box_height)
        
        # Logo
        logo_label = QLabel(self)
        logo_label.setGeometry(5, 5, 200, box_height)
        pix = QPixmap(LOGO_PATH)
        if not pix.isNull():
            scaled_pix = pix.scaled(logo_label.width(), logo_label.height(), Qt.KeepAspectRatio)
            logo_label.setPixmap(scaled_pix)



class SQCQ(GenericEgomotionTable):
    """SQCQ Dashboard Tabellenkonfiguration"""
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SQCQ Dashboard",
            row_labels=SQCQ_SENSOR_NAMES,
            columns=["Sensor", "Sensor Message Status", "Sensor Information"],
            geometry_func=self._geometry
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)

        self._update_column_widths()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_column_widths()

    def _update_column_widths(self):
        width = self.table.viewport().width()
        self.table.setColumnWidth(0, int(width * 0.25))  # Sensor
        self.table.setColumnWidth(1, int(width * 0.35))  # Status
        self.table.setColumnWidth(2, int(width * 0.40))  # Info

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.1)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 1.2)           # Boxbreite
        box_h = int(parent.height() * 0.6)          # Boxhöhe
        return (20, box_y, box_w, box_h)            # Abstand zum linken Rand: 20

class Egomotion_SRR_FL(GenericEgomotionTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FL - Egomotion",
            row_labels=EGO_SIGNALS,
            columns=["Signalname", "Unit", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.1)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 0.9)           # Boxbreite
        box_h = int(parent.height() * 0.8)          # Position auf der horizontalen Ebene 
        return (20, box_y, box_w, box_h)            # Abstand zum linken Rand: 20
    
class Egomotion_SRR_FR(GenericEgomotionTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FR - Egomotion",
            row_labels=EGO_SIGNALS,
            columns=["Signalname", "Unit", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.9)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 0.9)           # Boxbreite
        box_h = int(parent.height() * 0.8)          # Position auf der horizontalen Ebene 
        return (20, box_y, box_w, box_h)            # Abstand zum linken Rand: 20      
     

class Egomotion_SRR_RL(GenericEgomotionTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR RL - Egomotion",
            row_labels=EGO_SIGNALS,
            columns=["Signalname", "Unit", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.1)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 0.9)           # Boxbreite
        box_h = int(parent.height() * 0.8)          # Position auf der horizontalen Ebene 
        return (20, box_y, box_w, box_h)            # Abstand zum linken Rand: 20
    

class Egomotion_SRR_RR(GenericEgomotionTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR RR - Egomotion",
            row_labels=EGO_SIGNALS,
            columns=["Signalname", "Unit", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.9)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 0.9)           # Boxbreite
        box_h = int(parent.height() * 0.8)          # Position auf der horizontalen Ebene 
        return (20, box_y, box_w, box_h)            # Abstand zum linken Rand: 20  


class Egomotion_ARS_FRONT(GenericEgomotionTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="ARS FRONT - Egomotion",
            row_labels=EGO_SIGNALS,
            columns=["Signalname", "Unit", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.1)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 0.9)           # Boxbreite
        box_h = int(parent.height() * 0.8)          # Position auf der horizontalen Ebene 
        return (20, box_y, box_w, box_h)            # Abstand zum linken Rand: 20
    

class Egomotion_ARS_REAR(GenericEgomotionTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="ARS REAR - Egomotion",
            row_labels=EGO_SIGNALS,
            columns=["Signalname", "Unit", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.9)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 0.9)           # Boxbreite
        box_h = int(parent.height() * 0.8)          # Position auf der horizontalen Ebene 
        return (20, box_y, box_w, box_h)            # Abstand zum linken Rand: 20 


class SignalStatus_SRR_FL(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FL - Sensor Config Message Status",
            row_labels=SENSOR_CONFIG_SIGNALS,
            columns=["Signalname", "Status", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.88)               # Position auf horizontaler Ebene
        y = int(parent.height() * 0.1)               # Position auf vertikaler Ebene 
        w = int(parent.width() * 1)                  # Boxbreite
        h = int(parent.height() * 0.8)               # Boxhöhe
        return (x, y, w, h)
    

class SignalStatus_SRR_FR(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FR - Sensor Config Message Status",
            row_labels=SENSOR_CONFIG_SIGNALS,
            columns=["Signalname", "Status", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        x = int(parent.width() * 0.88)
        box_y = int(parent.height() * 0.9)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 1)             # Boxbreite
        box_h = int(parent.height() * 0.8)          # Position auf der horizontalen Ebene 
        return (x, box_y, box_w, box_h)             
    

class SignalStatus_SRR_RL(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR RL - Sensor Config Message Status",
            row_labels=SENSOR_CONFIG_SIGNALS,
            columns=["Signalname", "Status", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.88)                # Position auf horizontaler Ebene
        y = int(parent.height() * 0.1)                # Position auf vertikaler Ebene 
        w = int(parent.width() * 1)                   # Boxbreite
        h = int(parent.height() * 0.8)                # Boxhöhe
        return (x, y, w, h)
    

class SignalStatus_SRR_RR(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR RR - Sensor Config Message Status",
            row_labels=SENSOR_CONFIG_SIGNALS,
            columns=["Signalname", "Status", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        x = int(parent.width() * 0.88)
        box_y = int(parent.height() * 0.9)          # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 1)             # Boxbreite
        box_h = int(parent.height() * 0.8)          # Position auf der horizontalen Ebene 
        return (x, box_y, box_w, box_h)             
    

class SignalStatus_ARS_FRONT(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="ARS FRONT - Sensor Config Message Status",
            row_labels=SENSOR_CONFIG_SIGNALS,
            columns=["Signalname", "Status", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.88)                # Position auf horizontaler Ebene
        y = int(parent.height() * 0.1)                # Position auf vertikaler Ebene 
        w = int(parent.width() * 1)                   # Boxbreite
        h = int(parent.height() * 0.8)                # Boxhöhe
        return (x, y, w, h)
    

class SignalStatus_ARS_REAR(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="ARS REAR - Sensor Config Message Status",
            row_labels=SENSOR_CONFIG_SIGNALS,
            columns=["Signalname", "Status", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        x = int(parent.width() * 0.88)
        box_y = int(parent.height() * 0.9)           # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 1)              # Boxbreite
        box_h = int(parent.height() * 0.8)           # Position auf der horizontalen Ebene 
        return (x, box_y, box_w, box_h)               


        
"""Poitcloud Klasse & Implemetnierung der Checkboxen"""
class Pointcloud_SRR_FL(PointcloudCheckbox):
    def __init__(self, parent, gui_font, sensor_status_box):
        super().__init__(
            parent,
            gui_font,
            lambda parent: self._geometry(sensor_status_box)
        )

    def _geometry(self, sensor_status_box):
        x = sensor_status_box.x() + 7
        y = sensor_status_box.y() + sensor_status_box.height()
        w = 250
        h = 20
        return (x, y, w, h)
    

class Pointcloud_SRR_FR(PointcloudCheckbox):
    def __init__(self, parent, gui_font, sensor_status_box):
        super().__init__(
            parent,
            gui_font,
            lambda parent: self._geometry(sensor_status_box)
        )

    def _geometry(self, sensor_status_box):
        x = sensor_status_box.x() + 7
        y = sensor_status_box.y() + sensor_status_box.height() 
        w = 250
        h = 20
        return (x, y, w, h)
    
class Pointcloud_SRR_RL(PointcloudCheckbox):
    def __init__(self, parent, gui_font, sensor_status_box):
        super().__init__(
            parent,
            gui_font,
            lambda parent: self._geometry(sensor_status_box)
        )

    def _geometry(self, sensor_status_box):
        x = sensor_status_box.x() + 7
        y = sensor_status_box.y() + sensor_status_box.height()
        w = 250
        h = 20
        return (x, y, w, h)
    

class Pointcloud_SRR_RR(PointcloudCheckbox):
    def __init__(self, parent, gui_font, sensor_status_box):
        super().__init__(
            parent,
            gui_font,
            lambda parent: self._geometry(sensor_status_box)
        )

    def _geometry(self, sensor_status_box):
        x = sensor_status_box.x() + 7
        y = sensor_status_box.y() + sensor_status_box.height() 
        w = 250
        h = 20
        return (x, y, w, h)


    
class Pointcloud_ARS_FRONT(PointcloudCheckbox):
    def __init__(self, parent, gui_font, sensor_status_box):
        super().__init__(
            parent,
            gui_font,
            lambda parent: self._geometry(sensor_status_box)
        )

    def _geometry(self, sensor_status_box):
        x = sensor_status_box.x() + 7
        y = sensor_status_box.y() + sensor_status_box.height()
        w = 250
        h = 20
        return (x, y, w, h)
    

class Pointcloud_ARS_REAR(PointcloudCheckbox):
    def __init__(self, parent, gui_font, sensor_status_box):
        super().__init__(
            parent,
            gui_font,
            lambda parent: self._geometry(sensor_status_box)
        )

    def _geometry(self, sensor_status_box):
        x = sensor_status_box.x() + 7
        y = sensor_status_box.y() + sensor_status_box.height() 
        w = 250
        h = 20
        return (x, y, w, h)


class SensorInformationTable_SRR_FL(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FL - Sensor Information",
            row_labels=SENSOR_SIGNAL_INFORMATION,
            columns=["Signalname", "Result", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 1.8)                   # Position auf horizontaler Ebene
        y = int(parent.height() * 0.1)                  # Position auf vertikaler Ebene
        w = int(parent.width() * 1.25)                  # Boxbreite
        h = int(parent.height() * 0.8)                  # Boxhöhe
        return (x, y, w, h)
    
class SensorInformationTable_SRR_FR(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FR - Sensor Information",
            row_labels=SENSOR_SIGNAL_INFORMATION,
            columns=["Signalname", "Result", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        x = int(parent.width() * 1.8)
        box_y = int(parent.height() * 0.9)            # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 1.25)            # Boxbreite
        box_h = int(parent.height() * 0.8)            # Position auf der horizontalen Ebene 
        return (x, box_y, box_w, box_h)                
    

class SensorInformationTable_SRR_RL(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR RL - Sensor Information",
            row_labels=SENSOR_SIGNAL_INFORMATION,
            columns=["Signalname", "Result", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 1.8)                 # Position auf horizontaler Ebene
        y = int(parent.height() * 0.1)                # Position auf vertikaler Ebene
        w = int(parent.width() * 1.25)                # Boxbreite
        h = int(parent.height() * 0.8)                # Boxhöhe
        return (x, y, w, h)
    
class SensorInformationTable_SRR_RR(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR RR - Sensor Information",
            row_labels=SENSOR_SIGNAL_INFORMATION,
            columns=["Signalname", "Result", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        x = int(parent.width() * 1.8)
        box_y = int(parent.height() * 0.9)           # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 1.25)           # Boxbreite
        box_h = int(parent.height() * 0.8)           # Position auf der horizontalen Ebene 
        return (x, box_y, box_w, box_h)              # Abstand zum linken Rand: 20 
    

class SensorInformationTable_ARS_FRONT(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="ARS FRONT - Sensor Information",
            row_labels=SENSOR_SIGNAL_INFORMATION,
            columns=["Signalname", "Result", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 1.8)                 # Position auf horizontaler Ebene
        y = int(parent.height() * 0.1)                # Position auf vertikaler Ebene
        w = int(parent.width() * 1.25)                # Boxbreite
        h = int(parent.height() * 0.8)                # Boxhöhe
        return (x, y, w, h)
    
class SensorInformationTable_ARS_REAR(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="ARS REAR - Sensor Information",
            row_labels=SENSOR_SIGNAL_INFORMATION,
            columns=["Signalname", "Result", "Description"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        x = int(parent.width() * 1.8)
        box_y = int(parent.height() * 0.9)           # Position auf der vertikalen Ebene
        box_w = int(parent.width() * 1.25)           # Boxbreite
        box_h = int(parent.height() * 0.8)           # Position auf der horizontalen Ebene 
        return (x, box_y, box_w, box_h)             