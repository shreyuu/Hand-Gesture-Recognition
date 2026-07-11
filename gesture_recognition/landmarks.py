"""Landmark preprocessing shared by the recorder, trainer and recognizer."""

import numpy as np


def normalize_landmarks(landmarks):
    """Make landmarks translation- and scale-invariant.

    Takes the 21 MediaPipe hand landmarks as ``[x, y]`` pixel pairs (wrist
    first, landmark id 0), translates them so the wrist is the origin and
    scales them so the largest coordinate magnitude is 1. The result no longer
    depends on where the hand is in the frame, how far it is from the camera,
    or the camera resolution.

    Returns a list of ``[x, y]`` float pairs.
    """
    points = np.asarray(landmarks, dtype=np.float32)
    points = points - points[0]

    scale = np.abs(points).max()
    if scale > 0:
        points = points / scale

    return points.tolist()
