from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable
from fluent_flow.agent.llm import get_llm_instance
from fluent_flow.agent.prompts import CONVERSATION_PROMPT, CORRECTION_PROMPT
from fluent_flow.agent.types import AgentState

def get_grammar_check_chain() -> Runnable:
    """
    Grammar correction chain: takes AgentState['input'], returns updated AgentState.
    """
    llm = get_llm_instance()
    prompt = ChatPromptTemplate.from_template(CORRECTION_PROMPT)

    chain = (
        prompt
        | llm
        | JsonOutputParser()
    )

    def grammar_chain_wrapper(state: AgentState) -> AgentState:
        response = chain.invoke({"input": state["input"], "history": state["history"]})
        return {
            **state,
            "corrected": response["corrected"],
            "errors": response["errors"],
            "grade": response["grade"]
        }

    return grammar_chain_wrapper

def get_conversation_chain() -> Runnable:
    """
    Continuation chain: uses corrected or input, adds follow_up to AgentState.
    """
    llm = get_llm_instance()
    prompt = ChatPromptTemplate.from_template(CONVERSATION_PROMPT)

    chain = (
        prompt
        | llm
        | JsonOutputParser()
    )

    def conversation_chain_wrapper(input_dict: dict) -> dict:
        print(f"Conversation chain input: {input_dict}")
        response = chain.invoke(input_dict)
        return {
            "response": response["Tutor"]
        }

    return conversation_chain_wrapper

def get_grammar_prompt(input: str, history: str) -> str:
    """
    Formats the prompt for the grammar check chain.
    """
    prompt = ChatPromptTemplate.from_template(CORRECTION_PROMPT)
    return prompt.format(input=input, history=history)

def get_conversation_prompt(input: str, history: str) -> str:
    """
    Formats the prompt for the conversation chain.
    """
    prompt = ChatPromptTemplate.from_template(CONVERSATION_PROMPT)
    return prompt.format(input=input, history=history)


# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# from fluent_flow.agent.llm import get_llm_instance
# from fluent_flow.agent.prompts import CONVERSATION_PROMPT, CORRECTION_PROMPT
# from fluent_flow import logger
# from fluent_flow.agent.types import AgentState


# # class ErrorExplanation(TypedDict):
# #     original: str
# #     corrected: str
# #     explanation: str

# # class AgentState(TypedDict):
# #     input: str
# #     corrected: Optional[str]
# #     errors: Optional[List[ErrorExplanation]]
# #     grade: Optional[str]
# #     follow_up: Optional[str]


# def grammar_check_node(state: AgentState) -> dict:
#     """
#     Corrects the input text. Returns the corrected text, and explanation of each correction.
#     """
#     try:
#         llm = get_llm_instance()
#         prompt = ChatPromptTemplate.from_template(
#             CORRECTION_PROMPT
#         )
#         grammar_check_chain = prompt | llm | StrOutputParser()
#         logger.info(f"Grammar check node input: {state}")
#         result = grammar_check_chain.invoke(state['input'])
#         logger.info(f"Grammar check node result: {result}")
#         return {
#             'corrected': result['corrected'],
#             'errors': result['errors'],
#             'grade': result['grade']
#         }
#     except Exception as e:
#         logger.error(f"Error in grammar_check_node: {e}")
#         raise e
    

# def conversation_node(state: AgentState) -> dict:
#     """
#     Keeps the conversation going.
#     """
#     try:
#         llm = get_llm_instance()
#         prompt = ChatPromptTemplate.from_template(
#             CONVERSATION_PROMPT
#         )
#         conversation_chain = prompt | llm | StrOutputParser()

#         input = state['corrected'] if state['corrected'] else state['input']

#         result = conversation_chain.invoke(input)
#         return {
#             'response': result['response']
#         }
#     except Exception as e:
#         logger.error(f"Error in conversation_node: {e}")
#         raise e
