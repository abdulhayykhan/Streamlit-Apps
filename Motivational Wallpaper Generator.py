import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
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

    # Overlay for readability
    overlay = Image.new('RGBA', bg.size, (0, 0, 0, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)

    # Use default font with larger size
    max_font_size = 60
    min_font_size = 20
    font_size = max_font_size

    # Try fitting the text within the image width
    wrapped = []
    while font_size >= min_font_size:
        font = ImageFont.load_default()
        test_draw = ImageDraw.Draw(Image.new("RGB", (W, H)))
        wrapped = textwrap.wrap(quote_text, width=int(W / (font_size * 0.6)))
        total_height = len(wrapped) * (font_size + 10)
        if total_height <= H * 0.9:  # Allow a little margin
            break
        font_size -= 2

    # Draw text centered
    y_text = (H - total_height) // 2
    for line in wrapped:
        w, h = test_draw.textsize(line, font=font)
        x = (W - w) // 2
        draw.text((x, y_text), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
        y_text += font_size + 10

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
