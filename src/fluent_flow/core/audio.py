import sounddevice as sd
import soundfile as sf
import numpy as np
from fluent_flow import logger


def record_audio(duration=5, fs=44100):
    """Record audio for a specified duration."""
    logger.info("Recording will start in 3 seconds...")
    sd.sleep(3000)
    logger.info("Recording started...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    logger.info("Recording finished.")
    return recording.flatten()


def save_audio(data, filename="output.wav", fs=44100):
    """Save audio data to a WAV file."""
    sf.write(filename, data, fs)
    logger.info(f"Audio saved to {filename}")
