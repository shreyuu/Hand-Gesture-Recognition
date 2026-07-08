from collections import Counter, deque


class GestureSmoother:
    """
    Smooths gesture predictions to prevent rapid flickering between gestures
    """

    def __init__(self, history_length=10, confidence_threshold=0.5, dominance=0.4):
        self.history = deque(maxlen=history_length)
        self.history_length = history_length
        self.confidence_threshold = confidence_threshold
        self.dominance = dominance

    def update(self, gesture_name, confidence):
        """
        Add a new gesture prediction to the history
        """
        # Only consider predictions with sufficient confidence
        if confidence >= self.confidence_threshold:
            self.history.append(gesture_name)

    def get_dominant_gesture(self):
        """
        Return the most frequent gesture in the history, but only if it is
        dominant enough (appears in at least `dominance` of recent frames).
        """
        if not self.history:
            return ""

        dominant_gesture, max_count = Counter(self.history).most_common(1)[0]

        if max_count >= len(self.history) * self.dominance:
            return dominant_gesture
        return ""
