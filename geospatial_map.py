import pandas as pd
import folium
from folium.plugins import HeatMap

# Load dataset
data = pd.read_csv("data/processed/final_map_dataset.csv")

# Remove missing values
data = data.dropna(subset=["Latitude","Longitude","pollutant_avg"])

# Create map center
map_center = [data["Latitude"].mean(), data["Longitude"].mean()]

# Create map
m = folium.Map(location=map_center, zoom_start=10)

print("Base map created")

# -----------------------
# Heatmap Layer
# -----------------------
heat_data = data[["Latitude","Longitude","pollutant_avg"]].values.tolist()

HeatMap(
    heat_data,
    radius=25,
    blur=20,
    min_opacity=0.4,
    gradient={
        0.2: "blue",
        0.4: "green",
        0.6: "yellow",
        0.8: "orange",
        1.0: "red"
    }
).add_to(m)

print("Heatmap added")

for _, row in data.iterrows():

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=12,
        color="orange",
        fill=True,
        fill_color="orange",
        fill_opacity=0.9
    ).add_to(m)

    folium.map.Marker(
        [row["Latitude"], row["Longitude"]],
        icon=folium.DivIcon(
            html=f"""<div style="font-size:10pt;color:black;font-weight:bold">
            {int(row['pollutant_avg'])}
            </div>"""
        )
    ).add_to(m)
legend_html = '''
<div style="
position: fixed; 
bottom: 50px; left: 50px; width: 200px; height: 150px; 
background-color: white;
border:2px solid grey; z-index:9999; font-size:14px;
padding: 10px;
">

<b>Pollution Source</b><br>
<i style="color:purple">●</i> Industrial<br>
<i style="color:blue">●</i> Vehicular<br>
<i style="color:green">●</i> Agricultural<br>
<i style="color:red">●</i> Burning<br>
<br>
<b>Heatmap Intensity (PM2.5)</b><br>
Blue = Very Low<br>
Green = Moderate<br>
Yellow = High<br>
Red = Severe
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))
# ADD THIS TEST MARKER HERE 👇
folium.Marker(
    [data["Latitude"].iloc[0], data["Longitude"].iloc[0]],
    popup="Test Marker"
).add_to(m)

# -----------------------
# Pollution Source Markers
# -----------------------
for _, row in data.iterrows():

    source = row.get("pollution_source","Unknown")

    if source == "Industrial":
        color = "purple"

    elif source == "Vehicular":
        color = "blue"

    elif source == "Agricultural":
        color = "green"

    elif source == "Burning":
        color = "red"

    else:
        color = "gray"

    folium.Marker(
        location=[row["Latitude"],row["Longitude"]],
        popup=f"""
        <b>Source:</b> {source}<br>
        <b>PM2.5:</b> {row['pollutant_avg']}<br>
        <b>City:</b> {row['City']}
        """,
        icon=folium.Icon(color=color)
    ).add_to(m)

# -----------------------
# High Risk Zones
# -----------------------
for _, row in data.iterrows():

    if row["pollutant_avg"] > 100:

        folium.CircleMarker(
            location=[row["Latitude"],row["Longitude"]],
            radius=row["pollutant_avg"]/8,
            color="darkred",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            popup=f"High Risk Zone<br>PM2.5: {row['pollutant_avg']}"
        ).add_to(m)

# -----------------------
# Layer control
# -----------------------
folium.LayerControl().add_to(m)

# Save map
m.save("visualization/pollution_map.html")

print("Map saved successfully!")