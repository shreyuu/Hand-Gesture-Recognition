import time
import numpy as np
import cv2


class PerformanceAnalyzer:
    """
    Tracks performance metrics for the application.
    """

    def __init__(self, max_samples=100):
        self.detection_times = []
        self.prediction_times = []
        self.frame_times = []
        self.max_samples = max_samples
        self.last_frame_time = time.time()

    def start_frame(self):
        """Mark the start of a new frame"""
        self.last_frame_time = time.time()

    def log_detection_time(self, duration):
        """Log the time taken for hand detection"""
        self.detection_times.append(duration)
        if len(self.detection_times) > self.max_samples:
            self.detection_times.pop(0)

    def log_prediction_time(self, duration):
        """Log the time taken for gesture prediction"""
        self.prediction_times.append(duration)
        if len(self.prediction_times) > self.max_samples:
            self.prediction_times.pop(0)

    def end_frame(self):
        """Mark the end of a frame and calculate FPS"""
        now = time.time()
        frame_duration = now - self.last_frame_time
        self.frame_times.append(frame_duration)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
        return frame_duration

    def get_fps(self):
        """Calculate average frames per second"""
        if not self.frame_times:
            return 0
        avg_frame_time = np.mean(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0

    def get_metrics(self):
        """Get a dictionary of performance metrics"""
        metrics = {
            "fps": self.get_fps(),
            "avg_detection_time": (
                np.mean(self.detection_times) if self.detection_times else 0
            ),
            "avg_prediction_time": (
                np.mean(self.prediction_times) if self.prediction_times else 0
            ),
            "avg_frame_time": np.mean(self.frame_times) if self.frame_times else 0,
        }
        return metrics

    def draw_metrics(self, frame):
        """Draw performance metrics on the frame"""
        metrics = self.get_metrics()

        cv2.putText(
            frame,
            f"FPS: {metrics['fps']:.1f}",
            (frame.shape[1] - 150, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            1,
        )

        return frame
