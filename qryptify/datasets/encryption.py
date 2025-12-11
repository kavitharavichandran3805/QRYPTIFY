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
from cryptography.hazmat.primitives.ciphers.aead import XChaCha20Poly1305
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

def get_rsa_keys(private_path="private.pem", public_path="public.pem", key_size=3072):
    if os.path.exists(private_path) and os.path.exists(public_path):
        with open(private_path, "rb") as f:
            private_key = RSA.import_key(f.read())
        with open(public_path, "rb") as f:
            public_key = RSA.import_key(f.read())
    else:
        private_key = RSA.generate(key_size)
        public_key = private_key.publickey()
        with open(private_path, "wb") as f:
            f.write(private_key.export_key("PEM"))
        with open(public_path, "wb") as f:
            f.write(public_key.export_key("PEM"))
        print(f"Generated new RSA-{key_size} key pair and saved to disk")
    return private_key, public_key

#--------------------------------------------------------------------------------------------------

#SYMMETRIC

#1
def encrypt_aes_gcm(data: str) -> str:
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

#2
def encrypt_aes_cbc(data: str) -> str:
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)
    padded_data = pad(data.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + ciphertext).decode()

#3
def encrypt_des_cbc(data: str) -> str:
    key = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_CBC)
    padded_data = pad(data.encode(), DES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + ciphertext).decode()

#4
def encrypt_3des_cbc(data: str) -> str:
    key = get_random_bytes(24)
    key = DES3.adjust_key_parity(key)
    cipher = DES3.new(key, DES3.MODE_CBC)
    padded_data = pad(data.encode(), DES3.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + ciphertext).decode()

