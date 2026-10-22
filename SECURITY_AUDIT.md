# Security & Logic Audit

Date: 2026-10-22 · Scope: whole repository at `b86674e` (+ uncommitted working tree)

## Attack surface

A local desktop app with no server, database, auth, or LLM features.

- **Entry points:** `main.py recognize | record | train | settings`, plus an
  interactive prompt when run with no arguments.
- **Inputs:**
  - CLI args (`--profile`, `--gesture`)
  - `GESTURE_*` env vars
  - profile JSON (`data/profiles/`)
  - recordings (`recorded_gestures/*.json`)
  - model directory (`GESTURE_MODEL_PATH`)
  - webcam frames
  - Tk settings fields
- **Outbound network:** gTTS sends the recognised gesture name to Google
  (HTTPS).
- **Local writes:** profiles, recordings, `models/custom_model*`, `logs/fit`,
  the TTS mp3 cache.
- **Secrets / PII:** none found. Hand-landmark recordings are biometric-ish
  but gitignored.

## Scans

| Tool | Target | Result |
|---|---|---|
| gitleaks 8 (`git --log-opts=--all`) | all 47 commits | no leaks |
| gitleaks (`dir`) | working tree | 3 hits, all false positives in `.venv/share/jupyter` minified JS (`FourKeyMap=`) |
| pip-audit (uv-resolved lock of `requirements-dev.txt`, py3.11) | deps | keras 2.15.0: 25 advisories; protobuf 4.25.9: 1 advisory (DEP-1, DEP-2) |
| osv-scanner 2.7 | `requirements*.txt` | same keras/protobuf hits. Its pillow 9.5.0 / certifi / idna hits came from its own resolver; pip/uv resolve pillow 13.0.0 and current certifi/idna, so they're dismissed |
| bandit 1.9 | `gesture_recognition/`, `main.py` | B324 md5 (SEC-1 fix removes it); B404/B603 subprocess: list args, fixed player binary, hash-derived path, so not exploitable |
| semgrep (`--config auto`) | repo | mutable action tags in `ci.yml` (SEC-4); missing SRI in brag compositions (SEC-6) |
| npm audit | `brag-output*/composition/package.json` | not run: no dependencies declared |
| type checker | n/a | none configured in the repo; ruff only |

### Post-fix re-scan

- **gitleaks** (history + uncommitted changes): no leaks.
- **bandit:** B324 is gone; only the B404/B603 subprocess notes remain (not
  exploitable, see above).
- **semgrep:** a new `insecure-file-permissions` hit on
  `audio_manager.py:28` (`os.chmod(path, 0o700)`) is a false positive. The
  rule flags any execute bit, but 0700 is owner-only, and a directory needs
  `x` to be entered.
- **osv-scanner:** now also lists pygments 2.9.0, another artifact of its
  resolver. uv/pip resolve pygments 2.21.0, and pip-audit on that lock still
  reports only DEP-1 and DEP-2.

## Verification

- **Tests:** the full suite passes locally (59 tests, ruff clean). A CI-like
  venv (numpy, gTTS, pytest, ruff only) gives 52 passed and 4 skipped (the
  TF / Keras / display tests skip themselves).
- **Exploits re-attempted after the fixes:**
  - `GESTURE_CAM_INDEX=3` → 3
  - profile `"enable_voice": "false"` → False
  - profile `camera_index` set to a URL → warning, falls back to 0
  - real gTTS with the network forced to fail → no file left in the 0700
    cache dir, and an md5-named mp3 planted in `$TMPDIR` is not played
  - `main.py settings --profile ../../tmp/x` → argparse error, exit 2
  - `main.py train` on the repo's single recorded gesture → refused, nothing
    written
- **Smoke test:** `main.py --help` works, and the bundled model loads (10 names
  = 10 outputs) and predicts. The live webcam loop wasn't exercised; it needs a
  camera.

## Findings

Severity is contextual to a single-user desktop app. No Critical or High
findings.

