import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
import joblib
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide", page_icon="🌍")

# --- LOAD DATA & MODEL (Step 1 & 3) ---
@st.cache_data
def load_data():
    try:
        # Replace with your actual finalized dataset filename
        df = pd.read_csv('data/processed/final_combined_dataset.csv')
        # Ensure we have a dummy timestamp for the charts if one doesn't exist
        if 'timestamp' not in df.columns:
            df['timestamp'] = pd.date_range(start='1/1/2026', periods=len(df), freq='h')
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'final_combined_dataset.csv' is in the correct folder.")
        st.stop()
    return df

@st.cache_resource
def load_model_assets():
    try:
        model = joblib.load('models/best_pollution_model.joblib')
        encoder = joblib.load('models/label_encoder.joblib')
        scaler = joblib.load('models/feature_scaler.joblib')
        return model, encoder, scaler
    except FileNotFoundError:
        st.warning("Model files not found. The dashboard will run in visualization-only mode.")
        return None, None, None

df = load_data()
model, encoder, scaler = load_model_assets()

# --- SIDEBAR: USER INPUTS (Step 2) ---
st.sidebar.header("🎛️ Dashboard Controls")

# City/Location Filter (Assuming 'city' column exists, otherwise filtering by general dataset)
if 'city' in df.columns:
    selected_city = st.sidebar.selectbox("Select City", df['city'].unique())
    df_filtered = df[df['city'] == selected_city]
else:
    df_filtered = df.copy()

# Date Range Filter
min_date = pd.to_datetime(df['timestamp']).min().date()
max_date = pd.to_datetime(df['timestamp']).min().date()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Source Filter for Map
available_sources = ['All'] + list(df['pollution_source'].unique())
selected_source = st.sidebar.selectbox("Filter by Pollution Source", available_sources)

if selected_source != 'All':
    df_filtered = df_filtered[df_filtered['pollution_source'] == selected_source]

# --- MAIN DASHBOARD HEADER ---
st.title("🌍 EnviroScan: Real-Time Pollution Monitoring")
st.markdown("Monitor predictions, analyze geospatial trends, and receive real-time alerts.")

# --- REAL-TIME ALERTS (Step 4) ---
st.subheader("🚨 Status & Alerts")
current_pm25 = df_filtered['PM2.5'].mean()
current_no2 = df_filtered['NO2'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Average PM2.5", f"{current_pm25:.2f} µg/m³")
col2.metric("Average NO₂", f"{current_no2:.2f} µg/m³")

# Alert Logic
if current_pm25 > 50 or current_no2 > 40:
    st.error("⚠️ HIGH POLLUTION ALERT: Pollutant levels exceed safe thresholds in the selected area. Sensitive groups should limit outdoor exertion.")
elif current_pm25 > 30:
    st.warning("🟠 MODERATE WARNING: Pollution is building up. Continue monitoring.")
else:
    st.success("🟢 SAFE: Air quality is within acceptable limits.")

st.divider()

# --- CHARTS & VISUALIZATIONS (Step 5 & 6) ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Pollutant Trends Over Time")
    # Line chart for PM2.5 and NO2
    trend_data = df_filtered.melt(id_vars=['timestamp'], value_vars=['PM2.5', 'NO2'], 
                                  var_name='Pollutant', value_name='Concentration')
    fig_line = px.line(trend_data, x='timestamp', y='Concentration', color='Pollutant',
                       color_discrete_sequence=['red', 'orange'])
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    st.subheader("🥧 Predicted Source Distribution")
    # Pie chart showing the breakdown of pollution sources
    source_counts = df_filtered['pollution_source'].value_counts().reset_index()
    source_counts.columns = ['Source', 'Count']
    fig_pie = px.pie(source_counts, values='Count', names='Source', hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# --- MODULE 5: GEOSPATIAL MAP (Step 7) ---
st.subheader("🗺️ Interactive Pollution Heatmap & Source Markers")

# Initialize Map (Centered on the mean coordinates of the filtered data)
map_center = [df_filtered['latitude'].mean(), df_filtered['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=12, tiles="CartoDB dark_matter")

# 1. Add Heatmap Layer
heat_data = [[row['latitude'], row['longitude'], row['PM2.5']] for index, row in df_filtered.iterrows()]
HeatMap(heat_data, radius=15, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 1.0: 'red'}).add_to(m)

# 2. Add Source-Specific Markers & High-Risk Zones
colors = {'Vehicular': 'orange', 'Industrial': 'purple', 'Agricultural': 'green', 'Burning': 'red', 'Natural': 'blue'}

for index, row in df_filtered.iterrows():
    source = row['pollution_source']
    pm25_val = row['PM2.5']
    
    # High-Risk Zone Logic (Make marker larger and red if PM2.5 is very high)
    is_high_risk = pm25_val > 50
    marker_color = 'red' if is_high_risk else colors.get(source, 'gray')
    marker_radius = 8 if is_high_risk else 4

    popup_text = f"""
    <b>Source:</b> {source}<br>
    <b>PM2.5:</b> {pm25_val} µg/m³<br>
    <b>High Risk:</b> {'Yes' if is_high_risk else 'No'}
    """
    
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=marker_radius,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=200)
    ).add_to(m)

# Render the map in Streamlit
st_folium(m, width=1200, height=500)

st.divider()

# --- REPORT DOWNLOAD (Step 8) ---
st.subheader("📄 Export Data")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Current View as CSV",
    data=csv,
    file_name=f"pollution_report_{datetime.date.today()}.csv",
    mime="text/csv",
)
