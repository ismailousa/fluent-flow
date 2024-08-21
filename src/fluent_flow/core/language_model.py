from fluent_flow.services.openai_service import OpenAIService
from fluent_flow import logger


def process_text(input_text, chat_history, api_key):
    """Process text using a language model."""
    logger.info("Processing text with language model...")
    openai_service = OpenAIService(api_key)
    response = openai_service.generate_response(input_text, chat_history)
    logger.info("Text processing completed")
    return response.strip()
