# agents/voice_agent.py

import whisper
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import os

class VoiceAgent:
    def __init__(self):
        self.model = whisper.load_model("base")  # or 'tiny', 'small', 'medium'
        self.engine = pyttsx3.init()

    def record_audio(self, duration=5, fs=44100):
        print("🎤 Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        temp_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        write(temp_path, fs, audio)
        print(f"📁 Saved audio to {temp_path}")
        return temp_path

    def transcribe(self, audio_path):
        print("🧠 Transcribing...")
        result = self.model.transcribe(audio_path)
        return result["text"]

    def speak(self, text):
        print("🗣️ Speaking...")
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    agent = VoiceAgent()
    wav_file = agent.record_audio(duration=5)
    transcription = agent.transcribe(wav_file)
    print(f"User said: {transcription}")
    agent.speak("Hello! Here's your market update: " + transcription)
    os.remove(wav_file)
