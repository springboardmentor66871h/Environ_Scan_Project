import osmnx as ox
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import warnings
from datetime import datetime

# Suppress warnings
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

# Search radius (5km). If nothing is found within this radius, we cap the distance at 5000m.
SEARCH_RADIUS = 5000 
extraction_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
all_features = []

print(" Starting Advanced Proximity Analysis (Distance to Nearest Features)...")

def get_nearest_distance(point, tags, radius):
    """Fetches features and calculates distance to the nearest one in meters."""
    try:
        # Fetch features within radius
        gdf = ox.features_from_point(point, tags=tags, dist=radius)
        if gdf.empty:
            return radius # If none found, assume it's at least 'radius' meters away
        
        # Create a GeoSeries for our sensor point (Longitude first for Shapely)
        sensor_point = gpd.GeoSeries([Point(point[1], point[0])], crs="EPSG:4326")
        
        # Project both the sensor and the map features to meters (EPSG:3857)
        sensor_projected = sensor_point.to_crs("EPSG:3857").iloc[0]
        gdf_projected = gdf.to_crs("EPSG:3857")
        
        # Calculate distances from sensor to all features and find the minimum
        distances = gdf_projected.distance(sensor_projected)
        return round(distances.min(), 2)
    except Exception:
        return radius # Fallback if API fails or no data

for city, loc_data in locations.items():
    print(f"\n========== Scanning {city} ==========")
    
    for loc_name, meta in loc_data.items():
        print(f"  Calculating proximities for {loc_name}...")
        point = (meta['lat'], meta['lon'])
        
        features = {
            "city": city,
            "location": loc_name,
            "latitude": meta['lat'],
            "longitude": meta['lon'],
            "timestamp": extraction_timestamp
        }
        
        # 1. Distance to Nearest Major Road
        tags_roads = {'highway': ['trunk', 'primary', 'secondary', 'motorway']}
        features["dist_to_road_m"] = get_nearest_distance(point, tags_roads, SEARCH_RADIUS)
        
        # 2. Distance to Nearest Industrial Zone
        tags_ind = {'landuse': ['industrial', 'brownfield']}
        features["dist_to_industry_m"] = get_nearest_distance(point, tags_ind, SEARCH_RADIUS)

        # 3. Distance to Nearest Agricultural/Farmland
        tags_farm = {'landuse': ['farmland', 'orchard']}
        features["dist_to_farm_m"] = get_nearest_distance(point, tags_farm, SEARCH_RADIUS)

        # 4. Distance to Nearest Waste Dump
        tags_waste = {'landuse': ['landfill'], 'amenity': ['waste_disposal']}
        features["dist_to_waste_m"] = get_nearest_distance(point, tags_waste, SEARCH_RADIUS)

        all_features.append(features)
        print(f"  Nearest Road: {features['dist_to_road_m']}m | Industry: {features['dist_to_industry_m']}m")

# ==========================================
# EXPORT
# ==========================================
df_spatial = pd.DataFrame(all_features)
os.makedirs("data", exist_ok=True)
output_path = "data/India_Spatial_Distances.csv"
df_spatial.to_csv(output_path, index=False)

print(f"\nSUCCESS! Proximity features saved to {output_path}")