import pandas as pd
import osmnx as ox
import random

df = pd.read_csv("data/stations.csv")

# Get unique cities
unique_cities = df["City"].dropna().unique()

city_centers = {}

print("Getting city centers from OSM...")

for city in unique_cities:
    try:
        gdf = ox.geocode_to_gdf(city + ", India")
        center = gdf.geometry.centroid.iloc[0]
        city_centers[city] = (center.y, center.x)
        print(city, "✅")
    except:
        city_centers[city] = (None, None)
        print(city, "❌ Failed")

# Assign coordinates (small random offset around city center)
latitudes = []
longitudes = []

for city in df["City"]:
    lat, lon = city_centers.get(city, (None, None))

    if lat and lon:
        # Add small random spread so stations don't overlap
        latitudes.append(lat + random.uniform(-0.01, 0.01))
        longitudes.append(lon + random.uniform(-0.01, 0.01))
    else:
        latitudes.append(None)
        longitudes.append(None)

df["Latitude"] = latitudes
df["Longitude"] = longitudes

df.to_csv("data/stations_with_coordinates.csv", index=False)

print("✅ Coordinates generated successfully.")