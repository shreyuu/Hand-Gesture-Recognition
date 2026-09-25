# Brag Plan: Hand Gesture Recognition

## What is this app?
A Python desktop app that watches your webcam, turns your hand into 21 MediaPipe landmarks, classifies them with a TensorFlow model into 10 gestures (peace, rock, live long…), says the gesture out loud via gTTS, and lets you record + train your own.

## The angle
"Your hand is 21 dots." The whole product is a hand reduced to 21 red dots and white bones — the exact MediaPipe skeleton the app draws over the webcam feed. The video *is* that skeleton: it starts as the user's real recorded hand data (`recorded_gestures/index_20260709_201708.json`, 100 frames of an index point), then drops into a recreation of the actual OpenCV window, flips through gestures with the red `label (confidence)` text the app prints, talks back, gets retrained from the terminal, and signs off with the app's own on-screen instruction: **Press 'q' to quit.**

## Hook (first 2-3 seconds)
Black frame. 21 red dots pop in one at a time, bones snap between them, and the skeleton starts moving — it's a real recorded hand playing back. Line lands: **"Your hand is 21 dots."**

## Key moments (the middle)
- The skeleton lands inside a recreated "Hand Gesture Recognition" OpenCV window: red `peace (0.98)` label top-left, green `FPS: 29.8` top-right, white `Voice: OFF` + `Press 'v' to toggle voice, 'r' to record, 'q' to quit` bottom.
- The hand morphs gesture → gesture on the beat (thumbs up, rock, call me, okay, live long) while the label updates and a list of all 10 names from `data/gesture.names` highlights the current one.
- `v` keycap press → `Voice: ON` → a speech bubble says "live long" out loud.
- Terminal: `record` → `train` → `recognize --model custom`, with the real print strings from `recorder.py` / `trainer.py`.

## Outro / punchline
Open palm waves. "Hand Gesture Recognition" lands with "MediaPipe · TensorFlow · gTTS". Final line in the app's own mono voice: **Press 'q' to quit.**

## User flow worth showing
1. `python main.py recognize` → webcam window with the hand skeleton drawn over it.
2. Make a gesture → red label + confidence appears (smoothed, no flicker) → voice announces it.
3. `record` → `train` → `recognize --model custom` to teach it your own gesture.

## Tone
- Preset: default
- Creative direction: late-night webcam demo reel — the OpenCV debug window is the star
- Interpretation: playful but technical; mono "debug overlay" type for real app strings, one heavy display face for claims; comfortable 3–5s scenes, clean cuts, motion carried by the skeleton morphing on the beat.

## Format: landscape — 1920x1080
## Duration: 22.5s

