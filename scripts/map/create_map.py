import pandas as pd
import folium
from folium.plugins import HeatMap
import os

# Paths
DATA_PATH = os.path.join('data', 'processed', 'enviro_labeled_dataset.csv')
OUTPUT_PATH = os.path.join('outputs', 'pollution_map.html')

def generate_pro_aqi_map():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=['latitude', 'longitude', 'pm25'])

    # 1. Initialize Map with a Dark Theme (Professional AQI Look)
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], 
                   zoom_start=6, 
                   tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                   attr='&copy; OpenStreetMap contributors &copy; CARTO')

    # 2. Professional Heatmap Gradient (Green -> Yellow -> Orange -> Red -> Purple)
    # Similar to the AQI scale in your example image
    heat_data = df[['latitude', 'longitude', 'pm25']].values.tolist()
    HeatMap(heat_data, 
            radius=25, 
            blur=20, 
            min_opacity=0.4,
            gradient={0.0: 'green', 0.2: '#ffff00', 0.4: '#ff7e00', 0.6: '#ff0000', 1.0: '#8f3f97'}
           ).add_to(m)

    # 3. Custom Markers with "Indicators in Box" (Popups)
    source_colors = {
        'Industrial': '#9b59b6', # Purple
        'Vehicular': '#3498db',  # Blue
        'Agricultural': '#2ecc71', # Green
        'Burning': '#e74c3c',      # Red
        'Natural': '#f1c40f'       # Yellow
    }

    for _, row in df.iterrows():
        color = source_colors.get(row['pollution_source'], 'white')
        
        # Professional Popup (HTML/CSS) - Showing all indicators like Google Maps
        html = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding:10px; background-color:#2c3e50; color:white; border-radius:5px;">
            <h4 style="margin:0 0 10px 0; color:{color};">{row['pollution_source']}</h4>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #34495e;"><td><b>PM2.5:</b></td><td>{row['pm25']} µg/m³</td></tr>
                <tr style="border-bottom: 1px solid #34495e;"><td><b>City:</b></td><td>{row['city']}</td></tr>
                <tr style="border-bottom: 1px solid #34495e;"><td><b>Station:</b></td><td>{row['station']}</td></tr>
            </table>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            color='white',
            weight=1,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=folium.Popup(html, max_width=250)
        ).add_to(m)

    m.save(OUTPUT_PATH)
    print(f"Map Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_pro_aqi_map()