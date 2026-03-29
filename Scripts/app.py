import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import streamlit.components.v1 as components
import os

# Set up the page layout
st.set_page_config(page_title="EnviroScan Dashboard", page_icon="🌍", layout="wide")

# --- CONFIGURATION (MATCHING YOUR FOLDERS) ---
BASE_DIR = r"C:\Users\ajayk\Environ_Scan_Project"
DATA_FILE = os.path.join(BASE_DIR, "Processed", "dataset_with_predictions.csv")
MODEL_FILE = os.path.join(BASE_DIR, "Models", "pollution_model.pkl")
ENCODER_FILE = os.path.join(BASE_DIR, "Models", "label_encoder.pkl")
MAP_FILE = os.path.join(BASE_DIR, "Visualizations", "pollution_map.html")

# --- Load Data and Models ---
@st.cache_data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    st.error(f"Data file not found at {DATA_FILE}")
    return pd.DataFrame()

@st.cache_resource
def load_model_files():
    # Note: Ensure you have saved your encoders as .pkl files in the Models folder
    if os.path.exists(MODEL_FILE) and os.path.exists(ENCODER_FILE):
        model = joblib.load(MODEL_FILE)
        encoder = joblib.load(ENCODER_FILE)
        return model, encoder
    return None, None

df = load_data()
model, encoder = load_model_files()

if df.empty:
    st.stop()

# --- Step 1 & 2: Sidebar and User Inputs ---
st.sidebar.title("🌍 EnviroScan Navigator")
st.sidebar.write("Select a location to monitor environmental conditions.")

# Get a list of unique cities for the dropdown menu
city_col = next((col for col in df.columns if col.lower() == 'city'), 'City')
city_list = df[city_col].dropna().unique()
selected_city = st.sidebar.selectbox("Select City", sorted(city_list))

# Filter data for the selected city (Latest record)
city_data = df[df[city_col] == selected_city].iloc[-1] 

# --- Step 4: Implement Real-Time Pollution Alerts ---
st.title(f"Real-Time Monitoring: {selected_city}")

# Using PM25 for alerts as per your dataset column name
pm_val = city_data['PM25']
if pm_val > 150:
    st.error(f"🚨 **HIGH POLLUTION ALERT!** Dangerous levels of PM2.5 detected ({pm_val}). Please take precautions.")
elif pm_val > 50:
    st.warning(f"⚠️ **Moderate Pollution Warning:** Elevated levels of PM2.5 ({pm_val}).")
else:
    st.success(f"✅ **Air Quality is Good:** Current PM2.5 level is {pm_val}.")

# --- Step 3: Display Pollution Metrics ---
st.subheader("Current Environmental Metrics")
col1, col2, col3, col4 = st.columns(4)

# Handling metric display with fallback for missing columns
col1.metric("Temperature", f"{city_data.get('Temperature', 'N/A')} °C")
col2.metric("Humidity", f"{city_data.get('Humidity', 'N/A')} %")
col3.metric("PM2.5 Level", pm_val)

# Predicted Source from your dataset (already generated in Module 5)
predicted_source = city_data.get('POLLUTION_SOURCE', 'Unknown')
col4.metric("Predicted Source", predicted_source)

st.markdown("---")

# Use Tabs to keep the interface clean
tab1, tab2, tab3 = st.tabs(["🗺️ Interactive Map", "📊 Analytics & Charts", "📥 Download Reports"])

# --- Step 7: Embed the Interactive Map ---
with tab1:
    st.subheader("Geospatial Pollution Map")
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE, 'r', encoding='utf-8') as f:
            map_html = f.read()
        components.html(map_html, height=600, scrolling=True)
    else:
        st.info("Map file not found in Visualizations folder. Please run your map script.")

# --- Step 5 & 6: Display Trend Charts and Source Distribution ---
with tab2:
    st.subheader("National Source Distribution")
    colA, colB = st.columns(2)
    
    with colA:
        # Pie chart showing distribution of predicted pollution sources
        source_counts = df['POLLUTION_SOURCE'].value_counts().reset_index()
        source_counts.columns = ['Source', 'Count']
        fig_pie = px.pie(source_counts, names='Source', values='Count', title='Overall Pollution Sources', hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with colB:
        # Trend chart for the selected city
        city_trend = df[df[city_col] == selected_city].tail(20)
        fig_line = px.line(city_trend, y='PM25', title=f'PM2.5 Trend for {selected_city}', markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

# --- Step 8: Add Report Download Feature ---
with tab3:
    st.subheader("Download Environmental Data")
    st.write("Export the complete labeled dataset for external analysis.")
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Report (CSV)",
        data=csv,
        file_name='enviroscan_full_report.csv',
        mime='text/csv',
    )