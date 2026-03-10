import pandas as pd
import geopandas as gpd
import osmnx as ox
import time
from shapely.geometry import Point

# Keep the terminal output clean and use cache to speed things up
ox.settings.log_console = False
ox.settings.use_cache = True

print("Loading pollution dataset...")
df = pd.read_csv("data/raw/india_air_pollution_cleaned.csv")

# Get our unique locations
locations = df[['city', 'latitude', 'longitude']].drop_duplicates().reset_index(drop=True)
print(f"Found {len(locations)} unique locations.")
print("Extracting geographical features (This will take 5-10 minutes. Please let it run!)...")

# Define the Map Tags we want to find
tags = {
    "highway": True,
    "landuse": ["industrial", "commercial", "farmland", "meadow", "farm", "landfill", "waste_transfer_station", "brownfield"]
}

results = []

for index, row in locations.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    city = row['city']
    
    print(f"[{index + 1}/{len(locations)}] Scanning area around {city}...")
    
    # Default distances: If nothing is found nearby, assume it is far away (e.g., 5000 meters)
    dist_road = 5000.0
    dist_industry = 5000.0
    dist_farm = 5000.0
    dist_dump = 5000.0
    
    try:
        # Fetch map features within a 5km radius of this specific sensor
        features = ox.features_from_point((lat, lon), tags=tags, dist=5000)
        
        if not features.empty:
            # Create a point for our location and convert to meters (EPSG:3857) for accurate distance math
            center_pt = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326").to_crs(epsg=3857).iloc[0]
            features_proj = features.to_crs(epsg=3857)
            
            # Separate features by category
            roads = features_proj[features_proj['highway'].notna()]
            industrial = features_proj[features_proj['landuse'].isin(['industrial', 'commercial', 'brownfield'])]
            farmland = features_proj[features_proj['landuse'].isin(['farmland', 'meadow', 'farm'])]
            dumps = features_proj[features_proj['landuse'].isin(['landfill', 'waste_transfer_station'])]
            
            # Find the minimum distance to the nearest feature in each category
            if not roads.empty:
                dist_road = roads.distance(center_pt).min()
            if not industrial.empty:
                dist_industry = industrial.distance(center_pt).min()
            if not farmland.empty:
                dist_farm = farmland.distance(center_pt).min()
            if not dumps.empty:
                dist_dump = dumps.distance(center_pt).min()
                
    except Exception as e:
        # If the OpenStreetMap server glitches for one city, just skip it and use the defaults
        pass
        
    results.append({
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "distance_to_road_m": round(dist_road, 2),
        "distance_to_industry_m": round(dist_industry, 2),
        "distance_to_farmland_m": round(dist_farm, 2),
        "distance_to_dump_m": round(dist_dump, 2)
    })
    
    # Sleep to avoid hitting OpenStreetMap API rate limits
    time.sleep(1.2)

# Save the final table
location_df = pd.DataFrame(results)
output_file = "data/raw/location.csv"
location_df.to_csv(output_file, index=False)

print(f"\nSuccessfully saved location features to {output_file}!")
print("Module 1 & 2 (Feature Extraction) Completed!")