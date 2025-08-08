import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap

# --- Config ---
st.set_page_config(page_title="Motivational Wallpaper Generator", page_icon="🌄")
st.title("🌄 Motivational Wallpaper Generator")
st.write("Click below to generate a random motivational wallpaper!")

# --- Function to fetch quote ---
def fetch_quote():
    try:
        res = requests.get("https://api.quotable.io/random?tags=inspirational|motivational")
        if res.status_code == 200:
            data = res.json()
            return f'"{data["content"]}"\n\n— {data["author"]}'
    except:
        return "Stay positive, work hard, and make it happen!"

# --- Function to fetch image ---
def fetch_image():
    # Nature-based high-quality image from Unsplash
    image_url = "https://source.unsplash.com/featured/800x600?nature,landscape"
    res = requests.get(image_url)
    return Image.open(BytesIO(res.content))

# --- Overlay text on image ---
def generate_wallpaper(quote_text):
    bg = fetch_image().convert("RGB")
    draw = ImageDraw.Draw(bg)

    # Use system font (more consistent across platforms)
    try:
        font = ImageFont.truetype("arial.ttf", size=28)
    except:
        font = ImageFont.load_default()

    # Word-wrap the quote to fit nicely
    wrapped = textwrap.wrap(quote_text, width=40)

    W, H = bg.size
    text_height = len(wrapped) * 35
    y_text = (H - text_height) // 2

    for line in wrapped:
        w, h = draw.textsize(line, font=font)
        draw.text(((W - w) / 2, y_text), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
        y_text += 35

    return bg

# --- Button ---
if st.button("✨ Generate Wallpaper"):
    with st.spinner("Creating your motivational wallpaper..."):
        quote = fetch_quote()
        wallpaper = generate_wallpaper(quote)

        st.image(wallpaper, caption="🌟 Your Motivational Wallpaper", use_column_width=True)

        # Save to buffer
        buf = BytesIO()
        wallpaper.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Download Wallpaper",
            data=byte_im,
            file_name="motivational_wallpaper.jpg",
            mime="image/jpeg"
        )
