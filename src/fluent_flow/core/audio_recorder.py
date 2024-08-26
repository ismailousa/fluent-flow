import sounddevice as sd
import soundfile as sf
import numpy as np
from fluent_flow import logger


class AudioRecorder:
    def __init__(self, default_duration=5, default_fs=44100):
        self.default_duration = default_duration
        self.default_fs = default_fs
        self.default_filename = "audio.wav"

    def record(self, duration=None, fs=None):
        """
        Record audio for a specified duration.

        :param duration: Recording duration in seconds (default is self.default_duration)
        :param fs: Sampling frequency (default is self.default_fs)
        :return: Numpy array of recorded audio data
        """
        duration = duration or self.default_duration
        fs = fs or self.default_fs

        # logger.info("Recording will start in 3 seconds...")
        # sd.sleep(3000)
        logger.info("Recording started...")

        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished

        logger.info("Recording finished.")
        return recording.flatten()

    def save(self, data, filename=None, fs=None):
        """
        Save audio data to a WAV file.

        :param data: Numpy array of audio data
        :param filename: Output filename (default is self.default_filename)
        :param fs: Sampling frequency (default is self.default_fs)
        :return: Path to the saved file
        """
        filename = filename or self.default_filename
        fs = fs or self.default_fs

        sf.write(filename, data, fs)
        logger.info(f"Audio saved to {filename}")
        return filename

    def record_and_save(self, duration=None, fs=None, filename=None):
        """
        Record audio and save it to a file.

        :param duration: Recording duration in seconds (default is self.default_duration)
        :param fs: Sampling frequency (default is self.default_fs)
        :param filename: Output filename (default is self.default_filename)
        :return: Path to the saved file
        """
        audio_data = self.record(duration, fs)
        return self.save(audio_data, filename, fs)

    def set_default_duration(self, duration):
        """Set the default recording duration."""
        self.default_duration = duration
        logger.info(f"Default recording duration set to {duration} seconds")

    def set_default_fs(self, fs):
        """Set the default sampling frequency."""
        self.default_fs = fs
        logger.info(f"Default sampling frequency set to {fs} Hz")

    def set_default_filename(self, filename):
        """Set the default output filename."""
        self.default_filename = filename
        logger.info(f"Default output filename set to {filename}")
