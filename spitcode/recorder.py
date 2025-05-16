import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel
from pathlib import Path

RECORD_SECONDS = 10
SAMPLERATE = 16000
OUTPUT_WAV = "session/input.wav"
OUTPUT_TXT = "session/transcript.txt"

def record_audio():
    print(f"🎙️ Recording for {RECORD_SECONDS} seconds...")
    recording = sd.rec(int(RECORD_SECONDS * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    wav.write(OUTPUT_WAV, SAMPLERATE, recording)
    print("✅ Recording complete.")

def transcribe_audio():
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(OUTPUT_WAV)
    transcript = " ".join([seg.text for seg in segments])
    Path("session").mkdir(exist_ok=True)
    with open(OUTPUT_TXT, "w") as f:
        f.write(transcript)
    print(f"📝 Transcription saved to {OUTPUT_TXT}")
    return transcript

def run_record():
    record_audio()
    return transcribe_audio()