## Visual identity (from the project)
No CSS — identity comes from the OpenCV/MediaPipe overlay colors in `config.py`, `app.py`, `performance_analyzer.py`, and MediaPipe's default drawing spec.
- Background: near-black webcam dark, tinted warm `#0e0d10`
- Accent: OpenCV label red — `FONT_COLOR = (0, 0, 255)` BGR → `#ff2d2d` (also MediaPipe landmark dot red)
- Text: `#f2eeee` (OpenCV white `(255,255,255)`, tinted)
- Secondary: MediaPipe connection gray `#e0e0e0`; FPS green `(0,255,0)` → `#39ff5a` (FPS readout only)
- Display font: Archivo Black (heavy claims)
- Body/data font: JetBrains Mono (stands in for OpenCV's Hershey Simplex overlay text + terminal)
- Strongest visual element: the 21-point hand skeleton, red dots + light bones

## Share copy (draft)
My webcam now reads hand gestures, says them out loud, and learns new ones — 21 dots, 10 gestures, one `python main.py`.

## Audio direction
- Role: warm upbeat bed + moderate, motion-matched UI accents
- Music: `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` (120 BPM, quiet intro before the grid kicks in at ~3s — fits the dots hook)
- Music treatment: start at 0, bed ~0.32, fade out over the last ~1.2s
- Music cue guidance: preset `assets/music/cues/happy-beats-business-moves-vol-1-by-ende-dot-app.music-cues.json`. Beat grid every ~0.5s from 3.02. Window reveal ≈ 3.02; gesture morphs on 7.02 / 8.02 / 9.02 / 10.02 / 11.02 (every other beat — labels need ~1s holds); terminal lines on 15.52 / 16.52 / 17.52; outro title near 19.52, punchline on strong cue 20.02.
- Audio-reactive treatment: subtle; bass energy makes the red background glow behind the hand breathe. No waveform/EQ visuals.
- SFX posture: moderate — soft pops/ticks for dots, soft click per gesture change, key press for `v`, sparse key ticks for terminal typing, one warm hit for the outro.
- Audio-coupled moments: dots popping in, gesture morph ticks, `v` keypress, typed commands, outro title.
- Restraint rule: no stacked impacts, nothing harsh/high-frequency repeated; SFX never louder than ~0.7.

## Storyboard

### Scene 1 — 21 dots — 3.0s (0.0–3.0)
Black. 21 red landmark dots pop in (wrist first, then each finger), bones draw between them, then the skeleton plays back the real recorded index-point frames. Mono metadata: `recorded_gestures/index_20260709_201708.json · 100 frames · 21 landmarks`. Headline: "Your hand is 21 dots." (settled ≥1.4s).
Sequential/interaction: yes — 21 dots arrive one by one (fast accent, not text).
Audio intent: quiet intro, curiosity.
Audio-coupled idea: a few soft ticks across the dot sequence; a soft drop when the bones connect.
Music: intro bed.
Transition mood: clean → Scene 2 (camera pulls back, window chrome fades up around the hand).

### Scene 2 — The window — 4.0s (3.0–7.0)
Recreated OpenCV window titled "Hand Gesture Recognition" (left). Hand morphs to peace; red `peace (0.98)` appears top-left of the feed; green `FPS: 29.8`; bottom `Voice: OFF` + the real instruction line. Right column: "Real-time gesture recognition." / "MediaPipe + TensorFlow. Just a webcam."
Sequential/interaction: label appears after the pose settles.
Audio intent: the beat kicks in — "it's alive".
Audio-coupled idea: soft impact on window reveal.
Transition mood: clean → Scene 3 (same window stays).

### Scene 3 — Ten gestures — 5.0s (7.0–12.0)
Same window. Hand morphs every ~1s: thumbs up → rock → call me → okay → live long; label updates each time. Right column: "10 gestures out of the box." + all 10 names from `gesture.names` in a mono list, current one highlighted red.
Sequential/interaction: yes — 5 morphs on every other beat; each label holds ~1s. List is visible in full; only the highlight moves.
Audio intent: groove, momentum.
Audio-coupled idea: soft click per gesture change.
Transition mood: clean → Scene 4.

### Scene 4 — It talks back — 3.0s (12.0–15.0)
`v` keycap presses; `Voice: OFF` flips to `Voice: ON`; speech bubble with speaker icon pops by the hand: "live long". Right column: "It talks back." / "Text-to-speech via gTTS. Toggle with v."
Sequential/interaction: yes — simulated keypress.
Audio intent: playful.
Audio-coupled idea: keypress on `v`; soft pop on the bubble.
Transition mood: hard-ish cut → Scene 5.

### Scene 5 — Teach it yours — 4.0s (15.0–19.0)
Terminal window. Three commands typed, each followed by the real print line:
- `$ python main.py record --gesture index` → `Saved 100 samples to recorded_gestures/index_20260709_201708.json`
- `$ python main.py train` → `Model saved to models/custom_model`
- `$ python main.py recognize --model custom`
Headline: "Teach it your own."
Sequential/interaction: yes — typed lines on every other beat, full set held ≥1.2s at the end.
Audio intent: hands-on, builder energy.
Audio-coupled idea: sparse key ticks while typing; click on each Enter.
Transition mood: clean → Scene 6.

### Scene 6 — Press 'q' to quit — 3.5s (19.0–22.5)
Open-palm skeleton waves (left). "Hand Gesture Recognition" lands, "MediaPipe · TensorFlow · gTTS" under it, then the punchline in red mono: "Press 'q' to quit."
Audio intent: warm payoff, then fade.
Audio-coupled idea: warm hit on title; small click on the punchline (strong cue 20.02).
Transition mood: hold → end.

**Music mood for this video:** upbeat
**Audio summary:** quiet intro under the dots, the beat drops as the window appears, clicks ride the gesture morphs, key ticks through the terminal, warm hit on the title and a fade out under "Press 'q' to quit."
