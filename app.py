import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import streamlit.components.v1 as components
import os

# Set up the page layout
st.set_page_config(page_title="EnviroScan Dashboard", page_icon="🌍", layout="wide")

# --- Load Data and Models ---
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/labeled_environment_dataset.csv")

@st.cache_resource
def load_model():
    model = joblib.load("models/pollution_source_model.pkl")
    le_pollutant = joblib.load("models/pollutant_encoder.pkl")
    le_target = joblib.load("models/target_encoder.pkl")
    return model, le_pollutant, le_target

df = load_data()
model, le_pollutant, le_target = load_model()

# --- Step 1 & 2: Sidebar and User Inputs ---
st.sidebar.title("🌍 EnviroScan Navigator")
st.sidebar.write("Select a location to monitor real-time environmental conditions.")

# Get a list of unique cities for the dropdown menu
city_list = df['city'].dropna().unique()
selected_city = st.sidebar.selectbox("Select City", sorted(city_list))

# Filter data for the selected city
city_data = df[df['city'] == selected_city].iloc[0] # Grab the latest record for that city

# --- Step 4: Implement Real-Time Pollution Alerts ---
st.title(f"Real-Time Monitoring: {selected_city}")

# Define a safe threshold (e.g., PM2.5 over 50 or AQI equivalents)
if city_data['value'] > 150:
    st.error(f"🚨 **HIGH POLLUTION ALERT!** Dangerous levels of {city_data['pollutant'].upper()} detected ({city_data['value']}). Please take precautions.")
elif city_data['value'] > 50:
    st.warning(f"⚠️ **Moderate Pollution Warning:** Elevated levels of {city_data['pollutant'].upper()} ({city_data['value']}).")
else:
    st.success(f"✅ **Air Quality is Good:** Current {city_data['pollutant'].upper()} level is {city_data['value']}.")

# --- Step 3: Display Pollution Prediction Results ---
st.subheader("Current Environmental Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", f"{city_data['temperature']} °C")
col2.metric("Wind Speed", f"{city_data['wind_speed']} m/s")
col3.metric(f"Pollutant ({city_data['pollutant'].upper()})", city_data['value'])

# Generate a fresh prediction using the loaded ML Model
features_for_prediction = pd.DataFrame([{
    'pollutant_encoded': le_pollutant.transform([city_data['pollutant']])[0],
    'value': city_data['value'],
    'temperature': city_data['temperature'],
    'humidity': city_data['humidity'],
    'wind_speed': city_data['wind_speed'],
    'wind_direction': city_data['wind_direction'],
    'distance_to_road_m': city_data['distance_to_road_m'],
    'distance_to_industry_m': city_data['distance_to_industry_m'],
    'distance_to_dump_m': city_data['distance_to_dump_m'],
    'distance_to_farmland_m': city_data['distance_to_farmland_m']
}])

# Predict and decode the result
prediction_encoded = model.predict(features_for_prediction)[0]
predicted_source = le_target.inverse_transform([prediction_encoded])[0]

col4.metric("Predicted Source", predicted_source)

st.markdown("---")

# Use Tabs to keep the interface clean and avoid clutter (Mentor's note)
tab1, tab2, tab3 = st.tabs(["🗺️ Interactive Map", "📊 Analytics & Charts", "📥 Download Reports"])

# --- Step 7: Embed the Interactive Map ---
with tab1:
    st.subheader("Geospatial Pollution Map")
    map_path = "data/processed/interactive_pollution_map.html"
    if os.path.exists(map_path):
        with open(map_path, 'r', encoding='utf-8') as f:
            map_html = f.read()
        # Embed the folium map we made in Module 5
        components.html(map_html, height=600, scrolling=True)
    else:
        st.info("Map file not found. Please ensure 'generate_map.py' was run successfully.")

# --- Step 5 & 6: Display Trend Charts and Source Distribution ---
with tab2:
    st.subheader("National Source Distribution")
    colA, colB = st.columns(2)
    
    with colA:
        # Pie chart showing distribution of predicted pollution sources
        source_counts = df['pollution_source'].value_counts().reset_index()
        source_counts.columns = ['Source', 'Count']
        fig_pie = px.pie(source_counts, names='Source', values='Count', title='Overall Pollution Sources', hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with colB:
        # Bar chart showing top pollutants across the dataset
        pollutant_counts = df['pollutant'].value_counts().reset_index()
        pollutant_counts.columns = ['Pollutant', 'Count']
        fig_bar = px.bar(pollutant_counts, x='Pollutant', y='Count', title='Most Common Pollutants Detected', color='Pollutant')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- Step 8: Add Report Download Feature ---
with tab3:
    st.subheader("Download Environmental Data")
    st.write("Export the complete labeled dataset for external analysis or reporting.")
    
    # Convert dataframe to CSV for download
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Full Report (CSV)",
        data=csv,
        file_name='enviroscan_full_report.csv',
        mime='text/csv',
    )