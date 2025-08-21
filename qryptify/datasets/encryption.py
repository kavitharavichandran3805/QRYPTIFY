# import pandas as pd
# from Crypto.Cipher import AES, DES3
# from Crypto.Random import get_random_bytes
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
# # from pqcrypto.kem.kyber512 import generate_keypair, encapsulate, decapsulate
# import base64

# dataset_path=r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\processed_cleaned_file.csv"
# df=pd.read_csv(dataset_path,header=None)
# print(df.head())
# train_data=[]
# test_data=[]

# def pad_data(data,block_size):
#     if len(data.encode())%block_size!=0:
#         data+=' '
#     return data

# def encrypt_aes(data):
#     key=get_random_bytes(16)
#     cipher=AES.new(key,AES.MODE_ECB)
#     padded_data=pad_data(data,AES.block_size)
#     encrypted=cipher.encrypt(padded_data.encode())
#     return base64.b64encode(encrypted).decode()

        

# def merge_train(df):
#     df.to_csv("train.csv",mode='a',index=False,header=False)

# def merge_test(df):
#     df.to_csv("test.csv",mode='a',index=False,header=False)

# for idx,row in df.iterrows():
#     row_str=(',').join([str(i) for i in row.values()])

#     #AES
#     try:
#         encrypted_data=encrypt_aes(row_str)
#         if idx<1000:
#             train_data.append([encrypted_data,"Classical","AES"])
#         else:
#             test_data.append([encrypted_data,"Classical","AES"])
#     except Exception as e:
#         print("AES error")


# train_df=pd.DataFrame(train_data,columns=["Encrypted_Data","Algorithm Type","Algorithm"])
# test_df=pd.DataFrame(test_data,columns=["Encrypted_Data","Algorithm Type","Algorithm"])

# merge_train(train_df)
# merge_test(test_df)


import pandas as pd
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

dataset_path = r"D:\Final year project\QRYPTIFY\qryptify\datasets\processed_cleaned_file.csv"
df = pd.read_csv(dataset_path, header=None)
# print(df.head())
train_data = []
test_data = []

def pad_data(data, block_size):
    pad_len = block_size - (len(data.encode()) % block_size)
    return data + chr(pad_len) * pad_len

def encrypt_aes(data):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad_data(data, AES.block_size)
    encrypted = cipher.encrypt(padded_data.encode())
    return base64.b64encode(encrypted).decode()

def merge_train(df):
    df.to_csv("train.csv", mode='a', index=False, header=False)

def merge_test(df):
    df.to_csv("test.csv", mode='a', index=False, header=False)

for idx, row in df.iterrows():
    row_str = ','.join([str(i) for i in row.values])

    try:
        encrypted_data = encrypt_aes(row_str)
        if idx < 1000:
            train_data.append([encrypted_data, "Classical", "AES"])
        else:
            test_data.append([encrypted_data, "Classical", "AES"])
    except Exception as e:
        print(f"AES error on row {idx}: {e}")

train_df = pd.DataFrame(train_data, columns=["Encrypted_Data", "Algorithm Type", "Algorithm"])
test_df = pd.DataFrame(test_data, columns=["Encrypted_Data", "Algorithm Type", "Algorithm"])

merge_train(train_df)
merge_test(test_df)
