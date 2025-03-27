import streamlit as st
import numpy as np

def generate_random_key():
    """Generate a random invertible 2x2 matrix key."""
    while True:
        key = np.random.randint(1, 10, (2, 2))
        det = int(np.linalg.det(key))
        if det % 26 != 0 and det != 0:  # Ensure nonzero and invertible mod 26
            return key

def is_valid_key(matrix):
    """Check if matrix is invertible."""
    det = int(np.linalg.det(matrix))
    return det != 0 and det % 26 != 0

def encrypt_message(msg, key_matrix):
    """Encrypt the message using Hill Cipher (2x2 matrix)."""
    msg = msg.replace(" ", "").upper()  # Remove spaces & convert to uppercase
    if len(msg) % 2 != 0:
        msg += "X"  # Padding if odd-length

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    char_to_num = {char: i for i, char in enumerate(alphabet)}
    num_to_char = {i: char for i, char in enumerate(alphabet)}

    # Convert text to numbers
    msg_nums = [char_to_num[char] for char in msg]
    msg_matrix = np.array(msg_nums).reshape(-1, 2)

    # Encrypt
    encrypted_matrix = (msg_matrix @ key_matrix) % 26
    encrypted_text = "".join(num_to_char[num] for row in encrypted_matrix for num in row)
    
    return encrypted_text

st.title("🔐 Cryptography")

option = st.radio("Select an action:", ("Encode The Message", "Decode The Message"))

if option == "Encode The Message":
    msg = st.text_input("✍️ Enter your message:").upper()
    st.subheader("🔑 Enter your key matrix (2x2)")

    col1, col2 = st.columns(2)
    with col1:
        x11 = st.number_input("Row 1, Col 1", min_value=1, max_value=25, value=3)
        x21 = st.number_input("Row 2, Col 1", min_value=1, max_value=25, value=2)
    with col2:
        x12 = st.number_input("Row 1, Col 2", min_value=1, max_value=25, value=5)
        x22 = st.number_input("Row 2, Col 2", min_value=1, max_value=25, value=7)

    if st.button("🔀 Generate Random Key"):
        key = generate_random_key()
        x11, x12, x21, x22 = key[0, 0], key[0, 1], key[1, 0], key[1, 1]
        st.success(f"Generated Key: {key.tolist()}")

    key_matrix = np.array([[x11, x12], [x21, x22]])

    if st.button("🔒 Encode It!"):
        if is_valid_key(key_matrix):
            encrypted_text = encrypt_message(msg, key_matrix)
            st.success("✅ Encoding successful!")
            st.code(f"🔐 Encrypted Message: {encrypted_text}")
        else:
            st.error("❌ The key matrix is non-invertible. Choose another key.")
