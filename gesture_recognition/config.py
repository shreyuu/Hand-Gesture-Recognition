"""
Configuration settings for the Hand Gesture Recognition application.
"""

import os

import cv2

# Project root (the directory containing this package). Data and model paths are
# anchored to it so the app runs regardless of the current working directory.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Load environment variables with defaults
def get_env(key, default):
    return os.environ.get(key, default)


def _parse_bool(value):
    return value.strip().lower() in ("1", "true", "yes", "on")


# Settings that a user profile can also set. Each maps to
# (env var, parser for the env var's string value, built-in default).
# Read them with resolve_setting(), never directly.
PROFILE_SETTINGS = {
    "camera_index": ("GESTURE_CAM_INDEX", int, 0),
    "detection_confidence": ("GESTURE_DETECTION_CONF", float, 0.7),
    "enable_voice": ("GESTURE_VOICE_ENABLED", _parse_bool, False),
    "voice_language": ("GESTURE_VOICE_LANG", str, "en"),
}


def env_setting(name):
    """The env var value for a profile setting, or None if it isn't set."""
    env_var, parse, _ = PROFILE_SETTINGS[name]
    raw = os.environ.get(env_var)
    return parse(raw) if raw is not None else None


def default_setting(name):
    """The built-in default for a profile setting."""
    return PROFILE_SETTINGS[name][2]


def resolve_setting(name, profile=None):
    """Return the effective value of a profile setting.

    Three sources can provide a value:
      - env_setting(name): the env var, or None if unset
      - profile.get(name): what the user saved in their profile JSON, or None
        if the profile doesn't set it (profile itself may be None)
      - default_setting(name): the built-in default, always available
    """
    # TODO(you): decide which source wins. See the discussion in chat.
    # Placeholder until then: profile, else default (env vars are ignored).
    value = profile.get(name) if profile is not None else None
    return value if value is not None else default_setting(name)


# Camera settings
CAMERA_WIDTH = int(get_env("GESTURE_CAM_WIDTH", "640"))
CAMERA_HEIGHT = int(get_env("GESTURE_CAM_HEIGHT", "480"))
# Give up after this many consecutive failed frame reads (camera unplugged)
MAX_FAILED_READS = 50

# Hand detection settings
MAX_HANDS = int(get_env("GESTURE_MAX_HANDS", "1"))
TRACKING_CONFIDENCE = float(get_env("GESTURE_TRACKING_CONF", "0.5"))

# Model settings
MODEL_PATH = get_env("GESTURE_MODEL_PATH", os.path.join(BASE_DIR, "models", "mp_hand_gesture"))
GESTURE_NAMES_PATH = get_env("GESTURE_NAMES_PATH", os.path.join(BASE_DIR, "data", "gesture.names"))

# Voice feedback settings
VOICE_COOLDOWN_TIME = float(get_env("GESTURE_VOICE_COOLDOWN", "2"))
AUDIO_CACHE_SIZE = int(get_env("GESTURE_AUDIO_CACHE_SIZE", "20"))

# UI settings
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (0, 0, 255)  # Red (BGR)
FONT_SCALE = 1
FONT_THICKNESS = 2

# Advanced settings
SMOOTHING_HISTORY_LENGTH = int(get_env("GESTURE_SMOOTHING_LENGTH", "15"))
CONFIDENCE_THRESHOLD = float(get_env("GESTURE_CONFIDENCE_THRESHOLD", "0.5"))
