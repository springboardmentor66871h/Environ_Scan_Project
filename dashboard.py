import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EnviroScan Telemetry", page_icon="🌐", layout="wide")

# --- CUSTOM CSS (Matching the video's dark, compact theme) ---
st.markdown("""
<style>
    /* Global Theme */
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    
    /* Compact the padding to fit more on screen */
    .css-18e3th9 { padding-top: 2rem; padding-bottom: 2rem; padding-left: 1rem; padding-right: 1rem; }
    .css-1d391kg { padding-top: 1rem; }
    
    /* Container Styling (mimicking the dark panels in the video) */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
        background-color: #111827;
        border-radius: 8px;
        border: 1px solid #1f2937;
        padding: 10px;
    }
    
    /* Headers */
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #f8fafc; font-weight: 600; margin-bottom: 0px;}
    .main-header { font-size: 1.8rem; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-bottom: 20px;}
    
    /* Metric Cards (Compact) */
    div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: bold; color: #38bdf8;}
    div[data-testid="stMetricLabel"] { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase;}
    
    /* Alert Banners */
    .alert-danger { background-color: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 10px; border-radius: 4px; color: #ef4444;}
    .alert-warning { background-color: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 10px; border-radius: 4px; color: #f59e0b;}
    .alert-safe { background-color: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 10px; border-radius: 4px; color: #10b981;}
</style>
""", unsafe_allow_html=True)

# --- CACHE DATA & MODELS ---
@st.cache_data
def load_data():
    return pd.read_csv("data/Labeled_Master_Dataset.csv")

@st.cache_resource
def load_model():
    model = joblib.load("models/pollution_source_classifier.joblib")
    encoder = joblib.load("models/label_encoder.joblib")
    return model, encoder

df = load_data()
try:
    model, encoder = load_model()
    model_loaded = True
except:
    model_loaded = False

# --- SIDEBAR (Controls & Filters) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🌐 EnviroScan OS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Filtering
    st.subheader("Data Filters")
    city_list = ["Global View"] + list(df['city'].unique())
    selected_city = st.selectbox("Select Region", city_list, index=0)
    
    if selected_city != "Global View":
        filtered_df = df[df['city'] == selected_city]
    else:
        filtered_df = df
        
    st.markdown("---")
    
    # Real-time System Status (Simulated for dashboard feel)
    st.subheader("System Status")
    st.success("🟢 Sensors Online")
    st.success("🟢 AI Model Active")
    st.info(f"📊 Tracking {len(filtered_df):,} data points")
    
    st.markdown("---")
    # Export
    st.subheader("Data Export")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name=f"Telemetry_{selected_city}.csv", mime="text/csv", use_container_width=True)

# --- MAIN DASHBOARD LAYOUT ---
st.markdown("<div class='main-header'>Real-Time Environmental Telemetry</div>", unsafe_allow_html=True)

# --- TOP ROW: ALERTS & KEY METRICS ---
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns([2, 1, 1, 1])

with metric_col1:
    avg_pm25 = filtered_df['pm25'].mean()
    if avg_pm25 > 150:
        st.markdown(f"<div class='alert-danger'><b>🚨 CRITICAL ALERT:</b> PM2.5 levels at {avg_pm25:.1f} µg/m³. Hazardous air quality.</div>", unsafe_allow_html=True)
    elif avg_pm25 > 80:
        st.markdown(f"<div class='alert-warning'><b>⚠️ WARNING:</b> PM2.5 levels at {avg_pm25:.1f} µg/m³. Moderate risk detected.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='alert-safe'><b>✅ SYSTEM NOMINAL:</b> Air quality is within safe parameters.</div>", unsafe_allow_html=True)

with metric_col2: st.metric("Avg PM2.5", f"{avg_pm25:.1f}")
with metric_col3: st.metric("Avg NO₂", f"{filtered_df['no2'].mean():.1f}")
with metric_col4: st.metric("Avg SO₂", f"{filtered_df['so2'].mean():.1f}")

st.markdown("<br>", unsafe_allow_html=True)

# --- MIDDLE ROW: THE MAP AND ANALYTICS ---
# The video uses a large central map with charts on the side. 
map_col, chart_col = st.columns([2, 1])

with map_col:
    st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 10px;'>Spatial Pollution Distribution</h3>", unsafe_allow_html=True)
    map_path = "visualisation/pollution_heatmap_all_parameters.html"
    
    if os.path.exists(map_path):
        with open(map_path, 'r', encoding='utf-8') as f:
            map_html = f.read()
        components.html(map_html, height=500, scrolling=False) 
    else:
        st.error(f"Map file missing at {map_path}")

