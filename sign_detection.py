import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
import os
import time
from hand_tracking.HandTrackingModule import handDetector
from utils.audio_manager import AudioManager
from utils.gesture_smoothing import GestureSmoother

# Load the gesture recognizer model
model = load_model("models/mp_hand_gesture")

# Load class names
with open("gesture.names", "r") as f:
    classNames = f.read().split("\n")
print(classNames)

# Initialize audio manager for non-blocking voice output
audio_manager = AudioManager(cooldown_time=2)
enable_voice = False  # Change to True when you want to enable voice

# Initialize gesture smoothing
smoother = GestureSmoother(history_length=10)

# Initialize the webcam
cap = cv2.VideoCapture(1)  # if webcam not working change to (0)/(1)/(2)

# Initialize hand detector
detector = handDetector(detectionCon=0.7, maxHands=1)

while True:
    # Read each frame from the webcam
    success, frame = cap.read()
    if not success:
        print("Failed to capture image")
        continue

    # Flip the frame horizontally for a more intuitive mirror view
    frame = cv2.flip(frame, 1)

    # Find hands
    frame = detector.findHands(frame)

    # Find position of hand landmarks
    lmList = detector.findPosition(frame, draw=False)

    className = ""

    # Process landmarks if hand is detected
    if lmList:
        # Convert to format expected by model
        landmarks = [[lm[1], lm[2]] for lm in lmList]

        # Predict gesture
        prediction = model.predict([landmarks], verbose=0)
        classID = np.argmax(prediction)
        className = classNames[classID]
        confidence = float(prediction[0][classID])

        # Update gesture history for smoothing
        smoother.update(className, confidence)
        smooth_gesture = smoother.get_dominant_gesture()

        if smooth_gesture:
            # Generate and play voice feedback with cooldown
            if enable_voice:
                audio_manager.speak(smooth_gesture)

            # Display smoothed class name and confidence
            cv2.putText(
                frame,
                f"{smooth_gesture} ({confidence:.2f})",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

    # Add instructions
    cv2.putText(
        frame,
        f"Voice: {'ON' if enable_voice else 'OFF'}",
        (10, frame.shape[0] - 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        f"Press 'q' to quit, 'v' to toggle voice",
        (10, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    # Show the final output
    cv2.imshow("Hand Gesture Recognition", frame)

    # Key handling
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("v"):
        enable_voice = not enable_voice
        status = "enabled" if enable_voice else "disabled"
        print(f"Voice feedback {status}")

# Release resources
cap.release()
cv2.destroyAllWindows()
