"""
Configuration settings for the Hand Gesture Recognition application.
"""

import cv2
import os


# Load environment variables with defaults
def get_env(key, default):
    return os.environ.get(key, default)


# Camera settings
CAMERA_INDEX = int(get_env("GESTURE_CAM_INDEX", "1"))
CAMERA_WIDTH = int(get_env("GESTURE_CAM_WIDTH", "640"))
CAMERA_HEIGHT = int(get_env("GESTURE_CAM_HEIGHT", "480"))

# Hand detection settings
MAX_HANDS = int(get_env("GESTURE_MAX_HANDS", "1"))
DETECTION_CONFIDENCE = float(get_env("GESTURE_DETECTION_CONF", "0.7"))
TRACKING_CONFIDENCE = float(get_env("GESTURE_TRACKING_CONF", "0.5"))

# Model settings
MODEL_PATH = get_env("GESTURE_MODEL_PATH", "models/mp_hand_gesture")
GESTURE_NAMES_PATH = get_env("GESTURE_NAMES_PATH", "gesture.names")

# Voice feedback settings
ENABLE_VOICE_DEFAULT = get_env("GESTURE_VOICE_ENABLED", "False").lower() == "true"
VOICE_COOLDOWN_TIME = float(get_env("GESTURE_VOICE_COOLDOWN", "2"))
VOICE_LANGUAGE = get_env("GESTURE_VOICE_LANG", "en")
AUDIO_CACHE_SIZE = int(get_env("GESTURE_AUDIO_CACHE_SIZE", "20"))

# UI settings
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (0, 0, 255)  # Red (BGR)
FONT_SCALE = 1
FONT_THICKNESS = 2

# Advanced settings
SMOOTHING_HISTORY_LENGTH = int(get_env("GESTURE_SMOOTHING_LENGTH", "15"))
CONFIDENCE_THRESHOLD = float(get_env("GESTURE_CONFIDENCE_THRESHOLD", "0.5"))