with chart_col:
    # Source Distribution Pie Chart (Compact)
    st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 10px;'>Source Attribution</h3>", unsafe_allow_html=True)
    source_counts = filtered_df['pollution_source'].value_counts().reset_index()
    source_counts.columns = ['Source', 'Count']
    fig_pie = px.pie(source_counts, values='Count', names='Source', hole=0.6)
    fig_pie.update_layout(
        template='plotly_dark', 
        margin=dict(t=10, b=10, l=10, r=10), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False # Hide legend to save space like in the video
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True, height=250)
    
    # Hourly Trend Line Chart (instead of Bar) for a more "telemetry" feel
    st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 10px;'>24H PM2.5 Trend</h3>", unsafe_allow_html=True)
    hourly_trend = filtered_df.groupby('hour')['pm25'].mean().reset_index()
    fig_line = px.line(hourly_trend, x='hour', y='pm25')
    fig_line.update_layout(
        template='plotly_dark', 
        margin=dict(t=10, b=10, l=10, r=10), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None, yaxis_title=None
    )
    # Add a glowing fill to the line
    fig_line.update_traces(line=dict(color='#ef4444', width=3), fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.1)')
    st.plotly_chart(fig_line, use_container_width=True, height=200)

# --- BOTTOM ROW: AI DIAGNOSTICS MODULE ---
st.markdown("<h3 style='font-size: 1.2rem; margin-top: 20px; border-bottom: 1px solid #1f2937; padding-bottom: 5px;'>AI Diagnostics & Source Prediction</h3>", unsafe_allow_html=True)

if model_loaded:
    with st.form("prediction_form"):
        pred_col1, pred_col2, pred_col3, pred_col4 = st.columns([1, 1, 1, 1.5])
        
        with pred_col1:
            pm25 = st.number_input("PM2.5", value=50.0)
            pm10 = st.number_input("PM10", value=60.0)
            no2 = st.number_input("NO₂", value=20.0)
            co = st.number_input("CO", value=0.5)
        with pred_col2:
            so2 = st.number_input("SO₂", value=10.0)
            o3 = st.number_input("Ozone", value=30.0)
            temp = st.number_input("Temp (°C)", value=25.0)
            humid = st.number_input("Humidity %", value=60.0)
        with pred_col3:
            wind_spd = st.number_input("Wind (m/s)", value=3.0)
            wind_dir = st.number_input("Wind Dir (°)", value=180)
            hour = st.slider("Hour", 0, 23, 12)
            is_weekend = st.selectbox("Weekend", [0, 1])
        with pred_col4:
            dist_road = st.number_input("Dist Road (m)", value=50)
            dist_ind = st.number_input("Dist Industry (m)", value=5000)
            dist_farm = st.number_input("Dist Farm (m)", value=10000)
            dist_waste = st.number_input("Dist Waste (m)", value=8000)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button(label="EXECUTE AI DIAGNOSTIC", use_container_width=True)
            
    if submit_button:
        input_data = pd.DataFrame([[pm25, pm10, no2, co, so2, o3, temp, humid, wind_spd, wind_dir, dist_road, dist_ind, dist_farm, dist_waste, hour, is_weekend]], 
                                  columns=['pm25', 'pm10', 'no2', 'co', 'so2', 'o3', 'temperature_c', 'humidity_percent', 'wind_speed_mps', 'wind_direction_deg', 'dist_to_road_m', 'dist_to_industry_m', 'dist_to_farm_m', 'dist_to_waste_m', 'hour', 'is_weekend'])
        
        pred_num = model.predict(input_data)[0]
        pred_text = encoder.inverse_transform([pred_num])[0]
        probs = model.predict_proba(input_data)[0]
        confidence = max(probs) * 100
        
        # Display results in a high-tech style
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.markdown(f"<div style='border: 1px solid #38bdf8; padding: 15px; border-radius: 5px; text-align: center;'><span style='color: #94a3b8;'>PRIMARY SOURCE DETECTED</span><br><span style='font-size: 1.5rem; color: #38bdf8; font-weight: bold;'>{pred_text}</span></div>", unsafe_allow_html=True)
        with res_col2:
            # Create a gauge chart for confidence
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = confidence,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "AI Confidence Level", 'font': {'size': 14, 'color': '#94a3b8'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#10b981"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#1f2937",
                }
            ))
            fig_gauge.update_layout(height=150, margin=dict(t=20, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig_gauge, use_container_width=True)
        
else:
    st.error("AI Diagnostic Module Offline: Model files missing.")