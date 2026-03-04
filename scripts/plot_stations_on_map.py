import pandas as pd
import osmnx as ox
import matplotlib.pyplot as plt

df = pd.read_csv("data/stations_with_coordinates.csv")

place = "Chennai, India"

print("Loading map...")
G = ox.graph_from_place(place, network_type="drive")

fig, ax = ox.plot_graph(
    G,
    node_size=0,
    edge_linewidth=0.5,
    show=False,
    close=True
)

print("Plotting stations...")

for _, row in df.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]

    if pd.notna(lat) and pd.notna(lon):
        ax.scatter(lon, lat, c="red", s=50)

plt.title("Pollution Stations Map")
plt.savefig("data/stations_map_final.png", dpi=300)
plt.close()

print("Map saved successfully ✅")