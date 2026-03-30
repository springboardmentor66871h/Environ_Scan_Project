import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from datetime import datetime
import joblib
import pyttsx3

st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")
st.title("EnviroScan – Air Pollution Intelligence Dashboard")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("Navigate")
page = st.sidebar.radio("Go to", ["Dashboard", "Pie Chart", "Map", "History", "Downloads"])

# 🔍 SEARCH BY CITY
search_query = st.sidebar.text_input("Search City (e.g., Delhi, Chennai)")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/final_labeled_with_weather.csv")
    df = df.dropna(subset=["latitude", "longitude"])
    return df

df = load_data()

# -------------------------
# APPLY SEARCH FILTER
# -------------------------
if search_query:
    df = df[df["location"].str.contains(search_query, case=False, na=False)]

st.sidebar.write("Available Cities:", df["location"].dropna().unique())
st.sidebar.write(f"Filtered Records: {len(df)}")

# -------------------------
# LOAD MODEL
# -------------------------
@st.cache_resource
def load_model():
    return joblib.load("models/pollution_model.pkl")

model = load_model()

# -------------------------
# AQI FUNCTION
# -------------------------
def get_aqi_info(aqi):
    if aqi <= 50:
        return "Good", "Air quality is satisfactory."
    elif aqi <= 100:
        return "Moderate", "Acceptable air quality."
    elif aqi <= 150:
        return "Unhealthy for Sensitive", "Sensitive groups should be careful."
    elif aqi <= 200:
        return "Unhealthy", "Everyone may feel effects."
    elif aqi <= 300:
        return "Very Unhealthy", "Health warnings."
    else:
        return "Hazardous", "Serious health effects."

# =====================================================
# DASHBOARD
# =====================================================
if page == "Dashboard":

    total_records = len(df)
    avg_pm10 = round(df["PM10"].mean(), 2) if len(df) > 0 else 0
    pollution_sources = df["pollution_source"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", total_records)
    col2.metric("Average PM10", avg_pm10)
    col3.metric("Pollution Sources", pollution_sources)

    st.divider()

    st.subheader("Air Quality Index")

    if len(df) > 0:
        aqi_value = int(df["PM10"].mean())
        status, message = get_aqi_info(aqi_value)
        st.success(f"AQI: {aqi_value} — {status}")
        st.info(message)
    else:
        st.warning("No data available")

    def speak(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    if st.button("Speak AQI") and len(df) > 0:
        speak(f"Air quality is {status}. {message}")

    # Prediction
    try:
        feature_cols = [
            "CO", "NO2", "O3", "PM10", "SO2",
            "temperature", "humidity", "wind_speed",
            "distance_to_road_m", "distance_to_industry_m",
            "distance_to_farmland_m", "distance_to_dump_m"
        ]

        if len(df) > 0:
            sample = df.iloc[0]
            features = [sample.get(col, 0) for col in feature_cols]
            prediction = model.predict([features])[0]

            st.subheader("AI Prediction")
            st.success(f"Predicted Source: {prediction}")

    except Exception as e:
        st.error(f"Prediction error: {e}")

# =====================================================
# PIE CHART
# =====================================================
elif page == "Pie Chart":
    st.header("Pollution Source Distribution")

    if len(df) > 0:
        source_counts = df["pollution_source"].value_counts()

        fig, ax = plt.subplots()
        ax.pie(source_counts, labels=source_counts.index, autopct="%1.1f%%")
        ax.axis("equal")

        st.pyplot(fig)
    else:
        st.warning("No data available")

# =====================================================
# MAP
# =====================================================
elif page == "Map":
    st.header("Pollution Heatmap")

    if len(df) > 0:
        center_lat = df["latitude"].mean()
        center_lon = df["longitude"].mean()

        m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

        HeatMap(df[["latitude", "longitude", "PM10"]].values.tolist()).add_to(m)

        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=6,
                popup=f"{row['location']} | {row['pollution_source']} | PM10: {row['PM10']}"
            ).add_to(m)

        st_folium(m, width=1100, height=500)
    else:
        st.warning("No data available")

# =====================================================
# HISTORY
# =====================================================
elif page == "History":
    st.header("Pollution Trend")

    if len(df) > 0:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df["PM10"].reset_index(drop=True))
        ax.set_title("PM10 Trend")

        st.pyplot(fig)
    else:
        st.warning("No data available")

# =====================================================
# DOWNLOAD
# =====================================================
elif page == "Downloads":
    st.header("Download Data")

    if len(df) > 0:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Dataset", csv, "pollution_data.csv")
    else:
        st.warning("No data available")

# FOOTER
st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")