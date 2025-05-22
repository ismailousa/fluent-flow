import os
from dotenv import load_dotenv, find_dotenv
from fluent_flow.core.constants import *
from fluent_flow.utils.common import create_directories, read_yaml
from fluent_flow import logger

load_dotenv(find_dotenv())
logger.info(f"find_dotenv: {find_dotenv()}")

logger.info(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")



class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        logger.info(f"Reading the configuration file: {config_filepath}")
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts.root_dir])
        create_directories([self.config.artifacts.audio_dir])
        
        # Load environment variables once
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.vosk_model_path = os.getenv("VOSK_MODEL_PATH")
        
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")

    def get_audio_recorder_config(self) -> dict:
        config = self.config.fluent_flow.audio_recorder
        return {
                "default_duration": config.default_duration,
                "default_fs": config.default_fs,
                "output_dir": self.config.artifacts.audio_dir,
            }
            

    def get_speech_to_text_config(self) -> dict:
        config = self.config.fluent_flow.speech_to_text
        return {
                "default_engine": config.default_engine,
                "openai": self.get_openai_service_config(),
                "vosk": self.get_vosk_service_config(),
            }


    def get_text_to_speech_config(self) -> dict:
        config = self.config.fluent_flow.text_to_speech
        return {"default_lang": config.default_lang, "output_dir": self.config.artifacts.audio_dir}

    def get_language_model_config(self) -> dict:
        config = self.config.fluent_flow.language_model
        return {
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
                "openai": self.get_openai_service_config(),
            }

    def get_vosk_service_config(self) -> dict:
        config = self.config.fluent_flow.vosk_service
        return {"model_path": self.vosk_model_path, "sample_rate": config.sample_rate}
    
    def get_llm_config(self) -> dict:
        llm_config = self.config.fluent_flow.llm
        llm_config["api_key"] = self.openai_api_key
        return llm_config

    def get_openai_service_config(self) -> dict:
        config = self.config.fluent_flow.openai_service
        return {"api_url": config.api_url, "model": config.model, "api_key": self.openai_api_key}

    def get_streamlit_config(self) -> dict:
        config = self.config.fluent_flow.streamlit_app
        return {"host": config.host, "port": config.port}
