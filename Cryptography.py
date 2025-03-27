import streamlit as st
from cryptography.fernet import Fernet

# Function to generate a key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt a message
def encrypt_message(key, message):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

# Function to decrypt a message
def decrypt_message(key, encrypted_message):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

# Streamlit app
st.title("Simple Cryptography App")

# Generate a key
if st.button("Generate Key"):
    key = generate_key()
    st.session_state.key = key.decode()  # Store key in session state
    st.success(f"Key generated: {st.session_state.key}")

# Display the key
if 'key' in st.session_state:
    st.subheader("Your Key:")
    st.text(st.session_state.key)

# Encrypt a message
st.subheader("Encrypt a Message")
message_to_encrypt = st.text_area("Enter the message to encrypt:")
if st.button("Encrypt"):
    if 'key' in st.session_state:
        encrypted = encrypt_message(st.session_state.key.encode(), message_to_encrypt)
        st.success(f"Encrypted Message: {encrypted.decode()}")
    else:
        st.error("Please generate a key first.")

# Decrypt a message
st.subheader("Decrypt a Message")
message_to_decrypt = st.text_area("Enter the message to decrypt:")
if st.button("Decrypt"):
    if 'key' in st.session_state:
        try:
            decrypted = decrypt_message(st.session_state.key.encode(), message_to_decrypt.encode())
            st.success(f"Decrypted Message: {decrypted}")
        except Exception as e:
            st.error("Decryption failed. Please check your input.")
    else:
        st.error("Please generate a key first.")
