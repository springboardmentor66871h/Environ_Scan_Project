import pandas as pd
import osmnx as ox
from shapely.geometry import Point

# Load station coordinates
df = pd.read_csv("data/stations_with_coordinates.csv")

place = "Chennai, India"

print("Loading road network...")
G = ox.graph_from_place(place, network_type="drive")

# Convert to GeoDataFrame
roads = ox.graph_to_gdfs(G, nodes=False, edges=True)

distances = []

for _, row in df.iterrows():
    if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
        point = Point(row["Longitude"], row["Latitude"])
        nearest_edge = roads.geometry.distance(point).min()
        distances.append(nearest_edge)
    else:
        distances.append(None)

df["Distance_to_Nearest_Road"] = distances

df.to_csv("data/stations_with_spatial_features.csv", index=False)

print("Spatial feature added ✅")