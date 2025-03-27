import streamlit as st
import numpy as np

# Utility Functions
def is_valid_input(msg):
    """Check if input contains only alphabets and spaces."""
    return all(c.isalpha() or c.isspace() for c in msg)

def take_string(msg):
    """Convert string message to numerical values (A=0, B=1, ..., Z=25)."""
    return [ord(char) - ord('A') for char in msg if char.isalpha()]

def key_msg(msg_list, key_matrix):
    """Encrypt the message using matrix multiplication."""
    msg_matrix = np.array(msg_list).reshape(-1, 2).T
    encrypted = np.dot(key_matrix, msg_matrix) % 26
    return encrypted.T.flatten()

def check_numeric_input(msg):
    """Check if input contains only numeric values and spaces."""
    return all(i.isdigit() or i.isspace() for i in msg)

def inverse(matrix):
    """Calculate the modular inverse of a 2x2 key matrix (mod 26)."""
    det = int(np.round(np.linalg.det(matrix)))
    if det == 0:
        return None
    det_inv = pow(det, -1, 26)  # Modular inverse
    adjugate = np.array([[matrix[1, 1], -matrix[0, 1]], [-matrix[1, 0], matrix[0, 0]]])
    return (det_inv * adjugate) % 26

def inversekey_msg(numbers, inverse_key):
    """Decrypt the message using inverse matrix multiplication."""
    numbers_matrix = np.array(numbers).reshape(-1, 2).T
    decrypted = np.dot(inverse_key, numbers_matrix) % 26
    return decrypted.T.flatten()

def decode(num_list):
    """Convert numeric values back to a string message."""
    return ''.join(chr(int(num) + ord('A')) for num in num_list)

def generate_random_key():
    """Generate a random invertible 2x2 matrix key."""
    while True:
        key = np.random.randint(1, 10, (2, 2))
        if np.linalg.det(key) % 26 != 0:
            return key

# Streamlit UI
st.title("🔐 Cryptogram - Hill Cipher")
st.markdown("Encrypt and decrypt messages using a matrix-based cipher!")

option = st.radio("Select an action:", ("Encode The Message", "Decode The Message"))

if option == "Encode The Message":
    msg = st.text_input("✍️ Enter your message:").upper()
    st.subheader("🔑 Enter your key matrix (2x2)")
    
    col1, col2 = st.columns(2)
    with col1:
        x11 = st.number_input("Row 1, Col 1", min_value=1, max_value=25, value=2)
        x21 = st.number_input("Row 2, Col 1", min_value=1, max_value=25, value=1)
    with col2:
        x12 = st.number_input("Row 1, Col 2", min_value=1, max_value=25, value=3)
        x22 = st.number_input("Row 2, Col 2", min_value=1, max_value=25, value=4)

    if st.button("🔀 Generate Random Key"):
        key = generate_random_key()
        x11, x12, x21, x22 = key[0, 0], key[0, 1], key[1, 0], key[1, 1]
        st.success(f"Generated Key: {key.tolist()}")

    if st.button("🔒 Encode It!"):
        if is_valid_input(msg):
            key_matrix = np.array([[x11, x12], [x21, x22]])
            if np.linalg.det(key_matrix) == 0:
                st.error("❌ The key matrix is non-invertible. Choose another key.")
            else:
                encoded_msg = key_msg(take_string(msg), key_matrix)
                result_string = " ".join(map(str, encoded_msg))
                st.success("✅ Encoding successful!")
                st.code(f"Your Encoded Message: {result_string}\nKey Used: {key_matrix.tolist()}")
        else:
            st.warning("⚠️ Message can only contain alphabets and spaces.")

elif option == "Decode The Message":
    msg = st.text_input("🔢 Enter your encoded numbers (e.g., 34 2 55 8):")
    st.subheader("🔑 Enter your key matrix (2x2)")

    col1, col2 = st.columns(2)
    with col1:
        x11 = st.number_input("Row 1, Col 1", min_value=1, max_value=25, value=2)
        x21 = st.number_input("Row 2, Col 1", min_value=1, max_value=25, value=1)
    with col2:
        x12 = st.number_input("Row 1, Col 2", min_value=1, max_value=25, value=3)
        x22 = st.number_input("Row 2, Col 2", min_value=1, max_value=25, value=4)

    if st.button("🔓 Decode It!"):
        if check_numeric_input(msg):
            numbers = list(map(int, msg.split()))
            key_matrix = np.array([[x11, x12], [x21, x22]])
            if np.linalg.det(key_matrix) == 0:
                st.error("❌ The key matrix is non-invertible. Decryption is impossible.")
            else:
                inverse_key = inverse(key_matrix)
                if inverse_key is None:
                    st.error("❌ The key matrix does not have a valid modular inverse.")
                else:
                    decoded_result = inversekey_msg(numbers, inverse_key)
                    decoded_message = decode(decoded_result)
                    st.success("✅ Decoding successful!")
                    st.code(f"Decoded Message: {decoded_message}")
        else:
            st.warning("⚠️ Please enter only numeric values and spaces!")
