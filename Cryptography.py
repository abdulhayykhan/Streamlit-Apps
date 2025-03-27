import streamlit as st
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import base64

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key.decode(), public_key.decode()

def aes_encrypt(plain_text, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv=b'1234567890123456')
    encrypted_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    return base64.b64encode(encrypted_bytes).decode()

def aes_decrypt(cipher_text, key):
    try:
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv=b'1234567890123456')
        decrypted_bytes = unpad(cipher.decrypt(base64.b64decode(cipher_text)), AES.block_size)
        return decrypted_bytes.decode()
    except Exception:
        return "Decryption Failed: Invalid Key or Cipher Text"

def rsa_encrypt(plain_text, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_bytes = cipher.encrypt(plain_text.encode())
    return base64.b64encode(encrypted_bytes).decode()

def rsa_decrypt(cipher_text, private_key):
    try:
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        decrypted_bytes = cipher.decrypt(base64.b64decode(cipher_text))
        return decrypted_bytes.decode()
    except Exception:
        return "Decryption Failed: Invalid Key or Cipher Text"

st.title("🔐 Cryptography App")

st.sidebar.title("Select Encryption Type")
mode = st.sidebar.radio("Choose", ("AES Encryption", "AES Decryption", "RSA Encryption", "RSA Decryption", "Generate RSA Keys"))

if mode == "AES Encryption":
    text = st.text_area("Enter Text to Encrypt")
    aes_key = st.text_input("Enter 16-character AES Key", max_chars=16)
    if st.button("Encrypt"):
        if len(aes_key) == 16:
            encrypted_text = aes_encrypt(text, aes_key)
            st.success(f"Encrypted Text: {encrypted_text}")
        else:
            st.error("AES Key must be exactly 16 characters!")

elif mode == "AES Decryption":
    cipher_text = st.text_area("Enter AES Encrypted Text")
    aes_key = st.text_input("Enter 16-character AES Key", max_chars=16)
    if st.button("Decrypt"):
        if len(aes_key) == 16:
            decrypted_text = aes_decrypt(cipher_text, aes_key)
            st.success(f"Decrypted Text: {decrypted_text}")
        else:
            st.error("AES Key must be exactly 16 characters!")

elif mode == "RSA Encryption":
    text = st.text_area("Enter Text to Encrypt")
    public_key = st.text_area("Enter RSA Public Key")
    if st.button("Encrypt"):
        try:
            encrypted_text = rsa_encrypt(text, public_key)
            st.success(f"Encrypted Text: {encrypted_text}")
        except Exception:
            st.error("Invalid Public Key!")

elif mode == "RSA Decryption":
    cipher_text = st.text_area("Enter RSA Encrypted Text")
    private_key = st.text_area("Enter RSA Private Key")
    if st.button("Decrypt"):
        decrypted_text = rsa_decrypt(cipher_text, private_key)
        st.success(f"Decrypted Text: {decrypted_text}")

elif mode == "Generate RSA Keys":
    if st.button("Generate Keys"):
        private_key, public_key = generate_rsa_keys()
        st.text_area("Private Key (Keep Safe!)", private_key, height=200)
        st.text_area("Public Key (Share with Others)", public_key, height=200)
