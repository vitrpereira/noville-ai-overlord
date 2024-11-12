import streamlit as st
from openai_model import OpenAiModel
from veronica.veronica import Veronica

st.title("Speech Transcription App")
st.write("Upload an audio file, and the app will transcribe it.")

uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    st.write("Audio file uploaded successfully!")
    
    transcription = OpenAiModel().transcribe_audio(uploaded_file)

    st.subheader("Aqui está a transacrição do seu áudio:")
    st.write(transcription)
else:
    st.write("Please upload an audio file to get started.")
