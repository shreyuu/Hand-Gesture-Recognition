# Hand Gesture Recognition with MediaPipe and TensorFlow

**Table of Contents**

- [Hand Gesture Recognition with MediaPipe and TensorFlow](#hand-gesture-recognition-with-mediapipe-and-tensorflow)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [How It Works](#how-it-works)
  - [Supported Gestures](#supported-gestures)
  - [Customization](#customization)
    - [Adjusting Detection Sensitivity](#adjusting-detection-sensitivity)
    - [Changing the Webcam Source](#changing-the-webcam-source)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Introduction

This repository contains a Python-based application that recognizes hand gestures in real-time using computer vision techniques. Built with MediaPipe for hand tracking and TensorFlow for gesture classification, the system also provides audio feedback through text-to-speech conversion.

## Features

- Real-time hand gesture recognition through webcam
- Text-to-speech feedback for recognized gestures
- Pre-trained model for recognizing 10 common gestures
- Modular design with separate hand tracking module
- Visual display of hand landmarks and gesture labels

## Getting Started

### Prerequisites

- Python 3.7+ installed on your system
- Webcam access
- Internet connection (for initial model download)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/hand-gesture-recognition.git
   cd hand-gesture-recognition
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py recognize
   ```

## Project Structure

```
Hand-Gesture-Recognition/
├── main.py                          # CLI entry point (recognize / record / train / settings)
├── requirements.txt
├── gesture_recognition/             # application package
│   ├── config.py                    # configuration (env-var driven)
│   ├── app.py                       # real-time recognition app
│   ├── recorder.py                  # record gesture samples
│   ├── trainer.py                   # train a model on recorded samples
│   ├── user_profile.py              # per-user settings persistence
│   ├── tracking/
│   │   └── hand_detector.py         # MediaPipe hand-landmark detection
│   ├── services/
│   │   ├── audio_manager.py         # non-blocking text-to-speech
│   │   ├── gesture_manager.py       # model + class-name management
│   │   ├── gesture_smoothing.py     # prediction smoothing
│   │   ├── hand_state_monitor.py    # hand enter/exit detection
│   │   └── performance_analyzer.py  # FPS / timing metrics
│   └── ui/
│       └── settings_dialog.py       # Tkinter settings dialog
├── models/mp_hand_gesture/          # pre-trained TensorFlow model
├── data/
│   ├── gesture.names                # list of supported gestures
│   └── profiles/                    # user profiles (e.g. default.json)
├── scripts/                         # standalone / legacy demo scripts
│   ├── sign_detection.py            # legacy single-file recognition demo
│   ├── hand_tracking_demo.py        # minimal hand-tracking demo
│   └── tts_demo.py                  # minimal text-to-speech demo
└── docs/ARCHITECTURE.md             # folder-structure explanation
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for a fuller explanation of the layout.

## Usage

1. Launch the application:

   ```bash
   python main.py recognize            # real-time recognition (default)
   python main.py record               # record new gesture samples
   python main.py train                # train a model on recorded samples
   python main.py settings             # open the settings dialog
   ```

2. Position your hand in front of the camera
3. Make one of the supported gestures
4. The application will:
   - Display the recognized gesture name on screen
   - Provide audio feedback through speech (toggle with `v`)
5. Press 'q' to exit the application

## How It Works

The application works in three main steps:

1. **Hand Detection**: Uses MediaPipe to detect hand landmarks (21 key points on each hand)
2. **Feature Extraction**: Extracts the spatial coordinates of these landmarks
3. **Classification**: Feeds these coordinates to a pre-trained TensorFlow model to classify the gesture
4. **Feedback**: Displays the result visually and provides audio feedback

## Supported Gestures

The system can recognize 10 different hand gestures:

- Okay (👌)
- Peace (✌️)
- Thumbs up (👍)
- Thumbs down (👎)
- Call me (🤙)
- Stop (✋)
- Rock (🤘)
- Live long (Vulcan salute) (🖖)
- Fist (✊)
- Smile (finger smile)

## Customization

Settings are driven by `gesture_recognition/config.py` (with environment-variable
overrides) and per-user profiles under `data/profiles/`.

### Adjusting Detection Sensitivity

Set the detection confidence via an environment variable (or a profile's
`detection_confidence`):

```bash
GESTURE_DETECTION_CONF=0.5 python main.py recognize
```

Lower values (e.g., 0.5) will make detection more sensitive but may increase false positives.

### Changing the Webcam Source

If your webcam is not properly recognized, try changing the camera index:

```bash
GESTURE_CAM_INDEX=0 python main.py recognize   # try 0, 1, or 2
```

You can also change it persistently via the settings dialog (`python main.py settings`).

## Troubleshooting

- **No webcam detected**: Verify webcam connection and try different camera indices
- **Poor recognition**: Ensure good lighting and clear background
- **Slow performance**: Reduce the webcam resolution or try on a more powerful computer

## Contributing

Feel free to contribute to this project by providing feedback, code improvements, or additional features. Pull requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a pull request

## License

This project does not have a specific license. The code is provided as-is for educational and personal use. Please respect the licenses of the libraries and tools used in this project.

## Acknowledgments

- This project uses [MediaPipe](https://github.com/google/mediapipe) for hand landmark detection
- The gesture recognition model is built with [TensorFlow](https://www.tensorflow.org/)
- Text-to-speech conversion uses [gTTS](https://github.com/pndurette/gTTS)

Enjoy experimenting with hand gesture recognition and feel free to provide any feedback or improvements!
