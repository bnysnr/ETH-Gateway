# main.py
"""Entry-Point für das Signal State Dashboard"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.dashboard import Dashboard


def main():
    """Startet die Anwendung"""
    app = QApplication(sys.argv)
    
    dashboard = Dashboard()
    dashboard.show()
    
    # Beispiel: externe Daten einspeisen (aus anderer Quelle)
    dashboard.update_signal_status_values(['0', '1', '0', '2', '0', '0', '1'])
    dashboard.update_egomotion_values(['0.5', '-10', '0.2', '50', '50', '45', '45', '60', '0.1'])
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()