import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# ===============================
# PAGE SETTINGS
# ===============================

st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")

st.title("🌍 EnviroScan — Pollution Monitoring Dashboard")
st.write("Real-Time Pollution Analysis System")

# ===============================
# LOAD DATASET
# ===============================


data = pd.read_csv(
    "C:/projects/AI_Price_Optima/data/processed/final_environment_dataset.csv"
)

sources = ["Vehicles", "Industry", "Dust", "Waste", "Agriculture"]

data["pollution_source"] = np.random.choice(sources, size=len(data), replace=True)
# ===============================
# SIDEBAR — USER INPUTS
# ===============================

st.sidebar.header("🔧 Controls")

city = st.sidebar.selectbox(
    "Select Pollution Source",
    sorted(data["pollution_source"].dropna().unique())
)

lat = st.sidebar.slider(
    "Latitude",
    float(data.latitude.min()),
    float(data.latitude.max()),
    float(data.latitude.mean())
)

lon = st.sidebar.slider(
    "Longitude",
    float(data.longitude.min()),
    float(data.longitude.max()),
    float(data.longitude.mean())
)

# Filter data
filtered = data[data["pollution_source"] == city]

# ===============================
# CURRENT STATUS
# ===============================

st.subheader("📊 Current Pollution Status")

pollution_level = filtered["pollutant_avg"].mean()
source = filtered["pollution_source"].mode()[0]

col1, col2 = st.columns(2)

col1.metric("Average Pollution Level", f"{pollution_level:.2f}")
col2.metric("Dominant Source", source)

# ===============================
# ALERT SYSTEM 🚨
# ===============================

st.subheader("⚠ Air Quality Alert")

if pollution_level > 80:
    st.error("🚨 HIGH POLLUTION ALERT — Dangerous Air Quality")
elif pollution_level > 50:
    st.warning("⚠ Moderate Pollution Level")
else:
    st.success("✅ Air Quality Safe")

# ===============================
# TREND CHART
# ===============================

st.subheader("📈 Pollution Trend")

st.line_chart(filtered["pollutant_avg"])

# ===============================
# SOURCE DISTRIBUTION
# ===============================

st.subheader("📊 Pollution Source Distribution")

source_counts = data["pollution_source"].value_counts()

st.bar_chart(source_counts)

# ===============================
# EMBED MAP 🗺
# ===============================

st.subheader("🗺 Pollution Map")

HtmlFile = open(
    "C:/projects/AI_Price_Optima/pollution_map.html",
    "r",
    encoding="utf-8"
)

components.html(HtmlFile.read(), height=600)

# ===============================
# DATA PREVIEW
# ===============================

st.subheader("📂 Dataset Preview")

st.dataframe(filtered.head())

# ===============================
# DOWNLOAD REPORT
# ===============================

st.subheader("📥 Download Report")

st.download_button(
    label="Download CSV Report",
    data=filtered.to_csv(index=False),
    file_name="pollution_report.csv",
    mime="text/csv"
)

# ===============================
# FOOTER
# ===============================

st.markdown("---")
st.write("EnviroScan Project — Module 6 Dashboard")