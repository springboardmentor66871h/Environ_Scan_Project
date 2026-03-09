import pandas as pd
import folium
import numpy as np
from folium.plugins import HeatMap, MarkerCluster

# --------------------------------------------------
# STEP 1: Load dataset
# --------------------------------------------------

df = pd.read_csv("data/processed/final_dataset.csv")

print("Dataset loaded:", df.shape)

# Remove rows with missing coordinates or pm25
df = df.dropna(subset=["latitude", "longitude", "pm25", "pollution_source"])

print("Dataset after cleaning:", df.shape)

# --------------------------------------------------
# STEP 2: Slightly spread coordinates
# (helps visualize density better)
# --------------------------------------------------

np.random.seed(42)

df["lat_spread"] = df["latitude"] + np.random.normal(0, 0.02, len(df))
df["lon_spread"] = df["longitude"] + np.random.normal(0, 0.02, len(df))

# --------------------------------------------------
# STEP 3: Create base map
# --------------------------------------------------

m = folium.Map(
    location=[22.5, 78.9],   # center of India
    zoom_start=6,
    tiles="cartodbpositron"
)

# --------------------------------------------------
# STEP 4: Pollution Heatmap (PM2.5)
# --------------------------------------------------

heat_data = df[["lat_spread", "lon_spread", "pm25"]].values.tolist()

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
    "Industrial": "red",
    "Vehicular": "blue",
    "Agricultural": "green",
    "Burning": "orange",
    "Natural": "purple"
}

for _, row in df.iterrows():

    popup_text = f"""
    <b>City:</b> {row['city']} <br>
    <b>Source:</b> {row['pollution_source']} <br>
    <b>PM2.5:</b> {row['pm25']} <br>
    <b>PM10:</b> {row['pm10']}
    """

    folium.CircleMarker(
        location=[row["lat_spread"], row["lon_spread"]],
        radius=5,
        color=source_colors.get(row["pollution_source"], "black"),
        fill=True,
        fill_opacity=0.7,
        popup=popup_text
    ).add_to(marker_cluster)

# --------------------------------------------------
# STEP 6: High Risk Pollution Zones
# --------------------------------------------------

threshold = 120

high_layer = folium.FeatureGroup(name="High Risk Zones")

high_risk = df[df["pm25"] > threshold]

# calculate mean only for pm25
high_risk = high_risk.groupby(["latitude", "longitude"])["pm25"].mean().reset_index()

for _, row in high_risk.iterrows():

    folium.Circle(
        location=[row["latitude"], row["longitude"]],
        radius=2000,
        color="darkred",
        fill=True,
        fill_opacity=0.35,
        popup=f"High Pollution Zone<br>PM2.5: {round(row['pm25'],2)}"
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

m.save("pollution_map.html")

print("Map saved successfully → pollution_map.html")