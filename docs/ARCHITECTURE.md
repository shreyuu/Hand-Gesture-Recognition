# Project Architecture

This document explains how the codebase is organized and why.

## Layout

```
Hand-Gesture-Recognition/
├── main.py                  # Thin CLI entry point — parses args and dispatches to the package.
├── gesture_recognition/     # The application package (all importable source lives here).
├── models/                  # Pre-trained TensorFlow model artifacts.
├── data/                    # Committed input data + user profiles.
└── docs/                    # Documentation.
```

## `gesture_recognition/` (application package)

Everything the app imports lives inside one package so imports are explicit and
unambiguous (`from gesture_recognition.services.audio_manager import AudioManager`).

| Path | Responsibility |
|------|----------------|
| `config.py` | Central configuration. All values are environment-variable driven with sensible defaults. Paths are anchored to the project root via `BASE_DIR`. |
| `app.py` | `GestureRecognitionApp` — the real-time recognition loop (camera → detection → prediction → smoothing → UI/voice). |
| `landmarks.py` | Landmark normalization (wrist-relative, scale-invariant) shared by trainer and recognizer. |
| `dataset.py` | Loads recorded samples from disk. Kept TensorFlow-free so it is unit-testable with light dependencies. |
| `recorder.py` | Records labelled gesture samples (raw pixel coordinates) to `recorded_gestures/`. |
| `trainer.py` | `GestureTrainer` — trains a dense classifier on normalized recorded samples. |
| `user_profile.py` | `UserProfile` — loads/saves per-user settings under `data/profiles/`. |
| `tracking/` | Hand tracking. `hand_detector.py` wraps MediaPipe (`handDetector`). |
| `services/` | Supporting, single-responsibility services: audio (TTS), gesture data/model management, prediction smoothing, performance metrics. |
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

## Legacy demo scripts

The repository previously carried a `scripts/` directory holding a single-file
recognition demo plus minimal MediaPipe and gTTS examples. They were removed:
each duplicated logic the package already owns, and all three had drifted out of
sync with it (the recognition demo hard-coded a camera index and used the slow
`model.predict()` path that `services/gesture_manager.py` deliberately avoids).

They remain in history if ever needed for reference:

```bash
git show 77b6f14:scripts/sign_detection.py
git show 77b6f14:scripts/hand_tracking_demo.py
git show 77b6f14:scripts/tts_demo.py
```

## Conventions

- **Naming:** `snake_case` for modules and packages.
- **Paths:** never rely on the current working directory — `config.py` defines
  `BASE_DIR` (the project root) and every other module derives its paths from it,
  so the app runs from anywhere.
- **Configuration:** prefer environment variables (see `config.py`) and profiles
  over hard-coded constants.
