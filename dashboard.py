import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

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
# SIDEBAR INPUTS
# ------------------------------------------------
st.sidebar.header("User Inputs")

city = st.sidebar.selectbox(
    "Select City",
    sorted(data["city"].dropna().unique())
)

threshold = st.sidebar.slider("PM2.5 Alert Threshold", 0, 300, 100)

# Map controls (moved to sidebar → less flicker)
st.sidebar.subheader("Map Controls")
show_heatmap = st.sidebar.checkbox("Show Heatmap", True)
show_markers = st.sidebar.checkbox("Show Locations")
show_high = st.sidebar.checkbox("Show High Pollution Areas")

# ------------------------------------------------
# FILTER DATA (LATEST)
# ------------------------------------------------
filtered_data = data[data["city"] == city]

if filtered_data.empty:
    st.warning("No data available for selected city")
    st.stop()

filtered_data = filtered_data.sort_values(by="timestamp", ascending=False)
row = filtered_data.iloc[0]

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

confidence = 0
if hasattr(model, "predict_proba"):
    confidence = np.max(model.predict_proba(input_data)) * 100

# ------------------------------------------------
# SOURCE LABEL
# ------------------------------------------------
source_map = {
    0: "🌿 Natural",
    1: "🚗 Vehicular",
    2: "🏭 Industrial",
    3: "🔥 Burning",
    4: "🌾 Agricultural"
}
predicted_label = source_map.get(prediction, "Unknown")

# ------------------------------------------------
# DISPLAY
# ------------------------------------------------
st.write(f"📍 Location: {city} (Latest Data)")

st.subheader("Prediction Results")
col1, col2, col3 = st.columns(3)

col1.metric("Predicted Source", predicted_label)
col2.metric("Confidence", f"{confidence:.2f}%")
col3.metric("PM2.5 Level", round(row["pm25"], 2))

# ------------------------------------------------
# AQI
# ------------------------------------------------
if row["pm25"] <= 50:
    st.success("🟢 Good Air Quality")
elif row["pm25"] <= 100:
    st.warning("🟡 Moderate Air Quality")
else:
    st.error("🔴 Unhealthy Air Quality")

# ------------------------------------------------
# ALERT
# ------------------------------------------------
st.subheader("Pollution Alert")

if row["pm25"] > threshold:
    st.error("🚨 High Pollution Alert")
else:
    st.success("Air Quality Within Safe Limits")

# ------------------------------------------------
# SOURCE INSIGHT
# ------------------------------------------------
st.subheader("Source Insight")

if "Vehicular" in predicted_label:
    st.write("🚗 Traffic emissions are major contributors.")
elif "Industrial" in predicted_label:
    st.write("🏭 Industrial pollution detected.")
elif "Burning" in predicted_label:
    st.write("🔥 Burning activities contributing.")
elif "Agricultural" in predicted_label:
    st.write("🌾 Agricultural pollution detected.")
else:
    st.write("🌿 Natural environmental influence.")

# ------------------------------------------------
# TRENDS
# ------------------------------------------------
st.subheader("Pollution Trends")

city_data = data[data["city"] == city]

fig = px.line(
    city_data,
    x="timestamp",
    y=["pm25","pm10","no2","co"],
    title=f"Pollution Trends in {city}"
)

st.plotly_chart(fig, width='stretch')

# ------------------------------------------------
# SOURCE DISTRIBUTION
# ------------------------------------------------
if "pollution_source" in data.columns:
    st.subheader("Pollution Source Distribution")

    source_counts = city_data["pollution_source"].value_counts()

    fig2 = px.pie(
        values=source_counts.values,
        names=source_counts.index
    )

    st.plotly_chart(fig2, width='stretch')

# ------------------------------------------------
# MAP (NO FLICKER VERSION)
# ------------------------------------------------
st.subheader("Pollution Map")

map_data = filtered_data[["latitude","longitude","pm25"]].dropna()

if not map_data.empty:
    m = folium.Map(
        location=[map_data["latitude"].mean(), map_data["longitude"].mean()],
        zoom_start=12
    )

    if show_heatmap:
        HeatMap(map_data.values.tolist(), radius=15, blur=20).add_to(m)

    if show_markers:
        for _, r in map_data.iterrows():
            folium.CircleMarker(
                location=[r["latitude"], r["longitude"]],
                radius=6,
                color="blue",
                fill=True
            ).add_to(m)

    if show_high:
        high_data = map_data[map_data["pm25"] > threshold]
        for _, r in high_data.iterrows():
            folium.CircleMarker(
                location=[r["latitude"], r["longitude"]],
                radius=8,
                color="red",
                fill=True
            ).add_to(m)

    st_folium(m, width=1000, height=500)

# ------------------------------------------------
# DOWNLOAD
# ------------------------------------------------
st.subheader("Download Report")

csv = city_data.to_csv(index=False).encode("utf-8")

st.download_button("Download CSV", csv, "pollution_report.csv")