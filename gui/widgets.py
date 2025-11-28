# gui/widgets.py
"""Widget-Komponenten des Dashboards"""

from PyQt5.QtWidgets import QFrame, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from .window_settings import LOGO_PATH, EGO_SIGNALS, SENSOR_CONFIG_SIGNALS
from .functions import apply_font_to_table, create_table_item


class TitleBox(QFrame):
    """Titel-Box mit Logo und Überschrift"""
    def __init__(self, parent, gui_font):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)
        
        box_height = int(parent.height() * 0.15)
        self.setGeometry(0, 0, parent.width(), box_height)
        
        # Logo
        logo_label = QLabel(self)
        logo_label.setGeometry(5, 5, 200, box_height)
        pix = QPixmap(LOGO_PATH)
        if not pix.isNull():
            scaled_pix = pix.scaled(logo_label.width(), logo_label.height(), Qt.KeepAspectRatio)
            logo_label.setPixmap(scaled_pix)
        
        # Titel
        title_label = QLabel("Signal State Dashboard", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setGeometry(0, 0, parent.width(), box_height)


class EgomotionBox(QFrame):
    """Egomotion-Tabelle mit Sensordaten"""
    def __init__(self, parent, gui_font):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)
        self.gui_font = gui_font
        
        # Label
        label = QLabel("Egomotion", self, alignment=Qt.AlignHCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        # Tabelle - 9 Zeilen, 2 Spalten
        self.table = QTableWidget(9, 2, self)
        self.table.setHorizontalHeaderLabels(["Signalname", "Value"])
        self.table.setShowGrid(False)
        self.table.setFrameStyle(QFrame.NoFrame)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        
        # Einträge
        for i, name in enumerate(EGO_SIGNALS):
            item = QTableWidgetItem(name)
            item.setFont(gui_font)
            self.table.setItem(i, 0, item)
        
        apply_font_to_table(self.table, gui_font)
        
        # Positionierung
        box_y = int(parent.height() * 0.1) + 10
        box_height = int(parent.height() * 0.78)
        usable_width = parent.width()
        box_width = int(usable_width * 0.5)
        
        self.setGeometry(10, box_y, box_width, box_height)
        label.setGeometry(0, 15, box_width, 40)
        self.table.setGeometry(10, 50, box_width - 20, box_height - 60)


class SensorConfigBox(QFrame):
    """Sensor-Config-Tabelle mit Status-Infos"""
    def __init__(self, parent, gui_font):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)
        self.gui_font = gui_font
        
        # Label
        label = QLabel("Sensor Config Message Status", self, alignment=Qt.AlignHCenter)
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
        box_height = int(parent.height() * 0.65)
        usable_width = parent.width() - 30
        box_width = int(usable_width * 0.5)
        x = 10 + box_width + 10
        
        self.setGeometry(x, box_y, box_width, box_height)
        label.setGeometry(0, 15, box_width, 40)
        self.table.setGeometry(10, 50, box_width - 20, box_height - 60)


class PointcloudCheckbox(QCheckBox):
    """Checkbox für Pointcloud-Steuerung"""
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