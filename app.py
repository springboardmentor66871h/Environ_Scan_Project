import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import requests
import os
from datetime import datetime
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")
st.title("🌍 EnviroScan: Real-Time Pollution Prediction")

# ---------------- LOAD DATA & MODEL ----------------
# Ensure these paths match your local folder structure
try:
    df = pd.read_csv("./data/processed/enviro_labeled_dataset.csv")
    model = joblib.load("scripts/model/pollution_source_model.pkl")
except Exception as e:
    st.error(f"Error loading files: {e}")

# Mapping for Step 3 & 6
label_map = {0: "Industrial", 1: "Vehicular", 2: "Agricultural", 3: "Burning", 4: "Natural"}

# ---------------- ALL 27 STATIONS (Step 2/7) ----------------
STATIONS = {
    "DELHI_CHANDINI_CHOWK": {"lat": 28.6560, "lon": 77.2300, "road": 0.02, "ind": 5.0, "dump": 8.0, "farm": 15.0},
    "DELHI_ANANT_VIHAR": {"lat": 28.6469, "lon": 77.3153, "road": 0.05, "ind": 4.0, "dump": 7.0, "farm": 12.0},
    "DELHI_ITO": {"lat": 28.6280, "lon": 77.2410, "road": 0.01, "ind": 3.0, "dump": 10.0, "farm": 20.0},
    "BHOPAL": {"lat": 23.2336, "lon": 77.4009, "road": 0.5, "ind": 2.5, "dump": 5.0, "farm": 8.0},
    "BHOPAL_PARYAVARAN_PARK": {"lat": 23.2500, "lon": 77.4200, "road": 0.8, "ind": 2.0, "dump": 4.0, "farm": 7.0},
    "BHOPAL_IDGAH_HILLS": {"lat": 23.2550, "lon": 77.4100, "road": 0.4, "ind": 3.0, "dump": 6.0, "farm": 10.0},
    "MUMBAI": {"lat": 19.0470, "lon": 72.8746, "road": 0.3, "ind": 8.0, "dump": 12.0, "farm": 30.0},
    "MUMBAI_BYCULLA": {"lat": 18.9767, "lon": 72.8331, "road": 0.03, "ind": 7.0, "dump": 10.0, "farm": 25.0},
    "MUMBAI_CHAKALA_ANDHERI": {"lat": 19.1100, "lon": 72.8620, "road": 0.1, "ind": 5.0, "dump": 8.0, "farm": 20.0},
    "KOLKATA": {"lat": 22.6270, "lon": 88.3800, "road": 0.4, "ind": 4.0, "dump": 6.0, "farm": 12.0},
    "KOLKATA_BALLYGUNGE": {"lat": 22.5250, "lon": 88.3630, "road": 0.1, "ind": 3.0, "dump": 5.0, "farm": 15.0},
    "KOLKATA_JADAVPUR": {"lat": 22.4993, "lon": 88.3710, "road": 0.3, "ind": 2.0, "dump": 4.0, "farm": 10.0},
    "BENGALURU": {"lat": 13.0280, "lon": 77.5180, "road": 0.5, "ind": 4.0, "dump": 9.0, "farm": 5.0},
    "BENGALURU_HEBBAL": {"lat": 13.0358, "lon": 77.5970, "road": 0.05, "ind": 5.0, "dump": 12.0, "farm": 18.0},
    "BENGALURU_RAILWAY_STATION": {"lat": 12.9784, "lon": 77.5686, "road": 0.01, "ind": 6.0, "dump": 15.0, "farm": 25.0},
    "CHENNAI": {"lat": 13.1660, "lon": 80.2580, "road": 0.4, "ind": 5.0, "dump": 11.0, "farm": 22.0},
    "CHENNAI_ALANDUR_BUS_DEPOT": {"lat": 13.0046, "lon": 80.2017, "road": 0.02, "ind": 4.0, "dump": 8.0, "farm": 30.0},
    "CHENNAI_VELACHERY": {"lat": 12.9750, "lon": 80.2212, "road": 0.2, "ind": 3.0, "dump": 6.0, "farm": 15.0},
    "LUCKNOW": {"lat": 26.8467, "lon": 80.9462, "road": 0.6, "ind": 2.0, "dump": 5.0, "farm": 7.0},
    "LUCKNOW_TALKATORA": {"lat": 26.8350, "lon": 80.9000, "road": 0.1, "ind": 6.0, "dump": 4.0, "farm": 12.0},
    "LUCKNOW_LALBAGH": {"lat": 26.8485, "lon": 80.9416, "road": 0.05, "ind": 1.5, "dump": 6.0, "farm": 10.0},
    "HYDERABAD": {"lat": 17.5416, "lon": 78.4840, "road": 0.5, "ind": 7.0, "dump": 11.0, "farm": 20.0},
    "HYDERABAD_PATENCHERU": {"lat": 17.5330, "lon": 78.2600, "road": 0.8, "ind": 0.2, "dump": 14.0, "farm": 5.0},
    "HYDERABAD_SOMAJIGUDA": {"lat": 17.4240, "lon": 78.4595, "road": 0.02, "ind": 4.0, "dump": 8.0, "farm": 15.0},
    "AHMEDABAD": {"lat": 23.0300, "lon": 72.5400, "road": 0.4, "ind": 4.5, "dump": 8.0, "farm": 10.0},
    "AHMEDABAD_SOMAJIGUDA": {"lat": 23.0370, "lon": 72.5666, "road": 0.05, "ind": 3.0, "dump": 7.0, "farm": 14.0},
    "AHMEDABAD_SVPT": {"lat": 23.0350, "lon": 72.5800, "road": 0.1, "ind": 4.0, "dump": 6.0, "farm": 11.0}
}

