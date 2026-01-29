from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableWidget
)

from gui.window_parameter import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
)


class SQCQ_DASHBOARD(QMainWindow):
    def __init__(self, font=None, title=None):
        super().__init__()

        self.font = font
        self.title = title or WINDOW_TITLE

        # Fenster-Einstellungen
        self.setWindowTitle(self.title)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Sensor",
            "Sensor Config Message Status",
            "Sensor Information"
        ])

        layout.addWidget(self.table)

        # Nach dem Befüllen sinnvoll
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def geometry_from_parent(self, parent):
        box_y = int(parent.height() * 0.1)
        box_h = int(parent.height() * 0.38)
        box_w = int(parent.width() * 0.3)
        return (20, box_y, box_w, box_h)
