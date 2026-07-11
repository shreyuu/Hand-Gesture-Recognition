import cv2
from gesture_recognition.tracking.hand_detector import handDetector
from gesture_recognition.landmarks import normalize_landmarks
from gesture_recognition.services.gesture_manager import GestureManager
from gesture_recognition.services.gesture_smoothing import GestureSmoother
from gesture_recognition.services.audio_manager import AudioManager
from gesture_recognition.services.performance_analyzer import PerformanceAnalyzer
from gesture_recognition import config

# After this many consecutive frames without a hand, the last announced
# gesture is forgotten so it gets re-announced when the hand comes back.
HAND_ABSENT_RESET_FRAMES = 30


class GestureRecognitionApp:
    def __init__(self, profile=None, model_path=None, names_path=None, normalize=False):
        # Profile settings override config defaults when present
        self.profile = profile

        def setting(name, default):
            return profile.get(name, default) if profile is not None else default

        # Model + class names. `normalize` must match how the model was
        # trained: the bundled pretrained model expects raw pixel coordinates,
        # models trained by GestureTrainer expect normalized landmarks.
        self.gesture_manager = GestureManager(
            model_path or config.MODEL_PATH,
            names_path or config.GESTURE_NAMES_PATH,
        )
        self.normalize = normalize

        # Initialize the camera
        self.camera_index = setting("camera_index", config.CAMERA_INDEX)
        self.cap = self._open_camera()

        # Initialize hand detector
        self.detector = handDetector(
            detectionCon=setting("detection_confidence", config.DETECTION_CONFIDENCE),
            trackCon=config.TRACKING_CONFIDENCE,
            maxHands=config.MAX_HANDS,
        )

        # Voice settings
        self.enable_voice = setting("enable_voice", config.ENABLE_VOICE_DEFAULT)
        self.voice_language = setting("voice_language", config.VOICE_LANGUAGE)
        self.audio_manager = AudioManager(
            cooldown_time=config.VOICE_COOLDOWN_TIME, cache_size=config.AUDIO_CACHE_SIZE
        )

        # Gesture smoothing
        self.smoother = GestureSmoother(
            history_length=config.SMOOTHING_HISTORY_LENGTH,
            confidence_threshold=config.CONFIDENCE_THRESHOLD,
        )

        # Add performance analyzer
        self.perf_analyzer = PerformanceAnalyzer()

        self.no_hand_frames = 0

    def _open_camera(self):
        cap = cv2.VideoCapture(self.camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        if not cap.isOpened():
            raise RuntimeError(
                f"Could not open camera index {self.camera_index}. "
                "Set GESTURE_CAM_INDEX or the profile's camera_index."
            )
        return cap

    def speak_gesture(self, gesture_name):
        """Generate and play audio for a gesture using the audio manager"""
        if self.enable_voice:
            self.audio_manager.speak(gesture_name, lang=self.voice_language)

    def run(self):
        """Main application loop"""
        try:
            self._loop()
        finally:
            # Always release resources, even on error or Ctrl-C
            self.cap.release()
            cv2.destroyAllWindows()

    def _loop(self):
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
                self.no_hand_frames = 0

                # Convert landmarks to format expected by model
                landmarks = [[lm[1], lm[2]] for lm in lmList]
                if self.normalize:
                    landmarks = normalize_landmarks(landmarks)

                # Predict gesture
                className, confidence = self.gesture_manager.predict_gesture(landmarks)

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
            else:
                # Re-announce the gesture if the hand left and came back
                self.no_hand_frames += 1
                if self.no_hand_frames == HAND_ABSENT_RESET_FRAMES:
                    self.audio_manager.reset_last_spoken()

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
                # Pause the app and start recording mode. Release the camera
                # first — the recorder opens it itself, and most platforms
                # can't open the same camera twice.
                cv2.destroyWindow("Hand Gesture Recognition")
                self.cap.release()
                from gesture_recognition.recorder import record_gesture

                record_gesture()
                # Resume the app when recording is done
                self.cap = self._open_camera()

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
            "Press 'v' to toggle voice, 'r' to record, 'q' to quit",
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
