import streamlit as st
from st_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import time

st.set_page_config(page_title="Healthcare Translation Web App", layout="wide")
st.title("🩺 Healthcare Translation Web App")
st.caption("Real-time multilingual interpretation for patients and healthcare providers.")

# -----------------------
# Language map (expandable)
# -----------------------
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
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
    st.session_state.orig_buffer = []  # list of original transcript segments
if "tran_buffer" not in st.session_state:
    st.session_state.tran_buffer = []  # list of translated transcript segments
if "last_translated_text" not in st.session_state:
    st.session_state.last_translated_text = ""

def append_segments(orig_text: str):
    """Append original + translated segments to buffers."""
    orig_text = orig_text.strip()
    if not orig_text:
        return

    st.session_state.orig_buffer.append(orig_text)

    # Translate immediately if toggle is on
    if auto_translate:
        translated = GoogleTranslator(source=input_lang, target=output_lang).translate(orig_text)
        st.session_state.tran_buffer.append(translated)
        st.session_state.last_translated_text = translated

def transcribe_wav_bytes(wav_bytes: bytes, lang: str) -> str:
    """Transcribe WAV/MP3 bytes using Google Speech Recognition via speech_recognition."""
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(wav_bytes)
        tmp.flush()
        tmp_path = tmp.name
    with sr.AudioFile(tmp_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language=lang)
    except Exception:
        return ""

# -----------------------
# Layout: transcripts side-by-side
# -----------------------
left, right = st.columns(2)
with left:
    st.subheader("🎤 Original Transcript")
    st.text_area("Live Input", value="\n".join(st.session_state.orig_buffer), height=260, key="orig_textarea")
with right:
    st.subheader("🌍 Translated Transcript")
    st.text_area("Live Output", value="\n".join(st.session_state.tran_buffer), height=260, key="tran_textarea")

st.divider()

# -----------------------
# Microphone section
# -----------------------
st.subheader("Microphone")
st.caption("Click **Start Recording**, speak, then **Stop Recording** to append a segment to the live transcript.")

audio_dict = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    just_once=False,               # allow multiple recordings in one session
    use_container_width=True,
    format="wav"                   # returns bytes in WAV
)

if audio_dict and audio_dict.get("bytes"):
    st.audio(audio_dict["bytes"], format="audio/wav")
    with st.status("Processing microphone audio...", expanded=False):
        text = transcribe_wav_bytes(audio_dict["bytes"], input_lang)
        if text:
            append_segments(text)
            st.success("Segment transcribed" + (" & translated." if auto_translate else "."))
        else:
            st.warning("Could not understand the audio. Try speaking clearly or check language selection.")

# -----------------------
# File upload (optional)
# -----------------------
st.subheader("Upload Audio")
uploaded = st.file_uploader("Upload .wav or .mp3", type=["wav", "mp3"])
if uploaded:
    st.audio(uploaded, format=f"audio/{uploaded.type.split('/')[-1]}")
    with st.status("Transcribing uploaded audio...", expanded=False):
        text = transcribe_wav_bytes(uploaded.read(), input_lang)
        if text:
            append_segments(text)
            st.success("File transcribed" + (" & translated." if auto_translate else "."))
        else:
            st.warning("Could not process the uploaded audio.")

# -----------------------
# Manual translate box (optional typing)
# -----------------------
st.subheader("Manual Text (optional)")
manual_text = st.text_area(f"Type {input_lang_name} text to translate", height=120, placeholder="Type here…")
c1, c2 = st.columns([1,3])
with c1:
    if st.button("Translate Text"):
        if manual_text.strip():
            translated = GoogleTranslator(source=input_lang, target=output_lang).translate(manual_text.strip())
            st.session_state.orig_buffer.append(manual_text.strip())
            st.session_state.tran_buffer.append(translated)
            st.session_state.last_translated_text = translated
            st.success("Text translated and appended.")
        else:
            st.info("Please enter some text.")

# -----------------------
# Speak button for latest translation
# -----------------------
st.subheader("Audio Playback")
speak_col1, speak_col2 = st.columns([1, 4])
with speak_col1:
    if st.button("🔊 Speak Latest Translation"):
        if st.session_state.tran_buffer:
            to_speak = st.session_state.tran_buffer[-1]
            with st.spinner("Generating audio…"):
                tts = gTTS(to_speak, lang=output_lang)
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(tmp.name)
                st.session_state.last_audio_path = tmp.name
        else:
            st.info("No translated text yet.")
with speak_col2:
    if "last_audio_path" in st.session_state:
        st.audio(st.session_state.last_audio_path, format="audio/mp3")

# -----------------------
# Utilities
# -----------------------
st.divider()
u1, u2, u3 = st.columns(3)
with u1:
    if st.button("Clear Transcripts"):
        st.session_state.orig_buffer = []
        st.session_state.tran_buffer = []
        st.session_state.last_translated_text = ""
        st.session_state.pop("last_audio_path", None)
with u2:
    st.caption("Tip: If recognition is off, re-check language selections and try shorter segments.")
with u3:
    st.caption("Note: Accuracy for medical terminology may vary with this stack.")
