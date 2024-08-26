import streamlit as st
from fluent_flow.core.language_model import LanguageModel
from fluent_flow.core.speech_to_text import SpeechToText
from fluent_flow.core.text_to_speech import TextToSpeech
from fluent_flow.core.audio_recorder import AudioRecorder
from fluent_flow.config.configuration import ConfigurationManager
import time


def initialize_session_state():
    if "conversation_active" not in st.session_state:
        st.session_state.conversation_active = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ""
    if "config_manager" not in st.session_state:
        st.session_state.config_manager = ConfigurationManager()


def start_conversation():
    st.session_state.conversation_active = True
    st.session_state.chat_history = ""


def stop_conversation():
    st.session_state.conversation_active = False


def process_with_language_model(language_model, text_to_speech, transcription):
    with st.spinner("Processing with Language Model..."):
        try:
            response = language_model.process_text(transcription, st.session_state.chat_history)
            st.success("AI response generated")
            st.write(f"AI: {response}")

            # Update chat history
            st.session_state.chat_history = language_model.update_chat_history(
                st.session_state.chat_history, transcription, response
            )

            # Convert AI response to speech
            with st.spinner("Converting response to speech..."):
                audio_file = text_to_speech.convert(response)
                if audio_file:
                    st.audio(audio_file)
                    st.success("Audio response ready")

        except Exception as e:
            st.error(f"Error processing text: {str(e)}")


def main():
    st.title("German Speaking Coach")

    initialize_session_state()
    config_manager = ConfigurationManager()

    # Initialize the services using the configuration
    language_model_config = config_manager.get_language_model_config()
    speech_to_text_config = config_manager.get_speech_to_text_config()
    text_to_speech_config = config_manager.get_text_to_speech_config()
    audio_recorder_config = config_manager.get_audio_recorder_config()

    language_model = LanguageModel(language_model_config)
    speech_to_text = SpeechToText(speech_to_text_config)
    text_to_speech = TextToSpeech(text_to_speech_config)
    audio_recorder = AudioRecorder(audio_recorder_config)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Conversation", key="start_button"):
            start_conversation()
    with col2:
        if st.button("Stop Conversation", key="stop_button"):
            stop_conversation()

    if st.session_state.conversation_active:
        st.info("Conversation is active. Click 'Record' when you're ready to speak.")

        if st.button("Record", key="record_button"):
            with st.spinner("Preparing to record..."):
                time.sleep(1)  # Brief pause before recording starts

            st.write("Recording... Speak now!")
            audio_file = audio_recorder.record_and_save()
            st.success(f"Audio recorded and saved to {audio_file}")

            st.write("Transcribing audio...")
            transcription = speech_to_text.transcribe(audio_file)
            st.info(f"Transcription: {transcription}")

            process_with_language_model(language_model, text_to_speech, transcription)

            st.write("Preparing for next turn...")
            time.sleep(2)  # Short pause before next recording

    else:
        st.warning("Press 'Start Conversation' to begin.")

    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Conversation History")
        st.text_area("Chat", value=st.session_state.chat_history, height=300, disabled=True)


if __name__ == "__main__":
    main()
