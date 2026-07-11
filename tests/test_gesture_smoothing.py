from gesture_recognition.services.gesture_smoothing import GestureSmoother


def test_empty_history_returns_empty():
    smoother = GestureSmoother()
    assert smoother.get_dominant_gesture() == ""


def test_low_confidence_predictions_ignored():
    smoother = GestureSmoother(confidence_threshold=0.5)
    smoother.update("wave", 0.4)
    assert smoother.get_dominant_gesture() == ""


def test_dominant_gesture_returned():
    smoother = GestureSmoother(history_length=10, dominance=0.4)
    for _ in range(5):
        smoother.update("wave", 0.9)
    assert smoother.get_dominant_gesture() == "wave"


def test_no_dominant_gesture_when_flickering():
    smoother = GestureSmoother(history_length=10, dominance=0.6)
    for name in ["wave", "fist", "peace", "okay", "rock"] * 2:
        smoother.update(name, 0.9)
    assert smoother.get_dominant_gesture() == ""


def test_history_length_limits_memory():
    smoother = GestureSmoother(history_length=3, dominance=0.5)
    for _ in range(10):
        smoother.update("old", 0.9)
    for _ in range(3):
        smoother.update("new", 0.9)
    assert smoother.get_dominant_gesture() == "new"
