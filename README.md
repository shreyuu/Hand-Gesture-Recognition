# Hand Gesture Recognition with MediaPipe and TensorFlow

**Table of Contents**

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

This repository contains a Python script that uses the MediaPipe library and TensorFlow to recognize hand gestures from a webcam feed. It also utilizes the gTTS library to convert the recognized gestures into speech feedback.

## Getting Started

To run the code, follow these steps:

1. Clone this repository to your local machine.
2. Make sure you have the required dependencies installed. You can install them using `pip`: pip install opencv-python mediapipe tensorflow gtts
3. Download the pre-trained gesture recognizer model ('mp_hand_gesture') and the class names file ('gesture.names') and place them in the root directory of the repository.
4. Run the Python script: python gesture_recognition.py
5. The script will open your webcam feed and recognize hand gestures in real-time, providing speech feedback.

## Additional Information

- The `gesture_recognition.py` script uses the MediaPipe library to detect hand landmarks, and a pre-trained TensorFlow model to classify the hand gesture.
- Speech feedback is provided using the gTTS (Google Text-to-Speech) library.
- You can exit the program by pressing the 'q' key.

## Contributing

Feel free to contribute to this project by providing feedback, code improvements, or additional features. Pull requests are welcome!

## License

This project does not have a specific license. The code is provided as-is for educational and personal use. You are welcome to use, modify, and distribute it according to your own preferences. Please respect the licenses of the libraries and tools used in this project.

## Acknowledgments

- This code was created as a personal project for hand gesture recognition using open-source libraries and tools.

Enjoy experimenting with hand gesture recognition and feel free to provide any feedback or improvements!
