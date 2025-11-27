The system consists of two users:

User A (Receiver): Generates the RSA key pair and decrypts the final message.
User B (Sender): Generates the message and performs the encryption.


Step 1: RSA Key Generation (User A)
Before communication begins, User A must establish their identity and provide a way for User B to send secure data.

Generate Private Key: User A generates a 2048-bit RSA Private Key. This key is kept secret and never shared.
Extract Public Key: User A derives the Public Key from the Private Key.
Share Public Key: User A sends the Public Key to User B. This key can be shared openly without compromising security.


Step 2: Message Encryption (User B)
User B wants to send a secret message (M) to User A. Since RSA is slow and has size limits for direct data encryption, User B uses a hybrid approach.
A. Symmetric Encryption (AES)

Generate Session Key: User B generates a random 32-byte (256-bit) AES Key (K) and a 12-byte Initialization Vector (IV). This key is used for this specific session only.
Encrypt Message: User B encrypts the plaintext message M using AES-256-GCM with key K and the IV.

Algorithm: AES (Advanced Encryption Standard)
Mode: GCM (Galois/Counter Mode) - Provides both confidentiality and integrity.
Output: Ciphertext + Auth Tag.



B. Asymmetric Encryption (RSA)

Encrypt Session Key: User B takes the AES session key K and encrypts it using User A's RSA Public Key.

Algorithm: RSA
Padding: OAEP (Optimal Asymmetric Encryption Padding) with SHA-256.
Output: Encrypted AES Key.



C. Transmission
User B sends the following package to User A:

Ciphertext (The encrypted message)
IV (The initialization vector)
Auth Tag (The GCM integrity tag)
Encrypted AES Key (The key needed to unlock the ciphertext)


Step 3: Message Decryption (User A)
User A receives the package and reverses the process.
A. Decrypt Session Key (RSA)

User A takes the Encrypted AES Key.
User A uses their RSA Private Key (and OAEP padding) to decrypt it.
Result: User A now possesses the original 32-byte AES Session Key K.

B. Decrypt Message (AES)

User A uses the recovered AES Key K, the IV, and the Auth Tag.
User A decrypts the Ciphertext using AES-256-GCM.
Result: The original plaintext message M is revealed.
LB


Result: The original plaintext message M is revealed.
