import os
from fluent_flow.core.language_model import LanguageModel
from fluent_flow import logger
from fluent_flow.config.configuration import ConfigurationManager


def main():
    # Initialize ConfigurationManager
    config_manager = ConfigurationManager()

    # Get OpenAI service configuration
    openai_config = config_manager.get_openai_service_config()

    print("\nConfiguration loaded:")
    print(f"API URL: {openai_config.api_url}")
    print(f"Model: {openai_config.model}")
    print(f"API Key found: {'Yes' if openai_config.api_key else 'No'}")

    if not openai_config.api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        return

    # Initialize the LanguageModel with the configuration
    language_model = LanguageModel(openai_config.api_key, openai_config.model)
    chat_history = ""

    print("\nWelcome to the German Speaking Coach!")
    print("Type 'quit' to end the conversation.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            break

        try:
            response = language_model.process_text(user_input, chat_history)
            print(f"AI: {response}")

            # Update chat history
            chat_history = language_model.update_chat_history(
                chat_history, user_input, response
            )
        except Exception as e:
            logger.error(f"Error in conversation: {str(e)}")
            print("Sorry, there was an error processing your input. Please try again.")

    print("Thank you for using the German Speaking Coach. Auf Wiedersehen!")


if __name__ == "__main__":
    main()
