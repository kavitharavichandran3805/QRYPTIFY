import pandas as pd
import glob
import os

# Folder path where all CSVs are stored
folder_path = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\large_encrypted_dataset"

# Get list of all CSV files
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# Read and concatenate all CSVs
df = pd.concat((pd.read_csv(file) for file in csv_files), ignore_index=True)

# Save the merged DataFrame
df.to_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\large_encrypted_dataset\encrypted_merged_dataset.csv", index=False)

print(f"Merged {len(csv_files)} files successfully into 'merged_output.csv'")
