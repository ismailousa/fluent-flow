from typing import List
import streamlit as st
from fluent_flow.agent.tutor import TutorAgent
from fluent_flow.agent.types import ChatTurn

st.set_page_config(
    page_title="Fluent Flow - Deutsch Tutor",
    page_icon="🇩🇪",
    layout="centered",
)

# Hide default Streamlit menu & footer
st.markdown(
    """
    <style>
      #MainMenu, footer {visibility: hidden;}
      .stDeployButton {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Agent & History 
if "agent" not in st.session_state:
    st.session_state.agent = TutorAgent("👋  Hallo! Ich bin Coco, deine deutsche Sprachlehrerin."
            "Ich korrigiere deine Fehler, erkläre sie dir und führe lebendige Gespräche mit dir."
            "- Stell mir gleich deine erste Frage!")
    
    st.session_state["history"] = st.session_state.agent.state.history 

# Render Chat History
for turn in st.session_state.history:
    # user message
    if turn.user_input:
        msg = st.chat_message("user")
        msg.write(turn.user_input)

        # if there were corrections, show them in an expander
        if turn.corrected and turn.errors:
            with msg.container().expander("📝 Korrekturen anzeigen"):
                st.write(f"**Korrigierter Text:** {turn.corrected}")
                st.write("---")
                st.write("**Fehlererklärungen:**")
                for err in turn.errors:
                    st.write(f"- Original: {err['original']}")
                    st.write(f"  Korrigiert: {err['corrected']}")
                    st.write(f"  Erklärung: {err['explanation']}")
                    st.write("---")

    # tutor message
    if turn.agent_response:
        st.chat_message("assistant").write(turn.agent_response)

# Input Box
user_input = st.chat_input("Schreibe deine Nachricht auf Deutsch:")

if user_input:
    # send input to the agent, extend history, and rerun to display
    agent_state = st.session_state.agent.run(user_input)
    st.session_state.history = agent_state.history # history already extended by the agent
    st.rerun()
