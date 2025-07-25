import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
import time
from hand_tracking.HandTrackingModule import handDetector
from utils.gesture_smoothing import GestureSmoother
from utils.audio_manager import AudioManager
from utils.performance_analyzer import PerformanceAnalyzer
import config


class GestureRecognitionApp:
    def __init__(self):
        # Load the model
        self.model = load_model(config.MODEL_PATH)

        # Load class names
        with open(config.GESTURE_NAMES_PATH, "r") as f:
            self.classNames = f.read().split("\n")

        # Initialize the camera
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        self.cap.set(3, config.CAMERA_WIDTH)
        self.cap.set(4, config.CAMERA_HEIGHT)

        # Initialize hand detector
        self.detector = handDetector(
            detectionCon=config.DETECTION_CONFIDENCE, maxHands=config.MAX_HANDS
        )

        # Voice settings
        self.enable_voice = config.ENABLE_VOICE_DEFAULT
        self.audio_manager = AudioManager(
            cooldown_time=config.VOICE_COOLDOWN_TIME, cache_size=config.AUDIO_CACHE_SIZE
        )

        # Gesture smoothing
        self.smoother = GestureSmoother(history_length=15)

        # Add performance analyzer
        self.perf_analyzer = PerformanceAnalyzer()

        print(f"Loaded {len(self.classNames)} gestures: {', '.join(self.classNames)}")

    def speak_gesture(self, gesture_name):
        """Generate and play audio for a gesture using the audio manager"""
        if self.enable_voice:
            self.audio_manager.speak(gesture_name, lang=config.VOICE_LANGUAGE)

    def run(self):
        """Main application loop"""
        while True:
            self.perf_analyzer.start_frame()

            # Read frame
            success, frame = self.cap.read()
            if not success:
                print("Failed to capture image")
                continue

            # Flip frame horizontally
            frame = cv2.flip(frame, 1)

            # Find hands
            frame = self.detector.findHands(frame)
            lmList = self.detector.findPosition(frame, draw=False)

            # Process hand if detected
            if lmList:
                # Convert landmarks to format expected by model
                landmarks = [[lm[1], lm[2]] for lm in lmList]

                # Predict gesture
                prediction = self.model.predict([landmarks], verbose=0)
                classID = np.argmax(prediction)
                className = self.classNames[classID]
                confidence = float(prediction[0][classID])

                # Update gesture history
                self.smoother.update(className, confidence)
                smooth_gesture = self.smoother.get_dominant_gesture()

                # Voice feedback
                if smooth_gesture:
                    self.speak_gesture(smooth_gesture)

                # Display prediction
                cv2.putText(
                    frame,
                    f"{smooth_gesture} ({confidence:.2f})",
                    (10, 50),
                    config.FONT,
                    config.FONT_SCALE,
                    config.FONT_COLOR,
                    config.FONT_THICKNESS,
                )

            # Display UI elements
            self.draw_ui(frame)

            # Before displaying the frame
            frame = self.perf_analyzer.draw_metrics(frame)

            # End frame timing
            self.perf_analyzer.end_frame()

            # Show frame
            cv2.imshow("Hand Gesture Recognition", frame)

            # Handle key presses
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            elif key == ord("v"):
                self.enable_voice = not self.enable_voice
                print(
                    f"Voice feedback {'enabled' if self.enable_voice else 'disabled'}"
                )
            elif key == ord("r"):
                # Pause the app and start recording mode
                cv2.destroyWindow("Hand Gesture Recognition")
                from gesture_recorder import record_gesture

                record_gesture()
                # Resume the app when recording is done

        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()

    def draw_ui(self, frame):
        """Draw UI elements on the frame"""
        # Voice status
        status = "ON" if self.enable_voice else "OFF"
        cv2.putText(
            frame,
            f"Voice: {status}",
            (10, frame.shape[0] - 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

        # Instructions
        cv2.putText(
            frame,
            "Press 'v' to toggle voice, 'q' to quit",
            (10, frame.shape[0] - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )


if __name__ == "__main__":
    app = GestureRecognitionApp()
    app.run()
