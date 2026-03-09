import pandas as pd
import os

# Ensure processed folder exists
os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/pollution_data.csv")

print("Original Shape:", df.shape)
print("Columns:", df.columns)

# Fill missing values
df = df.ffill()

# Keep first 10000 rows
df = df.head(10000)

print("Cleaned Shape:", df.shape)
print(df.head())

# Save cleaned dataset
df.to_csv("data/processed/cleaned_data.csv", index=False)

print("Cleaned dataset saved successfully!")