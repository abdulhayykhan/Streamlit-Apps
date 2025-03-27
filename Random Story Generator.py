import streamlit as st
import random
import time

def generate_story(keyword):
    templates = [
        f"Once upon a time, in a faraway land, there was a {keyword} that changed everything!",
        f"In a world where {keyword} ruled, one hero stood against the odds.",
        f"Deep in the heart of the jungle, a mysterious {keyword} was discovered by an explorer.",
        f"Every night, the {keyword} would come to life, telling secrets of the past.",
        f"Legends spoke of a powerful {keyword} that could grant any wish."
    ]
    return random.choice(templates)

# Streamlit UI Setup
st.set_page_config(page_title="Story Generator", page_icon="📖")
st.title("📖 Random Story Generator ✨")
st.markdown("### Enter a keyword and create an exciting story!")

# Input and button layout
keyword = st.text_input("🔍 Enter a keyword for your story:")
col1, col2 = st.columns([1,1])

if col1.button("Generate Story 📝"):
    if keyword:
        with st.spinner("Creating your magical story..."):
            time.sleep(2)
            story = generate_story(keyword)
        
        st.success("Here's your story! 🎉")
        st.markdown(f"📖 **{story}**")
        st.balloons()
    else:
        st.warning("⚠️ Please enter a keyword to generate a story.")

if col2.button("Clear ❌"):
    st.experimental_rerun()
