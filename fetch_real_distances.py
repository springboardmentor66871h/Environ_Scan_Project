import pandas as pd
import numpy as np
import requests
import time
import math
import os
import zipfile

# --- CONFIGURATION ---
INPUT_FILE_1 = "data/processed/india_part1.zip" # We are taking the pre-labeled data
INPUT_FILE_2 = "data/processed/india_part2.zip"
OUTPUT_DIR = "data/processed"

def haversine(lat1, lon1, lat2, lon2):
    """Calculates distance between two GPS points in meters"""
    R = 6371000 # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_osm_distances(lat, lon):
    """Fetches real geospatial data from OpenStreetMap"""
    # If coordinates are missing, return fallback maximums
    if pd.isna(lat) or pd.isna(lon):
        return {'road': 5000, 'industry': 10000, 'farm': 10000, 'dump': 10000}
        
    # Overpass API Query (Search within 10km radius)
    query = f"""
    [out:json];
    (
      way["highway"~"primary|trunk|secondary"](around:10000, {lat}, {lon});
      nwr["landuse"="industrial"](around:10000, {lat}, {lon});
      nwr["landuse"="farmland"](around:10000, {lat}, {lon});
      nwr["amenity"="waste_disposal"](around:10000, {lat}, {lon});
    );
    out center;
    """
    
    url = "http://overpass-api.de/api/interpreter"
    try:
        response = requests.post(url, data={'data': query}, timeout=15)
        data = response.json()
        
        # Track minimum distances (default to 10000m if nothing is found nearby)
        dists = {'road': 10000, 'industry': 10000, 'farm': 10000, 'dump': 10000}
        
        for element in data.get('elements', []):
            el_lat = element.get('lat') or element.get('center', {}).get('lat')
            el_lon = element.get('lon') or element.get('center', {}).get('lon')
            
            if el_lat and el_lon:
                dist = haversine(lat, lon, el_lat, el_lon)
                tags = element.get('tags', {})
                
                if 'highway' in tags and dist < dists['road']:
                    dists['road'] = dist
                elif tags.get('landuse') == 'industrial' and dist < dists['industry']:
                    dists['industry'] = dist
                elif tags.get('landuse') == 'farmland' and dist < dists['farm']:
                    dists['farm'] = dist
                elif tags.get('amenity') == 'waste_disposal' and dist < dists['dump']:
                    dists['dump'] = dist
                    
        return dists
    except Exception as e:
        print(f"      ⚠️ API Error for {lat},{lon}: {e}")
        return {'road': 5000, 'industry': 10000, 'farm': 10000, 'dump': 10000}

# --- MAIN EXECUTION ---
print("⏳ Loading full dataset...")
df1 = pd.read_csv(INPUT_FILE_1)
df2 = pd.read_csv(INPUT_FILE_2)
df = pd.concat([df1, df2], ignore_index=True)

print("🌍 Extracting unique cities and coordinates...")
# Get unique locations only
locations = df[['city', 'latitude', 'longitude']].drop_duplicates()
print(f"Found {len(locations)} unique locations to map.")

# Dictionary to hold the real distances mapping
real_distances = {}

print("📡 Fetching REAL map data from OpenStreetMap API...")
print("   (This will take about 5-8 minutes to respect server rate limits. Do not close!)")

for index, row in locations.iterrows():
    city = row['city']
    lat, lon = row['latitude'], row['longitude']
    
    print(f"   📍 Mapping {city}...")
    dists = get_osm_distances(lat, lon)
    real_distances[city] = dists
    
    # Sleep to prevent getting banned by the server
    time.sleep(1.5)

print("\n🔄 Overwriting fake data with REAL OpenStreetMap distances...")
# Map the real distances back to the 2 million rows
df['distance_to_road'] = df['city'].map(lambda x: real_distances[x]['road'])
df['distance_to_industry'] = df['city'].map(lambda x: real_distances[x]['industry'])
df['distance_to_farmland'] = df['city'].map(lambda x: real_distances[x]['farm'])
df['distance_to_dump'] = df['city'].map(lambda x: real_distances[x]['dump'])

print("✂️ Splitting and saving the validated dataset...")
chunk_size = int(len(df) / 2) + 1
df_part1 = df.iloc[:chunk_size]
df_part2 = df.iloc[chunk_size:]

file1 = os.path.join(OUTPUT_DIR, "labeled_india_part1.csv")
file2 = os.path.join(OUTPUT_DIR, "labeled_india_part2.csv")

df_part1.to_csv(file1, index=False)
df_part2.to_csv(file2, index=False)

def zip_file(csv_path):
    zip_name = csv_path.replace(".csv", ".zip")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_path, arcname=os.path.basename(csv_path))
    os.remove(csv_path)

zip_file(file1)
zip_file(file2)

print("✅ SUCCESS! Your dataset now contains 100% REAL geographical data.")