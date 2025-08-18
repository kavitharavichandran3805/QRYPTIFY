from datasets import load_dataset
import pandas as pd

dataset=load_dataset("wikitext", "wikitext-103-raw-v1")
texts=dataset["train"]["text"]
texts=[line for line in texts if line.strip()!=""][:1000]

df=pd.DataFrame({"plain_text":texts})

print(df.head())