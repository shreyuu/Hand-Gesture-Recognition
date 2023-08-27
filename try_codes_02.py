import cv2
import numpy as np

# Function to detect fingers on a hand
def detect_fingers(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contours were found
    if not contours:
        cv2.putText(frame, "No hand detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return frame

    hand_contour = max(contours, key=cv2.contourArea)

    hull = cv2.convexHull(hand_contour, returnPoints=False)
    defects = cv2.convexityDefects(hand_contour, hull)

    finger_count = 0
    finger_names = {1: "Thumb", 2: "Index", 3: "Middle", 4: "Ring", 5: "Pinky"}

    for i in range(defects.shape[0]):
        s, e, f, _ = defects[i, 0]
        start = tuple(hand_contour[s][0])
        end = tuple(hand_contour[e][0])
        far = tuple(hand_contour[f][0])

        a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c))
        if angle <= np.pi / 2:
            finger_count += 1
            cv2.circle(frame, far, 4, [0, 0, 255], -1)

    finger_name = finger_names.get(finger_count, "Unknown")
    cv2.putText(frame, finger_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    return frame

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect fingers on the hand
    result_frame = detect_fingers(frame)

    # Display the result
    cv2.imshow('Finger Detection', result_frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
