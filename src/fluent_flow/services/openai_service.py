from openai import OpenAI
from fluent_flow import logger


class OpenAIService:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_prompt(self):
        return """
        Du bist ein freundlicher Tandem-Partner für Deutsch. Deine Aufgabe ist es, eine natürliche Konversation zu führen, dabei sanft zu korrigieren und natürlichere Ausdrucksweisen vorzuschlagen. Verwende das "du" und halte den Ton locker und authentisch.

        Richtlinien für deine Antworten:
        1. Reagiere zuerst natürlich auf den Inhalt der Aussage.
        2. Korrigiere wichtige Fehler sanft, indem du die korrekte Form in deiner Antwort verwendest.
        3. Schlage gelegentlich natürlichere Formulierungen vor, aber nicht bei jedem Satz.
        4. Stelle nur dann eine Frage, wenn es sich natürlich ergibt und nicht zu aufdringlich wirkt.
        5. Deine Antworten sollten kurz und natürlich sein, wie in einem echten Gespräch.

        Beispiel:
        Schüler: Ich hab gestern einen Film angeschaut, der war echt gut.
        Partner: Oh cool! Ich hab auch gestern einen Film gesehen. Was für einer war's bei dir?

        Aktuelles Gespräch:
        {chat_history}
        Schüler: {input_text}
        Partner:
        """

    def generate_response(self, input_text, chat_history=""):
        try:
            logger.info("Generating response from OpenAI")
            prompt = self.generate_prompt().format(chat_history=chat_history, input_text=input_text)

            messages = [
                {"role": "system", "content": "You are a helpful German language tutor."},
                {"role": "user", "content": prompt},
            ]

            response = self.client.chat.completions.create(model=self.model, messages=messages)
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in OpenAI service: {str(e)}")
            raise

    def process_text(self, input_text, chat_history):
        logger.info("Processing text with OpenAI...")
        try:
            response = self.generate_response(input_text, chat_history)
            updated_chat_history = self.update_chat_history(chat_history, input_text, response)
            logger.info("Text processing completed")
            return response, updated_chat_history
        except Exception as e:
            logger.error(f"Error in text processing: {str(e)}")
            return None, chat_history
