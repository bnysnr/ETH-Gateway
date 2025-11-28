import sys
import os
import time
import threading

# Füge den Pfad zu deinem Projektordner (ETH_Gateway) hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from publisher.can_msg_sender import can_msg_sender
from publisher.radar_status_reader import radar_status_reader

class data_interface:
    def __init__(self):
        self.signal_values = []
        self.radar_states = []
        self.can_msg_sender_obj = can_msg_sender() 
        self.radar_state_reader_obj = radar_status_reader()
        self.running = False

    def set_signal_values(self, signal_val_arr):
        self.signal_values = signal_val_arr

    def get_signal_values(self):
        return self.signal_values

    def set_radar_state_values(self, radar_state_arr):
        self.radar_states = radar_state_arr

    def get_radar_states(self):
        return self.radar_states

    def update_radar_state(self):
        """Aktualisiert Radar-Status aus dem Reader"""
        try:
            for values in self.radar_state_reader_obj.run():
                if not self.running:
                    break
                self.set_radar_state_values(values)
                print(f"Radar Status: {values}")
        except Exception as e:
            print(f"Fehler beim Lesen des Radar-Status: {e}")

    def update_can_message(self):
        """Liest aktualisierte CAN-Werte (keine erneute Übertragung)"""
        try:
            while self.running:
                signal_values = self.can_msg_sender_obj.get_vhc_can_val_arr()
                if signal_values:  # Nur setzen wenn nicht leer
                    self.set_signal_values(signal_values)
                time.sleep(0.5)
        except Exception as e:
            print(f"Fehler beim Lesen der CAN-Nachrichten: {e}")

    def start(self):
        """Startet CAN-Sender und Update-Threads"""
        if self.running:
            print("Already running!")
            return
        
        self.running = True
        
        self.can_msg_sender_obj.start()

        # Radar-Status-Thread starten
        radar_thread = threading.Thread(target=self.update_radar_state, daemon=True)
        radar_thread.start()

        # CAN-Nachrichten-Anzeigethread starten (nur lesen, kein Senden)
        can_thread = threading.Thread(target=self.update_can_message, daemon=True)
        can_thread.start()

    def stop(self):
        """Stoppt alle Threads"""
        self.running = False
        self.can_msg_sender_obj.stop()



if __name__ == "__main__":
    data_model_obj = data_interface()
    
    # Starte die Datenverarbeitung
    data_model_obj.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        data_model_obj.stop()