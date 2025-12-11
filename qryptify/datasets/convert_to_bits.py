import pandas as pd
import base64
import os
# from google.colab import files  # ✅ for downloading in Colab

def convert_and_download_bits(file_path: str):
    """
    Converts 'Encrypted_Data' column from Base64 to bits,
    keeps other columns, saves as '<name>_bits.csv',
    and downloads it in Google Colab.
    Shows progress every 100 rows.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"\n🔹 Processing file: {os.path.basename(file_path)}")

    # Read CSV
    df = pd.read_csv(file_path)
    
    if "Encrypted_Data" not in df.columns:
        raise ValueError("The file does not contain an 'Encrypted_Data' column.")
    
    total_rows = len(df)
    print(f"   Total rows: {total_rows}")

    # Function to convert Base64 → bits
    def to_bits_with_progress(index, b64_data):
        if index % 100 == 0 and index != 0:
            print(f"   ✅ {index}/{total_rows} rows converted...")
        try:
            cipher_bytes = base64.b64decode(b64_data)
            return ''.join(f'{byte:08b}' for byte in cipher_bytes)
        except Exception:
            return b64_data  # leave as is if not decodable

    # Convert column with progress
    df["Encrypted_Data"] = [
        to_bits_with_progress(i, val) for i, val in enumerate(df["Encrypted_Data"])
    ]
    
    # Save new file with "_bits" suffix
    new_path = file_path.replace(".csv", "_bits.csv")
    df.to_csv(new_path, index=False)
    print(f"✅ Finished converting: {os.path.basename(file_path)}")
    print(f"📄 Saved as: {new_path}")

    # Download the file in Colab
    # files.download(new_path)
    print("⬇️ File ready for download.\n")


# -----------------------------------------------
# MAIN SCRIPT
# -----------------------------------------------

folder = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\large_encrypted_dataset"

# 🛑 Add file names you want to SKIP here:
skip_files = {
    "camellia.csv",
    "aes_ctr.csv",
    "caesar.csv",
    "cast.csv",
    "chacha20.csv"
}

for fname in os.listdir(folder):
    if fname.endswith(".csv"):
        if fname in skip_files:
            print(f"⏩ Skipping file: {fname}")
            continue
        convert_and_download_bits(os.path.join(folder, fname))
