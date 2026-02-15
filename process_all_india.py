import pandas as pd
import numpy as np
import os
import glob
import difflib

# --- CONFIGURATION ---
ROOT_DATA_DIR = "data/raw/India_Air_Quality_2024_Raw"
OUTPUT_FILE = "data/processed/india_master_processed.csv"

FINAL_COLUMNS = [
    'state', 'city', 'latitude', 'longitude', 'timestamp',
    'pm25', 'pm10', 'no2', 'co', 'so2', 'o3',
    'temperature', 'humidity', 'wind_speed', 'wind_direction',
    'distance_to_road', 'distance_to_industry', 'distance_to_dump', 'distance_to_farmland'
]

print(f"🚀 Starting National Data Processing from: {ROOT_DATA_DIR}")
all_data = []

# 1. Walk through every State
if not os.path.exists(ROOT_DATA_DIR):
    print(f"❌ Error: Root folder not found: {ROOT_DATA_DIR}")
    exit()

for state in os.listdir(ROOT_DATA_DIR):
    state_path = os.path.join(ROOT_DATA_DIR, state)
    
    if os.path.isdir(state_path):
        # 2. Find the two subfolders (Handling typos like 'Polluants' or 'Metrological Dats')
        subfolders = os.listdir(state_path)
        poll_folder_name = next((s for s in subfolders if "pollu" in s.lower()), None)
        met_folder_name = next((s for s in subfolders if "metro" in s.lower() or "weather" in s.lower()), None)
        
        if poll_folder_name and met_folder_name:
            poll_path = os.path.join(state_path, poll_folder_name)
            met_path = os.path.join(state_path, met_folder_name)
            
            # 3. Iterate through Pollution Files (Primary)
            poll_files = glob.glob(os.path.join(poll_path, "*.csv"))
            
            for p_file in poll_files:
                city_filename = os.path.basename(p_file) # e.g., "Mysuru.csv"
                city_name = os.path.splitext(city_filename)[0] # "Mysuru"
                
                # 4. Find corresponding Weather File
                # We assume it has the same name "Mysuru.csv" inside the Met folder
                w_file = os.path.join(met_path, city_filename)
                
                if os.path.exists(w_file):
                    print(f"   Processing: {city_name}, {state}...")
                    
                    try:
                        # 5. Extract Metadata (Lat/Lon) from Weather File
                        # (Reading line 2 for coordinates)
                        lat, lon = np.nan, np.nan
                        with open(w_file, 'r') as f:
                            lines = f.readlines()
                            if len(lines) > 1:
                                parts = lines[1].split(',')
                                try:
                                    lat = float(parts[0])
                                    lon = float(parts[1])
                                except:
                                    pass

                        # 6. Read Data
                        # Pollution file usually has headers on line 1
                        df_poll = pd.read_csv(p_file)
                        
                        # Weather file usually has headers on line 4 (skip 3)
                        df_weather = pd.read_csv(w_file, skiprows=3)
                        
                        # 7. Standardize Columns
                        # Weather Mapping
                        df_weather.rename(columns={
                            'time': 'timestamp',
                            'temperature_2m (°C)': 'temperature',
                            'relative_humidity_2m (%)': 'humidity',
                            'wind_speed_10m (km/h)': 'wind_speed',
                            'wind_direction_10m (°)': 'wind_direction'
                        }, inplace=True)
                        
                        # Pollution Mapping
                        df_poll.rename(columns={
                            'Timestamp': 'timestamp',
                            'PM2.5 (µg/m³)': 'pm25',
                            'PM10 (µg/m³)': 'pm10',
                            'NO2 (µg/m³)': 'no2',
                            'SO2 (µg/m³)': 'so2',
                            'CO (mg/m³)': 'co',
                            'Ozone (µg/m³)': 'o3'
                        }, inplace=True)

                        # 8. Merge
                        # Create join key (YYYY-MM-DD HH)
                        df_poll['join_key'] = df_poll['timestamp'].astype(str).str[:13]
                        df_weather['join_key'] = df_weather['timestamp'].astype(str).str[:13].str.replace('T', ' ')
                        
                        merged = pd.merge(df_poll, df_weather, left_on='join_key', right_on='join_key', suffixes=('', '_y'))
                        
                        # 9. Add Features
                        merged['state'] = state
                        merged['city'] = city_name
                        merged['latitude'] = lat
                        merged['longitude'] = lon
                        
                        # Simulated Geospatial Data (for Milestone 1)
                        np.random.seed(len(city_name))
                        merged['distance_to_road'] = np.random.uniform(50, 800, len(merged))
                        merged['distance_to_industry'] = np.random.uniform(1000, 5000, len(merged))
                        merged['distance_to_dump'] = np.random.uniform(2000, 10000, len(merged))
                        merged['distance_to_farmland'] = np.random.uniform(500, 4000, len(merged))

                        # Select Final Columns
                        for col in FINAL_COLUMNS:
                            if col not in merged.columns:
                                merged[col] = np.nan
                        
                        all_data.append(merged[FINAL_COLUMNS])

                    except Exception as e:
                        print(f"      ❌ Error {city_name}: {e}")
                else:
                    # Weather file missing
                    pass

# 10. Save Master File
if all_data:
    print("💾 Combining all cities...")
    master_df = pd.concat(all_data, ignore_index=True)
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    master_df.to_csv(OUTPUT_FILE, index=False)
    
    print("------------------------------------------------")
    print(f"✅ SUCCESS! Processed {len(all_data)} cities.")
    print(f"📊 Total Rows: {len(master_df)}")
    print(f"📂 Saved to: {OUTPUT_FILE}")
    print("------------------------------------------------")
else:
    print("❌ No matches found. Check folder names manually.")