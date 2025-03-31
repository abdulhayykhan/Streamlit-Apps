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
    
    st.image("https://source.unsplash.com/600x300/?eid,celebration", use_container_width=True)
    
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
    
if __name__ == "__main__":
    main()