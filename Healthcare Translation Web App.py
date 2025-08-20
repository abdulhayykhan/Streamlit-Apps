import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

st.title("🩺 Healthcare Translation Web App")
st.write("Translate patient-provider conversations in real-time with multilingual support.")

# Map full names to language codes
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Arabic": "ar",
    "Hindi": "hi",
    "Urdu": "ur"
}

# Language selectors
input_lang_name = st.selectbox("Select Input Language:", list(languages.keys()))
output_lang_name = st.selectbox("Select Output Language:", list(languages.keys()))

input_lang = languages[input_lang_name]
output_lang = languages[output_lang_name]

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

            # Add Speak button
            if st.button("🔊 Speak Translation"):
                tts = gTTS(translated_text, lang=output_lang)
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(tmp_file.name)
                st.audio(tmp_file.name, format="audio/mp3")
