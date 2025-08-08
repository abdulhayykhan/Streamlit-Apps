import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap

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
    except:
        return None

# --- Generate wallpaper ---
def generate_wallpaper(quote_text):
    bg = fetch_image()
    if bg is None:
        st.error("❌ Failed to load image. Please try again.")
        return None

    bg = bg.convert("RGB")
    W, H = bg.size

    # Add transparent overlay for contrast
    overlay = Image.new('RGBA', bg.size, (0, 0, 0, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)

    # Use scalable built-in font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_size = 48
    font = ImageFont.truetype(font_path, font_size)

    # Wrap text based on image width
    max_chars_per_line = int(W / (font_size * 0.6))
    lines = textwrap.wrap(quote_text, width=max_chars_per_line)
    total_text_height = len(lines) * (font_size + 10)

    y = (H - total_text_height) // 2

    for line in lines:
        w, h = font.getsize(line)
        x = (W - w) // 2
        draw.text((x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
        y += font_size + 10

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
            st.download_button(
                label="📥 Download Wallpaper",
                data=buf.getvalue(),
                file_name="motivational_wallpaper.jpg",
                mime="image/jpeg"
            )
