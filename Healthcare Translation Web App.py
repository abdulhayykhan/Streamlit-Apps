import streamlit as st
import openai
from gtts import gTTS
import tempfile

# 🔑 OpenAI API Key (set in Streamlit Secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🩺 Healthcare Translation Web App")
st.write("Real-time multilingual translation between patients and healthcare providers.")

# Language selectors
input_lang = st.selectbox("Select Input Language:", ["en", "es", "fr", "ur"])
output_lang = st.selectbox("Select Output Language:", ["en", "es", "fr", "ur"])

# Upload audio
audio_file = st.file_uploader("🎤 Upload an audio file", type=["mp3", "wav", "m4a"])

original_text = ""
translated_text = ""

if audio_file:
    # 🔊 Transcribe audio with OpenAI Whisper
    with st.spinner("Transcribing audio..."):
        transcript = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        original_text = transcript.text
        st.subheader("📝 Original Transcript")
        st.text_area("Transcript", original_text, height=100)

    # 🌍 Translate text with GPT
    if st.button("Translate"):
        with st.spinner("Translating..."):
            prompt = f"Translate this healthcare conversation from {input_lang} to {output_lang}: {original_text}"
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a medical translation assistant."},
                          {"role": "user", "content": prompt}]
            )
            translated_text = response.choices[0].message.content
            st.subheader("🌍 Translated Transcript")
            st.text_area("Translation", translated_text, height=100)

            # 🔊 Generate speech from translated text
            tts = gTTS(translated_text, lang=output_lang)
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp_file.name)
            st.audio(tmp_file.name, format="audio/mp3")
