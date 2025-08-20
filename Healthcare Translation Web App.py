import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

st.title("🩺 Healthcare Translation Web App (Free Version)")
st.write("Translate patient-provider conversations with free APIs.")

# Language options
input_lang = st.selectbox("Select Input Language:", ["en", "es", "fr", "ur"])
output_lang = st.selectbox("Select Output Language:", ["en", "es", "fr", "ur"])

# File upload
audio_file = st.file_uploader("🎤 Upload an audio file", type=["wav", "mp3"])

original_text = ""
translated_text = ""

if audio_file:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            st.info("Transcribing...")
            original_text = recognizer.recognize_google(audio_data, language=input_lang)
            st.subheader("📝 Original Transcript")
            st.text_area("Transcript", original_text, height=100)
        except:
            st.error("Speech recognition failed. Try another file or language.")

    if original_text:
        if st.button("Translate"):
            st.info("Translating...")
            translated_text = GoogleTranslator(source=input_lang, target=output_lang).translate(original_text)
            st.subheader("🌍 Translated Transcript")
            st.text_area("Translation", translated_text, height=100)

            # Text-to-Speech
            tts = gTTS(translated_text, lang=output_lang)
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp_file.name)
            st.audio(tmp_file.name, format="audio/mp3")
