import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from io import BytesIO
import textwrap
import os

st.set_page_config(page_title="Motivational Wallpaper Generator", page_icon="🌄")
st.title("🌄 Motivational Wallpaper Generator")
st.write("Click below to generate a beautiful motivational wallpaper!")

# --- Fetch motivational quote ---
def fetch_quote():
    try:
        res = requests.get("https://api.quotable.io/random?tags=inspirational|motivational")
        if res.status_code == 200:
            data = res.json()
            return f'"{data["content"]}"\n\n— {data["author"]}'
    except:
        return "Stay positive, work hard, and make it happen!"

# --- Fetch image ---
def fetch_image():
    url = "https://picsum.photos/800/600"
    try:
        res = requests.get(url)
        img = Image.open(BytesIO(res.content))
        return img
    except UnidentifiedImageError:
        return None

# --- Generate wallpaper ---
def generate_wallpaper(quote_text):
    bg = fetch_image()
    if bg is None:
        st.error("❌ Failed to load image. Please try again.")
        return None

    bg = bg.convert("RGB")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)

    # Add overlay for readability
    overlay = Image.new('RGBA', bg.size, (0, 0, 0, 130))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)

    # Try loading stylish font
    try:
        font_path = "Lobster-Regular.ttf"
        font = ImageFont.truetype(font_path, 44)
    except:
        font = ImageFont.truetype("arial.ttf", 40)

    # Wrap and position text
    wrapped = textwrap.wrap(quote_text, width=35)
    line_height = 55
    total_height = len(wrapped) * line_height
    y_text = (H - total_height) // 2

    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        draw.text((x, y_text), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
        y_text += line_height

    return bg

# --- UI ---
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
