import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import joblib
import os
import numpy as np

# --- 1. CONFIGURATION ---
print("🗺️ Starting Improvised Geospatial Mapping Pipeline...")
DATA_FILE = "data/processed/labeled_india_part1.zip"
MODEL_FILE = "models/random_forest_enviroscan.joblib"
OUTPUT_MAP = "models/mysuru_pollution_map.html"

# --- 2. LOAD DATA & MODEL ---
print("⏳ Loading data and trained AI model...")
df = pd.read_csv(DATA_FILE)
model = joblib.load(MODEL_FILE)

# Filter for Mysuru and drop missing coordinates
df_mysuru = df[df['city'] == 'Mysuru'].dropna(subset=['latitude', 'longitude']).copy()

# Prevent browser crash
if len(df_mysuru) > 500:
    df_mysuru = df_mysuru.sample(n=500, random_state=42)

print("✨ Applying organic spread to markers for prototype...")
# FIXED: Using a Normal (Gaussian) distribution so it looks like a natural, organic cluster rather than a perfect square box.
df_mysuru['latitude'] = df_mysuru['latitude'] + np.random.normal(0, 0.025, size=len(df_mysuru))
df_mysuru['longitude'] = df_mysuru['longitude'] + np.random.normal(0, 0.025, size=len(df_mysuru))

# --- 3. GENERATE AI PREDICTIONS ---
print("🧠 Generating fresh source predictions using Random Forest...")
features = ['pm25', 'pm10', 'no2', 'so2', 'temperature', 'humidity', 'wind_speed', 
            'distance_to_road', 'distance_to_industry', 'distance_to_dump', 'distance_to_farmland']
df_mysuru[features] = df_mysuru[features].fillna(df_mysuru[features].median())
df_mysuru['predicted_source'] = model.predict(df_mysuru[features])

# --- 4. INITIALIZE BASE MAP ---
print("🌍 Building Interactive Folium Dashboard...")
center_lat, center_lon = df_mysuru['latitude'].mean(), df_mysuru['longitude'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB positron')

# --- 5. CREATE FILTERING LAYERS (FeatureGroups) ---
heatmap_layer = folium.FeatureGroup(name="🔥 Air Pollution Heatmap (PM2.5)", show=True)
high_risk_layer = folium.FeatureGroup(name="⚠️ Critical PM2.5 Zones (> 60)", show=True)

# FIXED: Changed show=True so these are visible immediately when the map opens
vehicular_cluster = MarkerCluster(name="🚗 Vehicular Sources", show=True)
industrial_cluster = MarkerCluster(name="🏭 Industrial Sources", show=True)
other_cluster = MarkerCluster(name="🌱 Agri/Natural Sources", show=True)

heatmap_layer.add_to(m)
high_risk_layer.add_to(m)
vehicular_cluster.add_to(m)
industrial_cluster.add_to(m)
other_cluster.add_to(m)

# --- 6. ADD HEATMAP ---
heat_data = df_mysuru[['latitude', 'longitude', 'pm25']].values.tolist()
# Tweaked blur and radius for a smoother, less blocky look
HeatMap(heat_data, radius=18, blur=15, max_zoom=15).add_to(heatmap_layer)

# --- 7. HELPER FUNCTION & MARKER LOGIC ---
def get_source_marker(source, pm25, popup_text, lat, lon):
    icon_map = {'Vehicular': 'car', 'Industrial': 'industry', 'Other': 'leaf'}
    marker_color_map = {'Vehicular': 'blue', 'Industrial': 'orange', 'Other': 'green'}
    
    icon_type = icon_map.get(source, 'leaf')
    marker_color = marker_color_map.get(source, 'green')

    return folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_text, max_width=250), 
        icon=folium.Icon(color=marker_color, icon=icon_type, prefix='fa')
    )

for index, row in df_mysuru.iterrows():
    lat, lon = row['latitude'], row['longitude']
    source, pm25 = row['predicted_source'], row['pm25']
    no2, so2 = row['no2'], row['so2']
    
    popup_text = f"""
    <b>Predicted Source:</b> {source}<br>
    <b>PM2.5:</b> {pm25:.1f} µg/m³<br>
    <b>NO2:</b> {no2:.1f} µg/m³<br>
    <b>SO2:</b> {so2:.1f} µg/m³
    """

    marker = get_source_marker(source, pm25, popup_text, lat, lon)
    if source == 'Vehicular':
        marker.add_to(vehicular_cluster)
    elif source == 'Industrial':
        marker.add_to(industrial_cluster)
    else:
        marker.add_to(other_cluster)
    
    if pm25 > 60:
        folium.CircleMarker(
            location=[lat, lon], radius=8, color='crimson',
            fill=True, fill_color='crimson', fill_opacity=0.7,
            popup=folium.Popup(f"<b>CRITICAL RISK</b><br>PM2.5: {pm25}", max_width=200)
        ).add_to(high_risk_layer)

# --- 8. FINALIZE AND EXPORT ---
folium.LayerControl(collapsed=False).add_to(m)

# Custom HTML legend 
legend_html = """
<div style="position: fixed; 
            bottom: 30px; left: 30px; width: 230px; height: 180px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:rgba(255,255,255,0.85);
            border-radius:6px; padding: 10px;">
  <b>Map Legend</b><br>
  <i class="fa fa-car" style="color:blue"></i> Vehicular Source Marker<br>
  <i class="fa fa-industry" style="color:orange"></i> Industrial Source Marker<br>
  <i class="fa fa-leaf" style="color:green"></i> Agri/Natural Source Marker<br>
  <span style="color:crimson; font-weight:bold;">●</span> <span style="font-weight:normal;color:black;">Critical PM2.5 (> 60)</span><br>
  <hr style="margin: 5px 0;">
  🔥 Heatmap: PM2.5 Pollution Density
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

m.save(OUTPUT_MAP)
print(f"✅ SUCCESS! Organic map saved to: {OUTPUT_MAP}")