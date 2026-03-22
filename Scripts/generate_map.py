import pandas as pd
import folium
import numpy as np
from folium.plugins import HeatMap, MarkerCluster
import os

print("Starting Geospatial Mapping Pipeline...")

# --- CONFIGURATION ---
BASE_DIR = r"C:\Users\ajayk\Environ_Scan_Project"
DATA_FILE = os.path.join(BASE_DIR, "Processed", "dataset_with_predictions.csv")
OUTPUT_MAP = os.path.join(BASE_DIR, "Visualizations", "pollution_map.html")

# --------------------------------------------------
# STEP 1: Load dataset
# --------------------------------------------------
print("Loading dataset...")
if not os.path.exists(DATA_FILE):
    print(f"Error: Could not find {DATA_FILE}")
    exit()

df = pd.read_csv(DATA_FILE)

print("Dataset loaded:", df.shape)

# Remove rows with missing coordinates or pm25
df = df.dropna(subset=["Latitude", "Longitude", "PM25", "POLLUTION_SOURCE"])

print("Dataset after cleaning:", df.shape)

# --------------------------------------------------
# STEP 2: Slightly spread coordinates
# (helps visualize density better)
# --------------------------------------------------
np.random.seed(42)

df["lat_spread"] = df["Latitude"] + np.random.normal(0, 0.02, len(df))
df["lon_spread"] = df["Longitude"] + np.random.normal(0, 0.02, len(df))

# Normalize column names to avoid case sensitivity issues in loops
city_col = next((col for col in df.columns if col.lower() == 'city'), None)
pm10_col = next((col for col in df.columns if col.lower() == 'pm10'), 'PM10')

# --------------------------------------------------
# STEP 3: Create base map
# --------------------------------------------------
m = folium.Map(
    location=[22.5, 78.9],   # center of India
    zoom_start=5,
    tiles="cartodbpositron"
)

# --------------------------------------------------
# STEP 4: Pollution Heatmap (PM2.5)
# --------------------------------------------------
heat_data = df[["lat_spread", "lon_spread", "PM25"]].values.tolist()

HeatMap(
    heat_data,
    radius=18,
    blur=25,
    min_opacity=0.4,
    max_zoom=10,
    gradient={
        0.1: "blue",
        0.3: "cyan",
        0.5: "green",
        0.7: "yellow",
        0.9: "orange",
        1.0: "red"
    }
).add_to(m)

# --------------------------------------------------
# STEP 5: Source specific markers
# --------------------------------------------------
marker_cluster = MarkerCluster(name="Pollution Sources").add_to(m)

source_colors = {
    "INDUSTRIAL": "red",
    "VEHICULAR": "blue",
    "AGRICULTURAL": "green",
    "BURNING": "orange",
    "NATURAL": "purple"
}

for _, row in df.iterrows():
    city_name = row[city_col] if city_col else "Unknown"
    source = str(row['POLLUTION_SOURCE']).upper()
    pm10_val = row[pm10_col] if pm10_col in df.columns else "N/A"

    popup_text = f"""
    <b>City:</b> {city_name} <br>
    <b>Source:</b> {source} <br>
    <b>PM2.5:</b> {row['PM25']} <br>
    <b>PM10:</b> {pm10_val}
    """

    folium.CircleMarker(
        location=[row["lat_spread"], row["lon_spread"]],
        radius=5,
        color=source_colors.get(source, "black"),
        fill=True,
        fill_opacity=0.7,
        popup=popup_text
    ).add_to(marker_cluster)

# --------------------------------------------------
# STEP 6: High Risk Pollution Zones
# --------------------------------------------------
threshold = 120

high_layer = folium.FeatureGroup(name="High Risk Zones")

high_risk = df[df["PM25"] > threshold]

# calculate mean only for pm25 based on original true coordinates
high_risk = high_risk.groupby(["Latitude", "Longitude"])["PM25"].mean().reset_index()

for _, row in high_risk.iterrows():
    folium.Circle(
        location=[row["Latitude"], row["Longitude"]],
        radius=20000, # Increased radius slightly so it's visible at country-level zoom
        color="darkred",
        fill=True,
        fill_opacity=0.35,
        popup=f"High Pollution Zone<br>PM2.5: {round(row['PM25'],2)}"
    ).add_to(high_layer)

high_layer.add_to(m)

# --------------------------------------------------
# STEP 7: Layer control
# --------------------------------------------------
folium.LayerControl().add_to(m)

# --------------------------------------------------
# STEP 8: Legend
# --------------------------------------------------
legend_html = """
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 240px;
background-color: white;
border:2px solid grey;
z-index:9999;
font-size:14px;
padding:10px;
">

<b>Pollution Source</b><br>
<span style="color:red;">●</span> Industrial<br>
<span style="color:blue;">●</span> Vehicular<br>
<span style="color:green;">●</span> Agricultural<br>
<span style="color:orange;">●</span> Burning<br>
<span style="color:purple;">●</span> Natural<br><br>

<b>Heatmap Intensity (PM2.5)</b><br>
Blue → Very Low<br>
Green → Moderate<br>
Yellow → High<br>
Red → Severe

</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# --------------------------------------------------
# STEP 9: Save map
# --------------------------------------------------
m.save(OUTPUT_MAP)

print(f"Map saved successfully → {OUTPUT_MAP}")