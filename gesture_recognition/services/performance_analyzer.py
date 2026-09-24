import time

import cv2
import numpy as np


class PerformanceAnalyzer:
    """
    Tracks frame timing for the application.
    """

    def __init__(self, max_samples=100):
        self.frame_times = []
        self.max_samples = max_samples
        self.last_frame_time = time.time()

    def start_frame(self):
        """Mark the start of a new frame"""
        self.last_frame_time = time.time()

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
        return {
            "fps": self.get_fps(),
            "avg_frame_time": np.mean(self.frame_times) if self.frame_times else 0,
        }

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
