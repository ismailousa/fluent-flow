import wave
import json
from vosk import Model, KaldiRecognizer
from fluent_flow import logger


def speech_to_text(audio_file, model_path):
    """Convert speech to text using Vosk."""
    logger.info(f"Starting speech-to-text conversion for {audio_file}")

    # Load Vosk model
    model = Model(model_path)

    # Open the audio file
    wf = wave.open(audio_file, "rb")

    # Check if the audio format is compatible
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        logger.error("Audio file must be WAV format mono PCM.")
        return None

    # Create recognizer
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # Process audio file
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    # Extract text from results
    text = " ".join([r["text"] for r in results if "text" in r])

    logger.info("Speech-to-text conversion completed")
    return text


import openai


def speech_to_text_with_whisper(audio_file_path, model="whisper-1"):
    """
    Convert speech to text using OpenAI Whisper.

    :param audio_file_path: Path to the audio file
    :param model: Whisper model to use (default is "whisper-1")
    :return: Transcribed text
    """
    logger.info(f"Starting speech-to-text conversion for {audio_file_path}")

    try:
        # Open the audio file in binary mode
        with open(audio_file_path, "rb") as audio_file:
            # Transcribe using OpenAI Whisper
            response = openai.Audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text",  # Options: "text", "json", "srt", "verbose_json", "vtt"
            )

        transcribed_text = response["text"]
        logger.info("Speech-to-text conversion completed")
        return transcribed_text

    except Exception as e:
        logger.error(f"Error in speech-to-text conversion: {str(e)}")
        return None
