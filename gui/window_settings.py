"""Fenstereinstellungen und Konstanten"""

# Fenster-Einstellungen
WINDOW_TITLE = "Vehicle Gateway Dashboard"
WINDOW_WIDTH = 1900     # 1300
WINDOW_HEIGHT = 950

# Schriftart
FONT_PATH = '/home/admin/Desktop/ETH_Gateway/assets/fonts/AUMOVIOOffice-Regular.ttf'
FONT_SIZE = 12

# Bilder
LOGO_PATH = "/home/admin/Desktop/ETH_Gateway/assets/image/Aumovio_Logo_orange_black_transparent.png"


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
    "Vehicle Longitudinal Acceleration",
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

SENSOR_SIGNAL_INFORMATION = [
    "Software Version",
    "Sensor Operation Mode",
    "Calibration",
    "Blockage Status",
    "Valid Detections"
]