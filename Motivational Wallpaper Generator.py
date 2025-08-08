import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from io import BytesIO
import textwrap

st.set_page_config(page_title="Motivational Wallpaper Generator", page_icon="🌄")
st.title("🌄 Motivational Wallpaper Generator")
st.write("Click below to generate a random motivational wallpaper!")

# --- Fetch motivational quote ---
def fetch_quote():
    try:
        res = requests.get("https://api.quotable.io/random?tags=inspirational|motivational")
        if res.status_code == 200:
            data = res.json()
            return f'"{data["content"]}"\n\n— {data["author"]}'
    except:
        return "Stay positive, work hard, and make it happen!"

# --- Fetch random image from safe source ---
def fetch_image():
    url = "https://picsum.photos/800/600"
    try:
        res = requests.get(url)
        img = Image.open(BytesIO(res.content))
        return img
    except UnidentifiedImageError:
        return None

# --- Generate final wallpaper image ---
def generate_wallpaper(quote_text):
    bg = fetch_image()
    if bg is None:
        st.error("❌ Failed to load image. Please try again.")
        return None

    bg = bg.convert("RGB")
    draw = ImageDraw.Draw(bg)

    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    wrapped = textwrap.wrap(quote_text, width=40)
    W, H = bg.size
    text_height = len(wrapped) * 35
    y_text = (H - text_height) // 2

    for line in wrapped:
        # Use textbbox instead of textsize
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((W - w) / 2, y_text), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
        y_text += 35

    return bg

# --- Generate Wallpaper Button ---
if st.button("✨ Generate Wallpaper"):
    with st.spinner("Generating..."):
        quote = fetch_quote()
        wallpaper = generate_wallpaper(quote)

        if wallpaper:
            st.image(wallpaper, caption="🌟 Your Motivational Wallpaper", use_column_width=True)

            buf = BytesIO()
            wallpaper.save(buf, format="JPEG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Download Wallpaper",
                data=byte_im,
                file_name="motivational_wallpaper.jpg",
                mime="image/jpeg"
            )
