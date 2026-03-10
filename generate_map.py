import pandas as pd
import folium
from folium.plugins import HeatMap
import os

print("Loading dataset for map generation...")
df = pd.read_csv("data/processed/labeled_environment_dataset.csv")

center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()
pollution_map = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles="CartoDB positron")

print("Adding Heatmap layer...")
heat_data = [[row['latitude'], row['longitude'], row['value']] for index, row in df.iterrows()]

heatmap_group = folium.FeatureGroup(name='🌡️ Pollution Heatmap')
HeatMap(heat_data, radius=15, blur=10, gradient={0.4: 'green', 0.6: 'yellow', 1.0: 'red'}).add_to(heatmap_group)
heatmap_group.add_to(pollution_map)

print("Building Filter Layers and Custom Icons...")
source_styles = {
    'Industrial': {'color': 'purple', 'icon': 'industry'},
    'Vehicular': {'color': 'blue', 'icon': 'car'},
    'Agricultural': {'color': 'orange', 'icon': 'leaf'},
    'Burning': {'color': 'darkred', 'icon': 'fire'},
    'Natural': {'color': 'green', 'icon': 'tree'}
}

layers = {
    'Industrial': folium.FeatureGroup(name='🏭 Industrial Sources'),
    'Vehicular': folium.FeatureGroup(name='🚗 Vehicular Sources'),
    'Agricultural': folium.FeatureGroup(name='🌾 Agricultural Sources'),
    'Burning': folium.FeatureGroup(name='🔥 Burning Sources'),
    'Natural': folium.FeatureGroup(name='🌳 Natural Sources')
}

# Sampling the data to keep the map clean and beautiful, just like you wanted!
sample_df = df.sample(n=min(300, len(df)), random_state=42)

for index, row in sample_df.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    source = row['pollution_source']
    pollutant = row['pollutant'].upper()
    val = row['value']
    
    popup_text = f"<b>Predicted Source:</b> {source}<br><b>Pollutant:</b> {pollutant} ({val})<br><b>City:</b> {row['city']}"
    style = source_styles.get(source, {'color': 'gray', 'icon': 'info-sign'})
    
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.Icon(color=style['color'], icon=style['icon'], prefix='fa')
    ).add_to(layers[source])
    
    if val > 150: 
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color='darkred',
            fill=True,
            fill_color='darkred',
            fill_opacity=0.6,
            popup="⚠️ HIGH RISK ZONE"
        ).add_to(layers[source])

for layer in layers.values():
    layer.add_to(pollution_map)

print("Adding the Filter Menu...")
folium.LayerControl(collapsed=False).add_to(pollution_map)

os.makedirs("data/processed", exist_ok=True)
map_path = "data/processed/interactive_pollution_map.html"
pollution_map.save(map_path)

print(f"SUCCESS: Clean Map with Filters and Custom Icons saved to {map_path}")