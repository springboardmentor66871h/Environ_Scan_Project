import streamlit as st
import pandas as pd
import joblib
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import pyttsx3
import matplotlib.pyplot as plt

# ------------------------
# Load Data
# ------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/final_labeled_with_weather.csv")

df = load_data()

# ------------------------
# Load Model
# ------------------------
model = joblib.load("models/pollution_model.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

# ------------------------
# Sidebar
# ------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio("Go to", [
    "Dashboard", "Pie Chart", "Map", "History", "Downloads"
])

# ------------------------
# Search City
# ------------------------
city = st.sidebar.text_input("Search City (e.g., Delhi, Chennai)")

if city:
    df = df[df["location"].str.contains(city, case=False, na=False)]

st.sidebar.write("Available Cities:", df["location"].dropna().unique())

# ------------------------
# DASHBOARD (PREMIUM UI)
# ------------------------
if page == "Dashboard":

    st.markdown(
        "<h1 style='text-align: center;'>EnviroScan – Air Pollution Intelligence Dashboard</h1>",
        unsafe_allow_html=True
    )

    # Horizontal cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style='background-color:#1f77b4;padding:20px;border-radius:10px;text-align:center'>
            <h3>Total Records</h3>
            <h2>{len(df)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background-color:#2ca02c;padding:20px;border-radius:10px;text-align:center'>
            <h3>Average PM10</h3>
            <h2>{round(df["PM10"].mean(), 2)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background-color:#ff7f0e;padding:20px;border-radius:10px;text-align:center'>
            <h3>Pollution Sources</h3>
            <h2>{df["pollution_source"].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # AQI Section
    avg_pm10 = df["PM10"].mean()

    if avg_pm10 < 50:
        status = "Good"
        color = "#2ecc71"
        message = "Air quality is good."
    elif avg_pm10 < 100:
        status = "Moderate"
        color = "#f1c40f"
        message = "Air quality is moderate."
    else:
        status = "Unhealthy for Sensitive"
        color = "#e74c3c"
        message = "Sensitive groups should be careful."

    st.markdown(f"""
    <div style='background-color:{color};padding:20px;border-radius:10px'>
        <h3>Air Quality Index</h3>
        <h2>AQI: {round(avg_pm10)} — {status}</h2>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Voice Feature (FIXED KEY)
    if st.button("🔊 Speak AQI", key="voice_btn"):
        engine = pyttsx3.init()
        engine.say(f"The air quality is {status}")
        engine.runAndWait()

# ------------------------
# PIE CHART (REAL PIE)
# ------------------------
elif page == "Pie Chart":
    st.title("Pollution Source Distribution")

    pie = df["pollution_source"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(pie, labels=pie.index, autopct='%1.1f%%')
    ax.set_title("Pollution Source Share")

    st.pyplot(fig)

# ------------------------
# MAP (HEATMAP)
# ------------------------
elif page == "Map":
    st.title("Pollution Heatmap")

    m = folium.Map(
        location=[df["latitude"].mean(), df["longitude"].mean()],
        zoom_start=5
    )

    heat_data = [
        [row["latitude"], row["longitude"], row["PM10"]]
        for _, row in df.iterrows()
    ]

    HeatMap(heat_data).add_to(m)

    st_folium(m, width=700)

# ------------------------
# HISTORY
# ------------------------
elif page == "History":
    st.title("Dataset Preview")
    st.dataframe(df.head(100))

# ------------------------
# DOWNLOAD
# ------------------------
elif page == "Downloads":
    st.title("Download Dataset")

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "pollution_data.csv"
    )

# ------------------------
# PREDICTION
# ------------------------
try:
    X_input = df[feature_columns]
    df["Predicted"] = model.predict(X_input)
except Exception as e:
    st.error(f"Prediction error: {e}")