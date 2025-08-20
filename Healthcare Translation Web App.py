import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration

st.set_page_config(page_title="Healthcare Translation Web App", layout="wide")

st.title("🩺 Healthcare Translation Web App")
st.write("Real-time multilingual translation for patients and healthcare providers.")

# Language options
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

input_lang_name = st.selectbox("Select Input Language:", list(languages.keys()))
output_lang_name = st.selectbox("Select Output Language:", list(languages.keys()))

input_lang = languages[input_lang_name]
output_lang = languages[output_lang_name]

col1, col2 = st.columns(2)
col1.subheader("🎤 Original Transcript")
col2.subheader("🌍 Translated Transcript")

# Shared variables
st.session_state["original_text"] = ""
st.session_state["translated_text"] = ""

# 📌 Microphone Live Transcription
rtc_config = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame):
        audio_data = frame.to_ndarray().astype("int16")
        audio = sr.AudioData(audio_data.tobytes(), frame.sample_rate, 2)
        try:
            text = self.recognizer.recognize_google(audio, language=input_lang)
            st.session_state["original_text"] = text
            st.session_state["translated_text"] = GoogleTranslator(source=input_lang, target=output_lang).translate(text)
        except:
            pass
        return frame

webrtc_streamer(
    key="mic",
    mode="recvonly",   
    audio_processor_factory=AudioProcessor,
    rtc_configuration=rtc_config,
    media_stream_constraints={"audio": True, "video": False},
)

# Display transcripts (auto-updating)
col1.text_area("Input", st.session_state.get("original_text", ""), height=200)
col2.text_area("Translation", st.session_state.get("translated_text", ""), height=200)

# 📂 File Upload (alternative input)
st.header("Or Upload an Audio File")
audio_file = st.file_uploader("Upload .wav or .mp3", type=["wav", "mp3"])

if audio_file:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            original_text = recognizer.recognize_google(audio_data, language=input_lang)
            translated_text = GoogleTranslator(source=input_lang, target=output_lang).translate(original_text)
            col1.text_area("Uploaded Transcript", original_text, height=100)
            col2.text_area("Uploaded Translation", translated_text, height=100)

            if st.button("🔊 Speak Uploaded Translation"):
                tts = gTTS(translated_text, lang=output_lang)
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(tmp_file.name)
                st.audio(tmp_file.name, format="audio/mp3")
        except:
            st.error("Could not process audio file.")
