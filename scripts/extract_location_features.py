import osmnx as ox
import pandas as pd
import math

CITIES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946)
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

records = []

for city, (lat, lon) in CITIES.items():

    tags = {
        "highway": True,
        "landuse": ["industrial", "landfill", "farmland"]
    }

    gdf = ox.features_from_point((lat, lon), tags=tags, dist=5000)

    min_distance = float("inf")

    for _, row in gdf.iterrows():
        if row.geometry.centroid:
            dist = haversine(lat, lon,
                             row.geometry.centroid.y,
                             row.geometry.centroid.x)
            min_distance = min(min_distance, dist)

    records.append({
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "nearest_feature_distance_m": min_distance
    })

df = pd.DataFrame(records)
df.to_csv("data/raw/location_features.csv", index=False)

print("Location features extracted successfully.")