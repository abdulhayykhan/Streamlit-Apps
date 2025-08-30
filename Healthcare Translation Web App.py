import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from audiorecorder import audiorecorder
import tempfile
import os

st.set_page_config(page_title="Healthcare Translation Web App with Generative AI", layout="wide", page_icon="🩺")
st.title("🩺 Healthcare Translation Web App")
st.caption("Real-time multilingual communication between patients and healthcare providers.")

# -----------------------
# Supported Languages (translation + speech)
# -----------------------
LANGS = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Arabic": "ar",
    "Hindi": "hi",
    "Urdu": "ur",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
}

# gTTS language mapping (fallback to en if not supported)
# (gTTS supports many; these are safe defaults)
TTS_LANG = {
    "zh-CN": "zh-CN",
    "zh-TW": "zh-TW",
    "en": "en", "es": "es", "fr": "fr", "de": "de",
    "ar": "ar", "hi": "hi", "ur": "ur", "ja": "ja",
    "ko": "ko", "ru": "ru", "pt": "pt", "it": "it",
}

# -----------------------
# Session State
# -----------------------
def ensure_state():
    st.session_state.setdefault("orig_buffer", [])
    st.session_state.setdefault("tran_buffer", [])
    # keys used to reset widgets on demand
    st.session_state.setdefault("uploader_key", 0)
    st.session_state.setdefault("rec_key", 0)

ensure_state()

col_lang1, col_lang2 = st.columns(2)
with col_lang1:
    in_name = st.selectbox("🎤 Input language", list(LANGS.keys()), index=0)
with col_lang2:
    out_name = st.selectbox("🌍 Output language", list(LANGS.keys()), index=1)

IN_CODE = LANGS[in_name]
OUT_CODE = LANGS[out_name]

# -----------------------
# Helpers
# -----------------------
def convert_to_wav(input_path_or_file) -> str:
    """Convert any audio (mp3/wav/etc.) to PCM WAV and return path."""
    audio = AudioSegment.from_file(input_path_or_file)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(tmp.name, format="wav")
    return tmp.name

def transcribe_wav(filepath: str, lang_code: str) -> str:
    r = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language=lang_code)
    except sr.UnknownValueError:
        return "(Could not understand audio)"
    except sr.RequestError:
        return "(Speech API unavailable)"
    except Exception as e:
        return f"(Transcription error: {e})"

def translate_text(text: str, src: str, tgt: str) -> str:
    try:
        return GoogleTranslator(source=src, target=tgt).translate(text)
    except Exception as e:
        return f"(Translation error: {e})"

def tts(text: str, lang_code: str) -> str:
    code = TTS_LANG.get(lang_code, "en")
    try:
        t = gTTS(text=text, lang=code)
        out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        t.save(out.name)
        return out.name
    except Exception as e:
        st.warning(f"TTS not available for {lang_code}. Using English. ({e})")
        t = gTTS(text=text, lang="en")
        out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        t.save(out.name)
        return out.name

def save_uploaded_to_temp(uploaded) -> str:
    ext = ".bin"
    if uploaded.type:
        ext = "." + uploaded.type.split("/")[-1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    tmp.write(uploaded.getvalue())
    tmp.flush()
    return tmp.name

# -----------------------
# Layout: transcripts (read-only)
# -----------------------
c1, c2 = st.columns(2)
with c1:
    st.subheader("🎤 Original Transcript")
    st.text_area("Input", value="\n".join(st.session_state.orig_buffer), height=220, disabled=True, key="orig_view")
with c2:
    st.subheader("🌍 Translated Transcript")
    st.text_area("Output", value="\n".join(st.session_state.tran_buffer), height=220, disabled=True, key="tran_view")

st.divider()

# -----------------------
# Mic Recorder
# -----------------------
st.subheader("🎙️ Record Speech")
mic_audio = audiorecorder("🔴 Record", "⏹️ Stop", key=f"rec_{st.session_state.rec_key}")

if len(mic_audio) > 0:
    # show playback
    buf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    mic_audio.export(buf.name, format="wav")
    st.audio(buf.name)

    # transcribe & translate
    text = transcribe_wav(buf.name, IN_CODE)
    st.session_state.orig_buffer.append(text)
    st.session_state.tran_buffer.append(translate_text(text, IN_CODE, OUT_CODE))

    # reset recorder so it doesn't re-append after rerun
    st.session_state.rec_key += 1
    st.rerun()

# -----------------------
# File Uploader
# -----------------------
st.subheader("📂 Upload Audio File")
uploaded = st.file_uploader(
    "Upload audio (WAV/MP3 supported)",
    type=["wav", "mp3", "m4a", "ogg"],
    key=f"uploader_{st.session_state.uploader_key}"
)

if uploaded is not None:
    try:
        src_path = save_uploaded_to_temp(uploaded)
        wav_path = convert_to_wav(src_path)
        text = transcribe_wav(wav_path, IN_CODE)
        st.session_state.orig_buffer.append(text)
        st.session_state.tran_buffer.append(translate_text(text, IN_CODE, OUT_CODE))
    finally:
        # reset uploader so the same file won't reprocess on rerun
        st.session_state.uploader_key += 1
        st.rerun()

# -----------------------
# Speak latest translation
# -----------------------
st.subheader("🔊 Audio Playback")
if st.button("Speak Latest Translation"):
    if st.session_state.tran_buffer:
        mp3_path = tts(st.session_state.tran_buffer[-1], OUT_CODE)
        st.audio(mp3_path, format="audio/mp3")
    else:
        st.info("No translated text available.")

# -----------------------
# Download transcripts
# -----------------------
if st.session_state.orig_buffer or st.session_state.tran_buffer:
    transcript = (
        "Original Transcript:\n" + "\n".join(st.session_state.orig_buffer) + "\n\n" +
        "Translated Transcript:\n" + "\n".join(st.session_state.tran_buffer)
    )
    st.download_button("📥 Download Transcript", transcript, file_name="transcript.txt", mime="text/plain")

st.divider()

# -----------------------
# Clear Transcripts (robust reset)
# -----------------------
if st.button("🧹 Clear Transcripts"):
    st.session_state.orig_buffer = []
    st.session_state.tran_buffer = []
    # also reset widget keys so uploader/recorder are cleared
    st.session_state.uploader_key += 1
    st.session_state.rec_key += 1
    st.rerun()
