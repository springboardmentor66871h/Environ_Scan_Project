import pandas as pd
import folium
from folium.plugins import HeatMap
import os
import numpy as np

print("🌍 STEP 1: Loading Dataset...")
df = pd.read_csv("data/Labeled_Master_Dataset.csv")

# Sample dataset for faster rendering
df_sample = df.sample(n=5000, random_state=42).copy()

print("🗺️ STEP 2: Initializing Base Map...")
avg_lat = df_sample['latitude'].mean()
avg_lon = df_sample['longitude'].mean()

m = folium.Map(
    location=[avg_lat, avg_lon],
    zoom_start=6,
    tiles='CartoDB positron' 
)

print("🔥 STEP 3: Creating Pollutant Heatmaps...")

pollutants = ['pm25','pm10','no2','so2','co','o3']

pollutant_names = {
    'pm25':'PM2.5',
    'pm10':'PM10',
    'no2':'NO₂',
    'so2':'SO₂',
    'co':'CO',
    'o3':'O₃'
}

gradients = {
    'pm25': {0.2:'green',0.4:'yellow',0.6:'orange',1:'red'},
    'pm10': {0.2:'blue',0.4:'cyan',0.6:'yellow',1:'red'},
    'no2':  {0.2:'purple',0.4:'blue',0.6:'lime',1:'yellow'},
    'so2':  {0.2:'green',0.4:'lime',0.6:'yellow',1:'red'},
    'co':   {0.2:'navy',0.4:'blue',0.6:'cyan',1:'white'},
    'o3':   {0.2:'purple',0.4:'magenta',0.6:'pink',1:'white'}
}

# Jitter controls the "spread" size for the clouds
jitter = 0.015

# --- 1. POLLUTANT HEATMAPS ---
for pol in pollutants:
    if pol not in df_sample.columns:
        continue

    print(f"Creating heatmap for {pol}")

    jitter_lat = df_sample['latitude'] + np.random.normal(0, jitter/2, len(df_sample))
    jitter_lon = df_sample['longitude'] + np.random.normal(0, jitter/2, len(df_sample))

    heat_data = [
        [lat,lon,val]
        for lat,lon,val in zip(jitter_lat,jitter_lon,df_sample[pol])
        if pd.notnull(val)
    ]

    layer = folium.FeatureGroup(
        name=f"🔥 {pollutant_names[pol]} Heatmap",
        show=True if pol=='pm25' else False
    )

    HeatMap(
        heat_data,
        radius=35,
        blur=25,
        min_opacity=0.3,
        max_zoom=12, 
        gradient=gradients.get(pol)
    ).add_to(layer)

    layer.add_to(m)

print("📍 STEP 4: Creating Pollution Source Clouds...")

# We define specific gradients for the sources to make them distinct clouds
source_gradients = {
    'Vehicular': {0.5: 'mediumpurple', 1.0: 'purple'},
    'Industrial': {0.5: 'gray', 1.0: 'black'},
    'Agricultural_Burning': {0.5: 'lightgreen', 1.0: 'darkgreen'},
    'Waste_Burning': {0.5: 'sandybrown', 1.0: 'darkorange'},
    'Natural_Dust': {0.5: 'tan', 1.0: 'saddlebrown'},
    'Background_Mixed': {0.5: 'lightblue', 1.0: 'blue'}
}

for source in source_gradients.keys():
    # Filter data for this specific source
    source_df = df_sample[df_sample['pollution_source'] == source]
    
    if len(source_df) == 0:
        continue
        
    layer = folium.FeatureGroup(name=f"📌 {source} Cloud", show=False)
    
    # Generate Gaussian jitter just for this source
    jitter_lat = source_df['latitude'] + np.random.normal(0, jitter/2, len(source_df))
    jitter_lon = source_df['longitude'] + np.random.normal(0, jitter/2, len(source_df))
    
    # Give it a uniform weight of 1 so the cloud density is based entirely on how many points there are
    heat_data = [[lat, lon, 1] for lat, lon in zip(jitter_lat, jitter_lon)]
    
    HeatMap(
        heat_data,
        radius=30,
        blur=20,
        min_opacity=0.4,
        max_zoom=12,
        gradient=source_gradients[source]
    ).add_to(layer)
    
    layer.add_to(m)


print("🚨 STEP 5: Creating High Risk Cloud...")

risk_group = folium.FeatureGroup(name="🚨 High Risk PM2.5 (>150)", show=False)

high = df_sample[df_sample['pm25'] > 150]

if len(high) > 0:
    # Generate jitter for the high risk cloud
    jitter_lat = high['latitude'] + np.random.normal(0, jitter/2, len(high))
    jitter_lon = high['longitude'] + np.random.normal(0, jitter/2, len(high))
    
    # Weight based on the actual PM2.5 value so worse areas glow brighter
    heat_data = [[lat, lon, val] for lat, lon, val in zip(jitter_lat, jitter_lon, high['pm25'])]
    
    HeatMap(
        heat_data,
        radius=40,       # Make the risk zones large and obvious
        blur=25,
        min_opacity=0.5, # Slightly higher opacity to stand out
        max_zoom=12,
        gradient={0.4: 'darkred', 0.8: 'red', 1.0: 'maroon'} # Intense danger colors
    ).add_to(risk_group)

risk_group.add_to(m)


print("🎛️ STEP 6: Layer Controls...")

folium.LayerControl(collapsed=False).add_to(m)

print("💾 STEP 7: Saving Map...")

os.makedirs("visualisation",exist_ok=True)

path="visualisation/pollution_heatmap_all_parameters.html"

m.save(path)

print("✅ Map saved to:",path)