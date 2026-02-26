import pandas as pd
import numpy as np
import os

print(" 1. Loading the 3 Datasets...")
try:
    # Ensure your file names match what is inside your /data/ folder!
    df_aq = pd.read_csv("data/India_Air_Quality.csv")
    df_weather = pd.read_csv("data/India_Weather.csv")
    
    # CHANGED: Loading the new Distances file instead of the Counts file
    df_spatial = pd.read_csv("data/India_Spatial_Distances.csv") 
except FileNotFoundError as e:
    print(f" Error: Could not find one of the CSV files. {e}")
    exit()

print(" 2. Standardizing Timestamps...")
# Ensure Pandas reads the timestamps identically in both files
df_aq['timestamp'] = pd.to_datetime(df_aq['timestamp'])
df_weather['timestamp'] = pd.to_datetime(df_weather['timestamp'])

print(" 3. Fusion Step 1: Merging Air Quality + Weather...")
# Inner join ensures we perfectly align the hours
df_master = pd.merge(df_aq, df_weather, on=['city', 'location', 'timestamp'], how='inner')

print(" 4. Fusion Step 2: Injecting Spatial Context (Distances)...")
# Drop the extraction timestamp from the spatial file so it doesn't overwrite our hourly timestamps
df_spatial_clean = df_spatial.drop(columns=['timestamp'], errors='ignore')

# Left join copies the static geography data across all thousands of hourly rows for that location
df_master = pd.merge(df_master, df_spatial_clean, on=['city', 'location'], how='left')

print(" 5. Engineering Temporal Machine Learning Features...")
# ML models love patterns! Let's extract the hour, day, and weekend status
df_master['hour'] = df_master['timestamp'].dt.hour
df_master['day_of_week'] = df_master['timestamp'].dt.dayofweek
df_master['month'] = df_master['timestamp'].dt.month
df_master['is_weekend'] = df_master['day_of_week'].isin([5, 6]).astype(int)

print("  6. Normalizing Data (Min-Max Scaling)...")
# Isolate all numeric columns that need to be scaled between 0.0 and 1.0 for the ML model
pollutants = ['pm25', 'pm10', 'no2', 'co', 'so2', 'o3']
weather = ['temperature_c', 'humidity_percent', 'pressure_hpa', 'wind_speed_mps']

# CHANGED: The script now dynamically normalizes any column containing 'dist_to_'
spatial = [col for col in df_spatial.columns if 'dist_to_' in col]

numeric_cols = pollutants + weather + spatial

# Create normalized versions of these columns
for col in numeric_cols:
    if col in df_master.columns:
        min_val, max_val = df_master[col].min(), df_master[col].max()
        if max_val > min_val:
            df_master[f'{col}_norm'] = (df_master[col] - min_val) / (max_val - min_val)
        else:
            df_master[f'{col}_norm'] = 0.0

print("7. Final Polish...")
# Round all numeric columns to 2 decimals for clean reading
df_master = df_master.round(2)

# This completely stops Excel from hiding the time or messing up the format!
df_master['timestamp'] = df_master['timestamp'].astype(str)
print(" 7. Final Polish...")
# Round all numeric columns to 2 decimals for clean reading
df_master = df_master.round(2)

# Save the final Master Dataset in BOTH formats
os.makedirs("data", exist_ok=True)

csv_output_path = "data/Combined_Dataset.csv"
excel_output_path = "data/Combined_Dataset.xlsx"

print("Saving as CSV (Optimized for Machine Learning speed)...")
df_master.to_csv(csv_output_path, index=False)

print("Saving as Excel (Optimized for human viewing and sharing)...")
df_master.to_excel(excel_output_path, index=False)

# This new print statement uses the correct variable names!
print(f"\nCombined dataset generated at both:\n 1. {csv_output_path}\n 2. {excel_output_path}")
print(f"Final Dataset Shape: {df_master.shape[0]} hourly rows, {df_master.shape[1]} columns")