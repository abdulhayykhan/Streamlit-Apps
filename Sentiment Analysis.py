import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import subprocess

try:
    import nltk
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "nltk"])
    import nltk

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

st.set_page_config(page_title="Sentiment Analyzer", page_icon="😊", layout="centered")
st.title("🔍 Sentiment Analysis App")
st.markdown("### Discover the emotion behind your words! ✨")

user_input = st.text_area("📝 Enter your text below:", "I love AI and Machine Learning!")

if st.button("🚀 Analyze Sentiment"):
    sentiment_scores = sia.polarity_scores(user_input)
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.05:
        sentiment = "😊 Positive"
        color = "green"
    elif compound_score <= -0.05:
        sentiment = "😞 Negative"
        color = "red"
    else:
        sentiment = "😐 Neutral"
        color = "gray"
    
    st.markdown(f"## <span style='color:{color};'>{sentiment}</span>", unsafe_allow_html=True)
    st.json(sentiment_scores)
    
    st.balloons() if sentiment == "😊 Positive" else st.snow() if sentiment == "😞 Negative" else None
