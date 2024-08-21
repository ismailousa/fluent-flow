import os
from box import ConfigBox
from dotenv import load_dotenv
from fluent_flow.utils.common import read_yaml
from fluent_flow import logger

# Load secrets from .env file
load_dotenv()


class ConfigurationManager:
    def __init__(self, config_filepath="config.yml"):
        logger.info(f"Reading the configuration file: {config_filepath}")
        self.config = read_yaml(config_filepath)

    def get_vosk_service_config(self) -> dict:
        config = self.config["fluent_flow"]["vosk_service"]
        model_path = os.getenv("VOSK_MODEL_PATH")
        return ConfigBox(
            {"model_path": model_path, "sample_rate": config["sample_rate"]}
        )

    def get_openai_service_config(self) -> dict:
        config = self.config["fluent_flow"]["openai_service"]
        api_key = os.getenv("OPENAI_API_KEY")
        return ConfigBox(
            {"api_url": config["api_url"], "model": config["model"], "api_key": api_key}
        )

    def get_streamlit_config(self) -> dict:
        config = self.config["fluent_flow"]["streamlit_app"]
        return ConfigBox({"host": config["host"], "port": config["port"]})

    def get_logger_config(self) -> dict:
        config = self.config["fluent_flow"]["logger"]
        return ConfigBox({"level": config["level"], "format": config["format"]})
