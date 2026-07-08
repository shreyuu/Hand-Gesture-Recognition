from gtts import gTTS
import os

# Text you want to convert to speech
text_to_speak = "Hello, this is an example of using gTTS on macOS."

# Initialize the gTTS object with the text
tts = gTTS(text=text_to_speak, lang='en')

# Save the generated speech as an audio file
audio_file_path = 'output_audio.mp3'
tts.save(audio_file_path)

# Play the generated audio using the default audio player on macOS
os.system(f"open {audio_file_path}")
