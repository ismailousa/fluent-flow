from fluent_flow.services.openai_service import OpenAIService
from fluent_flow import logger

# import vosk
import json
import wave


class SpeechToText:
    def __init__(self, api_key=None, engine="openai", model="whisper-1"):
        self.engine = engine
        self.model = model
        if engine == "openai":
            self.openai_service = OpenAIService(api_key, model)
        # elif engine == "vosk":
        #     vosk.SetLogLevel(-1)
        #     self.vosk_model = vosk.Model(model)  # Assuming 'model' is the path to Vosk model
        else:
            raise ValueError("Unsupported engine. Choose 'openai' or 'vosk'.")

    def transcribe(self, audio_file_path: str) -> str:
        """
        Convert speech to text using the selected engine.

        :param audio_file_path: Path to the audio file
        :return: Transcribed text
        """
        logger.info(f"Starting speech-to-text conversion for {audio_file_path} using {self.engine}")

        try:
            if self.engine == "openai":
                return self._transcribe_openai(audio_file_path)
            elif self.engine == "vosk":
                return self._transcribe_vosk(audio_file_path)
        except Exception as e:
            logger.error(f"Error in speech-to-text conversion: {str(e)}")
            return None

    def _transcribe_openai(self, audio_file_path: str) -> str:
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = self.openai_service.client.audio.transcriptions.create(
                    model=self.model, file=audio_file, response_format="text"
                )

            logger.info(f"Transcription response: {response}")
            transcription = response

            if not transcription:
                logger.warning("Transcription result is empty")
                return ""

            logger.info(f"Transcription result: {transcription}")
            return transcription

        except Exception as e:
            logger.error(f"Error in OpenAI transcription: {str(e)}")
            raise  # Re-raise the exception after logging

    def _transcribe_vosk(self, audio_file_path: str) -> str:
        # wf = wave.open(audio_file_path, "rb")
        # rec = vosk.KaldiRecognizer(self.vosk_model, wf.getframerate())

        # result = ""
        # while True:
        #     data = wf.readframes(4000)
        #     if len(data) == 0:
        #         break
        #     if rec.AcceptWaveform(data):
        #         result += json.loads(rec.Result())["text"] + " "

        # result += json.loads(rec.FinalResult())["text"]
        # return result.strip()
        pass

    def set_engine(self, engine: str, model: str = None):
        """
        Set a new engine and optionally a new model for transcription.

        :param engine: 'openai' or 'vosk'
        :param model: Model name for OpenAI or path to Vosk model
        """
        self.engine = engine
        if model:
            self.model = model

        if engine == "openai":
            self.openai_service = OpenAIService(self.openai_service.api_key, self.model)
        elif engine == "vosk":
            self.vosk_model = vosk.Model(self.model)
        else:
            raise ValueError("Unsupported engine. Choose 'openai' or 'vosk'.")

        logger.info(f"Speech-to-text engine updated to: {engine}, model: {self.model}")
