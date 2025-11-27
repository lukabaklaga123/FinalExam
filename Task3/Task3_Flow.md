# Task 3: TLS Communication Inspection & Analysis

## Overview

This task demonstrates how **TLS (Transport Layer Security)** protects communication between a client and server by inspecting a real connection to `google.com`.

---

## 1. Connection Details (google.com)

### Certificate Chain

The certificate chain establishes trust from the server to a trusted root authority:

- **Leaf Certificate**: `*.google.com`  
  - The server's identity certificate
  
- **Intermediate Certificate**: `GTS CA 1C3`  
  - Issued by Google Trust Services
  
- **Root Certificate**: `GlobalSign Root CA`  
  - Trusted by the operating system

---

### Cipher Suite

**Selected Cipher Suite**: `TLS_AES_256_GCM_SHA384`

| Component | Algorithm | Purpose |
|-----------|-----------|---------|
| **Key Exchange** | `ECDHE` (Elliptic Curve Diffie-Hellman Ephemeral) | Provides **Forward Secrecy** - even if private key is compromised later, past sessions remain secure |
| **Encryption** | `AES-256-GCM` | Provides **Confidentiality** - protects data from eavesdropping |
| **Integrity** | `SHA384/GCM` | Ensures data hasn't been tampered with |

---

### TLS Version

**Protocol**: `TLSv1.3`

-  The latest and most secure TLS standard
-  Faster handshake (1-RTT)
-  Removes insecure legacy features
-  Always provides forward secrecy

---

## 2. TLS Handshake Analysis

The handshake establishes a secure session between client and server:

### Handshake Steps

1. **Client Hello**  
   - Client sends supported cipher suites
   - Client sends a random nonce
   - Client announces TLS version support

2. **Server Hello**  
   - Server picks the best cipher suite: `TLS_AES_256_GCM_SHA384`
   - Server sends its own random nonce
   - Server confirms TLS version: `TLSv1.3`

3. **Certificate**  
   - Server sends its certificate chain
   - Proves the server is really `google.com`
   - Client verifies against trusted Root CAs

4. **Key Exchange**  
   - Both sides use **ECDHE** to independently calculate the same session key
   - This key is never transmitted over the network
   - Provides **Forward Secrecy**

5. **Finished**  
   - Handshake complete
   - Secure encryption begins using the session key
   - All application data (HTTP) is now encrypted


## 3. How TLS Provides Security

TLS provides three core security properties:

###  Confidentiality

**How it works:**
- All application data (HTTP) is encrypted using the negotiated **Symmetric Session Key**
- Algorithm: `AES-256-GCM`
- This prevents **eavesdropping**

**Protection:**
- Attackers cannot read the data even if they intercept network packets
- Only the client and server possess the session key


- Used by HTTPS, email (STARTTLS), VPNs, and virtually all secure internet protocols
