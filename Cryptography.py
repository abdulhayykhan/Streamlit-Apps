import streamlit as st
import module as md
import numpy as np

def generate_random_key():
    while True:
        key = np.random.randint(-10, 10, (2, 2))
        if np.linalg.det(key) != 0:
            return key.tolist()

st.title('🔐 Cryptogram - Hill Cipher')
st.markdown("Encrypt and decrypt messages using a matrix-based cipher!")

option = st.radio("Select an action:", ('Encode The Message', 'Decode The Message'))

if option == 'Encode The Message':
    msg = st.text_input("✍️ Enter your message:").upper()
    st.subheader("🔑 Enter your key matrix (2x2)")
    col1, col2 = st.columns([1, 1])
    with col1:
        x11 = st.number_input("Row 1, Col 1", min_value=-100, max_value=100, value=1)
        x21 = st.number_input("Row 2, Col 1", min_value=-100, max_value=100, value=0)
    with col2:
        x12 = st.number_input("Row 1, Col 2", min_value=-100, max_value=100, value=0)
        x22 = st.number_input("Row 2, Col 2", min_value=-100, max_value=100, value=1)
    
    if st.button("🔀 Generate Random Key"):
        key = generate_random_key()
        x11, x12, x21, x22 = key[0][0], key[0][1], key[1][0], key[1][1]
        st.success(f"Generated Key: {key}")
    
    if st.button("🔒 Encode It!"):
        if md.is_valid_input(msg):
            key_matrix = [[x11, x12], [x21, x22]]
            determinant = (x11 * x22) - (x12 * x21)
            if determinant == 0:
                st.error("❌ The key matrix is non-invertible. Choose another key.")
            else:
                encoded_msg = md.key_msg(md.take_string(msg), x11, x12, x21, x22)
                result_string = " ".join(map(str, encoded_msg))
                st.success("✅ Encoding successful!")
                st.code(f"Your Encoded Message: {result_string}\nKey Used: {key_matrix}")
        else:
            st.warning("⚠️ Message can only contain alphabets and spaces.")

elif option == 'Decode The Message':
    msg = st.text_input("🔢 Enter your encoded numbers (e.g., 34 2 55 8):")
    st.subheader("🔑 Enter your key matrix (2x2)")
    col1, col2 = st.columns([1, 1])
    with col1:
        x11 = st.number_input("Row 1, Col 1", min_value=-100, max_value=100, value=1)
        x21 = st.number_input("Row 2, Col 1", min_value=-100, max_value=100, value=0)
    with col2:
        x12 = st.number_input("Row 1, Col 2", min_value=-100, max_value=100, value=0)
        x22 = st.number_input("Row 2, Col 2", min_value=-100, max_value=100, value=1)
    
    if st.button("🔓 Decode It!"):
        if md.check_numeric_input(msg):
            numbers = list(map(int, msg.split()))
            key_matrix = [[x11, x12], [x21, x22]]
            determinant = (x11 * x22) - (x12 * x21)
            if determinant == 0:
                st.error("❌ The key matrix is non-invertible. Decryption is impossible.")
            else:
                inverse_key = md.inverse(key_matrix)
                decoded_result = md.inversekey_msg(numbers, inverse_key)
                decoded_message = md.decode(decoded_result)
                st.success("✅ Decoding successful!")
                st.code(f"Decoded Message: {decoded_message}")
        else:
            st.warning("⚠️ Please enter only numeric values and spaces!")
