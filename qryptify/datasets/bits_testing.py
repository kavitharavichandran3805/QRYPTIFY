# import pandas as pd

# algorithms_dict = {
#     "AES-GCM": 0,
#     "AES-CBC": 0,
#     "DES-CBC": 0,
#     "3DES-CBC": 0,
#     "Blowfish-CTR": 0,
#     "Twofish-CBC": 0,
#     "RC4": 0,
#     "RC5": 0,
#     "RC6": 0,
#     "IDEA": 0,
#     "ChaCha20": 0,
#     "Camellia-CBC": 0,
#     "CAST-128-CBC": 0,
#     "Salsa20": 0,
#     "Caesar": 0,
#     "ChaCha20-Poly1305": 0,
#     "RSA-PKCS1v1.5": 0,
#     "ECIES": 0,
#     "Hybrid-RSA-OAEP-AES": 0,
#     "Hybrid-ECIES-AES": 0,
#     "PGP-Armored": 0,
#     "TLS-ECDHE-AES": 0,
#     "Kyber-AES": 0,
#     "FrodoKEM-AES": 0,
#     "NTRU-AES": 0
# }

# def cipher_to_bits(text):
#     bits=''.join(f'{ord(c):08b}' for c in text)
#     return len(bits)


# df=pd.read_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\train.csv")
# total_rows=len(df)

# for i,row in df.iterrows():
#     length=cipher_to_bits(row["Encrypted_Data"])
#     if length<1000000:
#         algorithms_dict[row["Algorithm"]]+=1
#     if i%100 ==0:
#         print(f"Processed rows : {i}/{total_rows}")
# print(algorithms_dict)


import pandas as pd

# Helper function to convert text to bits
def cipher_to_bits(text):
    return len(''.join(f'{ord(c):08b}' for c in text))

# Read your dataset
df = pd.read_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\train.csv")

# Prepare a list to store new data
data_list = []

total_rows = len(df)

for i, row in df.iterrows():
    ciphertext = row["Encrypted_Data"]        # your ciphertext column
    algorithm = row["Algorithm"]             # your algorithm column
    num_bits = cipher_to_bits(ciphertext)    # calculate number of bits
    
    data_list.append({
        "Ciphertext": ciphertext,
        "Algorithm": algorithm,
        "Num_Bits": num_bits
    })
    
    if i % 100 == 0:
        print(f"Processed rows: {i}/{total_rows}")

# Create new DataFrame
df_bits = pd.DataFrame(data_list)

# Save to CSV if needed
df_bits.to_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\train_bits.csv", index=False)

print(df_bits.head())
