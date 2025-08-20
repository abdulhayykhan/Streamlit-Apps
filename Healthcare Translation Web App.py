import streamlit as st
from audiorecorder import audiorecorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
from io import BytesIO

st.set_page_config(page_title="Healthcare Translation Web App", layout="wide")
st.title("🩺 Healthcare Translation Web App")
st.caption("Real-time multilingual interpretation for patients and healthcare providers.")

# -----------------------
# Supported Languages (fixed for deep-translator)
# -----------------------
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",   # ✅ fixed
    "Arabic": "ar",
    "Hindi": "hi",
    "Urdu": "ur"
}

col_top1, col_top2, col_top3 = st.columns([1,1,1])
with col_top1:
    input_lang_name = st.selectbox("Input language", list(LANGUAGES.keys()), index=0)
with col_top2:
    output_lang_name = st.selectbox("Output language", list(LANGUAGES.keys()), index=1)
with col_top3:
    auto_translate = st.toggle("Auto-translate new audio", value=True)

input_lang = LANGUAGES[input_lang_name]
output_lang = LANGUAGES[output_lang_name]

# -----------------------
# Session state buffers
# -----------------------
if "orig_buffer" not in st.session_state:
    st.session_state.orig_buffer = []
if "tran_buffer" not in st.session_state:
    st.session_state.tran_buffer = []
if "last_audio_path" not in st.session_state:
    st.session_state.last_audio_path = None

def append_segments(orig_text: str):
    """Append original + translated segments to buffers."""
    orig_text = orig_text.strip()
    if not orig_text:
        return

    st.session_state.orig_buffer.append(orig_text)

    if auto_translate:
        translated = GoogleTranslator(source=input_lang, target=output_lang).translate(orig_text)
        st.session_state.tran_buffer.append(translated)

def transcribe_wav_file(filepath: str, lang: str) -> str:
    """Transcribe audio file using Google Speech Recognition."""
    r = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language=lang)
    except Exception:
        return ""

# -----------------------
# Layout: transcripts side-by-side (READ-ONLY)
# -----------------------
left, right = st.columns(2)
with left:
    st.subheader("🎤 Original Transcript")
    if st.session_state.orig_buffer:
        st.code("\n".join(st.session_state.orig_buffer), language="")
    else:
        st.info("No transcript yet.")
with right:
    st.subheader("🌍 Translated Transcript")
    if st.session_state.tran_buffer:
        st.code("\n".join(st.session_state.tran_buffer), language="")
    else:
        st.info("No translation yet.")

st.divider()

# -----------------------
# Microphone section
# -----------------------
st.subheader("Microphone Recording")
st.caption("Click **Record**, speak, then **Stop** to add a segment to transcripts.")

audio = audiorecorder("🎙️ Record", "⏹️ Stop")

if len(audio) > 0:
    # Play audio
    buf = BytesIO()
    audio.export(buf, format="wav")
    st.audio(buf.getvalue(), format="audio/wav")

    # Save temp file for SpeechRecognition
    wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(wav_file.name, format="wav")

    # Transcribe
    text = transcribe_wav_file(wav_file.name, input_lang)
    if text:
        append_segments(text)
        st.success("Audio transcribed" + (" & translated." if auto_translate else "."))
    else:
        st.warning("Could not transcribe audio.")

# -----------------------
# File upload (optional)
# -----------------------
st.subheader("Upload Audio")
uploaded = st.file_uploader("Upload .wav or .mp3", type=["wav", "mp3"])
if uploaded:
    st.audio(uploaded, format="audio/wav")
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded.type.split('/')[-1]}") as tmp:
        tmp.write(uploaded.read())
        tmp.flush()
        filepath = tmp.name

    text = transcribe_wav_file(filepath, input_lang)
    if text:
        append_segments(text)
        st.success("File transcribed" + (" & translated." if auto_translate else "."))
    else:
        st.warning("Could not process uploaded file.")

# -----------------------
# Manual text translation
# -----------------------
st.subheader("Manual Text (Optional)")
manual_text = st.text_area(f"Type {input_lang_name} text to translate", height=100, placeholder="Type here…")
if st.button("Translate Text"):
    if manual_text.strip():
        translated = GoogleTranslator(source=input_lang, target=output_lang).translate(manual_text.strip())
        st.session_state.orig_buffer.append(manual_text.strip())
        st.session_state.tran_buffer.append(translated)
        st.success("Text translated and appended.")
    else:
        st.info("Please enter some text.")

# -----------------------
# Speak button for latest translation
# -----------------------
st.subheader("Audio Playback")
if st.button("🔊 Speak Latest Translation"):
    if st.session_state.tran_buffer:
        to_speak = st.session_state.tran_buffer[-1]
        tts = gTTS(to_speak, lang=output_lang)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        st.session_state.last_audio_path = tmp.name
        st.audio(tmp.name, format="audio/mp3")
    else:
        st.info("No translated text yet.")

# -----------------------
# Download transcripts
# -----------------------
if st.session_state.orig_buffer or st.session_state.tran_buffer:
    transcript_text = "Original Transcript:\n" + "\n".join(st.session_state.orig_buffer) + "\n\n"
    transcript_text += "Translated Transcript:\n" + "\n".join(st.session_state.tran_buffer)

    st.download_button(
        label="📥 Download Transcript",
        data=transcript_text,
        file_name="transcript.txt",
        mime="text/plain"
    )

# -----------------------
# Clear transcripts
# -----------------------
st.divider()
if st.button("🧹 Clear Transcripts"):
    st.session_state.orig_buffer = []
    st.session_state.tran_buffer = []
    st.session_state.last_audio_path = None
    st.success("Transcripts cleared.")
