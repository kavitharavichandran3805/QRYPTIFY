import pandas as pd
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64


dataset_path = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\processed_cleaned_file.csv"


df = pd.read_csv(dataset_path, header=None)
# print(df.head())
train_data = []
test_data = []

# def pad_data(data, block_size):
#     pad_len = block_size - (len(data.encode()) % block_size)
#     return data + chr(pad_len) * pad_len

def encrypt_aes_gcm(data: str) -> str:
    key = get_random_bytes(16)  
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(key + cipher.nonce + tag + ciphertext).decode()


def encrypt_aes_cbc(data: str) -> str:
    key = get_random_bytes(16)  
    cipher = AES.new(key, AES.MODE_CBC)
    padded_data=pad(data.encode(),AES.block_size)
    ciphertext=cipher.encrypt(padded_data,)
    return base64.b64encode(key + cipher.iv + ciphertext).decode()

def encrypt_des_cbc(data: str) -> str:
    key = get_random_bytes(8)  
    cipher = DES.new(key, DES.MODE_CBC)
    padded_data = pad(data.encode(), DES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(key + cipher.iv + ciphertext).decode()

def merge_train(df,first_write=False):
    mode='w' if first_write else 'a'
    header=True if first_write else False
    df.to_csv("train.csv", mode=mode, index=False, header=header)

def merge_test(df,first_write=False):
    mode='w' if first_write else 'a'
    header=True if first_write else False
    df.to_csv("test.csv", mode=mode, index=False, header=header)

for idx, row in df.iterrows():
    row_str = ','.join([str(i) for i in row.values])

    try:
        encrypted_data = encrypt_des_cbc(row_str)
        if idx % 100 == 0:
            print(f"Processed {idx} rows")
        if idx < 1000:
            train_data.append([encrypted_data, "Symmetric (Block)","Classical", "DES-CBC"])
        else:
            test_data.append([encrypted_data, "Symmetric (Block)","Classical", "DES-CBC"])
    except Exception as e:
        print(f"Encryption error on row {idx}: {e}")

train_df = pd.DataFrame(train_data, columns=["Encrypted_Data","Category", "Algorithm Type", "Algorithm"])
test_df = pd.DataFrame(test_data, columns=["Encrypted_Data","Category", "Algorithm Type", "Algorithm"])

merge_train(train_df)
merge_test(test_df)
