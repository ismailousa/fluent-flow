from fluent_flow.services.openai_service import OpenAIService
from fluent_flow import logger


class LanguageModel:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.openai_service = OpenAIService(api_key, model)

    def process_text(self, input_text: str, chat_history: str) -> str:
        """Process the input text using the language model."""
        logger.info("Processing text with language model...")
        try:
            response = self.openai_service.generate_response(input_text, chat_history)
            logger.info("Text processing completed")
            return response.strip()
        except Exception as e:
            logger.error(f"Error in text processing: {str(e)}")
            return "Es tut mir leid, aber ich habe einen Fehler bei der Verarbeitung Ihrer Anfrage festgestellt."

    def update_chat_history(
        self,
        chat_history: str,
        new_human_text: str,
        new_ai_text: str,
        max_turns: int = 3,
    ) -> str:
        """Update chat history to keep only the last few exchanges."""
        chat_history += f"Mensch: {new_human_text}\nKI: {new_ai_text}\n"
        turns = chat_history.strip().split("\n")
        if len(turns) > max_turns * 2:
            turns = turns[-max_turns * 2 :]
        return "\n".join(turns)


# if __name__ == "__main__":
#     import os

#     lm = LanguageModel(api_key)
#     chat_history = ""

#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == 'quit':
#             break

#         response = lm.process_text(user_input, chat_history)
#         print("AI:", response)

#         chat_history = lm.update_chat_history(chat_history, user_input, response)
