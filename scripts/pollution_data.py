
import pandas as pd

file_path = r"C:\Users\21ag1\Downloads\pollution dataset.zip"
df = pd.read_csv(file_path,encoding="latin1")

print(df.head())
df.to_csv("pollution_data.csv", index=False)
