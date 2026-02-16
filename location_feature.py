import osmnx as ox
import pandas as pd
import os
import warnings
from datetime import datetime

# Suppress OSMnx UserWarnings for clean terminal output
warnings.filterwarnings('ignore')

# Master Location Dictionary
locations = {
    "Delhi": {
        "Anand_Vihar": {"lat": 28.6508, "lon": 77.3152},
        "RK_Puram": {"lat": 28.5632, "lon": 77.1869},
        "ITO": {"lat": 28.6284, "lon": 77.2410},
        "Punjabi_Bagh": {"lat": 28.6683, "lon": 77.1167},
        "Bawana": {"lat": 28.7955, "lon": 77.0324}
    },
    "Mumbai": {
        "Colaba": {"lat": 18.9067, "lon": 72.8147},
        "Worli": {"lat": 19.0163, "lon": 72.8166}
    },
    "Bengaluru": {
        "Peenya_Industrial": {"lat": 13.0285, "lon": 77.5197},
        "Silk_Board": {"lat": 12.9172, "lon": 77.6228}
    }
}

# CHANGED: The radius around the sensor to scan (5000 meters = 5km)
RADIUS = 5000 
extraction_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
all_features = []

print(f"Starting OSMnx Spatial Extraction ({RADIUS/1000}km radius)... This may take a few minutes.")

for city, loc_data in locations.items():
    print(f"\n========== Scanning {city} ==========")
    
    for loc_name, meta in loc_data.items():
        print(f" Extracting geography for {loc_name}...")
        point = (meta['lat'], meta['lon'])
        
        # Base dictionary for this location (Updated to 5km)
        features = {
            "city": city,
            "location": loc_name,
            "latitude": meta['lat'],
            "longitude": meta['lon'],
            "timestamp": extraction_timestamp,
            "major_roads_within_5km": 0,
            "industrial_zones_within_5km": 0,
            "farmland_within_5km": 0,
            "waste_dumps_within_5km": 0
        }
        
        # 1. ROADS (Major traffic arteries only)
        try:
            tags_roads = {'highway': ['trunk', 'primary', 'secondary', 'motorway']}
            roads = ox.features_from_point(point, tags=tags_roads, dist=RADIUS)
            features["major_roads_within_5km"] = len(roads)
        except Exception: pass
        
        # 2. INDUSTRIAL ZONES
        try:
            tags_ind = {'landuse': ['industrial', 'brownfield']}
            industrial = ox.features_from_point(point, tags=tags_ind, dist=RADIUS)
            features["industrial_zones_within_5km"] = len(industrial)
        except Exception: pass

        # 3. AGRICULTURAL / FARMLAND
        try:
            tags_farm = {'landuse': ['farmland', 'orchard', 'plant_nursery']}
            farm = ox.features_from_point(point, tags=tags_farm, dist=RADIUS)
            features["farmland_within_5km"] = len(farm)
        except Exception: pass

        # 4. WASTE DUMPS / LANDFILLS
        try:
            tags_waste = {'landuse': ['landfill'], 'amenity': ['waste_disposal']}
            waste = ox.features_from_point(point, tags=tags_waste, dist=RADIUS)
            features["waste_dumps_within_5km"] = len(waste)
        except Exception: pass

        # Append to master list
        all_features.append(features)
        print(f"  Found {features['major_roads_within_5km']} roads, {features['industrial_zones_within_5km']} industrial zones, {features['farmland_within_5km']} farms, {features['waste_dumps_within_5km']} dumpsites.")

# ==========================================
# EXPORT
# ==========================================
df_spatial = pd.DataFrame(all_features)
os.makedirs("data", exist_ok=True)
output_path = "data/India_Spatial_Features.csv"
df_spatial.to_csv(output_path, index=False)

print(f"\n SUCCESS! Spatial features saved to {output_path}")