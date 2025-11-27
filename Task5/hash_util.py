import hashlib
import json
import os

def compute_hashes(filepath):
    """Computes SHA-256, SHA-1, and MD5 hashes of a file."""
    hashes = {}
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            hashes['SHA-256'] = hashlib.sha256(data).hexdigest()
            hashes['SHA-1'] = hashlib.sha1(data).hexdigest()
            hashes['MD5'] = hashlib.md5(data).hexdigest()
        return hashes
    except FileNotFoundError:
        return None

def save_hashes(hashes, json_path):
    with open(json_path, "w") as f:
        json.dump(hashes, f, indent=4)

def verify_integrity(filepath, json_path):
    """Compares current file hashes against stored JSON."""
    current_hashes = compute_hashes(filepath)
    
    if not os.path.exists(json_path):
        print("[!] No hash record found.")
        return

    with open(json_path, "r") as f:
        stored_hashes = json.load(f)

    print(f"Checking integrity for: {filepath}")
    is_valid = True
    for algo, h_val in current_hashes.items():
        if stored_hashes.get(algo) != h_val:
            print(f"[FAIL] {algo} mismatch!")
            print(f"  Stored:  {stored_hashes.get(algo)}")
            print(f"  Current: {h_val}")
            is_valid = False
        else:
            print(f"[PASS] {algo} matches.")
    
    if is_valid:
        print("\n[+] Integrity Verified: File is authentic.")
    else:
        print("\n[!] WARNING: File has been tampered with!")

# --- Simulation ---
# 1. Create original file
with open("original.txt", "w") as f: f.write("This is critical data.")

# 2. Compute and store hashes
hashes = compute_hashes("original.txt")
save_hashes(hashes, "hashes.json")
print("Hashes stored for original.txt.\n")

# 3. Simulate tampering (modify file)
with open("original.txt", "a") as f: f.write(" MALICIOUS DATA")
print("Simulated tampering on original.txt...\n")

# 4. Verify integrity
verify_integrity("original.txt", "hashes.json")
