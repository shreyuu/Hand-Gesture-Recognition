"""
Configuration settings for the Hand Gesture Recognition application.
"""

import cv2

# Camera settings
CAMERA_INDEX = 1  # 0 for default camera, adjust as needed
CAMERA_WIDTH = 640  # Camera resolution width
CAMERA_HEIGHT = 480  # Camera resolution height

# Hand detection settings
MAX_HANDS = 1
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.5

# Model settings
MODEL_PATH = "models/mp_hand_gesture"
GESTURE_NAMES_PATH = "gesture.names"

# Voice feedback settings
ENABLE_VOICE_DEFAULT = False
VOICE_COOLDOWN_TIME = 2  # seconds between voice announcements
VOICE_LANGUAGE = "en"
AUDIO_CACHE_SIZE = 20  # Number of audio files to cache

# UI settings
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (0, 0, 255)  # Red (BGR)
FONT_SCALE = 1
FONT_THICKNESS = 2
