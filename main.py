import sys
from PyQt5.QtWidgets import QApplication
from gui.dashboard import Dashboard
from publisher.can_msg_sender import can_msg_sender
import threading




def main():
    """Startet die Anwendung"""
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    can_msg_sender_obj = can_msg_sender()

    dashboard.show()
    
    
    can_msg_sender_thread = threading.Thread(target=can_msg_sender_obj.start)
    can_msg_sender_thread.start()

    egomotion_thread = threading.Thread(target=dashboard.update_egomotion_value_thread)
    egomotion_thread.start()

    update_radar_status_val_thread = threading.Thread(target=dashboard.update_radar_status_thread)
    update_radar_status_val_thread.start()

    radarsensor_information_thread = threading.Thread(target=dashboard.update_radar_signal_information_thread)
    radarsensor_information_thread.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()