import pytest
from fluent_flow.agent.tutor import TutorAgent
from fluent_flow.agent.types import AgentState, ChatTurn

def test_agent_basic_flow():
    """
    Test basic flow of the agent with a simple German sentence
    """
    agent = TutorAgent()
    test_input = "Ich bin gehst nach Hause"
    
    result = agent.run(test_input)
    
    assert isinstance(result, AgentState)
    assert len(result.history) == 1
    turn = result.history[0]
    assert turn.user_input == test_input
    assert turn.corrected is not None
    assert turn.errors is not None
    assert turn.grade in ["green", "orange", "red"]
    assert turn.agent_response is not None

def test_agent_perfect_input():
    """
    Test agent behavior with grammatically correct input
    """
    agent = TutorAgent()
    test_input = "Ich gehe nach Hause."
    
    result = agent.run(test_input)
    
    assert isinstance(result, AgentState)
    assert len(result.history) == 1
    turn = result.history[0]
    assert turn.user_input == test_input
    assert turn.grade == "green"
    assert turn.agent_response is not None

def test_agent_error_handling():
    """
    Test agent's error handling with invalid input
    """
    agent = TutorAgent()
    
    # Test with empty input
    with pytest.raises(Exception):
        agent.run("")
    
    # Test with non-string input
    with pytest.raises(Exception):
        agent.run(None)

def test_agent_conversation_history():
    """
    Test agent maintains conversation history
    """
    agent = TutorAgent()
    inputs = [
        "Ich gehe nach Hause",
        "Was machst du heute?"
    ]
    
    for input_text in inputs:
        result = agent.run(input_text)
    
    assert len(result.history) == 2
    assert result.history[0].user_input == inputs[0]
    assert result.history[1].user_input == inputs[1]

if __name__ == "__main__":
    # Manual test
    # agent = TutorAgent()
    # test_sentence = "Ich habe gestern mit meinerm Freundin gespielt."
    # test_history = ""
    # print("Testing agent with:", test_sentence)
    
    # result = agent.run(test_sentence)
    # turn = result.history[0]
    
    # print("\nResults:")
    # print(f"Original: {turn.user_input}")
    # print(f"Corrected: {turn.corrected}")
    # print("\nErrors:")
    # for error in turn.errors:
    #     print(f"\nOriginal: {error["original"]}")
    #     print(f"Corrected: {error["corrected"]}")
    #     print(f"Explanation: {error["explanation"]}")
    # print(f"\nFluency Grade: {turn.grade}")
    # print(f"Agent Response: {turn.agent_response}")

    # Run all tests
    # test_agent_basic_flow()
    test_agent_perfect_input()
    # test_agent_error_handling()
    # test_agent_conversation_history()
    print("\nAll tests passed!")
