# gui/window_settings.py
"""Fenstereinstellungen und Konstanten"""

# Fenster-Einstellungen
WINDOW_TITLE = "Signal State Dashboard"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 475

# Schriftart
FONT_PATH = '/home/admin/Praxissemester/font/TTF/AUMOVIOOffice-Regular.ttf'
FONT_SIZE = 12

# Bilder
LOGO_PATH = "/home/admin/Praxissemester/script/Aumovio_Logo_orange_black_transparent.png"

# Layout-Proportionen
TITLE_BOX_HEIGHT_RATIO = 0.15
CONTENT_BOX_HEIGHT_RATIO = 0.85
BOX_SPACING = 10

# Tabellen-Daten
EGO_SIGNALS = [
    "Yaw Rate", 
    "Steering Wheel Angle", 
    "Lateral Acceleration",
    "Wheel Velocity Front Left", 
    "Wheel Velocity Front Right",
    "Wheel Velocity Rear Left", 
    "Wheel Velocity Rear Right",
    "Vehicle Velocity", 
    "Vehicle Longitudinal Acceleration"
]

SENSOR_CONFIG_SIGNALS = [
    "LongitudinalVelocity", 
    "LongitudinalAcceleration",
    "LateralAcceleration", 
    "YawRate",
    "SteeringAngle", 
    "DrivingDirection",
    "CharacteristicSpeed"
]

# Status-Beschreibungen
STATUS_DESCRIPTIONS = {
    0: "STATE VALID",
    1: "STATE INVALID",
    2: "STATE NOT AVAILABLE",
    3: "STATE DECREASED",
    4: "STATE SUBSTITUE",
    5: "STATE INPLAUSIBLE",
    6: "STATE OF CALC",
    7: "STATE SENSOR",
    8: "STATE EXTRAPOLATED",
    15: "STATE INIT",
    255: "STATE MAX"
}