# generic_pointcloud_checkbox.py

from PyQt5.QtWidgets import QCheckBox

class PointcloudCheckbox(QCheckBox):
    """Dynamische Checkbox für Pointcloud-Steuerung"""

    def __init__(self, parent, gui_font, geometry_func):
        super().__init__("Pointcloud deactivated", parent)

        self.setFont(gui_font)

        # Dynamische Positionierung
        x, y, w, h = geometry_func(parent)
        self.setGeometry(x, y, w, h)

        # Signal
        self.stateChanged.connect(self.on_state_changed)
    
    def on_state_changed(self, state):
        if self.isChecked():
            self.setText("Pointcloud activated")
        else:
            self.setText("Pointcloud deactivated")
