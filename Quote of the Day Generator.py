import streamlit as st
import requests
import urllib3

# Disable SSL warnings (only for development)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to fetch quote
def fetch_quote():
    url = "https://api.quotable.io/random"
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data["content"], data["author"]
        else:
            return "Failed to fetch a quote. Please try again.", "Unknown"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", "Unknown"

# Page configuration
st.set_page_config(page_title="Quote of the Day", page_icon="📜")

# Title
st.title("📜 Quote of the Day Generator")

# Button to generate quote
if st.button("Generate Quote 🎯"):
    with st.spinner("Fetching an inspiring quote..."):
        quote, author = fetch_quote()
        
        # Displaying quote in a simple and safe format
        st.text(f"\"{quote}\"")
        st.markdown(f"**— {author}**")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
