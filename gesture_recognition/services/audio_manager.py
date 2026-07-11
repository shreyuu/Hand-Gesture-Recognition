import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections import defaultdict

from gtts import gTTS


class AudioManager:
    """
    Handles text-to-speech conversion and audio playback in a non-blocking manner.
    """

    def __init__(self, cooldown_time=2, cache_size=20):
        self.cooldown_time = cooldown_time
        self.last_spoken_time = 0
        self.last_spoken_text = None
        self.audio_cache = {}
        self.cache_size = cache_size
        self.audio_thread = None
        self.lock = threading.Lock()
        self.temp_dir = tempfile.gettempdir()
        self._player = self._find_player()
        self._warned_no_player = False

        # Track phrase frequencies to prioritize cache
        self.gesture_frequency = defaultdict(int)

    @staticmethod
    def _find_player():
        """Find a command-line audio player for this platform."""
        if sys.platform == "darwin":
            return ["afplay"]
        for candidate, args in (
            ("mpg123", ["-q"]),
            ("ffplay", ["-nodisp", "-autoexit", "-loglevel", "quiet"]),
            ("mpv", ["--no-video", "--really-quiet"]),
        ):
            if shutil.which(candidate):
                return [candidate, *args]
        return None

    def speak(self, text, lang="en", slow=False):
        """
        Speak the given text. Non-blocking.

        A phrase is only announced when it changes (holding the same gesture
        doesn't repeat it), and never more often than the cooldown allows.
        """
        current_time = time.time()

        if text == self.last_spoken_text:
            return False

        # Respect cooldown period
        if (current_time - self.last_spoken_time) <= self.cooldown_time:
            return False

        # Only one playback at a time; drop the request if audio is busy
        if self.audio_thread is not None and self.audio_thread.is_alive():
            return False

        self.gesture_frequency[text] += 1
        self.last_spoken_time = current_time
        self.last_spoken_text = text

        self.audio_thread = threading.Thread(
            target=self._process_audio, args=(text, lang, slow), daemon=True
        )
        self.audio_thread.start()
        return True

    def reset_last_spoken(self):
        """Forget the last spoken phrase so it can be announced again."""
        self.last_spoken_text = None

    def _process_audio(self, text, lang, slow):
        """
        Process and play audio in a separate thread.
        """
        with self.lock:
            cache_key = (text, lang, slow)

            if cache_key in self.audio_cache:
                audio_path = self.audio_cache[cache_key]
            else:
                # hashlib (not hash()) so the filename is stable across runs
                # and cached files survive restarts.
                digest = hashlib.md5(
                    f"{text}|{lang}|{slow}".encode("utf-8")
                ).hexdigest()
                audio_path = os.path.join(self.temp_dir, f"gesture_{digest}.mp3")

                if not os.path.exists(audio_path):
                    try:
                        tts = gTTS(text=text, lang=lang, slow=slow)
                        tts.save(audio_path)
                    except Exception as e:
                        print(f"Text-to-speech failed for '{text}': {e}")
                        return

                self._update_cache(cache_key, audio_path)

            self._play(audio_path)

    def _play(self, audio_path):
        if self._player is None:
            if not self._warned_no_player:
                print(
                    "No audio player found (install mpg123, ffmpeg or mpv "
                    "for voice feedback)"
                )
                self._warned_no_player = True
            return
        try:
            subprocess.run(
                [*self._player, audio_path],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError as e:
            print(f"Audio playback failed: {e}")

    def _update_cache(self, cache_key, audio_path):
        """
        Update the audio cache, removing least used entries if needed
        """
        self.audio_cache[cache_key] = audio_path

        # If cache is full, remove the least frequently used entry
        if len(self.audio_cache) > self.cache_size:
            sorted_phrases = sorted(self.gesture_frequency.items(), key=lambda x: x[1])
            for phrase, _ in sorted_phrases:
                stale_keys = [k for k in self.audio_cache if k[0] == phrase]
                if stale_keys:
                    for key in stale_keys:
                        del self.audio_cache[key]
                    del self.gesture_frequency[phrase]
                    break
