# gui/functions.py
"""Hilfsfunktionen und BackEnd-Logik"""

from PyQt5.QtGui import QFontDatabase, QFont, QColor, QBrush
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from .window_settings import FONT_PATH, FONT_SIZE, STATUS_DESCRIPTIONS


def load_custom_font():
    """Lädt die Custom-Schriftart und gibt sie zurück"""
    font_id = QFontDatabase.addApplicationFont(FONT_PATH)
    if font_id == -1:
        print("Fehler beim Laden der Schriftart!")
        return QFont()
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        return QFont(font_family, FONT_SIZE)


def apply_font_to_table(table, font):
    """Wendet eine Schriftart auf die gesamte Tabelle an"""
    table.setFont(font)
    table.horizontalHeader().setFont(font)
    table.verticalHeader().setFont(font)
    for r in range(table.rowCount()):
        for c in range(table.columnCount()):
            item = table.item(r, c)
            if item:
                item.setFont(font)


def get_status_description(value):
    """Gibt die Beschreibung für einen Status-Wert zurück"""
    return STATUS_DESCRIPTIONS.get(value, "UNKNOWN")


def create_table_item(text, font, is_status=False, status_value='00'):
    """Erstellt ein formatiertes Table-Item"""
    item = QTableWidgetItem(text)
    item.setFont(font)
    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    
    # Farbcodierung für Status-Spalte
    if is_status:
        if status_value == '00':
            item.setForeground(QBrush(QColor("green")))
        else:
            item.setForeground(QBrush(QColor("red")))
    
    return item