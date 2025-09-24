import pandas as pd
from Crypto.Cipher import AES, DES, DES3, Blowfish, ARC4, PKCS1_OAEP, ChaCha20, CAST, Salsa20,ChaCha20_Poly1305,PKCS1_v1_5
from Crypto.PublicKey import RSA
from secretpy import CryptMachine
from secretpy.ciphers import Caesar
from Twofish import TwoFish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from IDEA import IDEA
from RC5 import rc5
from RC6.encrypt import encrypt
from RC6.rc6 import generateKey
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from Crypto.Protocol.KDF import HKDF as Crypto_HKDF
from Crypto.Hash import SHA256
from kyber_py.kyber import Kyber512
from FrodoKEM.frodo640.api_frodo640 import FrodoAPI640
import pq_ntru

# Test string to encrypt
TEST_STRING = "Hello, World! This is a test message for encryption algorithms."

print("=" * 80)
print("TESTING ALL 25 ENCRYPTION ALGORITHMS")
print("=" * 80)
print(f"Test string: '{TEST_STRING}'")
print(f"Test string length: {len(TEST_STRING)} characters")
print("=" * 80)

def get_rsa_keys(key_size=3072):
    """Generate RSA keys for testing"""
    private_key = RSA.generate(key_size)
    public_key = private_key.publickey()
    return private_key, public_key

# Generate RSA keys for testing
rsa_privkey, rsa_pubkey = get_rsa_keys()

# All encryption functions (copied from your code)
def encrypt_aes_gcm(data: str) -> str:
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def encrypt_aes_cbc(data: str) -> str:
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)
    padded_data = pad(data.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + ciphertext).decode()

def encrypt_des_cbc(data: str) -> str:
    key = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_CBC)
    padded_data = pad(data.encode(), DES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + ciphertext).decode()

def encrypt_3des_cbc(data: str) -> str:
    key = get_random_bytes(24)
    key = DES3.adjust_key_parity(key)
    cipher = DES3.new(key, DES3.MODE_CBC)
    padded_data = pad(data.encode(), DES3.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + ciphertext).decode()

