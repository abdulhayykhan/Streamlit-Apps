import streamlit as st
import random
import time

def main():
    st.set_page_config(page_title="Eid Mubarak Greeting", page_icon="🌙")
    st.title("🌙 Eid Mubarak!")
    
    girlfriend_name = "Alysha"  # Replace with your girlfriend's name
    
    # Text Animation Function
    def animated_text(text, delay=0.1):
        animated_str = ""
        for char in text:
            animated_str += char
            st.markdown(f"<h2 style='text-align: center; color: #FFA500;'>{animated_str}</h2>", unsafe_allow_html=True)
            time.sleep(delay)
    
    st.markdown("""<style> @keyframes fade { from {opacity: 0;} to {opacity: 1;} } .fade { animation: fade 2s infinite alternate; }</style>""", unsafe_allow_html=True)
    
    # Animated Eid Mubarak Message
    animated_text(f"Eid Mubarak, Alysha! 💖")
    
    st.markdown(
        """
        <p class='fade' style='text-align: center; font-size: 18px;'>
        May this Eid bring you joy, love, and countless blessings! 🌸✨
        </p>
        """, unsafe_allow_html=True
    )
    
    # Unique Feature: Infinite Love Animation
    st.markdown(
        """
        <div style='text-align: center;'>
            <h1 class='fade' style='color: red;'>❤️ ∞ ❤️</h1>
            <p class='fade' style='font-size: 18px;'>
                Our love is endless, just like this infinity symbol. Wishing you an Eid filled with happiness and love! 💕
            </p>
        </div>
        """, unsafe_allow_html=True
    )
    
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
