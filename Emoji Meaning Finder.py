import streamlit as st
import requests

# --- Get All Emoji Data from API ---
@st.cache_data(ttl=86400)  # Cache data for 1 day
def fetch_all_emojis():
    try:
        res = requests.get("https://emojihub.yurace.pro/api/all")
        if res.status_code == 200:
            return res.json()
        else:
            return []
    except Exception as e:
        st.error(f"Failed to load emojis: {e}")
        return []

# --- Function to find emoji data ---
def find_emoji_data(input_emoji, all_emojis):
    for emoji in all_emojis:
        if emoji.get("unicode") == input_emoji:
            return emoji
    return None

# --- Streamlit Page Config ---
st.set_page_config(page_title="Emoji Meaning Finder (API)", page_icon="🔍")
st.title("🔍 Emoji Meaning Finder")
st.caption("Find out what your emoji means using a live API!")

st.markdown("---")

# --- User Input ---
user_emoji = st.text_input("Paste any emoji here 👇", max_chars=2)

# --- Load API Data ---
with st.spinner("Loading emoji data..."):
    emoji_data = fetch_all_emojis()

# --- Process Input ---
if user_emoji:
    match = find_emoji_data(user_emoji, emoji_data)

    if match:
        st.subheader(f"📛 Name: {match.get('name', 'Unknown')}")
        st.write(f"📂 Category: {match.get('category', 'Unknown')}")
        st.write(f"🔤 Unicode: {match.get('unicode', 'N/A')}")
        if "group" in match:
            st.write(f"🗂️ Group: {match.get('group')}")
    else:
        st.warning("Emoji not found in database 😔")

# --- Optional: Display sample emojis ---
with st.expander("📚 View Some Available Emojis"):
    sample = [emoji["unicode"] for emoji in emoji_data[:30] if "unicode" in emoji and emoji["unicode"]]
    if sample:
        st.write(" ".join(sample))
    else:
        st.info("No sample emojis to show.")

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ using Streamlit + EmojiHub API")
