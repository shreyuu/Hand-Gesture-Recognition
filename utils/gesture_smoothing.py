class GestureSmoother:
    """
    Smooths gesture predictions to prevent rapid flickering between gestures
    """

    def __init__(self, history_length=10, confidence_threshold=0.5):
        self.history = []
        self.history_length = history_length
        self.confidence_threshold = confidence_threshold

    def update(self, gesture_name, confidence):
        """
        Add a new gesture prediction to the history
        """
        # Only consider predictions with sufficient confidence
        if confidence >= self.confidence_threshold:
            self.history.append(gesture_name)

        # Keep history at the desired length
        if len(self.history) > self.history_length:
            self.history.pop(0)

    def get_dominant_gesture(self):
        """
        Return the most frequent gesture in the history
        """
        if not self.history:
            return ""

        # Count occurrences of each gesture
        gesture_counts = {}
        for gesture in self.history:
            if gesture in gesture_counts:
                gesture_counts[gesture] += 1
            else:
                gesture_counts[gesture] = 1

        # Find the most common gesture
        dominant_gesture = ""
        max_count = 0

        for gesture, count in gesture_counts.items():
            if count > max_count:
                max_count = count
                dominant_gesture = gesture

        # Only return if it appears in at least 40% of the history
        if max_count >= self.history_length * 0.4:
            return dominant_gesture
        else:
            return ""
