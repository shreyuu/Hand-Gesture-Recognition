import os
import time
import threading
import tempfile
from gtts import gTTS
from collections import defaultdict


class AudioManager:
    """
    Handles text-to-speech conversion and audio playback in a non-blocking manner.
    """

    def __init__(self, cooldown_time=2, cache_size=20):
        self.cooldown_time = cooldown_time
        self.last_spoken_time = 0
        self.audio_cache = {}
        self.cache_size = cache_size
        self.audio_thread = None
        self.lock = threading.Lock()
        self.temp_dir = tempfile.gettempdir()

        # Track gesture frequencies to prioritize cache
        self.gesture_frequency = defaultdict(int)

    def speak(self, text, lang="en"):
        """
        Speak the given text if cooldown period has elapsed.
        This method is non-blocking.
        """
        current_time = time.time()

        # Respect cooldown period
        if (current_time - self.last_spoken_time) <= self.cooldown_time:
            return False

        # Update frequency count for this gesture
        self.gesture_frequency[text] += 1

        # Set last spoken time
        self.last_spoken_time = current_time

        # Start a new thread for audio processing
        if self.audio_thread is None or not self.audio_thread.is_alive():
            self.audio_thread = threading.Thread(
                target=self._process_audio, args=(text, lang), daemon=True
            )
            self.audio_thread.start()

        return True

    def _process_audio(self, text, lang):
        """
        Process and play audio in a separate thread.
        """
        with self.lock:
            # Check if we already have this text cached
            if text in self.audio_cache:
                audio_path = self.audio_cache[text]
            else:
                # Generate new audio file
                audio_path = os.path.join(self.temp_dir, f"gesture_{hash(text)}.mp3")
                tts = gTTS(text=text, lang=lang)
                tts.save(audio_path)

                # Add to cache
                self._update_cache(text, audio_path)

            # Play the audio
            os.system(f"afplay {audio_path}")

    def _update_cache(self, text, audio_path):
        """
        Update the audio cache, removing least used entries if needed
        """
        # Add new item to cache
        self.audio_cache[text] = audio_path

        # If cache is full, remove least frequently used items
        if len(self.audio_cache) > self.cache_size:
            # Sort gestures by frequency
            sorted_gestures = sorted(self.gesture_frequency.items(), key=lambda x: x[1])

            # Remove least used gesture from cache
            for gesture, _ in sorted_gestures:
                if gesture in self.audio_cache:
                    del self.audio_cache[gesture]
                    del self.gesture_frequency[gesture]
                    break
