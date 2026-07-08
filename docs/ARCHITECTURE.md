# Project Architecture

This document explains how the codebase is organized and why.

## Layout

```
Hand-Gesture-Recognition/
├── main.py                  # Thin CLI entry point — parses args and dispatches to the package.
├── gesture_recognition/     # The application package (all importable source lives here).
├── models/                  # Pre-trained TensorFlow model artifacts.
├── data/                    # Committed input data + user profiles.
├── scripts/                 # Standalone / legacy demo scripts, not imported by the app.
└── docs/                    # Documentation.
```

## `gesture_recognition/` (application package)

Everything the app imports lives inside one package so imports are explicit and
unambiguous (`from gesture_recognition.services.audio_manager import AudioManager`).

| Path | Responsibility |
|------|----------------|
| `config.py` | Central configuration. All values are environment-variable driven with sensible defaults. Paths are anchored to the project root via `BASE_DIR`. |
| `app.py` | `GestureRecognitionApp` — the real-time recognition loop (camera → detection → prediction → smoothing → UI/voice). |
| `recorder.py` | Records labelled gesture samples to `recorded_gestures/`. |
| `trainer.py` | `GestureTrainer` — trains an LSTM model from recorded samples. |
| `user_profile.py` | `UserProfile` — loads/saves per-user settings under `data/profiles/`. |
| `tracking/` | Hand tracking. `hand_detector.py` wraps MediaPipe (`handDetector`). |
| `services/` | Supporting, single-responsibility services: audio (TTS), gesture data/model management, prediction smoothing, hand enter/exit monitoring, performance metrics. |
| `ui/` | User-facing UI. `settings_dialog.py` is the Tkinter settings window. |

### Separation of concerns

- **Tracking** (input/perception) is isolated from **services** (processing helpers)
  and **ui** (presentation).
- **Configuration** and **profile persistence** are separated from behaviour, so
  settings can change without touching logic.
- The **entry point** (`main.py`) contains only CLI wiring — no business logic.

## `models/`

Pre-trained TensorFlow SavedModel (`mp_hand_gesture/`). Kept at the repo root by
ML convention and because `.gitattributes` marks these binaries as vendored.
Overridable via the `GESTURE_MODEL_PATH` environment variable.

## `data/`

Committed, non-code inputs:
- `gesture.names` — the list of recognised gesture labels (override with `GESTURE_NAMES_PATH`).
- `profiles/` — per-user JSON settings (e.g. `default.json`).

## `scripts/`

Standalone scripts that are **not** part of the application package:
- `sign_detection.py` — the original single-file recognition demo (superseded by
  `main.py recognize`, kept for reference). Adds the project root to `sys.path` so
  it can reuse the package when run directly.
- `hand_tracking_demo.py` — minimal MediaPipe hand-tracking demo.
- `tts_demo.py` — minimal gTTS text-to-speech demo.

## Conventions

- **Naming:** `snake_case` for modules and packages.
- **Paths:** never rely on the current working directory — `config.py` and
  `user_profile.py` anchor paths to the project root so the app runs from anywhere.
- **Configuration:** prefer environment variables (see `config.py`) and profiles
  over hard-coded constants.
