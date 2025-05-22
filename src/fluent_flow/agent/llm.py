from fluent_flow import logger
from fluent_flow.config.configuration import ConfigurationManager
from langchain_openai import ChatOpenAI

config_manager = ConfigurationManager()

def load_config():
    llm_config = config_manager.get_llm_config()
    return llm_config

def get_chat_llm():
    """
    Get the chat LLM depending on the config
    """
    try:
        llm_config = load_config()
        logger.info(f"Initializing chat LLM with model: {llm_config.model} and temperature: {llm_config.temperature}")
        if llm_config.provider == "openai":
            llm = ChatOpenAI(model=llm_config.model, temperature=llm_config.temperature, api_key=llm_config.api_key)
        else:
            raise ValueError(f"Provider {llm_config.provider} not supported")
        return llm
    except Exception as e:
        logger.error(f"Error getting chat LLM: {e}")
        raise e

# Initialize the global variable
_chat_llm_instance = None

def get_llm_instance():
    """
    Get the LLM instance if it exists, otherwise create it
    """
    global _chat_llm_instance
    if _chat_llm_instance is None:
        _chat_llm_instance = get_chat_llm()
    return _chat_llm_instance