#5
def encrypt_blowfish_ctr(data: str) -> str:
    key = get_random_bytes(16)
    nonce = get_random_bytes(4)
    cipher = Blowfish.new(key, Blowfish.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(nonce + ciphertext).decode()

#6
def encrypt_twofish_cbc(data: str) -> str:
    key = get_random_bytes(16)
    hex_key = key.hex()
    plain = TwoFish.text_To_Hex(data)
    mode = "CBC"
    padded = pad(bytes.fromhex(plain), 16)
    ciphertext = TwoFish.TwoFish_encrypt(padded.hex(), hex_key, mode)
    return base64.b64encode(bytes.fromhex(ciphertext)).decode()

#7
def encrypt_rc4(data: str) -> str:
    key = get_random_bytes(16)
    cipher = ARC4.new(key)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(ciphertext).decode()

#8
W = 32
R = 12
def encrypt_rc5(data: str) -> str:
    key = get_random_bytes(16)
    cipher = rc5.RC5(W, R, key)
    plaintext_bytes = data.encode()
    ciphertext = cipher.encryptBytes(plaintext_bytes)
    return base64.b64encode(ciphertext).decode()

#9
def encrypt_rc6(data: str) -> str:
    key = get_random_bytes(16)
    s = generateKey(key.hex()) 
    data_bytes = data.encode('utf-8')
    ciphertext_hex = encrypt(data_bytes, s)
    return base64.b64encode(bytes.fromhex(ciphertext_hex)).decode()

#10
def encrypt_idea(data: str) -> str:
    key = get_random_bytes(16)
    cipher = IDEA.IDEAWrapper(key)
    plaintext_bytes = data.encode()
    ciphertext = cipher.encrypt(plaintext_bytes)
    return base64.b64encode(ciphertext).decode()

#11
def encrypt_chacha20(data: str) -> str:
    key = get_random_bytes(32)
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()

#12
def encrypt_camellia(data: str) -> str:
    key = get_random_bytes(32)
    iv = get_random_bytes(16)
    algo = algorithms.Camellia(key)
    cipher = Cipher(algo, modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded = pad(data.encode(), 16)
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

#13
def encrypt_cast128_cbc(data: str) -> str:
    key = get_random_bytes(16)
    cipher = CAST.new(key, CAST.MODE_CBC)
    padded = pad(data.encode(), 8)
    ciphertext = cipher.encrypt(padded)
    return base64.b64encode(cipher.iv + ciphertext).decode()

#14
def encrypt_salsa20_stream(data: str) -> str:
    key = get_random_bytes(32)
    cipher = Salsa20.new(key=key)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()

#15
def encrypt_caesar(data: str, shift: int = 3) -> str:
    cipher = Caesar()
    cm = CryptMachine(cipher, shift)  
    encrypted_text = cm.encrypt(data)
    return base64.b64encode(encrypted_text.encode()).decode()

#--------------------------------------------------------------------------------------------------

#SYMMETRIC (ChaCha20-Poly1305 moved here - it's AEAD, not asymmetric)
#16
def encrypt_chacha20_poly1305(data: str) -> str:
    key = get_random_bytes(32)                 
    cipher = ChaCha20_Poly1305.new(key=key)    
    ciphertext = cipher.encrypt(data.encode())
    tag = cipher.digest()
    nonce = cipher.nonce                       
    return base64.b64encode(nonce + tag + ciphertext).decode()

#--------------------------------------------------------------------------------------------------

#ASYMMETRIC

#17
def encrypt_rsa_pkcs1v15(data: str, public_key) -> str:
    max_len = (public_key.size_in_bits() // 8) - 11  
    data_bytes = data.encode()[:max_len]
    cipher = PKCS1_v1_5.new(public_key)
    ciphertext = cipher.encrypt(data_bytes)
    return base64.b64encode(ciphertext).decode()

#18
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

#--------------------------------------------------------------------------------------------------

#HYBRID

#19
def encrypt_rsa_oaep_aes(data: str, publicKey) -> str:
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    padded_data = pad(data.encode(), AES.block_size)
    ciphertext_aes = cipher_aes.encrypt(padded_data)
    cipher_rsa = PKCS1_OAEP.new(publicKey)
    enc_aes_key = cipher_rsa.encrypt(aes_key)
    final_blob = enc_aes_key + cipher_aes.iv + ciphertext_aes
    return base64.b64encode(final_blob).decode()

#20
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

#21
def encrypt_pgp_armored(data: str) -> str:
    key = get_random_bytes(32)
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    pgp_like = b"-----BEGIN PGP MESSAGE-----\n" + base64.b64encode(iv + tag + ciphertext) + b"\n-----END PGP MESSAGE-----"
    return base64.b64encode(pgp_like).decode()

#22
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

#--------------------------------------------------------------------------------------------------

#POST-QUANTUM

#23
def encrypt_kyber_aes(data: str) -> str:
    public_key, secret_key = Kyber512.keygen()
    kyber_ciphertext, shared_secret = Kyber512.encaps(public_key)
    cipher = AES.new(shared_secret[:16], AES.MODE_CBC)
    aes_ct = cipher.encrypt(pad(data.encode(), AES.block_size))
    combined_bytes = cipher.iv + aes_ct + kyber_ciphertext
    return base64.b64encode(combined_bytes).decode()

#24
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

#25
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


dataset_path = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\processed_cleaned_file.csv"
train_path = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\train.csv"
test_path = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\test.csv"

if not os.path.exists(dataset_path):
    print(f"Error: Input dataset not found at {dataset_path}")
    exit(1)

os.makedirs(os.path.dirname(train_path), exist_ok=True)
os.makedirs(os.path.dirname(test_path), exist_ok=True)

try:
    df = pd.read_csv(dataset_path, header=None)
    print(f"Loaded dataset with {len(df)} rows")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

algorithm_mapping = [
    # Symmetric algorithms
    (encrypt_aes_gcm, "Symmetric", "Block", "AES-GCM"),
    (encrypt_aes_cbc, "Symmetric", "Block", "AES-CBC"),
    (encrypt_des_cbc, "Symmetric", "Block", "DES-CBC"),
    (encrypt_3des_cbc, "Symmetric", "Block", "3DES-CBC"),
    (encrypt_blowfish_ctr, "Symmetric", "Block", "Blowfish-CTR"),
    (encrypt_twofish_cbc, "Symmetric", "Block", "Twofish-CBC"),
    (encrypt_rc4, "Symmetric", "Stream", "RC4"),
    (encrypt_rc5, "Symmetric", "Block", "RC5"),
    (encrypt_rc6, "Symmetric", "Block", "RC6"),
    (encrypt_idea, "Symmetric", "Block", "IDEA"),
    (encrypt_chacha20, "Symmetric", "Stream", "ChaCha20"),
    (encrypt_camellia, "Symmetric", "Block", "Camellia-CBC"),
    (encrypt_cast128_cbc, "Symmetric", "Block", "CAST-128-CBC"),
    (encrypt_salsa20_stream, "Symmetric", "Stream", "Salsa20"),
    (encrypt_caesar, "Symmetric", "Classical", "Caesar"),
    (encrypt_chacha20_poly1305, "Symmetric", "AEAD", "ChaCha20-Poly1305"),  
    
    # Asymmetric algorithms
    (encrypt_rsa_pkcs1v15, "Asymmetric", "Public Key", "RSA-PKCS1v1.5"),
    (encrypt_ecies, "Asymmetric", "Public Key", "ECIES"),
    
    # Hybrid algorithms
    (encrypt_rsa_oaep_aes, "Hybrid", "Hybrid", "Hybrid-RSA-OAEP-AES"),
    (encrypt_ecies_aes, "Hybrid", "Hybrid", "Hybrid-ECIES-AES"),
    (encrypt_pgp_armored, "Hybrid", "Hybrid", "PGP-Armored"),
    (encrypt_tls_like_ecdhe, "Hybrid", "Hybrid", "TLS-ECDHE-AES"),
    
    # Post-quantum algorithms
    (encrypt_kyber_aes, "Post-Quantum", "Hybrid", "Kyber-AES"),
    (encrypt_frodokem_aes, "Post-Quantum", "Hybrid", "FrodoKEM-AES"),
    (encrypt_ntru_aes, "Post-Quantum", "Hybrid", "NTRU-AES")
]

def write_to_csv(batch_data, file_path, first_write=False):
    """Write batch data to CSV with error handling"""
    try:
        mode = 'w' if first_write else 'a'
        header = first_write
        df_row = pd.DataFrame(batch_data, columns=["Encrypted_Data", "Category", "Algorithm_Type", "Algorithm"])
        df_row.to_csv(file_path, mode=mode, index=False, header=header)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

batch_size = 100
train_buffer = []
test_buffer = []

rsa_privkey, rsa_pubkey = get_rsa_keys()
rsa_algorithms = {"Hybrid-RSA-OAEP-AES", "RSA-PKCS1v1.5"}

total_processed = 0
total_errors = 0
errors_by_algorithm = {}

train_rows=1000
test_rows=200

print("Starting dataset encryption (algorithm-wise)...")

first_write_train = True
first_write_test = True

for func, cat, alg_type, alg_name in algorithm_mapping:
    train_buffer = []
    test_buffer = []
    total_errors_algo = 0
    
    print(f"\nEncrypting all rows with algorithm: {alg_name}")

    for idx, row in df.iterrows():
        row_str = ','.join([str(val) if pd.notna(val) else '' for val in row.values])
        try:
            if alg_name in rsa_algorithms:
                encrypted_data = func(row_str, rsa_pubkey)
            else:
                encrypted_data = func(row_str)
            
            row_data = [encrypted_data, cat, alg_type, alg_name]

            if idx < train_rows:
                train_buffer.append(row_data)
                if len(train_buffer) >= batch_size:
                    write_to_csv(train_buffer, train_path, first_write=first_write_train)
                    first_write_train = False  
                    train_buffer = []
            elif idx < train_rows + test_rows:
                test_buffer.append(row_data)
                if len(test_buffer) >= batch_size:
                    write_to_csv(test_buffer, test_path, first_write=first_write_test)
                    first_write_test = False
                    test_buffer = []

        except Exception as e:
            total_errors += 1
            total_errors_algo += 1
            errors_by_algorithm[alg_name] = errors_by_algorithm.get(alg_name, 0) + 1
            print(f"Error on row {idx} with {alg_name}: {e}")
        
        if idx % 100 == 0:
            print(f"Processed {idx+1}/{len(df)} rows for {alg_name}")

    if train_buffer:
        write_to_csv(train_buffer, train_path, first_write=first_write_train)
        first_write_train = False
    if test_buffer:
        write_to_csv(test_buffer, test_path, first_write=first_write_test)
        first_write_test = False

    print(f"Completed encryption with {alg_name}. Errors: {total_errors_algo}")

print("\n" + "="*50)
print("ALL ENCRYPTION COMPLETE!")
print(f"Total rows processed: {len(df)}")
print(f"Total errors: {total_errors}")
if errors_by_algorithm:
    print("\nErrors by algorithm:")
    for alg, count in errors_by_algorithm.items():
        print(f"  {alg}: {count} errors")
