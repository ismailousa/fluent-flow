from typing import List, Optional
from fluent_flow.agent.chains import get_grammar_check_chain, get_conversation_chain
from fluent_flow.agent.types import AgentState, ChatTurn
from fluent_flow import logger



class TutorAgent:
    """
    TutorAgent processes:
    1. Grammar correction
    2. Error explanations
    3. Conversation continuation
    """

    def __init__(self, intro_message: Optional[str] = None):
        try:
            self.grammar_chain = get_grammar_check_chain()
            self.conversation_chain = get_conversation_chain()

            self.state: AgentState = AgentState(history=[])

            if intro_message:
                initial_turn = ChatTurn(
                    user_input="",
                    corrected=None,
                    errors=None,
                    grade=None,
                    agent_response=intro_message
                )
                self.state.history.append(initial_turn)
        except Exception as e:
            logger.error("Failed to initialize TutorAgent", exc_info=True)
            raise

    def _get_grammar_history(self, history: List[ChatTurn], n: int = 3) -> str:
        recent = history[-n:]
        if len(recent) == 0:
            return ""
        return "\n".join(
            f"Benutzer: {turn.user_input}\nTutor Korrektur: {turn.corrected or turn.user_input}\nTutor Grade: {turn.grade}" 
            for turn in recent
        )
    
    def _get_conversation_history(self, history: List[ChatTurn], n: int = 3) -> str:
        recent = history[-n:]
        if len(recent) == 0:
            return ""
        return "\n".join(
            f"Benutzer: {turn.corrected or turn.user_input}\nTutor: {turn.agent_response}"
            for turn in recent
        )

    def run(self, new_input: str) -> AgentState:
        try:
            logger.info(f"Running tutor agent with input: {new_input}")
            turn = ChatTurn(user_input=new_input)

            # Step 1: Grammar Correction
            grammar_prompt_input = {
                "input": turn.user_input,
                "history": self._get_grammar_history(self.state.history)
            }
            grammar_result = self.grammar_chain(grammar_prompt_input)
            logger.info(f"Grammar result: {grammar_result}")
            turn.corrected = grammar_result.get("corrected")
            turn.errors = grammar_result.get("errors")
            turn.grade = grammar_result.get("grade")

            # Step 2: Conversation
            convo_input = turn.corrected or turn.user_input
            conversation_prompt_input = {
                "input": convo_input,
                "history": self._get_conversation_history(self.state.history)
            }
            convo_result = self.conversation_chain(conversation_prompt_input)
            logger.info(f"Convo result: {convo_result}")
            turn.agent_response = convo_result.get("response")

            # Append turn to state
            self.state.history.append(turn)

            return self.state

        except Exception as e:
            logger.error("Chat turn failed", exc_info=True)
            raise

