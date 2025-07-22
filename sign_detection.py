import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
from gtts import gTTS
import os
import time
from hand_tracking.HandTrackingModule import handDetector

# Load the gesture recognizer model
model = load_model("models/mp_hand_gesture")

# Load class names
with open("gesture.names", "r") as f:
    classNames = f.read().split("\n")
print(classNames)

# Voice output flag - set to False to disable voice
enable_voice = False  # Change to True when you want to enable voice
last_spoken_time = 0
cooldown_time = 2  # seconds between voice announcements

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
        prediction = model.predict([landmarks])
        classID = np.argmax(prediction)
        className = classNames[classID]
        confidence = float(prediction[0][classID])

        # Generate and play voice feedback with cooldown
        current_time = time.time()
        if enable_voice and (current_time - last_spoken_time) > cooldown_time:
            tts = gTTS(text=className, lang="en")
            tts.save("gesture.mp3")
            os.system("afplay gesture.mp3")
            last_spoken_time = current_time

        # Display class name and confidence
        cv2.putText(
            frame,
            f"{className} ({confidence:.2f})",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

    # Add FPS counter
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
