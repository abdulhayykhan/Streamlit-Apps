import streamlit as st
import random
import time

def generate_story(keyword):
    characters = ["a brave knight", "a young scientist", "a curious explorer", "a wise old wizard", "a fearless adventurer"]
    settings = ["a mystical forest", "an ancient kingdom", "a futuristic city", "a hidden underground cave", "a floating island"]
    conflicts = ["discovered a powerful secret", "was given a dangerous quest", "found an ancient relic", "had to save their people", "uncovered a hidden truth"]
    resolutions = ["and changed the world forever", "and became a legend", "and found their true purpose", "and uncovered a new mystery", "and brought peace to the land"]
    
    character = random.choice(characters)
    setting = random.choice(settings)
    conflict = random.choice(conflicts)
    resolution = random.choice(resolutions)
    
    story = f"Once upon a time, in {setting}, {character} who loved {keyword} {conflict}. They faced many challenges, but in the end, they persevered {resolution}."
    return story

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
