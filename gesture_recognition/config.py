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


def _coerce(name, value):
    """Check a profile value has the setting's type, parsing strings.

    Profiles are hand-editable JSON, so e.g. ``"enable_voice": "false"``
    (a truthy string) or a camera_index that cv2.VideoCapture() would open as
    a URL or file must not be used as-is. Returns None if unusable.
    """
    _, parse, default = PROFILE_SETTINGS[name]
    expected = type(default)
    if type(value) is expected:
        return value
    if expected is float and type(value) is int:
        return float(value)
    if isinstance(value, str):
        try:
            return parse(value)
        except ValueError:
            pass
    print(f"Ignoring invalid {name!r} in profile: {value!r}")
    return None


def saved_setting(name, profile=None):
    """The profile's value for a setting, else the built-in default.

    Ignores env vars: this is what the settings dialog shows and saves, so a
    one-off env override never gets written into the profile.
    """
    value = profile.get(name) if profile is not None else None
    if value is not None:
        value = _coerce(name, value)
    return value if value is not None else default_setting(name)


def resolve_setting(name, profile=None):
    """Return the effective value of a profile setting.

    The env var wins (a one-off override), then the profile, then the
    built-in default. Unusable values are reported and skipped.
    """
    try:
        value = env_setting(name)
    except ValueError as e:
        print(f"Ignoring invalid {PROFILE_SETTINGS[name][0]}: {e}")
        value = None
    return value if value is not None else saved_setting(name, profile)


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