| ID | Sev | Category | Location | Exploit / failure scenario | Fix | Conf. | Status |
|---|---|---|---|---|---|---|---|
| BUG-2 | Medium | Logic: poisoned cache | `gesture_recognition/services/audio_manager.py:100-109` | `gTTS.save()` opens the target file *before* the HTTP request. Offline once → a 0-byte `gesture_<md5>.mp3` is left behind; `os.path.exists()` is then true forever (across restarts) and that gesture never speaks again. | Write to a temp file in the cache dir, `os.replace()` on success, unlink on failure | High (reproduced against the gTTS source) | Fixed |
| SEC-1 | Low | Insecure temp file (CWE-377) | `audio_manager.py:28,95-100` | Predictable name in the system temp dir, trusted if it exists. On Linux `/tmp` is shared, so another local user pre-creates `/tmp/gesture_$(md5 "okay\|en\|False").mp3`; the victim's app then feeds attacker-chosen media to mpg123/ffplay/mpv, or playback is blocked (DoS). Not exploitable on macOS (per-user `TMPDIR`, verified). | Per-user cache `$XDG_CACHE_HOME`/`~/.cache/hand-gesture-recognition/tts` created `0700`; sha256 names | High | Fixed |
| BUG-1 | Medium | Logic: config ignored | `gesture_recognition/config.py:55-58` | `resolve_setting()` is still a placeholder and never reads env vars. `GESTURE_CAM_INDEX=3` resolves to `0` (verified), although the README and the errors at `app.py:69` / `recorder.py:42` tell users to set it. | Precedence env > profile > default (decided by owner) | High (reproduced) | Fixed |
| BUG-3 | Low | Type confusion | `config.py:57` | Profile JSON values are used without type checks: `"enable_voice": "false"` turns voice **on** (verified); `"detection_confidence": "0.7"` crashes MediaPipe at start-up. | Coerce profile strings with the env-var parser; warn and fall back on invalid values | High (reproduced) | Fixed |
| SEC-2 | Low | Input validation | `config.py:57` → `app.py:63`, `recorder.py:38` | A shared or downloaded profile with `"camera_index": "https://host/x.m3u8"` (or a file path) is passed to `cv2.VideoCapture()`, which opens URLs and files through FFmpeg: the app fetches and decodes attacker-chosen media. | Same coercion as BUG-3, so `camera_index` must be an int | Medium (backend-dependent) | Fixed |
| SEC-3 | Low | Path traversal (CWE-22) | `gesture_recognition/user_profile.py:24,37`; `main.py:25,41,60` | `main.py settings --profile ../../../tmp/x` reads and writes `/tmp/x.json`. Local CLI only, so no privilege boundary is crossed; this is hardening. | `validate_profile_name()` (`[\w\- ]+`) as the argparse `type=` and in `UserProfile.__init__` | High | Fixed |
| SEC-4 | Low | CI supply chain | `.github/workflows/ci.yml` | No `permissions:` block, so push builds get the repo-default `GITHUB_TOKEN` (write on older repos) while installing unpinned `numpy`/`pytest` and running actions by mutable tag. A compromised PyPI release or retagged action could push to the repo. | `permissions: contents: read`; pin actions to commit SHAs; pin CI packages | Medium (depends on repo default) | Fixed |
| DEP-1 | Low | Vulnerable dependency | `requirements.txt` (`tensorflow==2.15.1` → `keras==2.15.0`) | 25 Keras advisories (e.g. CVE-2025-12060, PYSEC-2026-3629..3634), mostly code execution or path traversal when loading untrusted model files or using `get_file`. Only reachable here if someone points `GESTURE_MODEL_PATH` at, or replaces `models/` with, a malicious model. | Major upgrade to TF ≥ 2.16 / Keras 3, which changes SavedModel loading. Owner decision | High (scanner + code) | Needs decision |
| DEP-2 | Low | Vulnerable dependency | `requirements.txt` (transitive `protobuf==4.25.9`) | PYSEC-2026-1805: parsing of crafted protobuf data (reachable via model `.pb` files). | Fixed in protobuf 5.29.6, but `mediapipe==0.10.21` and TF 2.15 cap protobuf < 5. Blocked on DEP-1 / a mediapipe upgrade | High | Needs decision |
| BUG-4 | Low | Robustness | `gesture_recognition/services/gesture_manager.py:21,35` | Names count is never checked against model outputs. A trimmed `gesture.names` → `IndexError` mid-loop; a blank gesture name (dropped by the blank-line filter) → every later label silently shifted. | Fail fast in `load_resources()` with a clear `ValueError` | High | Fixed |
| BUG-5 | Low | Logic | `gesture_recognition/trainer.py:50` | `to_categorical()` infers the class count from the largest label. If the alphabetically last gesture's file is `[]`, labels have k-1 columns but the model has k outputs, and training crashes. | `num_classes=len(self.gestures)` | High | Fixed |
| BUG-9 | Low | Logic | `trainer.py:80-96` | One recorded gesture → a one-class softmax that reports that label at 1.00 for every hand. The comment says "more than one class", but nothing checks it. | Refuse to train with < 2 gestures (decided by owner) | High | Fixed |
| BUG-6 | Low | Crash | `gesture_recognition/ui/settings_dialog.py:92-93` | Typing non-numeric text in the camera spinbox → `IntVar.get()` raises `TclError` inside the Tk callback: Save silently does nothing, traceback on the console. | Catch `TclError`, show an error dialog. Prefill from profile/default (not env) so Save never bakes a one-off env override into the profile | High | Fixed |
| BUG-7 | Low | Data loss | `gesture_recognition/dataset.py:25`; `recorder.py:171-183` | A gesture name longer than ~234 bytes hits ENAMETOOLONG when saving, *after* recording: all samples are lost and the camera is never released (no `try/finally`). | Cap sanitised names at 64 chars; release the camera in `finally` | High | Fixed |
| BUG-8 | Low | UX logic | `main.py:68-90` | At the interactive prompt, a typo such as `trian` silently falls through to recognition mode and turns the camera on. | `parser.error()` on unknown modes | High | Fixed |
| SEC-5 | Info | Privacy | git history: commit `d25712f` (file removed in `6870a74`) | The committed TensorBoard event file name `events.out.tfevents.…Shreyash-MacBook-Pro.local…` exposes a hostname in the public GitHub history. | Optional history purge by the owner | High | Manual action |
| SEC-6 | Info | Missing SRI | `brag-output*/composition/index.html:7` | gsap is loaded from jsDelivr without `integrity=`. These are render-only video compositions and never served. | n/a | High | Won't fix: render-only artifact |
| ENV-1 | Info | Environment | local `.venv` (not in repo) | Both `opencv-python 5.0.0.93` and `opencv-contrib-python 4.11.0.86` are installed. They ship the same `cv2` module and conflict (`requirements.txt` warns about this). | `uv pip uninstall --python .venv/bin/python opencv-python` | High | Manual action |
| ENV-2 | Info | Environment | local `.venv` interpreter (uv-managed CPython 3.11.14) | The first `tkinter.Tk()` raises `TclError: Can't find a usable init.tcl`, so `python main.py settings` crashes on this machine (reproduced). The repo code is fine. | Set `TCL_LIBRARY=$(python -c 'import sys;print(sys.base_prefix)')/lib/tcl8.6`, or rebuild the venv on a Python with working Tk (e.g. `uv python install --reinstall 3.11`) | High | Manual action |

### Reviewed, not vulnerable

- `subprocess.run` uses list arguments: no shell, fixed player binary,
  hash-derived path.
- Only `json.load` is used for data; no pickle/yaml/eval/exec.
- Recorder filenames are already sanitised by `safe_gesture_name`.
- `keras.load_model` loads the bundled model, which has the same trust level
  as the code. See DEP-1 for the untrusted-model case.
- gTTS talks to Google over TLS. Only gesture names are sent.
