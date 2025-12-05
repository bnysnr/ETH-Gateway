# gui/widgets.py
"""Widget-Komponenten des Dashboards"""

from PyQt5.QtWidgets import QFrame, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from .window_settings import LOGO_PATH, EGO_SIGNALS, SENSOR_CONFIG_SIGNALS
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
            columns=["Signalname", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.1)          # Position auf der vertikalen Ebene
        box_h = int(parent.height() * 0.38)         # Position auf der horizontalen Ebene 
        box_w = int(parent.width() * 0.3)           # Boxbreite
        return (10, box_y, box_w, box_h)            # Abstand zum linken Rand: 10
    
class Egomotion_SRR_FR(GenericEgomotionTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="SRR FR - Egomotion",
            row_labels=EGO_SIGNALS,
            columns=["Signalname", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        box_y = int(parent.height() * 0.54)         # Position auf der vertikalen Ebene
        box_h = int(parent.height() * 0.38)         # Position auf der horizontalen Ebene 
        box_w = int(parent.width() * 0.3)           # Boxbreite
        return (10, box_y, box_w, box_h)            
    
"""    
class Egomotion_SRR_RL(GenericTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="Wheel Speed",
            row_labels=["FL", "FR", "RL", "RR"],
            columns=["Signalname", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.5) + 20
        y = int(parent.height() * 0.1) + 10
        w = int(parent.width() * 0.45)
        h = int(parent.height() * 0.38)
        return (x, y, w, h)
    

class Egomotion_SRR_RR(GenericTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="Wheel Speed",
            row_labels=["FL", "FR", "RL", "RR"],
            columns=["Signalname", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.5) + 20
        y = int(parent.height() * 0.1) + 10
        w = int(parent.width() * 0.45)
        h = int(parent.height() * 0.38)
        return (x, y, w, h)
    

class Egomotion_ARS_FRONT(GenericTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="Wheel Speed",
            row_labels=["FL", "FR", "RL", "RR"],
            columns=["Signalname", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.5) + 20
        y = int(parent.height() * 0.1) + 10
        w = int(parent.width() * 0.45)
        h = int(parent.height() * 0.38)
        return (x, y, w, h)
    

class Egomotion_ARS_REAR(GenericTable):
    def __init__(self, parent, gui_font):
        super().__init__(
            parent,
            gui_font,
            title="Wheel Speed",
            row_labels=["FL", "FR", "RL", "RR"],
            columns=["Signalname", "Value"],
            geometry_func=self._geometry
        )

    def _geometry(self, parent):
        # Position rechts neben Egomotion
        x = int(parent.width() * 0.5) + 20
        y = int(parent.height() * 0.1) + 10
        w = int(parent.width() * 0.45)
        h = int(parent.height() * 0.38)
        return (x, y, w, h)

 """        


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
        x = int(parent.width() * 0.35)                  # Position auf horizontaler Ebene
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
        x = int(parent.width() * 0.35)                  # Position auf horizontaler Ebene
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


"""    

class SensorConfigBox(QFrame):
    #Sensor-Config-Tabelle mit Status-Infos
    def __init__(self, parent, gui_font):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)
        self.gui_font = gui_font
        
        # Label
        label = QLabel("SRR FL - Sensor Config Message Status", self, alignment=Qt.AlignHCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        # Tabelle - 7 Zeilen, 3 Spalten
        self.table = QTableWidget(7, 3, self)
        self.table.setHorizontalHeaderLabels(["Signalname", "Status", "Description"])
        self.table.setShowGrid(False)
        self.table.setFrameStyle(QFrame.NoFrame)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        
        # Einträge
        for i, name in enumerate(SENSOR_CONFIG_SIGNALS):
            item = QTableWidgetItem(name)
            item.setFont(gui_font)
            self.table.setItem(i, 0, item)
        
        apply_font_to_table(self.table, gui_font)
        
        # Positionierung
        box_y = int(parent.height() * 0.1) + 10
        box_height = int(parent.height() * 0.32)
        total_width = parent.width() - 30
        box_width = int(total_width * 0.5)
        x = 10 + box_width + 10
        
        self.setGeometry(x, box_y, box_width, box_height)
        label.setGeometry(0, 15, box_width, 40)
        self.table.setGeometry(10, 50, box_width - 20, box_height - 60)
"""

""""

class PointcloudCheckbox(QCheckBox):
    #Checkbox für Pointcloud-Steuerung
    def __init__(self, parent, gui_font, sensor_config_box):
        super().__init__("Pointcloud deactivated", parent)
        self.setFont(gui_font)
        
        # Positionierung unter der Sensor-Config-Box
        cb_x = sensor_config_box.x() + 7
        cb_y = sensor_config_box.y() + sensor_config_box.height() + 10
        self.setGeometry(cb_x, cb_y, 250, 30)
        
        # Signal
        self.stateChanged.connect(self.on_state_changed)
    
    def on_state_changed(self, state):
        if self.isChecked():
            self.setText("Pointcloud activated")
        else:
            self.setText("Pointcloud deactivated")

"""