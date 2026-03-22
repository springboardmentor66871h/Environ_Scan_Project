import pandas as pd
import numpy as np
import os
import zipfile
from sklearn.model_selection import train_test_split

# --- CONFIGURATION ---
BASE_DIR = r"C:\Users\ajayk\Environ_Scan_Project"
INPUT_FILE = os.path.join(BASE_DIR, "Processed", "final_labeled_dataset.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "Processed")

print("Loading the finalized dataset...")

if not os.path.exists(INPUT_FILE):
    print(f"Error: Could not find {INPUT_FILE}")
    exit()

# --- 1. LOAD DATA ---
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} rows.")

# --- 2. INJECT REALISTIC SENSOR NOISE ---
print("Injecting realistic random noise to simulate sensor inaccuracies...")

features = [
    'PM25', 'PM10', 'NO2', 'CO', 'SO2', 
    'Dist_Road_km', 'Dist_Industry_km', 'Dist_Dump_km', 'Dist_Farmland_km'
]

# Ensure data is numeric before calculating math
for col in features:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna()

# Add Gaussian noise
# The 0.15 multiplier means we are adding 15% random variance based on each column's standard deviation.
noise_level = 0.05

for col in features:
    col_std = df[col].std()
    # Generate random numbers centered at 0
    noise = np.random.normal(loc=0.0, scale=col_std * noise_level, size=len(df))
    df[col] = df[col] + noise
    
    # Ensure pollutants and distances do not drop below 0 due to the noise
    df[col] = df[col].clip(lower=0)

print(f"Noise injection complete. Noise level factor: {noise_level}")

# --- 3. TRAIN-TEST SPLIT (80% / 20%) ---
print("Splitting data into 80% Training and 20% Testing...")
train_df, test_df = train_test_split(
    df, test_size=0.20, random_state=42, stratify=df['POLLUTION_SOURCE']
)

# Helper function to save and zip
def save_and_zip(df_chunk, file_name):
    csv_path = os.path.join(OUTPUT_DIR, f"{file_name}.csv")
    zip_path = os.path.join(OUTPUT_DIR, f"{file_name}.zip")
    
    # Save CSV
    df_chunk.to_csv(csv_path, index=False)
    
    # Zip it to save space
    print(f"Zipping {file_name}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_path, arcname=os.path.basename(csv_path))
    
    # Delete the unzipped CSV
    os.remove(csv_path)
    print(f"Created: {zip_path} ({len(df_chunk)} rows)")

save_and_zip(train_df, "training_data")
save_and_zip(test_df, "testing_data")

print("SUCCESS! 'training_data.zip' and 'testing_data.zip' are ready with realistic noise.")