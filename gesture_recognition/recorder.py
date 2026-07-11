import cv2
import os
import json
import time
from gesture_recognition.tracking.hand_detector import handDetector
from gesture_recognition import config

# Seconds between auto-saved samples while recording is active. Using a
# timestamp check (not time.sleep) keeps the preview responsive.
AUTO_SAMPLE_INTERVAL = 0.1

# Samples are stored as raw pixel coordinates; normalization happens at
# training/recognition time (see gesture_recognition.landmarks), so existing
# recordings stay usable if the normalization scheme changes.
RECORDINGS_DIR = os.path.join(config.BASE_DIR, "recorded_gestures")


def record_gesture():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    # Initialize webcam and hand detector from config (env-var overridable)
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cap.isOpened():
        print(
            f"Could not open camera index {config.CAMERA_INDEX}. "
            "Set GESTURE_CAM_INDEX to change it."
        )
        return
    detector = handDetector(
        detectionCon=config.DETECTION_CONFIDENCE, maxHands=config.MAX_HANDS
    )

    # Ask for gesture name
    gesture_name = input("Enter the name of the gesture to record: ").strip()
    if not gesture_name:
        print("No gesture name given, aborting.")
        cap.release()
        return

    sample_count = 0
    max_samples = 100
    samples = []

    print(
        f"Recording gesture '{gesture_name}'. Press 's' to save a sample, 'q' to finish."
    )
    print("Try to record the gesture in various positions and angles.")

    recording_active = False
    last_sample_time = 0.0
    failed_reads = 0

    while True:
        success, img = cap.read()
        if not success:
            failed_reads += 1
            if failed_reads > 50:
                print("Camera stopped delivering frames, aborting.")
                break
            continue
        failed_reads = 0

        # Flip image horizontally
        img = cv2.flip(img, 1)

        # Find hands
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=True)

        # Status display
        cv2.putText(
            img,
            f"Gesture: {gesture_name}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            img,
            f"Samples: {sample_count}/{max_samples}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        # Recording status
        status_text = "READY TO RECORD" if not recording_active else "RECORDING ACTIVE"
        status_color = (0, 255, 0) if not recording_active else (0, 0, 255)
        cv2.putText(
            img, status_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2
        )

        cv2.putText(
            img,
            "Press 'r' to toggle recording",
            (10, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            img,
            "Press 's' to save current frame",
            (10, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            img,
            "Press 'q' to quit",
            (10, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        # Show image
        cv2.imshow("Gesture Recorder", img)

        # Auto-save if recording is active and hand is detected
        now = time.time()
        if (
            recording_active
            and lmList
            and sample_count < max_samples
            and (now - last_sample_time) >= AUTO_SAMPLE_INTERVAL
        ):
            # Get landmarks in format [x, y]
            landmarks = [[lm[1], lm[2]] for lm in lmList]
            samples.append(landmarks)
            sample_count += 1
            last_sample_time = now
            print(f"Sample {sample_count} recorded")

            if sample_count >= max_samples:
                print("Maximum number of samples reached!")
                recording_active = False

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord("r"):
            recording_active = not recording_active
            print(f"Recording {'started' if recording_active else 'paused'}")
        elif key == ord("s") and lmList:
            # Manually save current frame
            landmarks = [[lm[1], lm[2]] for lm in lmList]
            samples.append(landmarks)
            sample_count += 1
            print(f"Sample {sample_count} manually recorded")

    # Save recorded samples
    if samples:
        filename = os.path.join(
            RECORDINGS_DIR, f"{gesture_name}_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(filename, "w") as f:
            json.dump(samples, f)
        print(f"Saved {sample_count} samples to {filename}")
    else:
        print("No samples recorded.")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    record_gesture()
