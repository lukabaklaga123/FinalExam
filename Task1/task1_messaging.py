from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def generate_rsa_keys():
    """Generates an RSA 2048-bit key pair."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_message(message, public_key):
    """
    Encrypts a message using Hybrid Encryption:
    1. Generates a random AES session key.
    2. Encrypts the message with AES-256-GCM.
    3. Encrypts the AES key with RSA.
    """
    # 1. Generate AES Session Key (32 bytes = 256 bits)
    aes_key = os.urandom(32)
    iv = os.urandom(12) # Recommended IV size for GCM

    # 2. Encrypt Message with AES-GCM
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()

    # 3. Encrypt AES Key with RSA
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext, iv, encryptor.tag, encrypted_aes_key

def decrypt_message(ciphertext, iv, tag, encrypted_aes_key, private_key):
    """
    Decrypts the message:
    1. Decrypts the AES key using RSA private key.
    2. Decrypts the message using the recovered AES key.
    """
    # 1. Decrypt AES Key with RSA
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 2. Decrypt Message with AES-GCM
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Task 1: Encrypted Messaging App Prototype ---")
    
    # 1. Setup (User A)
    print("[*] Generating RSA keys for User A...")
    priv_a, pub_a = generate_rsa_keys()

    # 2. Encryption (User B)
    msg_content = b"This is a top secret message for the Final Exam."
    print(f"[*] User B encrypting message: '{msg_content.decode()}'")
    
    ct, iv, tag, enc_key = encrypt_message(msg_content, pub_a)

    # Save deliverables
    with open("message.txt", "wb") as f: f.write(msg_content)
    with open("encrypted_message.bin", "wb") as f: f.write(iv + tag + ct) 
    with open("aes_key_encrypted.bin", "wb") as f: f.write(enc_key)
    print("[*] Artifacts saved (message.txt, encrypted_message.bin, aes_key_encrypted.bin)")

    # 3. Decryption (User A)
    print("[*] User A decrypting message...")
    try:
        decrypted_msg = decrypt_message(ct, iv, tag, enc_key, priv_a)
        with open("decrypted_message.txt", "wb") as f: f.write(decrypted_msg)
        print(f"[+] Success! Decrypted message: {decrypted_msg.decode()}")
    except Exception as e:
        print(f"[-] Decryption Failed: {e}")