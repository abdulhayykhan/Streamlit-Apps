import streamlit as st
import requests

# --- Config ---
NASA_API_KEY = "7v7A8UtXpqFbxch10Zq43xsgIXXxU7pzHVRzAg23"
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

# --- Function to get APOD data ---
def get_apod():
    params = {
        "api_key": NASA_API_KEY
    }
    try:
        response = requests.get(NASA_APOD_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Exception occurred: {str(e)}"}

# --- Streamlit Page Setup ---
st.set_page_config(page_title="NASA APOD Viewer", page_icon="🪐")
st.title("🌌 NASA Astronomy Picture of the Day")
st.caption("Powered by NASA Open APIs")

st.markdown("---")

# --- Load and Display Data ---
apod = get_apod()

if "error" in apod:
    st.error(apod["error"])
else:
    st.subheader(apod.get("title", "Untitled"))
    st.write(f"📅 Date: `{apod.get('date', 'N/A')}`")

    if apod.get("media_type") == "image":
        st.image(apod.get("url"), caption="📸 Credit: " + apod.get("copyright", "NASA"), use_column_width=True)
    elif apod.get("media_type") == "video":
        st.video(apod.get("url"))
    else:
        st.warning("Unknown media type received.")

    st.markdown("---")
    st.write(apod.get("explanation", "No explanation available."))

# --- Footer ---
st.markdown("---")
st.caption("Made with 🚀 by Abdul Hayy Khan using Streamlit + NASA API")
