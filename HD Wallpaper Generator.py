import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- Unsplash API Access Key ---
UNSPLASH_ACCESS_KEY = "OXzfR4GnNkUzaFbPpwVIfTVLdNwAg2c73GuwueB6ick"

# --- Streamlit UI ---
st.set_page_config(page_title="HD Wallpaper Generator", page_icon="🌄", layout="wide")
st.title("🖼️ HD Wallpaper Generator")
st.markdown("Generate stunning HD wallpapers based on your interests. No quotes, just pure visuals!")

# --- Popular Categories ---
popular_categories = [
    "Nature", "Space", "Abstract", "City", "Mountains", "Ocean", "Animals", "Cars", "Minimal", "Technology"
]

category = st.selectbox("Choose a wallpaper category or type your own keyword:", options=popular_categories + ["Custom..."])

if category == "Custom...":
    query = st.text_input("Enter your custom keyword:")
else:
    query = category

generate = st.button("🎨 Generate Wallpaper")

# --- Fetch image from Unsplash ---
def fetch_hd_wallpaper(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&client_id={UNSPLASH_ACCESS_KEY}"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    
    image_url = data['urls']['full']
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    return image, image_url

# --- Display image ---
if generate and query:
    with st.spinner("Fetching a beautiful wallpaper..."):
        try:
            image, image_url = fetch_hd_wallpaper(query)
            st.image(image, caption=f"Wallpaper for: {query}", use_column_width=True)
            st.success("HD Wallpaper generated successfully!")

            # Download button
            img_bytes = BytesIO()
            image.save(img_bytes, format='JPEG')
            st.download_button(
                label="📥 Download Wallpaper",
                data=img_bytes.getvalue(),
                file_name=f"{query.lower().replace(' ', '_')}_wallpaper.jpg",
                mime="image/jpeg"
            )
        except Exception as e:
            st.error("❌ Failed to generate wallpaper. Please try again.")
            st.exception(e)

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ by Abdul Hayy Khan using Streamlit + Unsplash API")
