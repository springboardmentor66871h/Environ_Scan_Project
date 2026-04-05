import pandas as pd
import folium
from folium.plugins import HeatMap

# --------------------------
# Load Dataset
# --------------------------

df = pd.read_csv("data/processed/final_labeled_dataset.csv")

# Remove rows with missing coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# --------------------------
# Add Extra Pollution Data (More Cities)
# --------------------------

extra_data = pd.DataFrame([
    ["Delhi", 28.61, 77.20, 180, 260, 60, 2.1, 25, 40, "Industrial"],
    ["Mumbai", 19.07, 72.87, 120, 190, 40, 1.5, 15, 35, "Vehicular"],
    ["Bangalore", 12.97, 77.59, 70, 110, 25, 1.0, 10, 30, "Natural"],
    ["Chennai", 13.08, 80.27, 90, 140, 30, 1.2, 12, 32, "Industrial"],
    ["Kolkata", 22.57, 88.36, 160, 230, 55, 1.8, 22, 38, "Burning"],
    ["Hyderabad", 17.38, 78.48, 95, 150, 35, 1.3, 14, 33, "Vehicular"],
    ["Ahmedabad", 23.02, 72.57, 140, 210, 48, 1.6, 20, 36, "Industrial"]
], columns=[
    "City","Latitude","Longitude","PM2.5","PM10","NO2","CO","SO2","O3","pollution_source"
])

df = pd.concat([df, extra_data], ignore_index=True)

# --------------------------
# Create Base Map
# --------------------------

center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

pollution_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=5
)

# --------------------------
# Create Heatmap Layer
# --------------------------

heat_data = [
    [row["Latitude"], row["Longitude"], row["PM2.5"]]
    for _, row in df.iterrows()
]

HeatMap(
    heat_data,
    radius=20,
    blur=25,
    max_zoom=13
).add_to(pollution_map)

# --------------------------
# Marker Colors for Sources
# --------------------------

color_map = {
    "Industrial": "red",
    "Vehicular": "blue",
    "Agricultural": "green",
    "Burning": "orange",
    "Natural": "purple"
}

# --------------------------
# Add Markers
# --------------------------

for _, row in df.iterrows():

    source = row["pollution_source"]
    color = color_map.get(source, "black")

    popup_text = f"""
    <b>City:</b> {row.get('City','Unknown')}<br>
    <b>Source:</b> {source}<br>
    <b>PM2.5:</b> {row['PM2.5']}<br>
    <b>PM10:</b> {row['PM10']}<br>
    <b>NO2:</b> {row['NO2']}
    """

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup_text,
        icon=folium.Icon(color=color)
    ).add_to(pollution_map)

# --------------------------
# High Risk Zones
# --------------------------

for _, row in df.iterrows():

    if row["PM2.5"] > 120:

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=row["PM2.5"] / 10,
            color="darkred",
            fill=True,
            fill_color="red",
            fill_opacity=0.7
        ).add_to(pollution_map)

# --------------------------
# Layer Control
# --------------------------

folium.LayerControl().add_to(pollution_map)

# --------------------------
# Save Map
# --------------------------

pollution_map.save("dashboard/pollution_map.html")

print("Map saved successfully!")