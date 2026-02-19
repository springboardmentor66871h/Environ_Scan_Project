import os
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import random

# ==========================================
# CONFIG
# ==========================================

BASE_PATH = r"D:\ENVIRON-SCAN"
RAW_PATH = os.path.join(BASE_PATH, "data", "raw")
os.makedirs(RAW_PATH, exist_ok=True)

cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639)
}

records = []

# ==========================================
# DISTANCE FUNCTION
# ==========================================

def calculate_distance(city_point, features):
    if features.empty:
        return None
    features = features.to_crs(epsg=3857)
    city_point = gpd.GeoSeries([city_point], crs="EPSG:4326").to_crs(epsg=3857)
    distances = features.distance(city_point.iloc[0])
    return distances.min()

# ==========================================
# MAIN LOOP
# ==========================================

for city, (lat, lon) in cities.items():

    print(f"\nProcessing spatial features for {city}...")

    tags = {
        "highway": True,
        "landuse": ["industrial", "landfill", "farmland"]
    }

    try:
        gdf = ox.features_from_point((lat, lon), tags=tags, dist=10000)
    except:
        print("OSM fetch failed for", city)
        continue

    roads = gdf[gdf.get("highway").notna()]
    industrial = gdf[gdf.get("landuse") == "industrial"]
    landfill = gdf[gdf.get("landuse") == "landfill"]
    farmland = gdf[gdf.get("landuse") == "farmland"]

    # Create 5 spatial points per city
    for i in range(5):

        offset_lat = lat + random.uniform(-0.02, 0.02)
        offset_lon = lon + random.uniform(-0.02, 0.02)

        city_point = Point(offset_lon, offset_lat)

        record = {
            "city": city,
            "latitude": offset_lat,
            "longitude": offset_lon,
            "distance_to_road": calculate_distance(city_point, roads),
            "distance_to_industry": calculate_distance(city_point, industrial),
            "distance_to_dump": calculate_distance(city_point, landfill),
            "distance_to_farmland": calculate_distance(city_point, farmland)
        }

        records.append(record)

location_df = pd.DataFrame(records)

file_path = os.path.join(RAW_PATH, "location_features.csv")
location_df.to_csv(file_path, index=False)

print("\nUpgraded location feature dataset saved.")
print("Total spatial points:", len(location_df))
