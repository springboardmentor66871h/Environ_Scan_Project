import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
import joblib
import datetime
import os
from pathlib import Path

# --- PAGE CONFIGURATION ---
# Set the page to wide mode with a clean layout
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide", page_icon="🌍")

# --- CUSTOM CSS FOR BEAUTIFUL UI ---
st.markdown("""
<style>
    /* Clean background */
    .stApp {
        background-color: #F8FAFC;
    }
    /* Style the metric cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    /* Add a hover effect to metric cards */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    /* Color the metric values beautifully */
    div[data-testid="stMetricValue"] {
        color: #1E293B;
        font-weight: 800;
    }
    /* Headers styling */
    h1, h2, h3 {
        color: #0F172A;
        font-family: 'Inter', sans-serif;
    }
    /* Sidebar beautification */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA & MODEL ---
@st.cache_data
def load_data():
    df = None 
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / 'Final_Labeled_Pollution_Dataset.csv',
        Path.cwd() / 'Final_Labeled_Pollution_Dataset.csv',
    ]

    for path in candidates:
        if path.exists():
            df = pd.read_csv(path)
            break

    if df is None:
        st.error("Dataset not found. Please place 'Final_Labeled_Pollution_Dataset.csv' in the same folder as app.py.")
        st.stop()

    if 'timestamp' not in df.columns or df['timestamp'].isna().all():
        df['timestamp'] = pd.date_range(start='1/1/2026', periods=len(df), freq='h')

    return df

@st.cache_resource
def load_model_assets():
    try:
        model = joblib.load('models/best_pollution_model.joblib')
        encoder = joblib.load('models/label_encoder.joblib')
        scaler = joblib.load('models/feature_scaler.joblib')
        return model, encoder, scaler
    except FileNotFoundError:
        return None, None, None

df = load_data()
model, encoder, scaler = load_model_assets()

# --- SIDEBAR: USER INPUTS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3203/3203071.png", width=80)
st.sidebar.title("EnviroScan")
st.sidebar.markdown("---")
st.sidebar.header("🎛️ Dashboard Controls")

if 'city' in df.columns:
    selected_city = st.sidebar.selectbox("🏙️ Select City", df['city'].unique())
    df_filtered = df[df['city'] == selected_city]
else:
    df_filtered = df.copy()

min_date = pd.to_datetime(df['timestamp']).min().date()
max_date = pd.to_datetime(df['timestamp']).max().date()
date_range = st.sidebar.date_input("📅 Select Date Range", [min_date, max_date])

available_sources = ['All'] + list(df['pollution_source'].unique())
selected_source = st.sidebar.selectbox("🔍 Filter by Source", available_sources)

if selected_source != 'All':
    df_filtered = df_filtered[df_filtered['pollution_source'] == selected_source]

# --- MAIN DASHBOARD HEADER ---
st.title("🌍 EnviroScan Analytics")
st.markdown("Monitor predictions, analyze geospatial trends, and receive real-time alerts through our intelligent dashboard.")
st.markdown("<br>", unsafe_allow_html=True) # Extra spacing

# --- REAL-TIME ALERTS ---
st.subheader("🚨 Live Environmental Status")
current_pm25 = df_filtered['pm25'].mean() 
current_no2 = df_filtered['no2'].mean()  

col1, col2, col3 = st.columns(3)
col1.metric("Average PM2.5", f"{current_pm25:.2f} µg/m³", "Target: <30", delta_color="inverse")
col2.metric("Average NO₂", f"{current_no2:.2f} µg/m³", "Target: <40", delta_color="inverse")
col3.metric("Total Records Analyzed", f"{len(df_filtered):,}")

st.markdown("<br>", unsafe_allow_html=True)

if current_pm25 > 50 or current_no2 > 40:
    st.error("⚠️ **HIGH POLLUTION ALERT:** Pollutant levels exceed safe thresholds. Sensitive groups should limit outdoor exertion.")
elif current_pm25 > 30:
    st.warning("🟠 **MODERATE WARNING:** Pollution is building up. Continue monitoring.")
else:
    st.success("🟢 **SAFE:** Air quality is within acceptable healthy limits.")

st.divider()

# --- CHARTS & VISUALIZATIONS ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Pollutant Trends Over Time")
    trend_data = df_filtered.melt(id_vars=['timestamp'], value_vars=['pm25', 'no2'], 
                                  var_name='Pollutant', value_name='Concentration')
    # Upgraded Plotly UI to 'plotly_white'
    fig_line = px.line(trend_data, x='timestamp', y='Concentration', color='Pollutant',
                       color_discrete_map={'pm25': '#EF4444', 'no2': '#F59E0B'},
                       template='plotly_white')
    fig_line.update_layout(margin=dict(l=0, r=0, t=30, b=0), legend_title_text='')
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    st.subheader("🥧 Source Distribution")
    source_counts = df_filtered['pollution_source'].value_counts().reset_index()
    source_counts.columns = ['Source', 'Count']
    fig_pie = px.pie(source_counts, values='Count', names='Source', hole=0.5,
                     color_discrete_sequence=px.colors.qualitative.Pastel,
                     template='plotly_white')
    fig_pie.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# --- MODULE 5: GEOSPATIAL MAP ---
st.subheader("🗺️ Interactive Pollution Heatmap")
st.markdown("Zoom and pan to explore high-risk zones and predicted emission sources.")

# Initialize Light Mode Map using "CartoDB positron"
map_center = [df_filtered['latitude'].mean(), df_filtered['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=12, tiles="CartoDB positron")

# Add Vibrant Heatmap Layer
heat_data = [[row['latitude'], row['longitude'], row['pm25']] for index, row in df_filtered.iterrows()] 
# Adjusted gradient to look incredible on a light map
HeatMap(heat_data, radius=18, blur=15, gradient={0.2: '#34d399', 0.5: '#fbbf24', 0.8: '#ef4444', 1.0: '#7f1d1d'}).add_to(m)

# Add Source-Specific Markers
colors = {'Vehicular': '#f59e0b', 'Industrial': '#8b5cf6', 'Agricultural': '#10b981', 'Burning': '#ef4444', 'Natural': '#3b82f6'}

for index, row in df_filtered.iterrows():
    source = row['pollution_source']
    pm25_val = row['pm25'] 

    is_high_risk = pm25_val > 50
    marker_color = '#ef4444' if is_high_risk else colors.get(source, '#64748b')
    marker_radius = 8 if is_high_risk else 5

    popup_text = f"""
    <div style="font-family: sans-serif; width: 150px;">
        <h4 style="margin-bottom: 5px; color: #1e293b;">{source}</h4>
        <b>PM2.5:</b> {pm25_val} µg/m³<br>
        <b>Risk:</b> <span style="color: {'red' if is_high_risk else 'green'}">{'High' if is_high_risk else 'Normal'}</span>
    </div>
    """

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=marker_radius,
        color='white', # White border around markers looks highly premium
        weight=1,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.9,
        popup=folium.Popup(popup_text, max_width=250)
    ).add_to(m)

# Render the map
st_folium(m, width=1200, height=550, returned_objects=[])

st.divider()

# --- REPORT DOWNLOAD ---
st.subheader("📄 Export Analytics")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Current View as CSV",
    data=csv,
    file_name=f"EnviroScan_Report_{datetime.date.today()}.csv",
    mime="text/csv",
)