def encrypt_blowfish_ctr(data: str) -> str:
    key = get_random_bytes(16)
    nonce = get_random_bytes(4)
    cipher = Blowfish.new(key, Blowfish.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(nonce + ciphertext).decode()

def encrypt_twofish_cbc(data: str) -> str:
    key = get_random_bytes(16)
    hex_key = key.hex()
    plain = TwoFish.text_To_Hex(data)
    mode = "CBC"
    padded = pad(bytes.fromhex(plain), 16)
    ciphertext = TwoFish.TwoFish_encrypt(padded.hex(), hex_key, mode)
    return base64.b64encode(bytes.fromhex(ciphertext)).decode()

def encrypt_rc4(data: str) -> str:
    key = get_random_bytes(16)
    cipher = ARC4.new(key)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(ciphertext).decode()

W = 32
R = 12
def encrypt_rc5(data: str) -> str:
    key = get_random_bytes(16)
    cipher = rc5.RC5(W, R, key)
    plaintext_bytes = data.encode()
    ciphertext = cipher.encryptBytes(plaintext_bytes)
    return base64.b64encode(ciphertext).decode()

def encrypt_rc6(data: str) -> str:
    key = get_random_bytes(16)
    s = generateKey(key.hex()) 
    data_bytes = data.encode('utf-8')
    ciphertext_hex = encrypt(data_bytes, s)
    return base64.b64encode(bytes.fromhex(ciphertext_hex)).decode()

def encrypt_idea(data: str) -> str:
    key = get_random_bytes(16)
    cipher = IDEA.IDEAWrapper(key)
    plaintext_bytes = data.encode()
    ciphertext = cipher.encrypt(plaintext_bytes)
    return base64.b64encode(ciphertext).decode()

def encrypt_chacha20(data: str) -> str:
    key = get_random_bytes(32)
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()

def encrypt_camellia(data: str) -> str:
    key = get_random_bytes(32)
    iv = get_random_bytes(16)
    algo = algorithms.Camellia(key)
    cipher = Cipher(algo, modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded = pad(data.encode(), 16)
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

def encrypt_cast128_cbc(data: str) -> str:
    key = get_random_bytes(16)
    cipher = CAST.new(key, CAST.MODE_CBC)
    padded = pad(data.encode(), 8)
    ciphertext = cipher.encrypt(padded)
    return base64.b64encode(cipher.iv + ciphertext).decode()

def encrypt_salsa20_stream(data: str) -> str:
    key = get_random_bytes(32)
    cipher = Salsa20.new(key=key)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()

def encrypt_caesar(data: str, shift: int = 3) -> str:
    cipher = Caesar()
    cm = CryptMachine(cipher, shift)  
    encrypted_text = cm.encrypt(data)
    return base64.b64encode(encrypted_text.encode()).decode()

def encrypt_chacha20_poly1305(data: str) -> str:
    key = get_random_bytes(32)                 
    cipher = ChaCha20_Poly1305.new(key=key)    
    ciphertext = cipher.encrypt(data.encode())
    tag = cipher.digest()
    nonce = cipher.nonce                       
    return base64.b64encode(nonce + tag + ciphertext).decode()

def encrypt_rsa_pkcs1v15(data: str, public_key) -> str:
    max_len = (public_key.size_in_bits() // 8) - 11  
    data_bytes = data.encode()[:max_len]
    cipher = PKCS1_v1_5.new(public_key)
    ciphertext = cipher.encrypt(data_bytes)
    return base64.b64encode(ciphertext).decode()

def encrypt_ecies(data: str) -> str:
    recipient_private = ec.generate_private_key(ec.SECP256R1(), default_backend())
    recipient_public = recipient_private.public_key()
    ephemeral_private = ec.generate_private_key(ec.SECP256R1(), default_backend())
    ephemeral_public = ephemeral_private.public_key()
    shared_secret = ephemeral_private.exchange(ec.ECDH(), recipient_public)
    key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'ecies',
        backend=default_backend()
    ).derive(shared_secret)
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    eph_bytes = ephemeral_public.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    return base64.b64encode(eph_bytes + iv + tag + ciphertext).decode()

def encrypt_rsa_oaep_aes(data: str, publicKey) -> str:
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    padded_data = pad(data.encode(), AES.block_size)
    ciphertext_aes = cipher_aes.encrypt(padded_data)
    cipher_rsa = PKCS1_OAEP.new(publicKey)
    enc_aes_key = cipher_rsa.encrypt(aes_key)
    final_blob = enc_aes_key + cipher_aes.iv + ciphertext_aes
    return base64.b64encode(final_blob).decode()

def encrypt_ecies_aes(data: str) -> str:
    recipient_private = ec.generate_private_key(ec.SECP256R1(), default_backend())
    recipient_public = recipient_private.public_key()
    eph_priv = ec.generate_private_key(ec.SECP256R1(), default_backend())
    eph_pub = eph_priv.public_key()
    shared = eph_priv.exchange(ec.ECDH(), recipient_public)
    key = HKDF(
        algorithm=hashes.SHA256(), 
        length=32, 
        salt=None, 
        info=b'ecies', 
        backend=default_backend()
    ).derive(shared)
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    eph_bytes = eph_pub.public_bytes(
        encoding=serialization.Encoding.X962, 
        format=serialization.PublicFormat.UncompressedPoint
    )
    return base64.b64encode(eph_bytes + iv + tag + ciphertext).decode()

def encrypt_pgp_armored(data: str) -> str:
    key = get_random_bytes(32)
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    pgp_like = b"-----BEGIN PGP MESSAGE-----\n" + base64.b64encode(iv + tag + ciphertext) + b"\n-----END PGP MESSAGE-----"
    return base64.b64encode(pgp_like).decode()

def encrypt_tls_like_ecdhe(data: str) -> str:
    server_private = ec.generate_private_key(ec.SECP256R1(), default_backend())
    server_public = server_private.public_key()
    client_eph = ec.generate_private_key(ec.SECP256R1(), default_backend())
    client_pub = client_eph.public_key()
    shared = client_eph.exchange(ec.ECDH(), server_public)
    key = HKDF(
        algorithm=hashes.SHA256(), 
        length=32, 
        salt=None, 
        info=b'tls-ecdhe', 
        backend=default_backend()
    ).derive(shared)
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    client_pub_bytes = client_pub.public_bytes(
        encoding=serialization.Encoding.X962, 
        format=serialization.PublicFormat.UncompressedPoint
    )
    return base64.b64encode(client_pub_bytes + iv + tag + ciphertext).decode()

def encrypt_kyber_aes(data: str) -> str:
    public_key, secret_key = Kyber512.keygen()
    kyber_ciphertext, shared_secret = Kyber512.encaps(public_key)
    cipher = AES.new(shared_secret[:16], AES.MODE_CBC)
    aes_ct = cipher.encrypt(pad(data.encode(), AES.block_size))
    combined_bytes = cipher.iv + aes_ct + kyber_ciphertext
    return base64.b64encode(combined_bytes).decode()

def encrypt_frodokem_aes(data: str) -> str:
    try:
        FrodoAPI = FrodoAPI640()
        public_key, private_key = FrodoAPI.crypto_kem_keypair_frodo640()
        ciphertext_kem, shared_secret = FrodoAPI.crypto_kem_enc_frodo640(public_key)
        aes_key = Crypto_HKDF(master=shared_secret, key_len=32, salt=None, hashmod=SHA256)
        iv = get_random_bytes(12)
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
        ciphertext_data, tag = cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(ciphertext_kem + iv + tag + ciphertext_data).decode()
    except Exception:
        return encrypt_aes_gcm(data)

def encrypt_ntru_aes(data: str) -> str:
    try:
        pub, priv = pq_ntru.generate_keypair()
        ct, ss = pq_ntru.encapsulate(pub)
        aes_key = Crypto_HKDF(master=ss, key_len=32, salt=None, hashmod=SHA256)
        iv = get_random_bytes(12)
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(ct + iv + tag + ciphertext).decode()
    except Exception:
        return encrypt_aes_gcm(data)

# Test configuration matching your original mapping
test_algorithms = [
    # SYMMETRIC ALGORITHMS
    (1, encrypt_aes_gcm, "Symmetric", "Block", "AES-GCM", "Standard"),
    (2, encrypt_aes_cbc, "Symmetric", "Block", "AES-CBC", "Standard"),
    (3, encrypt_des_cbc, "Symmetric", "Block", "DES-CBC", "Standard"),
    (4, encrypt_3des_cbc, "Symmetric", "Block", "3DES-CBC", "Standard"),
    (5, encrypt_blowfish_ctr, "Symmetric", "Block", "Blowfish-CTR", "Standard"),
    (6, encrypt_twofish_cbc, "Symmetric", "Block", "Twofish-CBC", "Standard"),
    (7, encrypt_rc4, "Symmetric", "Stream", "RC4", "Standard"),
    (8, encrypt_rc5, "Symmetric", "Block", "RC5", "Standard"),
    (9, encrypt_rc6, "Symmetric", "Block", "RC6", "Standard"),
    (10, encrypt_idea, "Symmetric", "Block", "IDEA", "Standard"),
    (11, encrypt_chacha20, "Symmetric", "Stream", "ChaCha20", "Standard"),
    (12, encrypt_camellia, "Symmetric", "Block", "Camellia-CBC", "Standard"),
    (13, encrypt_cast128_cbc, "Symmetric", "Block", "CAST-128-CBC", "Standard"),
    (14, encrypt_salsa20_stream, "Symmetric", "Stream", "Salsa20", "Standard"),
    (15, encrypt_caesar, "Symmetric", "Classical", "Caesar", "Classical"),
    (16, encrypt_chacha20_poly1305, "Symmetric", "AEAD", "ChaCha20-Poly1305", "AEAD"),
    
    # ASYMMETRIC ALGORITHMS
    (17, encrypt_rsa_pkcs1v15, "Asymmetric", "Public Key", "RSA-PKCS1v1.5", "RSA"),
    (18, encrypt_ecies, "Asymmetric", "Public Key", "ECIES", "ECC"),
    
    # HYBRID ALGORITHMS
    (19, encrypt_rsa_oaep_aes, "Hybrid", "Hybrid", "Hybrid-RSA-OAEP-AES", "RSA"),
    (20, encrypt_ecies_aes, "Hybrid", "Hybrid", "Hybrid-ECIES-AES", "ECC"),
    (21, encrypt_pgp_armored, "Hybrid", "Hybrid", "PGP-Armored", "Standard"),
    (22, encrypt_tls_like_ecdhe, "Hybrid", "Hybrid", "TLS-ECDHE-AES", "ECC"),
    
    # POST-QUANTUM ALGORITHMS
    (23, encrypt_kyber_aes, "Post-Quantum", "Hybrid", "Kyber-AES", "Post-Quantum"),
    (24, encrypt_frodokem_aes, "Post-Quantum", "Hybrid", "FrodoKEM-AES", "Post-Quantum"),
    (25, encrypt_ntru_aes, "Post-Quantum", "Hybrid", "NTRU-AES", "Post-Quantum")
]

# Test results storage
results = []
successful_tests = 0
failed_tests = 0

print("\nTesting each algorithm:")
print("-" * 80)

for test_num, func, category, alg_type, alg_name, special_type in test_algorithms:
    try:
        print(f"[{test_num:2d}/25] Testing {alg_name}...", end=" ")
        
        # Call the appropriate function based on special requirements
        if special_type == "RSA":
            encrypted = func(TEST_STRING, rsa_pubkey)
        else:
            encrypted = func(TEST_STRING)
        
        # Validate the result
        if encrypted and len(encrypted) > 0:
            print("✓ SUCCESS")
            results.append({
                'Test_Number': test_num,
                'Algorithm_Name': alg_name,
                'Category': category,
                'Type': alg_type,
                'Special_Type': special_type,
                'Status': 'SUCCESS',
                'Encrypted_Length': len(encrypted),
                'Encrypted_Data_Preview': encrypted[:50] + "..." if len(encrypted) > 50 else encrypted
            })
            successful_tests += 1
        else:
            print("✗ FAILED - Empty result")
            results.append({
                'Test_Number': test_num,
                'Algorithm_Name': alg_name,
                'Category': category,
                'Type': alg_type,
                'Special_Type': special_type,
                'Status': 'FAILED',
                'Error': 'Empty result',
                'Encrypted_Length': 0,
                'Encrypted_Data_Preview': ''
            })
            failed_tests += 1
            
    except Exception as e:
        print(f"✗ FAILED - {str(e)}")
        results.append({
            'Test_Number': test_num,
            'Algorithm_Name': alg_name,
            'Category': category,
            'Type': alg_type,
            'Special_Type': special_type,
            'Status': 'FAILED',
            'Error': str(e),
            'Encrypted_Length': 0,
            'Encrypted_Data_Preview': ''
        })
        failed_tests += 1

# Print summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print(f"Total algorithms tested: 25")
print(f"Successful tests: {successful_tests}")
print(f"Failed tests: {failed_tests}")
print(f"Success rate: {(successful_tests/25)*100:.1f}%")

if failed_tests > 0:
    print("\n" + "=" * 80)
    print("FAILED TESTS DETAILS:")
    print("=" * 80)
    for result in results:
        if result['Status'] == 'FAILED':
            print(f"❌ {result['Algorithm_Name']} ({result['Category']}) - Error: {result.get('Error', 'Unknown error')}")

print("\n" + "=" * 80)
print("SUCCESSFUL TESTS DETAILS:")
print("=" * 80)
for result in results:
    if result['Status'] == 'SUCCESS':
        print(f"✅ [{result['Test_Number']:2d}] {result['Algorithm_Name']:20} | {result['Category']:12} | {result['Type']:12} | Length: {result['Encrypted_Length']:4d}")

print("\n" + "=" * 80)
print("SAMPLE ENCRYPTED OUTPUTS:")
print("=" * 80)
sample_count = 0
for result in results:
    if result['Status'] == 'SUCCESS':  # Show first 5 successful encryptions
        print(f"\n{result['Algorithm_Name']}:")
        print(f"  Preview: {result['Encrypted_Data_Preview']}")
        sample_count += 1

print(f"\n{'='*80}")
print("TEST COMPLETE!")
if successful_tests == 25:
    print("🎉 ALL ALGORITHMS WORKING PERFECTLY! Ready for full dataset processing.")
elif successful_tests >= 20:
    print("⚠️  Most algorithms working. Check failed tests before proceeding.")
else:
    print("❌ Multiple algorithm failures. Please fix issues before proceeding.")
print("=" * 80)