"""Fenstereinstellungen und Konstanten"""

# Fenster-Einstellungen
WINDOW_TITLE = "Vehicle Gateway Dashboard"
WINDOW_WIDTH = 1920    
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

# Egomotion Signaleinheiten
EGO_SIGNAL_UNITS = [
    "rad/s",
    "rad",
    "m/s²",
    "m/s",
    "m/s",
    "m/s",
    "m/s",
    "m/s",
    "m/s²"
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
    "Azimuth Misalignment (rad)",
    "Elevation Misalignment (rad)",
    "Blockage Status",
    "Valid Detections",
    "Calibration",
    "Connection to Vehicle"
]

EGOMOTION_DEFAULT_VALUES = [
    "None",
    "None",
    "None",
    "None",
    "None",
    "None",
    "None"
]

RADAR_STATUS_DEFAULT_VALUES = [
    "02",
    "02",
    "02",
    "02",
    "02",
    "02",
    "02"
]

SIGNALE_INFORMATION_NOT_CONNECTED = [
    "NO CONNECTION",
    "NO CONNECTION",
    "NO CONNECTION",
    "NO CONNECTION",
    "NO CONNECTION",
    "NO CONNECTION",
    "NO CONNECTION",
    "NO CONNECTION"
]

SENSOR_OPERATION_MODE = {
    3: "NORMAL",
    8: "AIA MODE",
    9: "NO EMISSION"
}

BLOCKAGE_STATE = {
    0: "BLIND",
    1: "BLOCKAGE HIGH",
    2: "BLOCKAGE MID",
    3: "BLOCKAGE LOW",
    4: "NO BLOCKAGE"

}

BLOCKAGE_STATE_SELFTEST = {
    0: "SELFTEST FAILED",
    1: "SEFTTEST SUCCESS",
    2: "SELFTEST ONGOING"
}