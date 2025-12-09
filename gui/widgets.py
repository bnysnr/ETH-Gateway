# gui/widgets.py
"""Widget-Komponenten des Dashboards"""

from PyQt5.QtWidgets import QFrame, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from .window_settings import LOGO_PATH, EGO_SIGNALS, SENSOR_CONFIG_SIGNALS, SENSOR_SIGNAL_INFORMATION
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
        
        box_height = int(parent.height() * 0.1)
        self.setGeometry(0, 0, parent.width(), box_height)
        
        # Logo
        logo_label = QLabel(self)
        logo_label.setGeometry(5, 5, 200, box_height)
        pix = QPixmap(LOGO_PATH)
        if not pix.isNull():
            scaled_pix = pix.scaled(logo_label.width(), logo_label.height(), Qt.KeepAspectRatio)
            logo_label.setPixmap(scaled_pix)
        
        # Titel
        title_label = QLabel("Vehicle Gateway Dashboard", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setGeometry(0, 0, parent.width(), box_height)



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
        box_h = int(parent.height() * 0.38)         # Position auf der horizontalen Ebene 
        box_w = int(parent.width() * 0.3)           # Boxbreite
        return (20, box_y, box_w, box_h)            # Abstand zum linken Rand: 10
    
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
        box_y = int(parent.height() * 0.54)         # Position auf der vertikalen Ebene
        box_h = int(parent.height() * 0.38)         # Position auf der horizontalen Ebene 
        box_w = int(parent.width() * 0.3)           # Boxbreite
        return (20, box_y, box_w, box_h)            


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
        x = int(parent.width() * 0.34)                  # Position auf horizontaler Ebene
        y = int(parent.height() * 0.1)                  # Position auf vertikaler Ebene 
        w = int(parent.width() * 0.35)                  # Boxbreite
        h = int(parent.height() * 0.38)                 # Boxhöhe
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
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.34)                  # Position auf horizontaler Ebene
        y = int(parent.height() * 0.54)                   # Position auf vertikaler Ebene
        w = int(parent.width() * 0.35)                  # Boxbreite
        h = int(parent.height() * 0.38)                 # Boxhöhe
        return (x, y, w, h)
    

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



class SensorInformationTable_SRR_FL(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FL - Sensor Information",
            row_labels=SENSOR_SIGNAL_INFORMATION,
            columns=["Signalname", "Result"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.72)                   # Position auf horizontaler Ebene
        y = int(parent.height() * 0.1)                  # Position auf vertikaler Ebene
        w = int(parent.width() * 0.25)                   # Boxbreite
        h = int(parent.height() * 0.32)                 # Boxhöhe
        return (x, y, w, h)
    
class SensorInformationTable_SRR_FR(GenericSignalStatus):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FR - Sensor Information",
            row_labels=SENSOR_SIGNAL_INFORMATION,
            columns=["Signalname", "Result"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.72)                   # Position auf horizontaler Ebene
        y = int(parent.height() * 0.54)                 # Position auf vertikaler Ebene
        w = int(parent.width() * 0.25)                 # Boxbreite
        h = int(parent.height() * 0.32)                 # Boxhöhe
        return (x, y, w, h)