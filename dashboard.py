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
    df["date"] = df["timestamp"].dt.date

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

    if isinstance(model_data, dict):
        return model_data["model"]
    return model_data

model = load_model()

# ------------------------------------------------
# DATASET RANGE
# ------------------------------------------------
min_date = data["date"].min()
max_date = data["date"].max()

st.info(f"Dataset available from {min_date} to {max_date}")

# ------------------------------------------------
# SIDEBAR INPUTS
# ------------------------------------------------
st.sidebar.header("User Inputs")

city = st.sidebar.selectbox(
    "Select City",
    sorted(data["city"].dropna().unique())
)

date = st.sidebar.date_input(
    "Select Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

threshold = st.sidebar.slider(
    "PM2.5 Alert Threshold",
    0, 300, 100
)

# ------------------------------------------------
# FILTER DATA
# ------------------------------------------------
filtered_data = data[data["city"] == city]
filtered_data = filtered_data[filtered_data["date"] == date]

if filtered_data.empty:
    st.warning("No data available for selected city and date")
    st.stop()

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
# DISPLAY INFO
# ------------------------------------------------
st.write(f"📍 Location: {city}")
st.write(f"📅 Date: {date}")

# ------------------------------------------------
# METRICS
# ------------------------------------------------
st.subheader("Prediction Results")

col1, col2, col3 = st.columns(3)

col1.metric("Predicted Source", prediction)
col2.metric("Confidence", f"{confidence:.2f}%")
col3.metric("PM2.5 Level", row["pm25"])

# ------------------------------------------------
# AQI STATUS
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
# EXPLANATION
# ------------------------------------------------
st.info(f"The system predicts that pollution is mainly caused by **{prediction}** based on environmental and location features.")

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
        names=source_counts.index,
        title="Pollution Source Categories"
    )

    st.plotly_chart(fig2, width='stretch')

# ------------------------------------------------
# INTERACTIVE MAP (FINAL FIXED)
# ------------------------------------------------
st.subheader("Pollution Map")

colA, colB, colC = st.columns(3)

with colA:
    show_heatmap = st.checkbox("Show Heatmap", value=True)

with colB:
    show_markers = st.checkbox("Show Locations")

with colC:
    show_high = st.checkbox("Show High Pollution Areas")

map_data = filtered_data[["latitude","longitude","pm25"]].dropna()

if map_data.empty:
    st.warning("No map data available")
else:
    m = folium.Map(
        location=[map_data["latitude"].mean(), map_data["longitude"].mean()],
        zoom_start=12
    )

    # Heatmap
    if show_heatmap:
        HeatMap(map_data.values.tolist(), radius=15, blur=20).add_to(m)

    # Locations
    if show_markers:
        for _, r in map_data.iterrows():
            folium.CircleMarker(
                location=[r["latitude"], r["longitude"]],
                radius=7,
                color="blue",
                fill=True,
                fill_color="blue",
                fill_opacity=0.7,
                popup=f"PM2.5: {r['pm25']}"
            ).add_to(m)

    # High Pollution
    if show_high:
        high_data = map_data[map_data["pm25"] > threshold]

        if high_data.empty:
            st.warning("No high pollution areas for this threshold")
        else:
            for _, r in high_data.iterrows():
                folium.CircleMarker(
                    location=[r["latitude"], r["longitude"]],
                    radius=9,
                    color="red",
                    fill=True,
                    fill_color="red",
                    fill_opacity=0.9,
                    popup=f"🚨 PM2.5: {r['pm25']}"
                ).add_to(m)

    st_folium(m, key=f"map_{show_heatmap}_{show_markers}_{show_high}", width=1000, height=500)

# ------------------------------------------------
# DOWNLOAD
# ------------------------------------------------
st.subheader("Download Report")

csv = city_data.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "pollution_report.csv",
    "text/csv"
)