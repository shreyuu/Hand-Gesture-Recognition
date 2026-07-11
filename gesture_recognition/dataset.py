"""Loading of recorded gesture samples.

Kept free of TensorFlow imports so it can be unit-tested (and run in CI)
without installing the heavy ML dependencies.
"""

import json
import os

from gesture_recognition.landmarks import normalize_landmarks

# Recordings are saved as <gesture_name>_<YYYYmmdd>_<HHMMSS>.json, so the
# timestamp is always the last two underscore-separated parts.
TIMESTAMP_PARTS = 2


def gesture_name_from_filename(filename):
    """Extract the gesture name from a recording filename.

    Handles gesture names that themselves contain underscores, e.g.
    ``thumbs_up_20260709_201708.json`` -> ``thumbs_up``.
    """
    stem = os.path.splitext(filename)[0]
    return stem.rsplit("_", TIMESTAMP_PARTS)[0]


def load_samples(data_dir, normalize=True):
    """Load all recorded samples from ``data_dir``.

    Files are processed in sorted order so the label indices are reproducible
    across runs. Returns ``(x, y, gestures)`` where ``x`` is a list of
    landmark samples, ``y`` the matching label indices, and ``gestures`` the
    ordered label names.
    """
    x, y, gestures = [], [], []

    files = sorted(f for f in os.listdir(data_dir) if f.endswith(".json"))
    for filename in files:
        gesture_name = gesture_name_from_filename(filename)
        if gesture_name not in gestures:
            gestures.append(gesture_name)
        label = gestures.index(gesture_name)

        with open(os.path.join(data_dir, filename), "r") as f:
            samples = json.load(f)

        for sample in samples:
            if normalize:
                sample = normalize_landmarks(sample)
            x.append(sample)
            y.append(label)

    return x, y, gestures
