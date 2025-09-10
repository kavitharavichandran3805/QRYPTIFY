import pandas as pd
from Crypto.Cipher import AES,DES,DES3,Blowfish,ARC4,PKCS1_OAEP
from Crypto.PublicKey import RSA
from Twofish import TwoFish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
import os



dataset_path = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\processed_cleaned_file.csv"


df = pd.read_csv(dataset_path, header=None)
# print(df.head())
train_data = []
test_data = []

# def pad_data(data, block_size):
#     pad_len = block_size - (len(data.encode()) % block_size)
#     return data + chr(pad_len) * pad_len


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


def encrypt_aes_gcm(data: str) -> str:
    # print("Encrypting data using AES-GCM")
    key = get_random_bytes(16)  
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(key + cipher.nonce + tag + ciphertext).decode()


def encrypt_aes_cbc(data: str) -> str:
    # print("Encrypting data using AES-CBC")
    key = get_random_bytes(16)  
    cipher = AES.new(key, AES.MODE_CBC)
    padded_data=pad(data.encode(),AES.block_size)
    ciphertext=cipher.encrypt(padded_data,)
    return base64.b64encode(key + cipher.iv + ciphertext).decode()

def encrypt_des_cbc(data: str) -> str:
    # print("Encrypting data using DES-CBCP")
    key = get_random_bytes(8)  
    cipher = DES.new(key, DES.MODE_CBC)
    padded_data = pad(data.encode(), DES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(key + cipher.iv + ciphertext).decode()

def encrypt_3des_cbc(data: str) -> str:
    # print("Encrypting data using 3DES-CBC")
    key=get_random_bytes(24)
    key=DES3.adjust_key_parity(key)
    cipher=DES3.new(key,DES3.MODE_CBC)
    padded_data=pad(data.encode(),DES3.block_size)
    ciphertext=cipher.encrypt(padded_data)
    return base64.b64encode(key + cipher.iv + ciphertext).decode()

def encrypt_blowfish_ctr(data: str) -> str:
    # print("Encrypting data using BLOWFISH-CTR")
    key=get_random_bytes(16)
    nonce=get_random_bytes(4)
    cipher=Blowfish.new(key,Blowfish.MODE_CTR,nonce=nonce)
    ciphertext=cipher.encrypt(data.encode())
    return base64.b64encode(key + nonce + ciphertext).decode()

def encrypt_twofish_cbc(data: str) -> str:
    # print("Encrypting data using TWOFISH-CBC")
    key=get_random_bytes(16)
    hex_key=key.hex()
    plain=TwoFish.text_To_Hex(data)
    mode="CBC"
    ciphertext=TwoFish.TwoFish_encrypt(plain,hex_key,mode)
    return base64.b64encode(key + bytes.fromhex(ciphertext)).decode()

def encrypt_rc4(data: str) -> str:
    # print("Encrypting data using RC4")
    key=get_random_bytes(16)
    cipher=ARC4.new(key)
    ciphertext=cipher.encrypt(data.encode())
    return base64.b64encode(key + ciphertext).decode()


privateKey, publicKey = get_rsa_keys()

def encrypt_rsa_oaep_hybrid(data: str, publicKey) -> str:
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    padded_data = pad(data.encode(), AES.block_size)
    ciphertext_aes = cipher_aes.encrypt(padded_data)

    cipher_rsa = PKCS1_OAEP.new(publicKey)
    enc_aes_key = cipher_rsa.encrypt(aes_key)

    final_blob = enc_aes_key + cipher_aes.iv + ciphertext_aes
    return base64.b64encode(final_blob).decode()


def merge_train(df,first_write=False):
    mode='w' if first_write else 'a'
    header=True if first_write else False
    df.to_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\train.csv", mode=mode, index=False, header=header)

def merge_test(df,first_write=False):
    mode='w' if first_write else 'a'
    header=True if first_write else False
    df.to_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\test.csv", mode=mode, index=False, header=header)

for idx, row in df.iterrows():
    row_str = ','.join([str(i) for i in row.values])

    try:
        encrypted_data = encrypt_rsa_oaep_hybrid(row_str,publicKey)
        if idx % 100 == 0:
            print(f"Processed {idx} rows")
        if idx < 1000:
            train_data.append([encrypted_data, "Asymmetric","Hybrid", "Hybrid-RSA-OAEP-AES"])
        else:
            test_data.append([encrypted_data, "Asymmetric","Hybrid", "Hybrid-RSA-OAEP-AES"])
    except Exception as e:
        print(f"Encryption error on row {idx}: {e}")

train_df = pd.DataFrame(train_data, columns=["Encrypted_Data","Category", "Algorithm Type", "Algorithm"])
test_df = pd.DataFrame(test_data, columns=["Encrypted_Data","Category", "Algorithm Type", "Algorithm"])

merge_train(train_df)
merge_test(test_df)
