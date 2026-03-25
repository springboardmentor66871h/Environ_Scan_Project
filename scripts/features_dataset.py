import osmnx as ox
import pandas as pd
from geopy.distance import geodesic

# --------------------------
# Same 10 Cities
# --------------------------

cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462)
}

all_features = []

# --------------------------
# Extract OSM Features
# --------------------------

for city, (lat, lon) in cities.items():
    print(f"Processing {city}...")

    try:
        # Get features within 5km radius
        tags = {
            "highway": True,
            "landuse": ["industrial", "farmland"],
            "amenity": ["waste_disposal", "recycling"]
        }

        gdf = ox.features_from_point((lat, lon), tags=tags, dist=5000)

        roads = gdf[gdf["highway"].notnull()]
        industrial = gdf[gdf["landuse"] == "industrial"]
        farmland = gdf[gdf["landuse"] == "farmland"]
        dumps = gdf[gdf["amenity"].isin(["waste_disposal", "recycling"])]

        def min_distance(feature_gdf):
            if feature_gdf.empty:
                return None
            distances = [
                geodesic((lat, lon), (row.geometry.centroid.y, row.geometry.centroid.x)).km
                for _, row in feature_gdf.iterrows()
            ]
            return min(distances)

        all_features.append({
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "distance_to_road_km": min_distance(roads),
            "distance_to_industry_km": min_distance(industrial),
            "distance_to_dump_km": min_distance(dumps),
            "distance_to_farmland_km": min_distance(farmland)
        })

    except Exception as e:
        print(f"Error in {city}: {e}")

# --------------------------
# Save CSV
# --------------------------

df = pd.DataFrame(all_features)
df.to_csv(r"C:\Users\admin\Environ_Scan_Project\location_features.csv", index=False)

print("\n✅ Location feature extraction completed!")
print("Total cities processed:", len(df))
