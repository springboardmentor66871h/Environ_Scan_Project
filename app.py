


import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
# ===============================
# Page Config
# ===============================
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")
st.title("🌍 EnviroScan - Pollution Monitoring Dashboard")

# ===============================
# Load Data
# ===============================
data = pd.read_csv("data/processed/final_dataset.csv")

# Clean column names
data.columns = data.columns.str.strip()

# Convert date column
data["last_update"] = pd.to_datetime(data["last_update"], errors="coerce")

# ===============================
# Load Model
# ===============================
model = joblib.load("models/pollution_model.pkl")

# Label mapping (VERY IMPORTANT)
label_map = {
    0: "Agricultural",
    1: "Industrial",
    2: "Vehicular",
    3: "Burning",
    4: "Natural"
}

all_sources = ["Agricultural", "Industrial", "Vehicular", "Burning", "Natural"]

# ===============================
# Sidebar
# ===============================
st.sidebar.title("🌍 EnviroScan Navigator")

city = st.sidebar.selectbox(
    "Select City",
    data["City"].dropna().unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [
        data["last_update"].dt.date.min(),
        data["last_update"].dt.date.max()
    ]
)

# ===============================
# Filter Data
# ===============================
filtered_data = data[
    (data["City"] == city) &
    (data["last_update"].dt.date >= date_range[0]) &
    (data["last_update"].dt.date <= date_range[1])
]

if filtered_data.empty:
    st.warning("No data available")
    st.stop()

# ===============================
# Metrics
# ===============================
st.subheader("📊 Pollution Levels")

col1, col2, col3 = st.columns(3)

col1.metric("Average", round(filtered_data["pollutant_avg"].mean(), 2))
col2.metric("Minimum", round(filtered_data["pollutant_min"].mean(), 2))
col3.metric("Maximum", round(filtered_data["pollutant_max"].mean(), 2))

# ===============================
# Alert
# ===============================
st.subheader("🚨 Pollution Alert")

avg = filtered_data["pollutant_avg"].mean()

if avg > 80:
    st.error("High Pollution Alert")
elif avg > 50:
    st.warning("Moderate Pollution")
else:
    st.success("Air Quality Safe")

# ===============================
# Prediction
# ===============================
st.subheader("🤖 Predicted Pollution Source")

features = filtered_data[[
    "pollutant_min",
    "pollutant_max",
    "pollutant_avg",
    "Nearest_Road_km",
    "Nearest_Industry_km",
    "Nearest_Dump_km",
    "Nearest_Farm_km"
]].astype(float)

prediction = model.predict(features)

# Convert to label
prediction_labels = [label_map.get(p, str(p)) for p in prediction]

st.write("Predicted Source:", pd.Series(prediction_labels).mode()[0])

# ===============================
# TREND CHART (LIKE FRIEND)
# ===============================
st.subheader("📈 Pollution Trend")

trend = filtered_data.copy().reset_index(drop=True)

trend["time_seq"] = pd.date_range(
    start=trend["last_update"].min(),
    periods=len(trend),
    freq="H"
)

fig = px.line(
    trend,
    x="time_seq",
    y="pollutant_avg",
    markers=True,
    title="Pollution Trend Over Time",
    color_discrete_sequence=["#00C49F"]
)

st.plotly_chart(fig, width="stretch")

# ===============================
# SOURCE DISTRIBUTION (FULL FIX)
# ===============================
st.subheader("📊 Source Distribution")

city_data = data[data["City"] == city]

# Case 1: dataset already has labels
if "pollution_source" in city_data.columns:
    source_counts = city_data["pollution_source"].value_counts()

# Case 2: use model predictions
else:
    temp_features = city_data[[
        "pollutant_min",
        "pollutant_max",
        "pollutant_avg",
        "Nearest_Road_km",
        "Nearest_Industry_km",
        "Nearest_Dump_km",
        "Nearest_Farm_km"
    ]].astype(float)

    preds = model.predict(temp_features)

    preds = [label_map.get(p, str(p)) for p in preds]

    source_counts = pd.Series(preds).value_counts()

# Ensure ALL categories appear
source_counts = source_counts.reindex(all_sources, fill_value=0).reset_index()
source_counts.columns = ["Source", "Count"]

# PIE CHART
pie = px.pie(
    source_counts,
    names="Source",
    values="Count",
    hole=0.5,
    color="Source",
    color_discrete_map={
        "Agricultural": "#00C49F",
        "Industrial": "#FF8042",
        "Vehicular": "#0088FE",
        "Burning": "#FFBB28",
        "Natural": "#AA66CC"
    }
)

pie.update_traces(textinfo="percent+label")

st.plotly_chart(pie, width="stretch")

# ===============================
# HEATMAP
# ===============================
st.subheader("🗺 Pollution Heatmap")

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

map_data = filtered_data.dropna(
    subset=["Latitude", "Longitude", "pollutant_avg"]
)

if not map_data.empty:

    base_map = folium.Map(
        location=[map_data["Latitude"].mean(), map_data["Longitude"].mean()],
        zoom_start=10
    )

    heat_data = [
        [row["Latitude"], row["Longitude"], row["pollutant_avg"]]
        for _, row in map_data.iterrows()
    ]

    HeatMap(heat_data, radius=15, blur=20).add_to(base_map)

    st_folium(base_map, width=900, height=500)

else:
    st.warning("No valid map data available")

# ===============================
# DOWNLOAD
# ===============================
st.subheader("⬇ Download Report")

csv = filtered_data.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="pollution_report.csv",
    mime="text/csv"
)