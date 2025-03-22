import streamlit as st
import requests

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

st.title("🤣 Random Joke Generator 😂")
st.write("Click the button below to get a random joke!")

if st.button("Get a Joke!"):
    setup, delivery = get_joke()
    st.write("**" + setup + "**")
    st.write("😆 " + delivery)
