import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem
)
from PyQt5.QtCore import Qt
from .window_parameter import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
)

class SQCQ_DASHBOARD(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SQCQ Dashboard")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Sensor ID",
            "Operation Mode",
            "Azimuth",
            "Elevation",
            "Connection"
        ])

        layout.addWidget(self.table)

        #self.load_example_data()

        # 🔥 WICHTIG: erst NACH dem Befüllen
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        self.adjustSize()   # ⬅️ Fenster passt sich Tabelle an



    def load_example_data(self):
        data = [
            ("192.168.16.12", "8", "-0.000003", "-0.000003", "Connected"),
            ("192.168.16.13", "8", "0.000001", "0.000002", "Connected"),
            ("192.168.16.15", "-", "-", "-", "NO CONNECTION"),
        ]

        self.table.setRowCount(len(data))

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SQCQ_DASHBOARD()
    window.show()
    sys.exit(app.exec_())
"""