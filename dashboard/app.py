import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from datetime import datetime
import joblib
import pyttsx3

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")
st.title("EnviroScan – Air Pollution Intelligence Dashboard")

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
st.sidebar.title("Navigate")
page = st.sidebar.radio("Go to", ["Dashboard", "Pie Chart", "Map", "History", "Downloads"])

# -------------------------
# DARK / LIGHT MODE
# -------------------------
dark_mode = st.sidebar.toggle("Dark Mode", value=False)
metric_color = "white" if dark_mode else "black"

if dark_mode:
    st.markdown("""
        <style>
        body, .stApp { background-color: #0E1117; color: white; }
        .stButton>button { background-color: #444; color: white; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp { background-color: white; color: black; }
        .stButton>button { background-color: #f0f0f0; color: black; }
        </style>
    """, unsafe_allow_html=True)

# -------------------------
# SEARCH FILTER
# -------------------------
st.sidebar.header("Search")
search_location = st.sidebar.text_input("Search Area / City / State")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../data/processed/final_labeled_dataset.csv")
    df = df.dropna(subset=["Latitude", "Longitude"])
    return df

df = load_data()

# SEARCH FILTER
location_cols = ["City", "State", "Area"]
filtered_df = df.copy()
if search_location:
    search_location = search_location.lower()
    mask = pd.Series(False, index=filtered_df.index)
    for col in location_cols:
        if col in filtered_df.columns:
            mask = mask | filtered_df[col].astype(str).str.lower().str.contains(search_location, na=False)
    filtered_df = filtered_df[mask]

if filtered_df.empty:
    st.warning("No matching data found.")
    st.stop()

# -------------------------
# LOAD MODEL
# -------------------------
@st.cache_resource
def load_model():
    return joblib.load("../models/pollution_model.pkl")

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
# PAGE 1 — DASHBOARD
# =====================================================
if page == "Dashboard":

    # -------------------------
    # CUSTOM METRICS (HTML for color control)
    # -------------------------
    total_records = len(filtered_df)
    avg_pm25 = round(filtered_df["PM2.5"].mean(), 2)
    pollution_sources = filtered_df["pollution_source"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<h3 style='color:{metric_color}'>Total Records<br>{total_records}</h3>", unsafe_allow_html=True)
    col2.markdown(f"<h3 style='color:{metric_color}'>Average PM2.5<br>{avg_pm25}</h3>", unsafe_allow_html=True)
    col3.markdown(f"<h3 style='color:{metric_color}'>Pollution Sources<br>{pollution_sources}</h3>", unsafe_allow_html=True)

    st.divider()

    # AQI
    st.subheader("Air Quality Index")
    aqi_value = int(filtered_df["PM2.5"].mean())
    status, message = get_aqi_info(aqi_value)
    st.success(f"AQI: {aqi_value} — {status}")
    st.info(message)

    # Voice alert
    def speak(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    if st.button("Speak Air Quality"):
        speak(f"Air quality is {status}. {message}")

    # AI Prediction
    try:
        feature_cols = ["PM2.5","PM10","NO2","SO2","CO","O3","Temperature","Humidity","WindSpeed"]
        for col in feature_cols:
            if col not in filtered_df.columns:
                filtered_df[col] = 0
        valid_rows = filtered_df.dropna(subset=feature_cols)
        if valid_rows.empty:
            st.warning("No valid data for AI prediction.")
        else:
            sample = valid_rows.iloc[0]
            features = [sample[col] for col in feature_cols]
            prediction = model.predict([features])[0]
            st.subheader("AI Prediction")
            st.success(f"Predicted Source: {prediction}")
    except Exception as e:
        st.error(f"Model prediction unavailable: {e}")

# =====================================================
# PAGE 2 — PIE CHART
# =====================================================
elif page == "Pie Chart":
    st.header("Pollution Source Distribution")
    source_counts = filtered_df["pollution_source"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(source_counts, labels=source_counts.index, autopct="%1.1f%%")
    ax.axis("equal")
    st.pyplot(fig)

# =====================================================
# PAGE 3 — MAP
# =====================================================
elif page == "Map":
    st.header("Pollution Heatmap")
    center_lat = filtered_df["Latitude"].mean()
    center_lon = filtered_df["Longitude"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)
    HeatMap(filtered_df[["Latitude", "Longitude", "PM2.5"]].values.tolist()).add_to(m)
    for _, row in filtered_df.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=6,
            popup=f"{row['pollution_source']} | PM2.5: {row['PM2.5']}"
        ).add_to(m)
    st_folium(m, width=1100, height=500)

# =====================================================
# PAGE 4 — HISTORY
# =====================================================
elif page == "History":
    st.header("Pollution Trend Analysis")
    st.write("This graph shows how PM2.5 levels vary across recorded observations.")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(filtered_df["PM2.5"].reset_index(drop=True))
    ax.set_xlabel("Observation Number")
    ax.set_ylabel("PM2.5 Level")
    ax.set_title("PM2.5 Variation Trend")
    st.pyplot(fig)

# =====================================================
# PAGE 5 — DOWNLOADS
# =====================================================
elif page == "Downloads":
    st.header("Download Data")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Dataset", csv, "pollution_data.csv", "text/csv")

# FOOTER
st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
