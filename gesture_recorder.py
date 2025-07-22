import cv2
import numpy as np
import os
import json
import time
from hand_tracking.HandTrackingModule import handDetector


def record_gesture():
    # Create directory for saved gestures if it doesn't exist
    if not os.path.exists("recorded_gestures"):
        os.makedirs("recorded_gestures")

    # Initialize webcam and hand detector
    cap = cv2.VideoCapture(1)  # Change as needed
    detector = handDetector(detectionCon=0.7, maxHands=1)

    # Ask for gesture name
    gesture_name = input("Enter the name of the gesture to record: ")
    sample_count = 0
    max_samples = 100
    samples = []

    print(
        f"Recording gesture '{gesture_name}'. Press 's' to save a sample, 'q' to finish."
    )
    print(f"Try to record the gesture in various positions and angles.")

    recording_active = False

    while True:
        success, img = cap.read()
        if not success:
            continue

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
        if recording_active and lmList and sample_count < max_samples:
            # Get landmarks in format [x, y]
            landmarks = [[lm[1], lm[2]] for lm in lmList]
            samples.append(landmarks)
            sample_count += 1
            print(f"Sample {sample_count} recorded")
            time.sleep(0.1)  # Small delay between samples

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
        filename = (
            f"recorded_gestures/{gesture_name}_{time.strftime('%Y%m%d_%H%M%S')}.json"
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
