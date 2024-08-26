import os
from gtts import gTTS
from pydub import AudioSegment
from fluent_flow import logger


class TextToSpeech:
    def __init__(self, default_lang="de"):
        self.default_lang = default_lang

    def convert(self, text, lang=None, save_mp3=False, save_wav=True):
        """
        Convert text to speech.

        :param text: The text to convert to speech
        :param lang: The language of the text (default is German)
        :param save_mp3: Whether to save the audio as MP3
        :param save_wav: Whether to save the audio as WAV
        :return: Dictionary with paths to saved files
        """
        lang = lang or self.default_lang
        logger.info(f"Converting text to speech in {lang}...")

        try:
            tts = gTTS(text=text, lang=lang)
            mp3_filename = "tts.mp3"
            wav_filename = "tts.wav"
            output_files = {}

            # Save as MP3
            if save_mp3:
                tts.save(mp3_filename)
                output_files["mp3"] = mp3_filename
                logger.info(f"Audio saved as MP3: {mp3_filename}")

            # Convert to WAV if requested
            if save_wav:
                audio = AudioSegment.from_mp3(mp3_filename)
                audio.export(wav_filename, format="wav")
                output_files["wav"] = wav_filename
                logger.info(f"Audio converted to WAV: {wav_filename}")

            logger.info("Text-to-speech conversion completed")
            return output_files

        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {str(e)}")
            return None

    def set_default_language(self, lang):
        """Set the default language for text-to-speech conversion."""
        self.default_lang = lang
        logger.info(f"Default language set to: {lang}")

    def cleanup_files(self, files):
        """Remove temporary audio files."""
        for file_path in files.values():
            try:
                os.remove(file_path)
                logger.info(f"Removed temporary file: {file_path}")
            except Exception as e:
                logger.error(f"Error removing file {file_path}: {str(e)}")
