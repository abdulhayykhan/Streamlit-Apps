import streamlit as st
import random

def main():
    st.set_page_config(page_title="Eid Mubarak Greeting", page_icon="🌙")
    st.title("🌙 Eid Mubarak!")
    
    girlfriend_name = "Alysha"  # Replace with your girlfriend's name
    
    st.markdown(
        f"""
        <h2 style='text-align: center; color: #FFA500;'>
        Eid Mubarak, {girlfriend_name}! 💖
        </h2>
        <p style='text-align: center; font-size: 18px;'>
        May this Eid bring you joy, love, and countless blessings! 🌸✨
        </p>
        """, unsafe_allow_html=True
    )
    
    st.image("https://source.unsplash.com/600x300/?eid,celebration", use_column_width=True)
    
    st.write("\n")
    st.write("**Special Message:**")
    special_message = st.text_area("Write a personal Eid message for her:", "Wishing you a beautiful Eid filled with happiness and love!")
    
    if st.button("Send Greeting 💌"):
        st.success("Your heartfelt message has been sent! 💕")
        st.write(f"**Your Message:** {special_message}")
    
    # Unique Feature: Random Eid Wishes
    eid_wishes = [
        "May your life be as sweet as Eid desserts! 🍰",
        "Sending you a moonlit night full of love and happiness! 🌙",
        "May all your dreams come true this Eid! ✨",
        "Happiness, peace, and prosperity to you! 🌸",
        "Eid is special, but you're even more special! 💖"
    ]
    
    random_wish = random.choice(eid_wishes)
    st.write("\n")
    st.markdown(f"### 🌟 Surprise Eid Wish: {random_wish}")
    
    # Unique Feature: Eid Song
    st.write("\n")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    
if __name__ == "__main__":
    main()
