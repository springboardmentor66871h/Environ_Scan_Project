import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import folium
from folium.plugins import HeatMap

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")
st.title("🌍 EnviroScan: Pollution Monitoring Dashboard")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/final_dataset.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["city"] = df["city"].astype(str)
    df = df[df["city"] != "nan"]
    return df

data = load_data()

# ------------------------------------------------
# LOAD MODEL
# ------------------------------------------------
@st.cache_resource
def load_model():
    model_data = joblib.load("models/best_model.joblib")
    return model_data["model"] if isinstance(model_data, dict) else model_data

model = load_model()

# ------------------------------------------------
# LABEL MAP
# ------------------------------------------------
label_map = {
    0: "Natural",
    1: "Vehicular",
    2: "Industrial",
    3: "Burning",
    4: "Agricultural"
}

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------
st.sidebar.header("User Inputs")

city = st.sidebar.selectbox(
    "Select City",
    sorted(data["city"].dropna().unique())
)

threshold = st.sidebar.slider("PM2.5 Alert Threshold", 0, 300, 100)

# ------------------------------------------------
# FILTER DATA
# ------------------------------------------------
city_data = data[data["city"] == city]

if city_data.empty:
    st.warning("No data available")
    st.stop()

city_data = city_data.sort_values(by="timestamp", ascending=False)
row = city_data.iloc[0]

# ------------------------------------------------
# MODEL INPUT
# ------------------------------------------------
input_data = pd.DataFrame({
    "latitude":[row["latitude"]],
    "longitude":[row["longitude"]],
    "pm25":[row["pm25"]],
    "pm10":[row["pm10"]],
    "co":[row["co"]],
    "no2":[row["no2"]],
    "so2":[row["so2"]],
    "o3":[row["o3"]],
    "temperature":[row["temperature"]],
    "humidity":[row["humidity"]],
    "wind_speed":[row["wind_speed"]],
    "wind_direction":[row["wind_direction"]],
    "distance_to_road":[row["distance_to_road"]],
    "distance_to_industry":[row["distance_to_industry"]],
    "distance_to_dump":[row["distance_to_dump"]],
    "distance_to_farmland":[row["distance_to_farmland"]]
})

# ------------------------------------------------
# PREDICTION
# ------------------------------------------------
prediction = model.predict(input_data)[0]

if isinstance(prediction, (int, np.integer)):
    predicted_label = label_map.get(int(prediction), "Unknown")
else:
    predicted_label = str(prediction)

confidence = 0
if hasattr(model, "predict_proba"):
    confidence = np.max(model.predict_proba(input_data)) * 100

# ------------------------------------------------
# DISPLAY
# ------------------------------------------------
st.subheader("Prediction Results")
c1, c2, c3 = st.columns(3)

c1.metric("Predicted Source", predicted_label)
c2.metric("Confidence", f"{confidence:.2f}%")
c3.metric("PM2.5 Level", round(row["pm25"],2))

# AQI
if row["pm25"] <= 50:
    st.success("🟢 Good Air Quality")
elif row["pm25"] <= 100:
    st.warning("🟡 Moderate Air Quality")
else:
    st.error("🔴 Unhealthy Air Quality")

# ALERT
st.subheader("Pollution Alert")
if row["pm25"] > threshold:
    st.error("🚨 High Pollution Alert")
else:
    st.success("Air Quality Within Safe Limits")

# ------------------------------------------------
# TRENDS
# ------------------------------------------------
st.subheader("Pollution Trends")

fig = px.line(city_data, x="timestamp", y=["pm25","pm10","no2","co"])
st.plotly_chart(fig, width='stretch')

# ------------------------------------------------
# MAP (REALISTIC + NO FLICKER)
# ------------------------------------------------
st.subheader("Pollution Map")

map_data = city_data[["latitude","longitude","pm25"]].dropna()

if len(map_data) > 200:
    map_data = map_data.sample(200, random_state=42)

if map_data.empty:
    st.warning("No map data available")
else:
    base_lat = map_data["latitude"].iloc[0]
    base_lon = map_data["longitude"].iloc[0]

    # ------------------------------------------------
    # REALISTIC GRID-BASED SPREAD
    # ------------------------------------------------
    grid_size = 12
    lat_range = np.linspace(base_lat - 0.02, base_lat + 0.02, grid_size)
    lon_range = np.linspace(base_lon - 0.02, base_lon + 0.02, grid_size)

    grid_points = []

    for lat in lat_range:
        for lon in lon_range:
            pm = np.random.choice(map_data["pm25"])
            grid_points.append([lat, lon, pm])

    map_data = pd.DataFrame(grid_points, columns=["latitude","longitude","pm25"])

    # create map
    m = folium.Map(
        location=[base_lat, base_lon],
        zoom_start=11
    )

    HeatMap(
        map_data.values.tolist(),
        radius=10,
        blur=15
    ).add_to(m)

    # legend
    legend_html = """
    <div style="
        position: fixed; 
        bottom: 50px; left: 50px; width: 180px; height: 120px; 
        background-color: white; 
        border:1px solid grey; z-index:9999; font-size:12px;
        padding: 8px;">
        <b>Pollution Intensity</b><br>
        🔵 Low<br>
        🟢 Medium<br>
        🔴 High
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # save + display (NO FLICKER)
    m.save("temp_map.html")

    with open("temp_map.html", "r", encoding="utf-8") as f:
        html_data = f.read()

    st.components.v1.html(html_data, height=500)

# ------------------------------------------------
# DOWNLOAD
# ------------------------------------------------
st.subheader("Download Report")

csv = city_data.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "pollution_report.csv")