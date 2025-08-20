import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import openai
import tempfile
import os

# 🔑 Set OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🩺 Healthcare Translation Web App")
st.write("Real-time multilingual translation between patients and healthcare providers.")

# Language selection
input_lang = st.selectbox("Select Input Language:", ["en", "es", "fr", "ur"])
output_lang = st.selectbox("Select Output Language:", ["en", "es", "fr", "ur"])

# Speech recognition
st.header("🎤 Record or Upload Audio")
recognizer = sr.Recognizer()
audio_file = st.file_uploader("Upload a .wav file", type=["wav"])

original_text = ""
if audio_file is not None:
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            original_text = recognizer.recognize_google(audio_data, language=input_lang)
            st.subheader("📝 Original Transcript")
            st.text_area("Input Transcript", original_text, height=100)
        except:
            st.error("Speech recognition failed. Try another file.")

# Translation with OpenAI
translated_text = ""
if original_text:
    if st.button("Translate"):
        prompt = f"Translate the following healthcare conversation from {input_lang} to {output_lang}: {original_text}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a medical translation assistant."},
                      {"role": "user", "content": prompt}]
        )
        translated_text = response["choices"][0]["message"]["content"]

        st.subheader("🌍 Translated Transcript")
        st.text_area("Translated Text", translated_text, height=100)

        # Generate speech from translated text
        tts = gTTS(translated_text, lang=output_lang)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        st.audio(tmp_file.name, format="audio/mp3")
