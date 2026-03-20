import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import io
from datetime import datetime
import requests
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="EnviroScan Dashboard",
    layout="wide"
)

st.title("🌍 EnviroScan: Real-Time Air Pollution Monitoring System")

st_autorefresh(interval=10000, key="refresh")
st.caption("🔴 Live Data Updating Every 10 Seconds")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("Final_Labeled_Pollution_Dataset.csv")
df.columns = df.columns.str.strip()

# -----------------------------
# API FUNCTION
# -----------------------------
API_KEY = "88c81421405483f41aef52baf7faaeda"

def get_real_time_pollution(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()
        comp = data["list"][0]["components"]

        return {
            "pm25": comp.get("pm2_5", 0),
            "pm10": comp.get("pm10", 0),
            "no2": comp.get("no2", 0),
            "co": comp.get("co", 0)
        }

    except:
        return None

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("📊 Dashboard Controls")

city = st.sidebar.selectbox("Select City", df["city"].unique())

city_data = df[df["city"] == city]

if city_data.empty:
    st.error("No data available for selected city")
    st.stop()

lat = city_data["latitude"].iloc[0]
lon = city_data["longitude"].iloc[0]

# -----------------------------
# GET LIVE DATA
# -----------------------------
live_data = get_real_time_pollution(lat, lon)

# -----------------------------
# AQI FUNCTION
# -----------------------------
def get_aqi_status(pm25):
    if pm25 <= 30:
        return "Good", "green"
    elif pm25 <= 80:
        return "Moderate", "orange"
    else:
        return "Unhealthy", "red"

# -----------------------------
# Current Metrics
# -----------------------------
st.subheader("📈 Current Pollution Metrics")

col1, col2, col3, col4 = st.columns(4)

if live_data:
    pm25_value = live_data["pm25"]
    pm10_value = live_data["pm10"]
    no2_value = live_data["no2"]
    co_value = live_data["co"] / 1000

    st.success("✅ Live Data from API")

else:
    pm25_value = city_data["pm25"].mean()
    pm10_value = city_data["pm10"].mean()
    no2_value = city_data["no2"].mean()
    co_value = city_data["co"].mean()

    st.warning("⚠ Using Dataset (API not available)")

col1.metric("PM2.5 (µg/m³)", round(pm25_value,2))
col2.metric("PM10 (µg/m³)", round(pm10_value,2))
col3.metric("NO2 (ppb)", round(no2_value,2))
col4.metric("CO (ppm)", round(co_value,2))

st.caption(f"🕒 Last Updated: {datetime.now().strftime('%H:%M:%S')}")

# -----------------------------
# AQI DISPLAY
# -----------------------------
aqi_status, color = get_aqi_status(pm25_value)

st.markdown(f"""
### Air Quality Status: <span style='color:{color}'>{aqi_status}</span>
""", unsafe_allow_html=True)

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("Models/pollution_source_model.joblib")
encoder = joblib.load("Models/label_encoder.joblib")

input_data = pd.DataFrame({
    "co":[co_value],
    "no2":[no2_value],
    "o3":[0],
    "pm10":[pm10_value],
    "pm25":[pm25_value],
    "so2":[0],
    "Temperature":[0],
    "Humidity":[0],
    "Wind Speed":[0],
    "Wind Direction":[0],
    "dist_road":[0],
    "dist_industry":[0],
    "dist_dump":[0],
    "dist_farmland":[0]
})

prediction = model.predict(input_data)
source = encoder.inverse_transform(prediction)

st.subheader("🔍 Predicted Pollution Source")
st.success(source[0])

# -----------------------------
# Alerts
# -----------------------------
st.subheader("⚠️ Pollution Alerts")

if pm25_value > 150:
    st.error(f"🚨 Unhealthy Air! PM2.5 = {pm25_value:.2f}")
elif pm25_value > 80:
    st.warning(f"⚠ Moderate Air Quality PM2.5 = {pm25_value:.2f}")
else:
    st.success(f"✅ Good Air Quality PM2.5 = {pm25_value:.2f}")

# -----------------------------
# Trends
# -----------------------------
st.subheader("Pollution Trends")
st.line_chart(city_data[["pm25","pm10","no2","co"]])

# -----------------------------
# TABS
# -----------------------------
st.markdown("## 📑 Environmental Data")

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Map",
    "📊 Sources",
    "🤖 AI Model",
    "📥 Download"
])

# TAB 1
with tab1:
    try:
        with open("pollution_map.html","r",encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=600)
    except:
        st.warning("Map not found")

# TAB 2
with tab2:

    st.subheader("📊 Pollution Source Distribution")

    if "pollution_source" in df.columns:

        # -----------------------------
        # PIE + BAR CHART
        # -----------------------------
        col1, col2 = st.columns(2)

        # Pie Chart
        fig_pie = px.pie(
            df,
            names="pollution_source",
            title="Overall Distribution"
        )
        col1.plotly_chart(fig_pie, use_container_width=True)

        # Bar Chart
        source_counts = df["pollution_source"].value_counts()

        fig_bar = px.bar(
            x=source_counts.index,
            y=source_counts.values,
            labels={"x": "Source", "y": "Count"},
            title="Source Comparison"
        )
        col2.plotly_chart(fig_bar, use_container_width=True)

        # -----------------------------
        # CITY-WISE ANALYSIS
        # -----------------------------
        st.subheader("🏙️ City-wise Pollution Source")

        city_source = df.groupby(["city", "pollution_source"]).size().reset_index(name="count")

        fig_city = px.bar(
            city_source,
            x="city",
            y="count",
            color="pollution_source",
        )

        st.plotly_chart(fig_city, use_container_width=True)


# TAB 3
with tab3:

    st.subheader("🤖 AI Model Analysis")

    # Row 1 → Confusion Matrices
    col1, col2 = st.columns(2)

    col1.markdown("### Random Forest")
    col1.image("Image/Matrix.png", use_container_width=True)

    col2.markdown("### Decision Tree")
    col2.image("Image/Matrix-Decision_tree.png", use_container_width=True)

    # Row 2
    col1, col2 = st.columns(2)

    col1.markdown("### XGBoost")
    col1.image("Image/Matrix-XGBoost.png", use_container_width=True)

    col2.markdown("### Feature Importance")
    col2.image("Image/Random_forest.png", use_container_width=True)

# TAB 4
with tab4:
    report_df = city_data.copy()
    label_map = {
    "A": "Natural",
    "B": "Vehicular",
    "C": "Industrial",
    "D": "Agriculture"
    }

    report_df["Predicted Source"] = label_map.get(source[0], source[0])
    report_df["Generated Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.download_button(
        "Download CSV",
        report_df.to_csv(index=False),
        f"{city}_report.csv"
    )