import streamlit as st
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_quote():
    url = "https://api.quotable.io/random"
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data["content"], data["author"]
        else:
            return "Failed to fetch a quote. Try again!", "Unknown"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", "Unknown"

st.set_page_config(page_title="Quote of the Day", page_icon="📜")
st.title("📜 Quote of the Day Generator")

if st.button("Generate Quote 🎯"):
    with st.spinner("Fetching an inspiring quote..."):
        quote, author = fetch_quote()
        st.write(f"**❝ {quote} ❞**")
        st.write(f"— *{author}*")

# Footer
st.markdown("---")
st.write("Made with ❤️ using Streamlit")
