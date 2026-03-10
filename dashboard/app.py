import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

st.set_page_config(page_title="Pollution Monitoring Dashboard", layout="wide")

st.title("🌍 Pollution Monitoring & Source Prediction Dashboard")

# -----------------------------
# Generate Sample Dataset
# -----------------------------
cities = [
    ("Delhi",28.61,77.20),
    ("Mumbai",19.07,72.87),
    ("Bangalore",12.97,77.59),
    ("Chennai",13.08,80.27),
    ("Kolkata",22.57,88.36),
    ("Hyderabad",17.38,78.48),
    ("Pune",18.52,73.85),
    ("Ahmedabad",23.02,72.57)
]

data = []

for city,lat,lon in cities:
    for i in range(50):
        data.append({
            "city":city,
            "lat":lat + np.random.normal(0,0.05),
            "lon":lon + np.random.normal(0,0.05),
            "pm25":np.random.randint(40,250),
            "pm10":np.random.randint(50,300),
            "no2":np.random.randint(10,120),
            "source":np.random.choice(["Traffic","Industry","Construction","Natural"])
        })

df = pd.DataFrame(data)

# -----------------------------
# Metrics Section
# -----------------------------
st.subheader("📊 Current Pollution Metrics")

col1,col2,col3 = st.columns(3)

col1.metric("Average PM2.5", round(df["pm25"].mean(),2))
col2.metric("Average PM10", round(df["pm10"].mean(),2))
col3.metric("Average NO2", round(df["no2"].mean(),2))

# -----------------------------
# Pollution Trend Chart
# -----------------------------
st.subheader("📈 Pollution Trend Analysis")

trend_df = df.groupby("city")[["pm25","pm10","no2"]].mean().reset_index()

fig = px.bar(
    trend_df,
    x="city",
    y=["pm25","pm10","no2"],
    barmode="group",
    title="Average Pollution by City"
)

st.plotly_chart(fig, width="stretch")

# -----------------------------
# Pollution Source Distribution
# -----------------------------
st.subheader("🏭 Pollution Source Distribution")

source_counts = df["source"].value_counts().reset_index()
source_counts.columns = ["source","count"]

fig2 = px.pie(
    source_counts,
    names="source",
    values="count",
    title="Pollution Sources"
)

st.plotly_chart(fig2, width="stretch")

# -----------------------------
# Interactive Pollution Map
# -----------------------------
st.subheader("🗺️ Pollution Heatmap")

m = folium.Map(location=[22.5,78.9], zoom_start=5)

heat_data = df[["lat","lon","pm25"]].values.tolist()

HeatMap(heat_data).add_to(m)

st_folium(m, width=900, height=500)

# -----------------------------
# Pollution Alerts
# -----------------------------
st.subheader("🚨 Pollution Alerts")

danger = df[df["pm25"] > 200]

if len(danger) > 0:
    st.error(f"⚠️ {len(danger)} locations detected with dangerous PM2.5 levels")
else:
    st.success("Air quality within safe range")

# -----------------------------
# ML Model (Source Prediction)
# -----------------------------
st.subheader("🤖 Pollution Source Prediction")

X = df[["pm25","pm10","no2"]]
y = df["source"]

model = RandomForestClassifier()
model.fit(X,y)

pm25 = st.slider("PM2.5 Level",0,300,120)
pm10 = st.slider("PM10 Level",0,400,150)
no2 = st.slider("NO2 Level",0,200,40)

if st.button("Predict Pollution Source"):

    prediction = model.predict([[pm25,pm10,no2]])[0]

    st.success(f"Predicted Source: {prediction}")

# -----------------------------
# Data Table
# -----------------------------
st.subheader("📄 Pollution Dataset")

st.dataframe(df, width="stretch")

# -----------------------------
# Download Report
# -----------------------------
st.subheader("⬇ Download Pollution Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "pollution_report.csv",
    "text/csv"
)