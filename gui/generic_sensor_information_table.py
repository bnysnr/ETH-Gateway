from PyQt5.QtWidgets import QFrame, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from .functions import apply_font_to_table

class GenericSensorInformationTable(QFrame):
    
    def __init__(self, parent, gui_font, title, row_labels, columns, geometry_func):
        super().__init__(parent)

        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)
        self.gui_font = gui_font
        self.title = title
        self.columns = columns
        self.row_labels = row_labels

        # Positionierung dynamisch übergeben
        x, y, w, h = geometry_func(parent)
        self.setGeometry(x, y, w, h)

        # Titel
        label = QLabel(title, self, alignment=Qt.AlignHCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        label.setGeometry(0, 15, w - 50, 40)

        # Tabelle
        self.table = QTableWidget(len(row_labels), len(columns), self)
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setShowGrid(False)
        self.table.setFrameStyle(QFrame.NoFrame)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)

        self.table.setGeometry(0, 50, w - 20, h - 60)

        # Zeileneinträge
        for i, name in enumerate(row_labels):
            item = QTableWidgetItem(name)
            item.setFont(gui_font)
            self.table.setItem(i, 0, item)

        # Schrift anwenden
        apply_font_to_table(self.table, gui_font)

    def update_values(self, values: list):
        """Aktualisiert die Werte in der Tabelle"""
        for i, value in enumerate(values):
            item = QTableWidgetItem(str(value))
            item.setFont(self.gui_font)
            self.table.setItem(i, 1, item)
