import streamlit as st
import requests
import time

def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any?type=twopart"
    response = requests.get(url)
    if response.status_code == 200:
        joke_data = response.json()
        setup = joke_data.get("setup", "No joke found.")
        delivery = joke_data.get("delivery", "")
        return setup, delivery
    else:
        return "Error fetching joke", ""

st.set_page_config(page_title="Random Joke Generator", page_icon="🤣")
st.title("🤣 Random Joke Generator 😂")
st.write("Click the button below to get a random joke and have a good laugh!")

# Adding a fun emoji separator
st.markdown("---")

if st.button("Get a Joke! 😂"):
    with st.spinner("Fetching a hilarious joke for you..."):
        time.sleep(1.5)  # Simulating a small delay for better engagement
        setup, delivery = get_joke()
    
    st.success("Here’s your joke:")
    st.write(f"**{setup}**")
    time.sleep(1)  # Small pause before punchline
    st.write(f"😆 **{delivery}**")
    
    # Adding an option to get another joke
    st.markdown("---")
    st.write("Want another joke? Click the button again! 🎭")
