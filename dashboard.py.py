import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# =============================
# PAGE TITLE
# =============================

st.set_page_config(page_title="EnviroScan Dashboard")
st.title("🌍 EnviroScan: Pollution Monitoring Dashboard")

# =============================
# LOAD DATA
# =============================

data = pd.read_csv("data/final_environment_dataset.csv")

# =============================
# SIDEBAR — USER INPUTS
# =============================

st.sidebar.header("User Controls")

city = st.sidebar.selectbox(
    "Select City",
    data["city"].unique() if "city" in data.columns else ["Default"]
)

lat = st.sidebar.number_input("Latitude", value=17.38)
lon = st.sidebar.number_input("Longitude", value=78.48)

# =============================
# FILTER DATA
# =============================

if "city" in data.columns:
    filtered = data[data["city"] == city]
else:
    filtered = data

latest = filtered.iloc[-1]

# =============================
# STEP 3: PREDICTION RESULTS
# =============================

st.header("🔮 Pollution Prediction")

st.metric("Predicted Source", latest.get("pollution_source", "Unknown"))
st.metric("PM2.5 Level", latest.get("pm25", 0))
st.metric("NO₂ Level", latest.get("no2", 0))

# =============================
# STEP 4: ALERT SYSTEM
# =============================

st.header("🚨 Pollution Alerts")

if latest.get("pm25", 0) > 100:
    st.error("⚠ High PM2.5 — Unhealthy Air")

if latest.get("no2", 0) > 80:
    st.warning("⚠ High NO₂ — Hazardous")

# =============================
# STEP 5: TREND CHART
# =============================

st.header("📈 Pollution Trends")

if "date" in filtered.columns:
    fig = px.line(
        filtered,
        x="date",
        y=["pm25", "no2"],
        title="Pollution Trend Over Time"
    )
    st.plotly_chart(fig)

# =============================
# STEP 6: SOURCE DISTRIBUTION
# =============================

st.header("🥧 Source Distribution")

if "pollution_source" in filtered.columns:
    pie = px.pie(
        filtered,
        names="pollution_source",
        title="Pollution Sources"
    )
    st.plotly_chart(pie)

# =============================
# STEP 7: INTERACTIVE MAP
# =============================

st.header("🗺 Pollution Map")

m = folium.Map(location=[lat, lon], zoom_start=10)

for _, row in filtered.iterrows():
    if "latitude" in row and "longitude" in row:
        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=row.get("pollution_source", "Unknown")
        ).add_to(m)

st_folium(m)

# =============================
# STEP 8: DOWNLOAD REPORT
# =============================

st.header("📥 Download Report")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV Report",
    csv,
    "pollution_report.csv",
    "text/csv"
)