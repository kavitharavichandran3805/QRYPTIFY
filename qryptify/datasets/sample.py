import pandas as pd

df=pd.read_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\train.csv")
# df.to_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\test.csv", index=True)

# df.iloc[1000:1200, df.columns.get_loc('Algorithm')] = 'Twofish-CBC'
print(df.columns)
df = df.drop(columns=[ 'Unnamed: 0'])
df.to_csv(r"C:\\Users\\Dell\\Desktop\\DESKTOP_FOLDER\\FINAL YEAR PROJECT\\qryptify\\datasets\\train.csv", index=False)

