import pandas as pd
import numpy as np
import os
import zipfile

# --- CONFIGURATION ---
INPUT_FILE = "data/processed/india_master_processed.csv"  # The unzipped CSV
OUTPUT_DIR = "data/processed"

print("⏳ Loading the massive dataset (this may take a moment)...")

if not os.path.exists(INPUT_FILE):
    print(f"❌ Error: Could not find {INPUT_FILE}")
    print("   If you deleted the CSV, please unzip your previous zip file to recover it first.")
    exit()

# Load Data
df = pd.read_csv(INPUT_FILE)
total_rows = len(df)
print(f"   Loaded {total_rows} rows.")

# Split into 2 chunks
chunk_size = int(total_rows / 2) + 1
df_part1 = df.iloc[:chunk_size]
df_part2 = df.iloc[chunk_size:]

print("✂️ Splitting data...")

# Save Part 1
file1 = os.path.join(OUTPUT_DIR, "india_part1.csv")
df_part1.to_csv(file1, index=False)
print(f"   Saved Part 1: {len(df_part1)} rows")

# Save Part 2
file2 = os.path.join(OUTPUT_DIR, "india_part2.csv")
df_part2.to_csv(file2, index=False)
print(f"   Saved Part 2: {len(df_part2)} rows")

# Zip them automatically to save space
print("📦 Zipping files...")

def zip_file(csv_path):
    zip_name = csv_path.replace(".csv", ".zip")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_path, arcname=os.path.basename(csv_path))
    print(f"   Created: {zip_name}")
    os.remove(csv_path) # Remove the raw CSV to save space

zip_file(file1)
zip_file(file2)

print("✅ SUCCESS! You now have 'india_part1.zip' and 'india_part2.zip'.")