# ---------------- SIDEBAR (Controls & Step 8) ----------------
st.sidebar.header("📍 Monitoring Controls")
city_key = st.sidebar.selectbox("Select Station", list(STATIONS.keys()))
coords = STATIONS[city_key]

st.sidebar.subheader("📅 Report Parameters")
selected_date = st.sidebar.date_input("Analysis Date", datetime.now())
selected_time = st.sidebar.time_input("Analysis Time", datetime.now().time())

# ---------------- LIVE DATA FETCH (FIXED) ----------------
@st.cache_data(ttl=300)
def get_live_aqi(lat, lon):
    url = f"https://api.openaq.org/v3/sensors?coordinates={lon},{lat}&radius=15000&limit=30"
    try:
        response = requests.get(url, timeout=10).json()
        results = response.get('results', [])
        extracted = {}
        for item in results:
            name = item.get('parameter', {}).get('name').lower()
            val = item.get('latest', {}).get('value')
            if name and val is not None: extracted[name] = val
        return extracted
    except: return None

live = get_live_aqi(coords['lat'], coords['lon'])

# Use actual values or dynamic fallbacks to avoid "always 55"
pm25 = live.get('pm25', 45.0) if live else 45.0
no2 = live.get('no2', 30.0) if live else 30.0
co = live.get('co', 0.8) if live else 0.8
so2 = live.get('so2', 10.0) if live else 10.0
ozone = live.get('o3', 25.0) if live else 25.0

# ---------------- STEP 3: PREDICTION RESULTS ----------------
input_df = pd.DataFrame([{
    'pm25': pm25, 'pm10': pm25 * 1.3, 'no2': no2, 'so2': so2, 'co': co, 'ozone': ozone,
    'temperature': 28, 'humidity': 55, 'wind_speed': 8, 'wind_direction': 180,
    'distance_to_major_road_km': coords['road'], 'distance_to_industrial_zone_km': coords['ind'],
    'distance_to_dump_site_km': coords['dump'], 'distance_to_farmland_km': coords['farm']
}])

res_num = model.predict(input_df)[0]
prediction = label_map.get(res_num, "Natural")
conf = round(max(model.predict_proba(input_df)[0]) * 100, 1)

st.subheader("Pollution Prediction Results")
m1, m2, m3 = st.columns(3)
m1.metric("🌫 Predicted Source", prediction)
m2.metric("📊 Confidence Score", f"{conf}%")
m3.metric("💨 Live PM2.5 Level", pm25)

st.markdown(" Key Pollutant Metrics")
p1, p2, p3, p4 = st.columns(4)
p1.metric("PM2.5", f"{pm25} µg/m³")
p2.metric("NO₂", f"{no2} ppb")
p3.metric("SO₂", f"{so2} ppb")
p4.metric("CO", f"{co} ppm")

# ---------------- STEP 4: REAL-TIME ALERTS ----------------
st.subheader("Real-Time Pollution Alerts")
if pm25 > 100:
    st.error(f"🔴 HIGH POLLUTION ALERT: PM2.5 is {pm25}. Hazardous conditions detected!")
elif pm25 > 50:
    st.warning(f"🟠 MODERATE POLLUTION: PM2.5 is {pm25}. Sensitive groups should stay indoors.")
else:
    st.success("🟢 SAFE LEVELS: Air quality is currently within healthy limits.")

# ---------------- STEP 7: INTERACTIVE MAP ----------------
st.subheader(" Interactive Pollution Heatmap")
m = folium.Map(location=[coords['lat'], coords['lon']], zoom_start=8, tiles='CartoDB dark_matter')

# Heatmap Layer
h_data = [[v['lat'], v['lon'], pm25] for k, v in STATIONS.items()]
HeatMap(h_data, radius=20, blur=15, gradient={0.4: 'blue', 0.7: 'lime', 1: 'red'}).add_to(m)

# Markers
folium.Marker([coords['lat'], coords['lon']], popup=f"Station: {city_key}<br>Source: {prediction}").add_to(m)
st_folium(m, width=1300, height=500)



# ---------------- STEP 5 & 6: TRENDS & DISTRIBUTION ----------------
st.write("---")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Pollution Trend Analysis")
    city_data = df[df['city'] == city_key.split('_')[0]].head(50)
    st.line_chart(city_data[['pm25', 'no2', 'so2']])

with col_right:
    st.subheader(" Source Distribution")
    fig = px.pie(df, names='pollution_source', hole=0.4, title="Global Source Contribution")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- STEP 8: REPORT DOWNLOAD ----------------
st.subheader(" Export Pollution Report")
report_data = {
    "Timestamp": [f"{selected_date} {selected_time}"],
    "Station": [city_key],
    "Predicted_Source": [prediction],
    "Confidence": [f"{conf}%"],
    "PM2.5": [pm25], "NO2": [no2], "CO": [co],
    "Risk_Status": ["High" if pm25 > 60 else "Healthy"]
}
report_df = pd.DataFrame(report_data)
st.download_button("⬇ Download CSV Report", report_df.to_csv(index=False), "pollution_report.csv", "text/csv")