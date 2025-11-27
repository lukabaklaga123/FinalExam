# Task 2: Secure File Exchange (RSA + AES)

## Overview

This task simulates a real-world scenario where Alice wants to send a large file securely to Bob. Since asymmetric encryption (RSA) is slow and can only encrypt small amounts of data, a **hybrid approach** is used.

---

## The Process

### 1. Bob Generates Keys (RSA)

- Bob creates a public/private RSA key pair.
- He gives his **Public Key** to Alice.
- He keeps his **Private Key** secret.

**Output Files:**
- `bob_private_key.pem`
- `bob_public_key.pem`

---

### 2. Alice Prepares the Package

- Alice creates the file: `alice_message.txt`
- Alice generates a random **AES Key** (32 bytes) and **IV** (16 bytes)

---

### 3. Alice Encrypts the File (Symmetric)

- Alice uses the fast **AES Key** to encrypt the file.
- **Result**: `encrypted_file.bin`

**Why AES?** Fast and efficient for large files.

---

### 4. Alice Encrypts the Key (Asymmetric)

- Alice takes the **AES Key** and encrypts it using **Bob's Public Key**.
- **Result**: `aes_key_encrypted.bin`

**Why encrypt the key?** Only Bob (who has the Private Key) can decrypt this to get the AES key back.

---

### 5. Bob Decrypts the Key

- Bob receives `aes_key_encrypted.bin`
- He uses his **RSA Private Key** to decrypt it
- **Result**: Bob now has the original **AES Key**

---

### 6. Bob Decrypts the File

- Bob uses the recovered **AES Key** (and the **IV**) to decrypt `encrypted_file.bin`
- **Result**: Bob recovers the original file `alice_message.txt`



---

## Comparison: AES vs RSA

| Feature | AES (Symmetric) | RSA (Asymmetric) |
|---------|----------------|------------------|
| **Speed** |  Extremely fast and efficient. Hardware accelerated. |  Slow and computationally expensive (1000x slower). |
| **Key Type** | Single shared secret key | Public/Private key pair |
| **Data Size** |  Unlimited - perfect for large files |  Limited - only small data (~245 bytes for RSA-2048) |
| **Use Case** |  Bulk data encryption (files, streams) |  Key exchange, digital signatures, small data |
| **Security Basis** | Security relies on keeping the single key secret | Security relies on the difficulty of factoring large primes |
| **Key Distribution** |  Challenging - how to share the key securely? |  Easy - public key can be shared openly |

---

## Why Use Hybrid Encryption?

The hybrid approach combines the **best of both worlds**:

-  **AES** handles the heavy lifting (encrypting large files) efficiently
-  **RSA** solves the key distribution problem securely
-  Fast performance with strong security
-  Scalable for files of any size

---

