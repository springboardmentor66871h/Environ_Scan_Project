import pandas as pd
import numpy as np
import os

# --- CONFIGURATION ---
BASE_DIR = r"C:\Users\ajayk\Environ_Scan_Project"
INPUT_FILE = os.path.join(BASE_DIR, "Processed", "final_labeled_dataset.csv") 
OUTPUT_FILE = os.path.join(BASE_DIR, "Processed", "dataset_with_predictions.csv")

print("Generating Multi-City Geospatial Data...")

if not os.path.exists(INPUT_FILE):
    print(f"Error: Could not find {INPUT_FILE}")
    exit()

df = pd.read_csv(INPUT_FILE)

# --- 1. FIX COLUMN NAMES ---
if 'PM2.5' in df.columns:
    df['PM25'] = df['PM2.5']
if 'POLLUTION_SOURCE' not in df.columns and 'pollution_source' in df.columns:
    df['POLLUTION_SOURCE'] = df['pollution_source']

# --- 2. DYNAMIC MULTI-CITY COORDINATES ---
# Automatically find the city column (handles 'city', 'City', 'CITY')
city_col = next((col for col in df.columns if col.lower() == 'city'), None)

if city_col:
    unique_cities = df[city_col].unique()
    print(f"Found {len(unique_cities)} unique cities. Distributing them across the map...")
    
    city_coords = {}
    # Generate a unique, consistent base location (Roughly within India) for each city
    for city in unique_cities:
        # Use a seed based on the city name so it stays consistent every time you run it
        np.random.seed(abs(hash(str(city))) % (2**32 - 1)) 
        base_lat = np.random.uniform(10.0, 30.0)  # India's rough Latitude spread
        base_lon = np.random.uniform(70.0, 90.0)  # India's rough Longitude spread
        city_coords[city] = (base_lat, base_lon)
        
    lats = []
    lons = []
    
    # Assign the base coordinates + a small random scatter so markers don't overlap perfectly
    for index, row in df.iterrows():
        city_name = row[city_col]
        base_lat, base_lon = city_coords[city_name]
        lats.append(base_lat + np.random.uniform(-0.08, 0.08))
        lons.append(base_lon + np.random.uniform(-0.08, 0.08))
        
    df['Latitude'] = lats
    df['Longitude'] = lons

else:
    print("Warning: No 'city' column found! Spreading points randomly.")
    df['Latitude'] = np.random.uniform(10.0, 30.0, size=len(df))
    df['Longitude'] = np.random.uniform(70.0, 90.0, size=len(df))

# --- 3. SAVE ---
df.to_csv(OUTPUT_FILE, index=False)
print(f"Success! Multi-city geospatial file created at: {OUTPUT_FILE}")