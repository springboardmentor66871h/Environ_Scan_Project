import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import folium
from streamlit_folium import st_folium
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")

# ---------------- CSS (WHITE PROFESSIONAL UI) ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
    color: #1e293b;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #0f172a;
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}
.metric-card h2 {
    color: #2563eb;
}
.alert-box {
    background: #fde68a;
    padding: 12px;
    border-radius: 10px;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, "labeled_dataset.csv")
model_path = os.path.join(BASE_DIR, "models", "pollution_model.joblib")

# ---------------- LOAD DATA ----------------
if not os.path.exists(data_path):
    st.error(f"❌ Dataset not found at:\n{data_path}")
    st.stop()

df = pd.read_csv(data_path)

# FIX DATA
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df = df.dropna(subset=['latitude', 'longitude'])

# ---------------- LOAD MODEL ----------------
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 EnviroScan Dashboard")

cities = df['city'].dropna().unique()

if len(cities) == 0:
    st.error("❌ No city data found in dataset")
    st.stop()

selected_city = st.sidebar.selectbox("Select City", cities)

city_data = df[df['city'] == selected_city].iloc[0]

# ---------------- HEADER ----------------
st.markdown(
    f"<div class='main-title'>📍 {selected_city} Environmental Monitoring</div>",
    unsafe_allow_html=True
)

pm25 = city_data['pm25']

# ---------------- ALERT ----------------
if pm25 > 100:
    st.markdown(
        f"<div class='alert-box'>⚠ High Pollution Alert: PM2.5 = {pm25}</div>",
        unsafe_allow_html=True
    )

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class='metric-card'>
<h4>Temperature</h4>
<h2>{city_data['temperature']} °C</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class='metric-card'>
<h4>Humidity</h4>
<h2>{city_data['humidity']} %</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class='metric-card'>
<h4>PM2.5</h4>
<h2>{pm25}</h2>
</div>
""", unsafe_allow_html=True)

# ---------------- PREDICTION ----------------
features = ['pm25','no2','o3','temperature','humidity','wind_speed','pressure']

if model:
    try:
        X_pred = pd.DataFrame([city_data[features]])
        prediction = model.predict(X_pred)[0]
    except:
        prediction = "Error"
else:
    prediction = city_data.get('source_label', "N/A")

col4.markdown(f"""
<div class='metric-card'>
<h4>Pollution Source</h4>
<h2>{prediction}</h2>
</div>
""", unsafe_allow_html=True)

st.write("---")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🗺 Map", "📊 Analytics", "📥 Download"])

# ================= MAP =================
with tab1:
    st.subheader("Geospatial View (India)")

    lat = float(city_data['latitude'])
    lon = float(city_data['longitude'])

    m = folium.Map(location=[lat, lon], zoom_start=7)

    # Color logic
    if pm25 > 100:
        color = "red"
    elif pm25 > 60:
        color = "orange"
    else:
        color = "green"

    popup = f"""
    <b>City:</b> {selected_city}<br>
    <b>PM2.5:</b> {pm25}<br>
    <b>Temp:</b> {city_data['temperature']}°C<br>
    <b>Humidity:</b> {city_data['humidity']}%
    """

    folium.Marker(
        [lat, lon],
        popup=popup,
        icon=folium.Icon(color=color)
    ).add_to(m)

    folium.Circle(
        [lat, lon],
        radius=20000,
        color=color,
        fill=True,
        fill_opacity=0.2
    ).add_to(m)

    st_folium(m, use_container_width=True, height=550)

# ================= ANALYTICS =================
with tab2:
    st.subheader("Pollution Analysis")

    fig1 = px.histogram(df, x="pm25", title="PM2.5 Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.scatter(
        df,
        x="temperature",
        y="pm25",
        color="source_label",
        title="Temperature vs Pollution"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ================= DOWNLOAD =================
with tab3:
    st.subheader("Download Data")

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Dataset",
        data=csv,
        file_name="enviroscan_data.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("EnviroScan AI Dashboard | Built with Streamlit 🚀")