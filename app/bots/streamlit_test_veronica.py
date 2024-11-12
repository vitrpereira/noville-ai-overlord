import streamlit as st
from io import BytesIO
from veronica.veronica import Veronica
import os

# Initialize Veronica agent
veronica = Veronica()

def main():
    st.title("Veronica - AI Study Companion")

    st.markdown("""
    **Veronica** é sua assistente de AI para estudar para as provas. Coloque o áudio desejado, e Verônica te ajudará a entender seu conteúdo.
    """)
    
    # File upload section
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "flac"])
    
    if uploaded_file is not None:
        # Display uploaded audio file details
        st.audio(uploaded_file, format="audio/wav")
        
        # Transcribe the audio
        transcription = veronica.invoke(user_input="", audio_file=uploaded_file)

        # Display the transcription
        st.subheader("Transcription")
        st.write(transcription)
        
        # Initial prompt after transcription
        st.subheader("Let's Start!")
        st.write("Estou pronta! Por onde você quer começar?")

        # Text input for user to interact with Veronica
        user_input = st.text_input("Your message:", "")
        
        if user_input:
            response = veronica.invoke(user_input=user_input, audio_file=uploaded_file)
            st.subheader("Veronica's Response:")
            st.write(response)

if __name__ == "__main__":
    main()
