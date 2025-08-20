import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from audiorecorder import audiorecorder
import tempfile

# -----------------------
# Helper Functions
# -----------------------

def convert_to_wav(input_file):
    """Convert any audio file (mp3, wav, etc.) to PCM WAV format."""
    audio = AudioSegment.from_file(input_file)
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_wav.name, format="wav")
    return temp_wav.name

def transcribe_audio(filepath, lang="en"):
    """Transcribe WAV audio file to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        return "(Could not understand audio)"
    except sr.RequestError:
        return "(API unavailable)"

def translate_text(text, src_lang, tgt_lang):
    """Translate text using Google Translator (deep-translator)."""
    try:
        return GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)
    except Exception as e:
        return f"(Translation error: {str(e)})"

def speak_text(text, lang="en"):
    """Convert text to speech and return audio path."""
    tts = gTTS(text=text, lang=lang)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

# -----------------------
# Streamlit App
# -----------------------
st.set_page_config(page_title="Healthcare Translation Web App", layout="wide")

st.title("🩺 Healthcare Translation Web App")
st.write("Real-time multilingual communication between patients and healthcare providers.")

# Language selection
langs = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Arabic": "ar",
    "Hindi": "hi",
    "Urdu": "ur"
}

input_lang_name = st.selectbox("🎤 Input Language", list(langs.keys()))
output_lang_name = st.selectbox("🌍 Output Language", list(langs.keys()))

input_lang = langs[input_lang_name]
output_lang = langs[output_lang_name]

# Transcript buffers
if "orig_buffer" not in st.session_state:
    st.session_state.orig_buffer = []
if "tran_buffer" not in st.session_state:
    st.session_state.tran_buffer = []

# -----------------------
# Mic Recorder
# -----------------------
st.subheader("🎙️ Record Speech")
audio = audiorecorder("🔴 Record", "⏹️ Stop")

if len(audio) > 0:
    # Save mic audio to temp file
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_audio.name, format="wav")
    # Transcribe
    text = transcribe_audio(temp_audio.name, input_lang)
    st.session_state.orig_buffer.append(text)
    # Translate
    translated = translate_text(text, input_lang, output_lang)
    st.session_state.tran_buffer.append(translated)

# -----------------------
# File Uploader
# -----------------------
st.subheader("📂 Upload Audio File")
uploaded_file = st.file_uploader("Upload (WAV/MP3 supported)", type=["wav", "mp3"])

if uploaded_file is not None:
    wav_path = convert_to_wav(uploaded_file)
    text = transcribe_audio(wav_path, input_lang)
    st.session_state.orig_buffer.append(text)
    translated = translate_text(text, input_lang, output_lang)
    st.session_state.tran_buffer.append(translated)

# -----------------------
# Display transcripts
# -----------------------
col1, col2 = st.columns(2)
with col1:
    st.subheader("Original Transcript")
    st.text_area("Input Speech", value="\n".join(st.session_state.orig_buffer), height=200, disabled=True)
with col2:
    st.subheader("Translated Transcript")
    st.text_area("Output Speech", value="\n".join(st.session_state.tran_buffer), height=200, disabled=True)

# -----------------------
# Playback
# -----------------------
if st.session_state.tran_buffer:
    last_translation = st.session_state.tran_buffer[-1]
    audio_path = speak_text(last_translation, output_lang)
    st.audio(audio_path)

# -----------------------
# Download transcript
# -----------------------
if st.session_state.orig_buffer or st.session_state.tran_buffer:
    transcript_text = "Original Transcript:\n" + "\n".join(st.session_state.orig_buffer) + "\n\n"
    transcript_text += "Translated Transcript:\n" + "\n".join(st.session_state.tran_buffer)
    st.download_button("📥 Download Transcript", transcript_text, file_name="transcript.txt")

# -----------------------
# Clear
# -----------------------
if st.button("🧹 Clear Transcripts"):
    st.session_state.orig_buffer = []
    st.session_state.tran_buffer = []
