import sys
import types

# CI installs only the lightweight test dependencies, not OpenCV. config.py
# needs cv2 for one font constant, so give it a stand-in when cv2 is missing.
try:
    import cv2  # noqa: F401
except ImportError:
    sys.modules["cv2"] = types.SimpleNamespace(FONT_HERSHEY_SIMPLEX=0)
