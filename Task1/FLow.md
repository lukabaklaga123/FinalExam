# Encrypted Messaging App Prototype

## Overview

The system consists of two users:

- **User A (Receiver)**: Generates the RSA key pair and decrypts the final message.
- **User B (Sender)**: Generates the message and performs the encryption.

---

## Step 1: RSA Key Generation (User A)

Before communication begins, User A must establish their identity and provide a way for User B to send secure data.

1. **Generate Private Key**: User A generates a 2048-bit RSA Private Key. This key is kept secret and never shared.
   - Output: `rsa_private_key.pem`
   
2. **Extract Public Key**: User A derives the Public Key from the Private Key.
   - Output: `rsa_public_key.pem`
   
3. **Share Public Key**: User A sends the Public Key to User B. This key can be shared openly without compromising security.

---

## Step 2: Message Encryption (User B)

User B wants to send a secret message (`M`) to User A. Since RSA is slow and has size limits for direct data encryption, User B uses a hybrid approach.

### A. Symmetric Encryption (AES)

1. **Generate Session Key**: User B generates a random 32-byte (256-bit) AES Key (`K`) and a 12-byte Initialization Vector (IV). This key is used for this specific session only.
   - Key Size: `256 bits (32 bytes)`
   - IV Size: `12 bytes`

2. **Encrypt Message**: User B encrypts the plaintext message `M` using AES-256-GCM with key `K` and the `IV`.
   - Algorithm: `AES` (Advanced Encryption Standard)
   - Mode: `GCM` (Galois/Counter Mode) - Provides both confidentiality and integrity.
   - Output: `ciphertext` + `auth_tag`

### B. Asymmetric Encryption (RSA)

1. **Encrypt Session Key**: User B takes the AES session key `K` and encrypts it using User A's RSA Public Key.
   - Algorithm: `RSA`
   - Padding: `OAEP` (Optimal Asymmetric Encryption Padding) with SHA-256
   - Output: `encrypted_aes_key`

### C. Transmission

User B sends the following package to User A:

- `ciphertext` - The encrypted message
- `iv` - The initialization vector
- `auth_tag` - The GCM integrity tag
- `encrypted_aes_key` - The key needed to unlock the ciphertext

---

## Step 3: Message Decryption (User A)

User A receives the package and reverses the process.

### A. Decrypt Session Key (RSA)

1. User A takes the `encrypted_aes_key`.
2. User A uses their RSA Private Key (and OAEP padding) to decrypt it.
3. **Result**: User A now possesses the original 32-byte AES Session Key `K`.

### B. Decrypt Message (AES)

1. User A uses the recovered AES Key `K`, the `iv`, and the `auth_tag`.
2. User A decrypts the `ciphertext` using AES-256-GCM.
3. **Result**: The original plaintext message `M` is revealed.


- **OAEP Padding**: Prevents padding oracle attacks
- **Authentication Tag**: Cryptographic integrity verification
- **Session Keys**: One-time use keys for forward secrecy
