import streamlit as st
import requests
import time

# Function to get a joke from JokeAPI
def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any?type=twopart"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            joke_data = response.json()
            setup = joke_data.get("setup", "No joke found.")
            delivery = joke_data.get("delivery", "")
            return setup, delivery
        else:
            return "Error fetching joke", ""
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", ""

# Configure page
st.set_page_config(page_title="Random Joke Generator", page_icon="🤣")

# Page title and intro
st.title("🤣 Random Joke Generator")
st.write("Click the button below to get a random joke and have a good laugh!")

st.markdown("---")

# Button interaction
if st.button("Get a Joke!"):
    with st.spinner("Fetching a hilarious joke for you..."):
        time.sleep(1.5)
        setup, delivery = get_joke()

    # Show joke using plain text for mobile compatibility
    st.success("Here’s your joke:")
    st.text(setup)
    time.sleep(1)
    st.text(delivery)

    st.markdown("---")
    st.caption("Want another joke? Just click the button again! 😄")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
