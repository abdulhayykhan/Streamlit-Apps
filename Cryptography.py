import streamlit as st
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

class CryptographyApp:
    def __init__(self):
        st.set_page_config(page_title="Cryptography Toolkit", page_icon="🔐")
    
    def caesar_cipher(self, text, shift, mode='encrypt'):
        """Implement Caesar Cipher encryption and decryption."""
        result = ""
        for char in text:
            if char.isalpha():
                # Determine the case and base
                is_upper = char.isupper()
                base = ord('A') if is_upper else ord('a')
                
                # Perform shift
                if mode == 'encrypt':
                    shifted = (ord(char) - base + shift) % 26
                else:
                    shifted = (ord(char) - base - shift) % 26
                
                result += chr(shifted + base)
            else:
                result += char
        return result
    
    def generate_symmetric_key(self, password):
        """Generate a symmetric key using PBKDF2."""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def symmetric_encryption(self, text, password, mode='encrypt'):
        """Symmetric encryption using Fernet."""
        try:
            if mode == 'encrypt':
                key, salt = self.generate_symmetric_key(password)
                f = Fernet(key)
                encrypted = f.encrypt(text.encode())
                return base64.urlsafe_b64encode(salt + encrypted).decode(), salt
            else:
                decoded = base64.urlsafe_b64decode(text.encode())
                salt = decoded[:16]
                encrypted_text = decoded[16:]
                
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000
                )
                key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
                
                f = Fernet(key)
                decrypted = f.decrypt(encrypted_text).decode()
                return decrypted
        except Exception as e:
            return f"Error: {str(e)}"
    
    def hash_text(self, text, algorithm='SHA-256'):
        """Generate hash of the input text."""
        if algorithm == 'SHA-256':
            return hashlib.sha256(text.encode()).hexdigest()
        elif algorithm == 'MD5':
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == 'SHA-1':
            return hashlib.sha1(text.encode()).hexdigest()
    
    def base64_encode_decode(self, text, mode='encode'):
        """Base64 encoding and decoding."""
        if mode == 'encode':
            return base64.b64encode(text.encode()).decode()
        else:
            return base64.b64decode(text.encode()).decode()
    
    def xor_cipher(self, text, key):
        """XOR cipher for encryption and decryption."""
        return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, key * (len(text) // len(key) + 1)))
    
    def run(self):
        """Main Streamlit app runner."""
        st.title("🔐 Cryptography Toolkit")
        
        # Sidebar navigation
        menu = st.sidebar.radio("Select Cryptography Method", [
            "Caesar Cipher", 
            "Symmetric Encryption", 
            "Hashing", 
            "Base64 Encoding", 
            "XOR Cipher"
        ])
        
        # Caesar Cipher Section
        if menu == "Caesar Cipher":
            st.header("Caesar Cipher")
            col1, col2 = st.columns(2)
            with col1:
                caesar_text = st.text_area("Enter Text")
                caesar_shift = st.slider("Shift Value", 1, 25, 3)
            with col2:
                mode = st.radio("Mode", ["Encrypt", "Decrypt"])
                
            if st.button("Process Caesar Cipher"):
                if mode == "Encrypt":
                    result = self.caesar_cipher(caesar_text, caesar_shift, 'encrypt')
                else:
                    result = self.caesar_cipher(caesar_text, caesar_shift, 'decrypt')
                st.success(f"Result: {result}")
        
        # Symmetric Encryption Section
        elif menu == "Symmetric Encryption":
            st.header("Symmetric Encryption (Fernet)")
            col1, col2 = st.columns(2)
            with col1:
                sym_text = st.text_area("Enter Text")
                sym_password = st.text_input("Encryption Password", type="password")
            with col2:
                sym_mode = st.radio("Mode", ["Encrypt", "Decrypt"])
                
            if st.button("Process Symmetric Encryption"):
                if sym_mode == "Encrypt":
                    result, salt = self.symmetric_encryption(sym_text, sym_password, 'encrypt')
                    st.success(f"Encrypted Text: {result}")
                else:
                    result = self.symmetric_encryption(sym_text, sym_password, 'decrypt')
                    st.success(f"Decrypted Text: {result}")
        
        # Hashing Section
        elif menu == "Hashing":
            st.header("Text Hashing")
            hash_text = st.text_area("Enter Text to Hash")
            hash_algo = st.selectbox("Select Hash Algorithm", 
                ["SHA-256", "MD5", "SHA-1"])
            
            if st.button("Generate Hash"):
                result = self.hash_text(hash_text, hash_algo)
                st.success(f"{hash_algo} Hash: {result}")
        
        # Base64 Section
        elif menu == "Base64 Encoding":
            st.header("Base64 Encoding/Decoding")
            base64_text = st.text_area("Enter Text")
            base64_mode = st.radio("Mode", ["Encode", "Decode"])
            
            if st.button("Process Base64"):
                if base64_mode == "Encode":
                    result = self.base64_encode_decode(base64_text, 'encode')
                else:
                    result = self.base64_encode_decode(base64_text, 'decode')
                st.success(f"Result: {result}")
        
        # XOR Cipher Section
        elif menu == "XOR Cipher":
            st.header("XOR Cipher")
            col1, col2 = st.columns(2)
            with col1:
                xor_text = st.text_area("Enter Text")
            with col2:
                xor_key = st.text_input("Encryption Key")
            
            if st.button("Process XOR Cipher"):
                result = self.xor_cipher(xor_text, xor_key)
                st.success(f"Result: {result}")

def main():
    app = CryptographyApp()
    app.run()

if __name__ == "__main__":
    main()
