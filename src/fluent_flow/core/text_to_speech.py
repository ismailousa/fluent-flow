from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from fluent_flow import logger


def text_to_speech(text, lang="de"):
    """Convert text to speech."""
    logger.info("Converting text to speech...")
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    play(audio)
    logger.info("Text-to-speech conversion completed")
    return "output.mp3"


# def text_to_speech(text, language='de', mp3_filename='output.mp3', wav_filename='output.wav'):
#     """Convert text to speech in German and save as a WAV file."""
#     try:
#         # Convert text to speech and save as MP3
#         tts = gTTS(text=text, lang=language)
#         tts.save(mp3_filename)
#         logger.info(f"Text-to-speech conversion completed and saved to {mp3_filename}")

#         # Convert MP3 to WAV
#         audio = AudioSegment.from_mp3(mp3_filename)
#         audio.export(wav_filename, format='wav')
#         logger.info(f"Audio converted to WAV and saved to {wav_filename}")

#         # Optionally, remove the MP3 file if you only want the WAV
#         # os.remove(mp3_filename)

#     except Exception as e:
#         logger.error(f"Error in text-to-speech conversion: {str(e)}")
