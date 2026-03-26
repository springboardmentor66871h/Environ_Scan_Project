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

st.title("🌍 EnviroScan – Air Pollution Intelligence Dashboard")

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
st.sidebar.title("📂 Navigate")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Pie Chart", "Map", "History", "Downloads"]
)

# -------------------------
# DARK MODE
# -------------------------
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

if dark_mode:
    st.markdown("""
        <style>
        body {background-color: #0E1117; color: white;}
        </style>
    """, unsafe_allow_html=True)

# -------------------------
# SEARCH FILTER (ONLY FILTER)
# -------------------------
st.sidebar.header("Search")
search_location = st.sidebar.text_input("🔎 Search Area / City / State")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("../data/processed/final_labeled_dataset.csv")

df = load_data()
df = df.dropna(subset=["Latitude", "Longitude"])

# SEARCH WORKING FILTER ⭐
filtered_df = df.copy()

if search_location:
    search_location = search_location.lower()
    filtered_df = filtered_df[
        filtered_df.astype(str)
        .apply(lambda row: row.str.lower().str.contains(search_location).any(), axis=1)
    ]

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
        return "Good 🟢", "Air quality is satisfactory."
    elif aqi <= 100:
        return "Moderate 🟡", "Acceptable air quality."
    elif aqi <= 150:
        return "Unhealthy for Sensitive 🟠", "Sensitive groups careful."
    elif aqi <= 200:
        return "Unhealthy 🔴", "Everyone may feel effects."
    elif aqi <= 300:
        return "Very Unhealthy 🟣", "Health warnings."
    else:
        return "Hazardous ⚫", "Serious health effects!"

# =====================================================
# PAGE 1 — DASHBOARD
# =====================================================
if page == "Dashboard":

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(filtered_df))
    col2.metric("Average PM2.5", round(filtered_df["PM2.5"].mean(), 2))
    col3.metric("Pollution Sources", filtered_df["pollution_source"].nunique())

    st.divider()

    # AQI
    st.subheader("🌫 Air Quality Index")
    aqi_value = int(filtered_df["PM2.5"].mean())
    status, message = get_aqi_info(aqi_value)

    st.success(f"AQI: {aqi_value} — {status}")
    st.info(message)

    # Voice alert
    def speak(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    if st.button("🔊 Speak Air Quality"):
        speak(f"Air quality is {status}. {message}")

    # AI Prediction
    try:
        sample = filtered_df.iloc[0]
        features = [
            sample["PM2.5"], sample["PM10"], sample["NO2"],
            sample["SO2"], sample["CO"], sample["O3"]
        ]
        prediction = model.predict([features])[0]
        st.subheader("🤖 AI Prediction")
        st.success(f"Predicted Source: {prediction}")
    except:
        st.warning("Model prediction unavailable.")

# =====================================================
# PAGE 2 — PIE CHART ⭐
# =====================================================
elif page == "Pie Chart":

    st.header("📊 Pollution Source Distribution")

    source_counts = filtered_df["pollution_source"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(source_counts, labels=source_counts.index, autopct="%1.1f%%")
    ax.axis("equal")

    st.pyplot(fig)

# =====================================================
# PAGE 3 — MAP
# =====================================================
elif page == "Map":

    st.header("🗺 Pollution Heatmap")

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

    st.header("📈 Pollution Trend Analysis")

    st.write("This graph shows how PM2.5 levels vary across recorded observations.")

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(filtered_df["PM2.5"].reset_index(drop=True))
    ax.set_xlabel("Observation Number")
    ax.set_ylabel("PM2.5 Level")
    ax.set_title("PM2.5 Variation Trend")

    st.pyplot(fig)
# =====================================================
# PAGE 5 — DOWNLOADS
# =====================================================
elif page == "Downloads":

    st.header("⬇ Download Data")

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Filtered Dataset",
        csv,
        "pollution_data.csv",
        "text/csv"
    )

# FOOTER
st.caption(f"🕒 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")