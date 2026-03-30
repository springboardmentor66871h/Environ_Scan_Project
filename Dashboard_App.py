
#      DASHBOARD          


import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import (HeatMap, MarkerCluster, MiniMap,
                             Draw, MeasureControl, LocateControl, Fullscreen)
from streamlit_folium import st_folium
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import time
import smtplib
import urllib.request
import urllib.parse
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="EnviroScan Elite Pro",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=""
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }
h1,h2,h3,h4 { font-family: 'Poppins', sans-serif; }
body { background:#f5f7fa; color:#1a1a1a; }
.main { background:#f5f7fa; }


.pro-card {
    background:#ffffff; border:2px solid #e1e8ed; border-radius:16px;
    padding:28px; box-shadow:0 4px 12px rgba(0,0,0,.08);
    transition:all .3s ease; margin:12px 0;
}
.pro-card:hover {
    box-shadow:0 8px 24px rgba(33,150,243,.15);
    transform:translateY(-3px); border-color:#2196F3;
}


.metric-card {
    background:linear-gradient(145deg,#ffffff,#f8fafb);
    border:3px solid #e3e8ef; border-radius:18px;
    padding:26px; text-align:center;
    transition:all .4s cubic-bezier(.4,0,.2,1);
    position:relative; overflow:hidden;
}
.metric-card::before {
    content:''; position:absolute; top:0; left:-100%;
    width:100%; height:100%;
    background:linear-gradient(90deg,transparent,rgba(33,150,243,.12),transparent);
    transition:left .6s;
}
.metric-card:hover::before { left:100%; }
.metric-card:hover {
    border-color:#2196F3;
    box-shadow:0 8px 28px rgba(33,150,243,.2);
    transform:translateY(-4px) scale(1.02);
}
.metric-label {
    font-size:13px; font-weight:700; color:#5a6c7d;
    text-transform:uppercase; letter-spacing:1.8px; margin-bottom:12px;
}
.metric-value {
    font-size:46px; font-weight:900; color:#1a1a1a;
    font-family:'Poppins',sans-serif; margin:12px 0;
    text-shadow:0 2px 4px rgba(0,0,0,.1);
}
.metric-subtitle { font-size:17px; font-weight:600; color:#2196F3; margin-top:10px; }
.metric-description { font-size:13px; color:#64748b; margin-top:6px; font-weight:500; }


@keyframes pulse-critical {
    0%,100%{ transform:scale(1); box-shadow:0 6px 20px rgba(244,67,54,.4); }
    50%{ transform:scale(1.015); box-shadow:0 10px 32px rgba(244,67,54,.6); }
}
.alert-critical {
    background:linear-gradient(135deg,#f44336,#e91e63);
    color:#fff; padding:24px 35px; border-radius:14px;
    text-align:center; font-weight:700; font-size:22px;
    animation:pulse-critical 2s infinite; margin:25px 0;
    border:3px solid #c62828; box-shadow:0 8px 24px rgba(244,67,54,.4);
}
.alert-warning {
    background:linear-gradient(135deg,#ff9800,#ff5722);
    color:#fff; padding:20px 28px; border-radius:12px;
    font-weight:600; font-size:19px;
    box-shadow:0 6px 18px rgba(255,152,0,.3);
}
.alert-success {
    background:linear-gradient(135deg,#4CAF50,#388E3C);
    color:#fff; padding:18px 24px; border-radius:12px;
    font-weight:600; font-size:17px;
    box-shadow:0 6px 18px rgba(76,175,80,.3);
}


.section-header {
    font-size:32px; font-weight:800; color:#1a1a1a;
    margin:35px 0 24px; padding-bottom:14px;
    border-bottom:4px solid #2196F3; font-family:'Poppins',sans-serif;
}
.section-subheader {
    font-size:24px; font-weight:700; color:#2c3e50; margin:24px 0 18px;
}


.divider {
    height:3px;
    background:linear-gradient(90deg,transparent,#2196F3,transparent);
    margin:40px 0; position:relative;
}
.divider::before {
    content:''; position:absolute; left:50%; top:50%;
    transform:translate(-50%,-50%); background:#f5f7fa;
    padding:0 18px; color:#2196F3; font-size:18px;
}


[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#1e3a8a 0%,#1e40af 100%);
}
[data-testid="stSidebar"] * { color:#ffffff !important; }
[data-testid="stSidebar"] label {
    color:#ffffff !important; font-weight:600 !important;
    font-size:14px !important; margin-bottom:8px !important;
}


[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] textarea {
    background:#f0f4f8 !important; color:#1a1a1a !important;
    border:2px solid #cbd5e1 !important; border-radius:8px !important;
    padding:10px 12px !important; font-size:14px !important;
}
[data-testid="stSidebar"] input:focus,
[data-testid="stSidebar"] select:focus {
    background:#ffffff !important; border-color:#60a5fa !important;
    box-shadow:0 0 0 3px rgba(96,165,250,.3) !important;
}
[data-testid="stSidebar"] input::placeholder { color:#64748b !important; }


.sidebar-section {
    background:rgba(255,255,255,0.12) !important; 
    border:2px solid rgba(255,255,255,0.2) !important;
    border-radius:12px !important;
    padding:18px !important;
    margin:16px 0 !important;
    backdrop-filter:blur(10px) !important;
}

.sidebar-section-blue {
    background:linear-gradient(135deg,rgba(33,150,243,0.2),rgba(33,150,243,0.12)) !important;
    border:2px solid rgba(33,150,243,0.4) !important;
    border-radius:12px !important;
    padding:18px !important;
    margin:16px 0 !important;
}

.sidebar-section-green {
    background:linear-gradient(135deg,rgba(76,175,80,0.2),rgba(76,175,80,0.12)) !important;
    border:2px solid rgba(76,175,80,0.4) !important;
    border-radius:12px !important;
    padding:18px !important;
    margin:16px 0 !important;
}

.sidebar-section-orange {
    background:linear-gradient(135deg,rgba(255,152,0,0.2),rgba(255,152,0,0.12)) !important;
    border:2px solid rgba(255,152,0,0.4) !important;
    border-radius:12px !important;
    padding:18px !important;
    margin:16px 0 !important;
}

.sidebar-section-red {
    background:linear-gradient(135deg,rgba(244,67,54,0.2),rgba(244,67,54,0.12)) !important;
    border:2px solid rgba(244,67,54,0.4) !important;
    border-radius:12px !important;
    padding:18px !important;
    margin:16px 0 !important;
}

.sidebar-section-purple {
    background:linear-gradient(135deg,rgba(156,39,176,0.2),rgba(156,39,176,0.12)) !important;
    border:2px solid rgba(156,39,176,0.4) !important;
    border-radius:12px !important;
    padding:18px !important;
    margin:16px 0 !important;
}

.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stSelectbox>div>div>select,
.stDateInput>div>div>input,
.stTextArea>div>div>textarea {
    background:#f8fafc !important; border:2px solid #cbd5e1 !important;
    border-radius:10px !important; color:#1a1a1a !important;
    padding:12px 14px !important; font-size:15px !important;
    font-weight:500 !important;
}
.stTextInput>div>div>input:focus,
.stNumberInput>div>div>input:focus {
    background:#ffffff !important; border-color:#2196F3 !important;
    box-shadow:0 0 0 3px rgba(33,150,243,.2) !important;
}
input::placeholder,textarea::placeholder { color:#64748b !important; opacity:.8 !important; }


.stButton>button {
    background:linear-gradient(135deg,#2196F3,#1976D2);
    color:#fff; border:none; border-radius:10px;
    padding:14px 32px; font-weight:700; font-size:15px;
    transition:all .3s ease; box-shadow:0 6px 16px rgba(33,150,243,.4);
    text-transform:uppercase; letter-spacing:.5px;
}
.stButton>button:hover {
    transform:translateY(-3px);
    box-shadow:0 10px 28px rgba(33,150,243,.6);
}


.stProgress>div>div>div {
    background:linear-gradient(90deg,#2196F3,#1976D2); border-radius:10px;
}

.dataframe { background:#ffffff !important; color:#1a1a1a !important;
    border:2px solid #e0e0e0 !important; border-radius:10px !important; }
.dataframe th {
    background:linear-gradient(135deg,#2196F3,#1976D2) !important;
    color:#fff !important; font-weight:700 !important; padding:14px !important;
}
.dataframe td { color:#1a1a1a !important; padding:12px !important; }


.chart-container {
    background:#ffffff; border:2px solid #e1e8ed; border-radius:14px;
    padding:24px; margin:18px 0; box-shadow:0 4px 16px rgba(0,0,0,.08);
}


@keyframes blink { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:.4;transform:scale(.9);} }
.live-dot {
    display:inline-block; width:12px; height:12px; background:#4CAF50;
    border-radius:50%; animation:blink 1.5s infinite;
    margin-right:10px; box-shadow:0 0 10px #4CAF50;
}


.header-bar {
    background:linear-gradient(135deg,#1e3a8a,#1e40af);
    color:#fff; padding:32px 45px; border-radius:16px;
    margin-bottom:35px; box-shadow:0 8px 24px rgba(30,58,138,.3);
}
.header-title {
    font-size:48px; font-weight:900; color:#fff; margin:0;
    font-family:'Poppins',sans-serif; text-shadow:0 4px 8px rgba(0,0,0,.2);
}
.header-subtitle { font-size:19px; color:#e0e7ff; margin-top:10px; font-weight:500; }


.info-box { background:#e3f2fd; border-left:5px solid #2196F3;
    padding:18px 24px; border-radius:8px; color:#1a1a1a; margin:14px 0; font-weight:500; }
.warning-box { background:#fff3e0; border-left:5px solid #FF9800;
    padding:18px 24px; border-radius:8px; color:#1a1a1a; margin:14px 0; font-weight:500; }
.success-box { background:#e8f5e9; border-left:5px solid #4CAF50;
    padding:18px 24px; border-radius:8px; color:#1a1a1a; margin:14px 0; font-weight:500; }


.map-container {
    border:4px solid #2196F3; border-radius:18px; overflow:hidden;
    box-shadow:0 8px 32px rgba(33,150,243,.25); margin:24px 0;
}

.prediction-box {
    background:#fff; border:3px solid #2196F3; border-radius:14px;
    padding:28px; margin:18px 0; box-shadow:0 6px 20px rgba(33,150,243,.2);
}
.prediction-title { font-size:22px; font-weight:700; color:#1a1a1a; margin-bottom:16px; }
.prediction-value { font-size:36px; font-weight:800; color:#2196F3; margin:12px 0; }
.confidence-bar { background:#e0e0e0; height:32px; border-radius:16px; overflow:hidden; margin:16px 0; }
.confidence-fill {
    background:linear-gradient(90deg,#4CAF50,#8BC34A); height:100%; border-radius:16px;
    display:flex; align-items:center; justify-content:center;
    color:#fff; font-weight:700; font-size:15px;
}


.stat-box {
    background:#fff; border:2px solid #e1e8ed; border-radius:12px;
    padding:22px; text-align:center; margin:12px 0; transition:all .3s ease;
}
.stat-box:hover { box-shadow:0 6px 20px rgba(33,150,243,.15); transform:translateY(-2px); }
.stat-number { font-size:38px; font-weight:800; color:#2196F3; font-family:'Poppins',sans-serif; }
.stat-label { font-size:14px; color:#5a6c7d; font-weight:600; margin-top:10px;
    text-transform:uppercase; letter-spacing:1.2px; }


.feature-highlight {
    background:linear-gradient(135deg,#2196F3,#1976D2); color:#fff;
    padding:24px 30px; border-radius:12px; margin:20px 0;
    font-weight:600; font-size:16px; box-shadow:0 6px 20px rgba(33,150,243,.4);
}


::-webkit-scrollbar { width:14px; height:14px; }
::-webkit-scrollbar-track { background:#f1f5f9; border-radius:10px; }
::-webkit-scrollbar-thumb { background:linear-gradient(135deg,#2196F3,#1976D2);
    border-radius:10px; border:3px solid #f1f5f9; }
::-webkit-scrollbar-thumb:hover { background:linear-gradient(135deg,#1976D2,#1565C0); }


@keyframes fadeInUp { from{opacity:0;transform:translateY(30px);} to{opacity:1;transform:translateY(0);} }
.animated-fade { animation:fadeInUp .6s ease-out; }


.stTabs [data-baseweb="tab"] { background:#f8fafc; border-radius:8px; padding:12px 24px; font-weight:600; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#2196F3,#1976D2); color:#fff !important; }


.stMultiSelect>div>div>div { background:#f8fafc !important; border:2px solid #cbd5e1 !important; border-radius:10px !important; }
.stRadio>div { background:#f8fafc; padding:12px; border-radius:10px; border:2px solid #e1e8ed; }
.stCheckbox>label { font-weight:600 !important; color:#1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='header-bar animated-fade'>
    <div class='header-title'> EnviroScan Elite Pro</div>
    <div class='header-subtitle'>
        <span class='live-dot'></span>
        Advanced Environmental Intelligence &amp; Pollution Source Prediction System
    </div>
</div>
""", unsafe_allow_html=True)

defaults = {
    'alert_history': [], 'predictions_log': [],
    'email_sent': False, 'sms_sent': False,
    'analysis_count': 0, 'last_aqi': 0
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

MODEL_PATH = r"C:\Users\admin\Environ_Scan_Project\model\final_pollution_model.pkl"

CITY_MAP = {
    0:"Ahmedabad",1:"Bengaluru",2:"Chennai",3:"Delhi",4:"Hyderabad",
    5:"Jaipur",6:"Kolkata",7:"Lucknow",8:"Mumbai",9:"Pune"
}

SOURCE_EMOJI = {"Vehicular":" ","Industrial":" ","Agricultural":" ","Burning":" ","Natural":" "}

POLL_COLORS = {
    'PM2.5':'#f44336','PM10':'#FF9800','NO2':'#2196F3',
    'SO2':'#9C27B0','CO':'#4CAF50','O3':'#00BCD4'
}

@st.cache_resource(show_spinner=False)
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        st.error(f"Model error: {e}")
        return None

with st.spinner(" Initialising AI engine…"):
    model = load_model()

if model is None:
    st.error(" Model not found. Check MODEL_PATH at top of file.")
    st.stop()

MODEL_FEATURES = list(model.feature_names_in_)

def calculate_aqi(row):
    return max(abs(row['PM2.5'])*1.0, abs(row['PM10'])*0.5,
               abs(row['NO2'])*0.8,   abs(row['SO2'])*0.7,
               abs(row['CO'])*0.3,    abs(row['O3'])*0.6)

def get_aqi_category(aqi):
    if aqi<=50:   return "Good",       "#4CAF50","Excellent air quality"
    if aqi<=100:  return "Satisfactory","#8BC34A","Acceptable air quality"
    if aqi<=200:  return "Moderate",   "#FFC107","Sensitive groups affected"
    if aqi<=300:  return "Poor",       "#FF9800","Health effects for all"
    if aqi<=400:  return "Very Poor",  "#FF5722","Serious health alert"
    return               "Severe",     "#f44336","Emergency conditions"

def calculate_health_index(row):
    return (0.40*abs(row['PM2.5']) + 0.20*abs(row['NO2']) +
            0.20*abs(row['SO2'])  + 0.10*abs(row['CO'])  +
            0.10*abs(row['O3']))

def classify_severity(pm):
    if pm>250: return "🔴 Hazardous"
    if pm>150: return "🟠 Severe"
    if pm>100: return "🟡 Moderate"
    return           "🟢 Low"

def advanced_root_cause(row):
    causes = []
    hr = row.get('hour', -1)
    src = row.get('predicted_source','')
    if src=='Vehicular' and hr in [7,8,9,17,18,19,20]:
        causes.append("Peak-hour traffic congestion")
    if src=='Industrial' and hr>=22:
        causes.append("Night-shift industrial operations")
    if src=='Industrial' and hr<=6:
        causes.append("Early morning industrial discharge")
    ws = row.get('wind_speed', 5)
    if ws < 1.5:
        causes.append("Stagnant air / near-zero wind")
    elif ws < 2.5:
        causes.append("Low wind — limited pollutant dispersion")
    if row.get('humidity', 50) > 78:
        causes.append("High humidity trapping fine particles")
    if row.get('temperature', 25) < 15:
        causes.append("Temperature inversion layering")
    if row.get('distance_to_road_km', 99) < 0.5:
        causes.append("Proximity to high-traffic road")
    if row.get('distance_to_industry_km', 99) < 1.0:
        causes.append("Close to industrial zone")
    if src=='Agricultural':
        causes.append("Crop-residue burning season")
    if src=='Burning':
        causes.append("Open waste combustion detected")
    if row.get('is_weekend', 0)==1 and row.get('PM2.5',0)>150:
        causes.append("Weekend construction / leisure activity")
    if not causes:
        causes.append("Mixed urban emission — multi-factor origin")
    return " | ".join(causes)

def send_real_email(to_addr, subject, html_body,
                    smtp_host, smtp_port, sender, password):
    
    try:
        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From']    = sender
        msg['To']      = to_addr
        msg.attach(MIMEText(html_body, 'html'))
        with smtplib.SMTP(smtp_host, int(smtp_port), timeout=12) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(sender, password)
            srv.sendmail(sender, to_addr, msg.as_string())
        return True, "Email sent successfully "
    except smtplib.SMTPAuthenticationError:
        return False, "Auth failed — use Gmail App Password, not your Gmail login password"
    except smtplib.SMTPConnectError:
        return False, f"Cannot connect to {smtp_host}:{smtp_port}"
    except Exception as e:
        return False, str(e)

def build_email_body(city, avg_aqi, max_aqi, aqi_label, aqi_color,
                     dominant_source, aqi_desc, n_anomalies, recs):
    rec_html = "".join(f"<li>{r}</li>" for r in recs[:6])
    return f"""
<html><body style='font-family:Arial,sans-serif;background:#f5f7fa;padding:20px;'>
  <div style='max-width:600px;margin:auto;background:#fff;border-radius:16px;
              border-top:6px solid {aqi_color};padding:30px;'>
    <h2 style='color:#f44336;margin:0 0 20px;'>  Critical Air Quality Alert</h2>
    <table style='width:100%;border-collapse:collapse;'>
      <tr><td style='padding:10px;background:#fce4ec;font-weight:bold;border-radius:4px;'>📍 Location</td>
          <td style='padding:10px;'>{city}</td></tr>
      <tr><td style='padding:10px;background:#fce4ec;font-weight:bold;'> Avg AQI</td>
          <td style='padding:10px;color:{aqi_color};font-weight:bold;font-size:18px;'>{avg_aqi:.1f}</td></tr>
      <tr><td style='padding:10px;background:#fce4ec;font-weight:bold;'> Max AQI</td>
          <td style='padding:10px;'>{max_aqi:.1f}</td></tr>
      <tr><td style='padding:10px;background:#fce4ec;font-weight:bold;'>Category</td>
          <td style='padding:10px;color:{aqi_color};font-weight:bold;'>{aqi_label}</td></tr>
      <tr><td style='padding:10px;background:#fce4ec;font-weight:bold;'> Source</td>
          <td style='padding:10px;'>{dominant_source}</td></tr>
      <tr><td style='padding:10px;background:#fce4ec;font-weight:bold;'>Status</td>
          <td style='padding:10px;'>{aqi_desc}</td></tr>
      <tr><td style='padding:10px;background:#fce4ec;font-weight:bold;'> Anomalies</td>
          <td style='padding:10px;'>{n_anomalies} pollution spikes detected</td></tr>
      <tr><td style='padding:10px;background:#fce4ec;font-weight:bold;'> Time</td>
          <td style='padding:10px;'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
    </table>
    <div style='background:#ffebee;border-radius:8px;padding:16px;margin-top:20px;'>
      <h3 style='color:#c62828;margin:0 0 12px;'>Immediate Actions Required</h3>
      <ul style='margin:0;padding-left:20px;line-height:1.9;'>
        <li>Avoid all non-essential outdoor activities</li>
        <li>Use N95/FFP2 respirator masks if going outside</li>
        <li>Keep windows and doors sealed</li>
        <li>Run HEPA air purifiers indoors</li>
        <li>Monitor health symptoms — seek medical help if needed</li>
        <li>Keep children and elderly indoors</li>
      </ul>
    </div>
    <div style='background:#e8f5e9;border-radius:8px;padding:16px;margin-top:16px;'>
      <h3 style='color:#2e7d32;margin:0 0 12px;'>AI Recommendations</h3>
      <ol style='margin:0;padding-left:20px;line-height:1.9;'>{rec_html}</ol>
    </div>
    <p style='color:#90a4ae;font-size:11px;margin-top:20px;'>
      Auto-generated by EnviroScan Elite Pro AI Engine | Do not reply
    </p>
  </div>
</body></html>"""

def send_real_sms(phone, message, api_key):
  
    try:
        clean = phone.replace("+91","").replace("-","").replace(" ","").strip()
        if len(clean) != 10 or not clean.isdigit():
            return False, "Invalid phone — must be 10 digits (Indian numbers)"
        payload = json.dumps({
            "route":    "q",
            "message":  message[:160],
            "language": "english",
            "flash":    0,
            "numbers":  clean
        }).encode('utf-8')
        req = urllib.request.Request(
            "https://www.fast2sms.com/dev/bulkV2",
            data=payload,
            headers={"authorization": api_key, "Content-Type":"application/json"}
        )
        resp   = urllib.request.urlopen(req, timeout=12)
        result = json.loads(resp.read().decode())
        if result.get("return"):
            return True,  f"SMS sent to +91-{clean}"
        return False, result.get("message","Unknown error from Fast2SMS")
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code} — check API key"
    except Exception as e:
        return False, str(e)

def build_sms_text(city, avg_aqi, aqi_label, dominant_source):
    return (f"EnviroScan ALERT | {city} | "
            f"AQI:{avg_aqi:.0f} ({aqi_label}) | "
            f"Source:{dominant_source} | "
            f"AVOID outdoors. Use N95 mask. "
            f"{datetime.now().strftime('%d/%m %H:%M')}")

with st.sidebar:
    st.markdown("## Control Panel")
    st.markdown("---")

    st.markdown("<div class='sidebar-section-blue'>", unsafe_allow_html=True)
    st.markdown("### Data Source")

    uploaded_file = st.file_uploader(
        "Upload Pollution Dataset (CSV)", type=['csv'],
        help="CSV with columns: PM2.5, PM10, NO2, SO2, CO, O3, etc."
    )

    st.markdown("""
<style>
/* File uploader box background & border */
div.stFileUploader {
    background-color:#1e1e2f !important;  /* light background */
    border-radius: 12px !important;
    padding: 12px !important;
    border: 1px solid #cfd8dc !important;
}

/* Change "Browse files" button */
div.stFileUploader button {
    background-color: #4caf50 !important;  /* green button */
    color: white !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    padding: 0px 12px !important;
}

/* Hover effect for button */
div.stFileUploader button:hover {
    background-color: #45a049 !important;
}
</style>
""", unsafe_allow_html=True)

    st.markdown("---")

    
    st.markdown("<div class='sidebar-section-green'>", unsafe_allow_html=True)
    st.markdown("###  Manual Input")
    with st.expander("Enter Location & Parameters", expanded=False):
        manual_city = st.text_input("City Name", placeholder="e.g., Delhi")
        c1,c2 = st.columns(2)
        with c1: manual_lat = st.number_input("Latitude",  value=28.6139, format="%.4f")
        with c2: manual_lon = st.number_input("Longitude", value=77.2090, format="%.4f")

        st.markdown("**Pollutant Concentrations (µg/m³):**")
        c1,c2 = st.columns(2)
        with c1:
            manual_pm25 = st.number_input("PM2.5", min_value=0.0, value=50.0, step=1.0)
            manual_no2  = st.number_input("NO2",   min_value=0.0, value=30.0, step=1.0)
            manual_co   = st.number_input("CO",    min_value=0.0, value=1.0,  step=0.1)
        with c2:
            manual_pm10 = st.number_input("PM10",  min_value=0.0, value=80.0, step=1.0)
            manual_so2  = st.number_input("SO2",   min_value=0.0, value=15.0, step=1.0)
            manual_o3   = st.number_input("O3",    min_value=0.0, value=40.0, step=1.0)

        st.markdown("**Weather Parameters:**")
        c1,c2,c3 = st.columns(3)
        with c1: manual_temp     = st.number_input("Temp °C",   value=25.0, step=0.5)
        with c2: manual_humidity = st.number_input("Humidity %", value=60.0, step=1.0)
        with c3: manual_wind     = st.number_input("Wind m/s",   value=2.5,  step=0.1)

        analyze_manual = st.button("Analyze Manual Input", width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")


    st.markdown("<div class='sidebar-section-orange'>", unsafe_allow_html=True)

    st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
}

/* ONLY sidebar radio buttons */
[data-testid="stSidebar"] div[role="radiogroup"] {
    background-color: #2c2c34 !important;
    padding: 8px;
    border-radius: 8px;
}

/* ONLY sidebar radio text */
[data-testid="stSidebar"] div[role="radiogroup"] label {
    color: #FFFFFF !important;  /* change to white for visibility */
    font-weight: 500;
}

/* Hover effect */
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    color: #4caf50 !important;
}

</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown("### Time Range Filter")
    time_mode = st.radio("Period", ["All Data","Last 7 Days","Last 30 Days","Custom Range"])
    if time_mode == "Custom Range":
        c1,c2 = st.columns(2)
        with c1: start_date = st.date_input("Start", value=datetime.now()-timedelta(days=30))
        with c2: end_date   = st.date_input("End",   value=datetime.now())
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("<div class='sidebar-section-red'>", unsafe_allow_html=True)
    st.markdown("### Alert Settings")
    alert_threshold = st.slider("AQI Alert Threshold", 50, 500, 200, 10)

    enable_email = st.checkbox(" Enable Email Alerts")
    if enable_email:
        st.markdown("*Gmail → Settings → Security → App Passwords*")
        email_to       = st.text_input("Recipient Email",    placeholder="recipient@example.com")
        email_sender   = st.text_input("Your Gmail Address", placeholder="you@gmail.com")
        email_password = st.text_input("Gmail App Password (16 chars)",
                                        placeholder="xxxx xxxx xxxx xxxx", type="password")
        smtp_host = "smtp.gmail.com"
        smtp_port = 587

    enable_sms = st.checkbox(" Enable SMS Alerts (Fast2SMS)")
    if enable_sms:
        st.markdown("*Free SMS: [fast2sms.com](https://www.fast2sms.com)*")
        sms_phone   = st.text_input("Mobile Number", placeholder="91XXXXXXXXXX or 10-digit")
        sms_api_key = st.text_input("Fast2SMS API Key",
                                     placeholder="Paste from fast2sms.com dashboard",
                                     type="password")

    if st.button(" Reset Alert State"):
        st.session_state.email_sent = False
        st.session_state.sms_sent   = False
        st.success("Alert state reset — will send again on next trigger")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("<div class='sidebar-section-purple'>", unsafe_allow_html=True)
    st.markdown("### Advanced Settings")
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.05)
    show_3d       = st.checkbox("Enable 3D Visualizations",   value=True)
    show_radar    = st.checkbox("Enable Radar Chart",          value=True)
    show_heatmap  = st.checkbox("Enable Day/Hour Heatmap",     value=True)
    show_corr     = st.checkbox("Enable Correlation Heatmap",  value=True)
    show_forecast = st.checkbox("Enable 7-Day Trend Forecast", value=True)
    auto_refresh  = st.checkbox("Auto-refresh every 30 s",     value=False)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### System Status")
    st.markdown(f"""
    <div style='padding:16px;background:rgba(255,255,255,.12);border-radius:12px;font-size:13px;'>
        <span class='live-dot'></span><b>Status:</b> Active<br>
        <b>Model:</b> Loaded ✓<br>
        <b>Analyses Run:</b> {st.session_state.analysis_count}<br>
        <b>Alerts Fired:</b> {len(st.session_state.alert_history)}<br>
        <b>Email Sent:</b> {'Yes ✓' if st.session_state.email_sent else 'No'}<br>
        <b>SMS Sent:</b>   {'Yes ✓' if st.session_state.sms_sent   else 'No'}<br>
        <b>Updated:</b> {datetime.now().strftime('%H:%M:%S')}
    </div>""", unsafe_allow_html=True)

if uploaded_file or analyze_manual:

    st.session_state.analysis_count += 1

    if analyze_manual:
        st.markdown("<div class='section-header animated-fade'> Manual Input Analysis</div>",
                    unsafe_allow_html=True)
        mrow = {
            'PM2.5':manual_pm25,'PM10':manual_pm10,'NO2':manual_no2,
            'SO2':manual_so2,'CO':manual_co,'O3':manual_o3,
            'temperature':manual_temp,'humidity':manual_humidity,
            'wind_speed':manual_wind,'latitude':manual_lat,'longitude':manual_lon,
            'city_name':manual_city or 'Manual Entry','timestamp':datetime.now(),
            'hour':datetime.now().hour,'day':datetime.now().day,
            'month':datetime.now().month,'year':datetime.now().year,
            'day_of_week':datetime.now().weekday(),'is_weekend':int(datetime.now().weekday()>=5)
        }
        df      = pd.DataFrame([mrow])
        df['aqi']          = df.apply(calculate_aqi, axis=1)
        df['health_index'] = df.apply(calculate_health_index, axis=1)
        full_df      = df.copy()
        selected_city = manual_city or 'Manual Entry'

    else:
        with st.spinner("Loading & processing environmental data…"):
            prog = st.progress(0)
            full_df = pd.read_csv(uploaded_file)
            prog.progress(20)

      
            if 'timestamp' not in full_df.columns:
                if {'year','month','day','hour'}.issubset(full_df.columns):
                    full_df['timestamp'] = pd.to_datetime(full_df[['year','month','day','hour']])
                else:
                    full_df['timestamp'] = datetime.now()
            full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])
            prog.progress(40)

        
            if 'aqi' not in full_df.columns:
                full_df['aqi'] = full_df.apply(calculate_aqi, axis=1)

            full_df['health_index'] = full_df.apply(calculate_health_index, axis=1)

     
            if 'city_name' not in full_df.columns and 'city' in full_df.columns:
                full_df['city_name'] = full_df['city'].map(CITY_MAP)

       
            full_df['day_of_week'] = full_df['timestamp'].dt.dayofweek
            full_df['is_weekend']  = full_df['day_of_week'].isin([5,6]).astype(int)
            if 'hour' in full_df.columns:
                full_df['hour_category'] = pd.cut(
                    full_df['hour'], bins=[0,6,12,18,24],
                    labels=['Night','Morning','Afternoon','Evening'])
            prog.progress(70)

            if time_mode == "Last 7 Days":
                full_df = full_df[full_df['timestamp'] >= datetime.now()-timedelta(days=7)]
            elif time_mode == "Last 30 Days":
                full_df = full_df[full_df['timestamp'] >= datetime.now()-timedelta(days=30)]
            elif time_mode == "Custom Range":
                full_df = full_df[
                    (full_df['timestamp'].dt.date >= start_date) &
                    (full_df['timestamp'].dt.date <= end_date)]
            prog.progress(100)
            time.sleep(0.15)
            prog.empty()

       
        st.markdown("<div class='section-header animated-fade'>Location Selection</div>",
                    unsafe_allow_html=True)
        c1,c2,c3 = st.columns([2,2,1])
        with c1:
            cities = ["All Cities"] + sorted(full_df['city_name'].dropna().unique().tolist())
            selected_city = st.selectbox("Select City for Analysis", cities)
        with c2:
            if selected_city != "All Cities":
                coords = full_df[full_df['city_name']==selected_city][['latitude','longitude']].mean()
                st.markdown(f"<div class='info-box'><b>📍 Coordinates:</b> "
                            f"{coords['latitude']:.4f}°N, {coords['longitude']:.4f}°E</div>",
                            unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-box'>"
                        f"<div class='stat-number'>{len(full_df):,}</div>"
                        f"<div class='stat-label'>Records</div></div>",
                        unsafe_allow_html=True)

        df = (full_df.copy() if selected_city=="All Cities"
              else full_df[full_df['city_name']==selected_city].copy())

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header animated-fade'>AI Pollution Source Prediction</div>",
                unsafe_allow_html=True)

    with st.spinner("Running ML classification…"):
        X = df.copy()
        drop = ['city','city_name','timestamp','pollution_source',
                'day_of_week','is_weekend','hour_category','aqi','health_index']
        X.drop(columns=[c for c in drop if c in X.columns], inplace=True)
        for col in MODEL_FEATURES:
            if col not in X.columns:
                X[col] = 0
        X = X[MODEL_FEATURES].apply(pd.to_numeric, errors='coerce').fillna(0)

        df['predicted_source'] = model.predict(X)
        proba = model.predict_proba(X)
        df['confidence']      = proba.max(axis=1)
        df['high_confidence'] = df['confidence'] >= confidence_threshold

 
        st.session_state.predictions_log.append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'city': selected_city,
            'records': len(df),
            'dom_source': df['predicted_source'].mode()[0],
            'avg_conf': round(df['confidence'].mean()*100,1)
        })

    dominant_source = df['predicted_source'].mode()[0]
    avg_confidence  = df['confidence'].mean()
    high_conf_count = int(df['high_confidence'].sum())
    emoji = SOURCE_EMOJI.get(dominant_source," ")

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class='prediction-box'>
            <div class='prediction-title'>Dominant Pollution Source</div>
            <div class='prediction-value'>{emoji} {dominant_source}</div>
            <div style='font-size:14px;color:#5a6c7d;margin-top:12px;'>
                Primary emission category in {selected_city}
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='prediction-box'>
            <div class='prediction-title'>Average Model Confidence</div>
            <div class='prediction-value'>{avg_confidence*100:.1f}%</div>
            <div class='confidence-bar'>
                <div class='confidence-fill' style='width:{avg_confidence*100:.1f}%;'>
                    {avg_confidence*100:.1f}%
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
    with c3:
        pct = (high_conf_count/len(df)*100) if len(df) else 0
        st.markdown(f"""
        <div class='prediction-box'>
            <div class='prediction-title'>High-Confidence Predictions</div>
            <div class='prediction-value'>{high_conf_count:,}</div>
            <div style='font-size:14px;color:#5a6c7d;margin-top:12px;'>
                {pct:.1f}% meet ≥{confidence_threshold*100:.0f}% threshold
            </div>
        </div>""", unsafe_allow_html=True)

    with st.expander("Per-Source Probability Breakdown (All Classes)", expanded=False):
        classes = model.classes_
        prob_df = pd.DataFrame(proba, columns=classes)
        prob_df.insert(0,'City',    df['city_name'].values    if 'city_name' in df.columns else 'N/A')
        prob_df.insert(1,'Time', pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M').values if 'timestamp' in df.columns else 'N/A')
        prob_df['Prediction'] = df['predicted_source'].values
        prob_df['Confidence'] = df['confidence'].values
        st.dataframe(
            prob_df.head(150).style
              .background_gradient(subset=list(classes), cmap='Blues')
              .format({c:'{:.1%}' for c in list(classes)+['Confidence']}),
            use_container_width=True, height=380)

    with st.expander("Detailed Prediction Table", expanded=False):
        dcols = [c for c in ['city_name','timestamp','PM2.5','PM10','NO2',
                              'predicted_source','confidence','aqi'] if c in df.columns]
        pred_display = df[dcols].head(200).copy()

        if 'timestamp' in pred_display.columns:
            pred_display['timestamp'] = pd.to_datetime(pred_display['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(
            pred_display.style
              .background_gradient(subset=['confidence'], cmap='Greens')
              .background_gradient(subset=['PM2.5'],      cmap='Reds')
              .format({'confidence':'{:.1%}','PM2.5':'{:.1f}',
                       'PM10':'{:.1f}','NO2':'{:.1f}','aqi':'{:.1f}'}),
            use_container_width=True, height=420)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    avg_aqi = df['aqi'].mean()
    max_aqi = df['aqi'].max()
    aqi_label, aqi_color, aqi_desc = get_aqi_category(avg_aqi)
    st.session_state.last_aqi = avg_aqi

    st.markdown("<div class='section-header animated-fade'>Real-Time Pollution Alerts</div>",
                unsafe_allow_html=True)

    recs = []
    if avg_aqi > 300:
        recs += ["Issue immediate public health emergency advisory",
                 "Mandate N95/FFP2 masks for all outdoor movement",
                 "Close schools, suspend outdoor events",
                 "Advise complete stay-indoors for vulnerable groups"]
    elif avg_aqi > 200:
        recs += ["Issue official air quality warning",
                 "Restrict outdoor activities for children & elderly",
                 "Limit strenuous exercise outdoors"]
    if dominant_source == "Vehicular":
        recs += ["Implement odd-even vehicle rationing",
                 "Enhance public transport frequency",
                 "Incentivise electric vehicles"]
    if dominant_source == "Industrial":
        recs += ["Enforce immediate emission controls",
                 "Conduct industrial compliance audit",
                 "Mandate cleaner fuel switch"]
    if dominant_source == "Agricultural":
        recs += ["Issue no-burning advisory to farmers",
                 "Deploy water tankers for road wetting"]
    if dominant_source == "Burning":
        recs += ["Deploy fire-watch teams in affected zones",
                 "Strict penalties for open waste burning"]
    if not recs:
        recs = ["Continue regular monitoring","Maintain current emission controls"]

    if avg_aqi > alert_threshold:
        st.markdown(f"""
        <div class='alert-critical'>
            ️ CRITICAL AIR QUALITY ALERT — {aqi_label.upper()} 
            <div style='font-size:17px;margin-top:12px;'>
                Avg AQI: <b>{avg_aqi:.1f}</b> &nbsp;|&nbsp;
                Peak AQI: <b>{max_aqi:.1f}</b> &nbsp;|&nbsp;
                Threshold: <b>{alert_threshold}</b> &nbsp;|&nbsp;
                {aqi_desc}
            </div>
            <div style='font-size:15px;margin-top:8px;'>
                Source: {emoji} {dominant_source} &nbsp;|&nbsp;
                Confidence: {avg_confidence*100:.1f}%
            </div>
        </div>""", unsafe_allow_html=True)

        alert_entry = {
            'Timestamp':   datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'City':        selected_city,
            'Avg AQI':     round(avg_aqi,1),
            'Max AQI':     round(max_aqi,1),
            'Category':    aqi_label,
            'Source':      dominant_source,
            'Confidence %': round(avg_confidence*100,1)
        }
        st.session_state.alert_history.append(alert_entry)

        col_em, col_sms = st.columns(2)
        with col_em:
            if enable_email:
                if email_to and email_sender and email_password:
                    if not st.session_state.email_sent:
                        n_anom = len(df[df.get('anomaly',-1)==-1]) if 'anomaly' in df.columns else 0
                        html = build_email_body(
                            selected_city, avg_aqi, max_aqi, aqi_label,
                            aqi_color, dominant_source, aqi_desc, n_anom, recs)
                        ok, msg = send_real_email(
                            email_to,
                            f"EnviroScan Alert — {selected_city} | AQI {avg_aqi:.0f}",
                            html, smtp_host, smtp_port, email_sender, email_password)
                        if ok:
                            st.success(f" {msg} → {email_to}")
                            st.session_state.email_sent = True
                        else:
                            st.error(f" Email failed: {msg}")
                    else:
                        st.info(" Email already sent this session (click Reset Alert State in sidebar)")
                else:
                    st.warning(" Fill recipient email, sender Gmail & App Password to send.")

        with col_sms:
            if enable_sms:
                if sms_phone and sms_api_key:
                    if not st.session_state.sms_sent:
                        sms_text = build_sms_text(selected_city, avg_aqi, aqi_label, dominant_source)
                        ok, msg = send_real_sms(sms_phone, sms_text, sms_api_key)
                        if ok:
                            st.success(f" {msg}")
                            st.session_state.sms_sent = True
                        else:
                            st.error(f" SMS failed: {msg}")
                    else:
                        st.info(" SMS already sent this session (click Reset Alert State in sidebar)")
                else:
                    st.warning(" Fill phone number & Fast2SMS API key to send.")

    elif avg_aqi > alert_threshold * 0.8:
        st.markdown(f"""
        <div class='alert-warning'>
            ️ Air Quality Warning — {aqi_label} — Avg AQI: {avg_aqi:.1f}
            (Approaching threshold of {alert_threshold})
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='alert-success'>
             Air Quality within Safe Limits — {aqi_label} — Avg AQI: {avg_aqi:.1f}
        </div>""", unsafe_allow_html=True)

    if st.session_state.alert_history:
        with st.expander(f" Alert History — {len(st.session_state.alert_history)} events fired",
                         expanded=False):
            ah_df = pd.DataFrame(st.session_state.alert_history)
            st.dataframe(ah_df.style.background_gradient(subset=['Avg AQI'], cmap='Reds'),
                         use_container_width=True)
        if st.button(" Clear Alert History + Reset Email/SMS"):
            st.session_state.alert_history = []
            st.session_state.email_sent    = False
            st.session_state.sms_sent      = False
            st.rerun()

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header animated-fade'>Executive Dashboard</div>",
                unsafe_allow_html=True)

    worst_city     = (full_df.groupby('city_name')['aqi'].mean().idxmax()
                      if 'city_name' in full_df.columns else "N/A")
    critical_count = int((df['aqi']>300).sum())
    avg_health     = df['health_index'].mean() if 'health_index' in df.columns else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    cards = [
        (c1,"AQI Status",   aqi_label[:15],    f"Index: {avg_aqi:.1f}",         aqi_desc),
        (c2,"Dominant Src", emoji,             dominant_source,                  "AI Prediction"),
        (c3,"Most Affected","",              worst_city,                       "Highest avg AQI"),
        (c4,"AI Confidence",f"{avg_confidence*100:.0f}%","Model Accuracy",      f"{high_conf_count:,} high-confidence"),
        (c5,"Critical Cases",str(critical_count),"AQI > 300",                   "Emergency level"),
    ]
    for col,lbl,val,sub,desc in cards:
        col.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{lbl}</div>
            <div class='metric-value' style='font-size:44px;'>{val}</div>
            <div class='metric-subtitle'>{sub}</div>
            <div class='metric-description'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Average Pollutant Concentrations")
    polls = ['PM2.5','PM10','NO2','SO2','CO','O3']
    avgs  = [abs(df[p].mean()) for p in polls]
    fig_sub = go.Figure(go.Bar(
        x=polls, y=avgs,
        marker_color=[POLL_COLORS[p] for p in polls],
        text=[f"{v:.1f}" for v in avgs], textposition='outside'))
    fig_sub.update_layout(
        plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=320,
        yaxis=dict(title="Avg Concentration (µg/m³)", gridcolor='#e0e0e0'),
        margin=dict(t=20,b=20))
    st.plotly_chart(fig_sub, use_container_width=True, config={'responsive': True})

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header animated-fade'>Pollutant Trend Analysis</div>",
                unsafe_allow_html=True)

    sel_poll = st.multiselect(
        "Select Pollutants to Visualize",
        ["PM2.5","PM10","NO2","SO2","CO","O3"],
        default=["PM2.5","NO2","CO"])

    tab1,tab2,tab3,tab4 = st.tabs(["Hourly Trends","Daily Trends","Day/Hour Heatmap","Radar"])

    with tab1:
        if sel_poll and 'hour' in df.columns:
            hourly = df.groupby('hour')[sel_poll].mean().reset_index()
            fig_h  = go.Figure()
            for p in sel_poll:
                fig_h.add_trace(go.Scatter(
                    x=hourly['hour'], y=hourly[p],
                    mode='lines+markers', name=p,
                    line=dict(color=POLL_COLORS.get(p,'#2196F3'), width=3),
                    marker=dict(size=9, line=dict(width=2, color='white')),
                    hovertemplate=f'<b>{p}</b><br>Hour:%{{x}}:00<br>Conc:%{{y:.2f}} µg/m³<extra></extra>'))
            fig_h.update_layout(
                title=f"Hourly Average — {selected_city}",
                xaxis=dict(title="Hour of Day", gridcolor='#e0e0e0',
                           tickmode='linear', dtick=2),
                yaxis=dict(title="Concentration (µg/m³)", gridcolor='#e0e0e0'),
                plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                height=500, hovermode='x unified', legend=dict(orientation='h', y=-0.15))
            st.plotly_chart(fig_h, use_container_width=True, config={'responsive': True})

            if sel_poll:
                peak_h = df.groupby('hour')['PM2.5'].mean().idxmax()
                st.markdown(f"<div class='info-box'> <b>Peak PM2.5 Hour:</b> "
                            f"{peak_h:02d}:00 — Consider targeted interventions at this time</div>",
                            unsafe_allow_html=True)
        else:
            st.info("Select pollutants above and ensure 'hour' column exists.")

    with tab2:
        if sel_poll and 'timestamp' in df.columns:
            daily = df.groupby(df['timestamp'].dt.date)[sel_poll].mean().reset_index()
            daily.columns = ['date'] + sel_poll
            fig_d = px.area(daily, x='date', y=sel_poll,
                             title=f"Daily Trend — {selected_city}",
                             color_discrete_map=POLL_COLORS)
            fig_d.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=470,
                                xaxis=dict(title='Date'), yaxis=dict(title='Concentration (µg/m³)'))
            st.plotly_chart(fig_d, use_container_width=True, config={'responsive': True})

            if show_forecast and len(daily) > 7:
                st.markdown("#### 📡 7-Day Rolling Trend (Forecast Basis)")
                daily['PM2.5_7d_avg'] = daily['PM2.5'].rolling(7, min_periods=1).mean()
                fig_fc = go.Figure()
                fig_fc.add_trace(go.Scatter(x=daily['date'], y=daily['PM2.5'],
                    mode='lines', name='Actual PM2.5', line=dict(color='#f44336', width=2)))
                fig_fc.add_trace(go.Scatter(x=daily['date'], y=daily['PM2.5_7d_avg'],
                    mode='lines', name='7-Day Rolling Avg',
                    line=dict(color='#2196F3', width=3, dash='dash')))
                fig_fc.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=380,
                    xaxis=dict(title='Date',gridcolor='#e0e0e0'),
                    yaxis=dict(title='PM2.5 (µg/m³)',gridcolor='#e0e0e0'))
                st.plotly_chart(fig_fc, use_container_width=True, config={'responsive': True})

    with tab3:
        if show_heatmap and 'hour' in df.columns and 'day_of_week' in df.columns:
            hm = df.groupby(['hour','day_of_week'])['PM2.5'].mean().reset_index()
            pv = hm.pivot(index='day_of_week', columns='hour', values='PM2.5')
            days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
            fig_hm = go.Figure(go.Heatmap(
                z=pv.values,
                x=pv.columns,
                y=[days[i] for i in pv.index],
                colorscale='RdYlGn_r', showscale=True,
                hovertemplate='Day:%{y}<br>Hour:%{x}<br>PM2.5:%{z:.1f} µg/m³<extra></extra>'))
            fig_hm.update_layout(
                title=f"PM2.5 Concentration — Day vs Hour Heatmap ({selected_city})",
                xaxis=dict(title='Hour of Day',tickmode='linear',dtick=2),
                yaxis=dict(title='Day of Week'),
                plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=440)
            st.plotly_chart(fig_hm, use_container_width=True, config={'responsive': True})
        else:
            st.info("Heatmap needs 'hour' and 'day_of_week' columns in data.")

    with tab4:
        if show_radar:
            r_vals = [abs(df[p].mean()) for p in ['PM2.5','PM10','NO2','SO2','CO','O3']]
        
            mx = max(r_vals) if max(r_vals)>0 else 1
            r_norm = [v/mx*100 for v in r_vals]
            fig_r = go.Figure()
            fig_r.add_trace(go.Scatterpolar(
                r=r_norm,
                theta=['PM2.5','PM10','NO2','SO2','CO','O3'],
                fill='toself',
                fillcolor='rgba(33,150,243,0.25)',
                line=dict(color='#2196F3', width=3),
                name='Current Levels (normalised)'))
            fig_r.update_layout(
                polar=dict(radialaxis=dict(visible=True,gridcolor='#e0e0e0',range=[0,100]),
                           angularaxis=dict(gridcolor='#e0e0e0'), bgcolor='#ffffff'),
                paper_bgcolor='#ffffff', height=460,
                title=f"Multi-Pollutant Radar — {selected_city} (% of max concentration)")
            st.plotly_chart(fig_r, use_container_width=True, config={'responsive': True})
       
            radar_df = pd.DataFrame({'Pollutant':['PM2.5','PM10','NO2','SO2','CO','O3'],
                                     'Avg Conc (µg/m³)': [round(v,2) for v in r_vals],
                                     'Normalised %':     [round(v,1) for v in r_norm]})
            st.dataframe(radar_df, use_container_width=True, hide_index=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header animated-fade'>Pollution Source Distribution</div>",
                unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        src = df['predicted_source'].value_counts().reset_index()
        src.columns = ['Source','Count']
        fig_pie = go.Figure(go.Pie(
            labels=src['Source'], values=src['Count'], hole=0.45,
            marker=dict(colors=['#2196F3','#4CAF50','#FF9800','#f44336','#9C27B0'],
                        line=dict(color='#ffffff',width=3)),
            textinfo='label+percent',
            textfont=dict(size=14,color='#1a1a1a'),
            hovertemplate='<b>%{label}</b><br>Count:%{value:,}<br>Share:%{percent}<extra></extra>'))
        fig_pie.update_layout(title=f"Predicted Source Mix — {selected_city}",
                               paper_bgcolor='#ffffff', height=450)
        st.plotly_chart(fig_pie, use_container_width=True, config={'responsive': True})

    with c2:
        if 'hour_category' in df.columns:
            std = df.groupby(['hour_category','predicted_source']).size().reset_index(name='count')
            fig_s = px.bar(std, x='hour_category', y='count', color='predicted_source',
                           title=f"Source by Time of Day — {selected_city}",
                           color_discrete_sequence=['#2196F3','#4CAF50','#FF9800','#f44336','#9C27B0'],
                           barmode='stack',
                           labels={'hour_category':'Time of Day','count':'Records'})
            fig_s.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=450)
            st.plotly_chart(fig_s, use_container_width=True, config={'responsive': True})
        else:
     
            if 'month' in df.columns:
                sm = df.groupby(['month','predicted_source']).size().reset_index(name='count')
                fig_sm = px.bar(sm, x='month', y='count', color='predicted_source',
                                title="Source Distribution by Month", barmode='group',
                                color_discrete_sequence=['#2196F3','#4CAF50','#FF9800','#f44336','#9C27B0'])
                fig_sm.update_layout(plot_bgcolor='#ffffff',paper_bgcolor='#ffffff',height=450)
                st.plotly_chart(fig_sm, use_container_width=True, config={'responsive': True})

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header animated-fade'>City Comparison Mode</div>",
                unsafe_allow_html=True)

    all_cities = sorted(full_df['city_name'].dropna().unique().tolist())
    if len(all_cities) >= 2:
        cmp_sel = st.multiselect("Select cities to compare",
                                  all_cities,
                                  default=all_cities[:min(5,len(all_cities))])
        if len(cmp_sel) >= 2:
         
            rows = []
            for city in cmp_sel:
                c = full_df[full_df['city_name']==city]
             
                Xc = c.copy()
                Xc.drop(columns=[col for col in drop if col in Xc.columns], inplace=True, errors='ignore')
                for col in MODEL_FEATURES:
                    if col not in Xc.columns: Xc[col]=0
                Xc = Xc[MODEL_FEATURES].apply(pd.to_numeric,errors='coerce').fillna(0)
                src_mode = model.predict(Xc)
                rows.append({
                    'City':             city,
                    'Records':          len(c),
                    'Avg AQI':          round(c['aqi'].mean(),1),
                    'Max AQI':          round(c['aqi'].max(),1),
                    'Avg PM2.5':        round(c['PM2.5'].mean(),1),
                    'Avg NO2':          round(c['NO2'].mean(),1),
                    'Avg SO2':          round(c['SO2'].mean(),1),
                    'Avg Wind (m/s)':   round(c['wind_speed'].mean(),2),
                    'Critical (>300)':  int((c['aqi']>300).sum()),
                    'Dom Source':       pd.Series(src_mode).mode()[0],
                })
            cmp_df = pd.DataFrame(rows)

            fig_cmp = go.Figure()
            for metric,color in [('Avg AQI','#2196F3'),('Avg PM2.5','#f44336'),('Avg NO2','#9C27B0')]:
                fig_cmp.add_trace(go.Bar(name=metric, x=cmp_df['City'], y=cmp_df[metric],
                                          marker_color=color,
                                          text=cmp_df[metric], textposition='outside'))
            fig_cmp.update_layout(barmode='group', title="City-wise Comparison",
                                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=460,
                                   xaxis=dict(title='City'),
                                   yaxis=dict(title='Level / Index', gridcolor='#e0e0e0'))
            st.plotly_chart(fig_cmp, use_container_width=True, config={'responsive': True})

          
            num_cols = ['Avg AQI','Max AQI','Avg PM2.5','Avg NO2','Avg SO2']
            st.dataframe(
                cmp_df.style.background_gradient(subset=['Avg AQI','Avg PM2.5'],cmap='YlOrRd')
                            .format({c:'{:.1f}' for c in num_cols}),
                use_container_width=True)

            st.markdown("#### Multi-City Radar Comparison")
            fig_cr = go.Figure()
            poll_cats = ['PM2.5','PM10','NO2','SO2','CO','O3']
            c_colors  = ['#2196F3','#f44336','#FF9800','#4CAF50','#9C27B0','#00BCD4','#607D8B','#795548']
            for i,city in enumerate(cmp_sel[:8]):
                cv = full_df[full_df['city_name']==city]
                r  = [abs(cv[p].mean()) for p in poll_cats]
                mx = max(r) if max(r)>0 else 1
                fig_cr.add_trace(go.Scatterpolar(
                    r=[v/mx*100 for v in r], theta=poll_cats,
                    fill='toself', name=city, opacity=0.6,
                    line=dict(color=c_colors[i%len(c_colors)], width=2)))
            fig_cr.update_layout(
                polar=dict(radialaxis=dict(visible=True,gridcolor='#e0e0e0',range=[0,100]),
                           angularaxis=dict(gridcolor='#e0e0e0'), bgcolor='#ffffff'),
                paper_bgcolor='#ffffff', height=500, title="Multi-City Pollutant Radar")
            st.plotly_chart(fig_cr, use_container_width=True, config={'responsive': True})
    else:
        st.info("City comparison needs at least 2 cities in the dataset.")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    

    st.markdown("<div class='section-header animated-fade'>Advanced Geospatial Intelligence</div>",
                unsafe_allow_html=True)

    map_mode = st.radio(
        "Map Visualization Mode",
        ["Heatmap Overlay","Risk Zone Markers","Cluster Analysis","Multi-Layer View"],
        horizontal=True)
    

    geo = df[['latitude','longitude']].dropna()
    if len(geo) > 0:
        m = folium.Map(location=[geo['latitude'].mean(), geo['longitude'].mean()],
                       zoom_start=6, tiles='OpenStreetMap', control_scale=True)

        if "Heatmap" in map_mode:
            HeatMap(df[['latitude','longitude','PM2.5']].dropna().values.tolist(),
                    radius=20, blur=28, max_zoom=13,
                    gradient={0.0:'blue',0.3:'cyan',0.5:'lime',0.7:'yellow',1.0:'red'},
                    min_opacity=0.4).add_to(m)

        elif "Risk Zone" in map_mode:
            for _,row in df.dropna(subset=['latitude','longitude']).head(200).iterrows():
                cat,col,_ = get_aqi_category(row['aqi'])
                ic = 'green' if row['aqi']<=100 else 'orange' if row['aqi']<=200 else 'red'
                popup_html = (f"<div style='width:210px;font-family:Arial;font-size:13px;'>"
                              f"<b style='color:{col};'>{row.get('city_name','—')}</b><br>"
                              f"AQI: <b>{row['aqi']:.1f}</b> ({cat})<br>"
                              f"PM2.5: {row['PM2.5']:.1f} µg/m³<br>"
                              f"Source: {row.get('predicted_source','—')}<br>"
                              f"Conf: {row.get('confidence',0)*100:.1f}%<br>"
                              f"Temp: {row.get('temperature',0):.1f}°C | "
                              f"Wind: {row.get('wind_speed',0):.1f} m/s</div>")
                folium.Marker(
                    [row['latitude'],row['longitude']],
                    popup=folium.Popup(popup_html,max_width=240),
                    tooltip=f"{row.get('city_name','?')}: {cat} ({row['aqi']:.0f})",
                    icon=folium.Icon(color=ic,icon='info-sign')).add_to(m)

        elif "Cluster" in map_mode:
            DBSCAN(eps=0.08,min_samples=20).fit(geo)
            mc = MarkerCluster(name="Pollution Stations",overlay=True,control=True).add_to(m)
            for _,row in df.dropna(subset=['latitude','longitude']).head(400).iterrows():
                cat,col,_ = get_aqi_category(row['aqi'])
                folium.CircleMarker(
                    [row['latitude'],row['longitude']], radius=7,
                    popup=f"{row.get('city_name','?')}: AQI {row['aqi']:.1f} — {cat}",
                    tooltip=f"{row.get('city_name','?')}: {cat}",
                    color=col, fill=True, fillColor=col, fillOpacity=0.7, weight=2).add_to(mc)

        else:  
            fg_heat = folium.FeatureGroup(name="PM2.5 Heatmap",show=True)
            HeatMap(df[['latitude','longitude','PM2.5']].dropna().values.tolist(),
                    radius=16,blur=22).add_to(fg_heat)
            fg_heat.add_to(m)
            fg_risk = folium.FeatureGroup(name="Risk Markers",show=True)
            for _,row in df.dropna(subset=['latitude','longitude']).head(200).iterrows():
                cat,col,_ = get_aqi_category(row['aqi'])
                folium.CircleMarker(
                    [row['latitude'],row['longitude']], radius=6,
                    popup=f"{row.get('city_name','?')}: {cat}",
                    color=col,fill=True,fillOpacity=0.65).add_to(fg_risk)
            fg_risk.add_to(m)
            fg_mc = folium.FeatureGroup(name="Station Clusters",show=False)
            mc2 = MarkerCluster().add_to(fg_mc)
            for _,row in df.dropna(subset=['latitude','longitude']).head(400).iterrows():
                cat,col,_ = get_aqi_category(row['aqi'])
                folium.Marker(
                    [row['latitude'],row['longitude']],
                    tooltip=f"{row.get('city_name','?')}: {row['aqi']:.0f}",
                    icon=folium.Icon(color='blue',icon='cloud')).add_to(mc2)
            fg_mc.add_to(m)
            folium.LayerControl().add_to(m)

        Draw(export=True, filename='pollution_zones.geojson', position='topleft').add_to(m)
        MeasureControl(position='bottomleft', primary_length_unit='kilometers').add_to(m)
        MiniMap(toggle_display=True, position='bottomright').add_to(m)
        LocateControl(auto_start=False).add_to(m)
        Fullscreen(position='topright').add_to(m)

        st.markdown("<div class='map-container'>", unsafe_allow_html=True)
        st_folium(m, width=1400, height=680)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='info-box'>
            ️ <b>Map Tools Available:</b> Draw zones (top-left) • Measure distances (bottom-left) •
            Locate your position • Toggle layers (Multi-Layer mode) • Full-screen view (top-right)
        </div>""", unsafe_allow_html=True)
    else:
        st.warning("No valid latitude/longitude data to render map.")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if show_3d and 'hour' in df.columns and 'day' in df.columns:
        st.markdown("<div class='section-header animated-fade'>3D Pollution Dynamics</div>",
                    unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        with c1:
            piv = (df.groupby(['hour','day'])['PM2.5'].mean().reset_index()
                     .pivot(index='hour',columns='day',values='PM2.5'))
            fig_surf = go.Figure(go.Surface(
                z=piv.values, x=piv.columns, y=piv.index,
                colorscale='Jet', showscale=True,
                hovertemplate='Day:%{x}<br>Hour:%{y}<br>PM2.5:%{z:.1f}<extra></extra>'))
            fig_surf.update_layout(
                title=f"3D PM2.5 Surface — {selected_city}",
                scene=dict(xaxis_title='Day',yaxis_title='Hour',
                           zaxis_title='PM2.5 µg/m³',bgcolor='#ffffff'),
                paper_bgcolor='#ffffff', height=520)
            st.plotly_chart(fig_surf, use_container_width=True, config={'responsive': True})

        with c2:
            samp = df.sample(min(600,len(df)), random_state=42)
            fig_sc3 = go.Figure(go.Scatter3d(
                x=samp['PM2.5'], y=samp['NO2'], z=samp['SO2'],
                mode='markers',
                marker=dict(size=5,color=samp['aqi'],colorscale='Jet',
                            showscale=True,colorbar=dict(title="AQI"),opacity=0.8,
                            line=dict(color='#ffffff',width=0.5)),
                text=samp.get('city_name',pd.Series(['?']*len(samp))),
                hovertemplate=('<b>%{text}</b><br>PM2.5:%{x:.1f}'
                               '<br>NO2:%{y:.1f}<br>SO2:%{z:.1f}<extra></extra>')))
            fig_sc3.update_layout(
                title="3D Pollutant Correlation Space (coloured by AQI)",
                scene=dict(xaxis_title='PM2.5',yaxis_title='NO2',
                           zaxis_title='SO2',bgcolor='#ffffff'),
                paper_bgcolor='#ffffff', height=520)
            st.plotly_chart(fig_sc3, use_container_width=True, config={'responsive': True})

        if show_corr:
            st.markdown("#### Pollutant Correlation Matrix")
            corr_cols = [c for c in ['PM2.5','PM10','NO2','SO2','CO','O3',
                                      'temperature','humidity','wind_speed'] if c in df.columns]
            corr_m = df[corr_cols].corr()
            fig_corr = go.Figure(go.Heatmap(
                z=corr_m.values, x=corr_m.columns, y=corr_m.columns,
                colorscale='RdBu', zmid=0, showscale=True,
                text=[[f"{v:.2f}" for v in row] for row in corr_m.values],
                texttemplate='%{text}',
                hovertemplate='%{y} vs %{x}: %{z:.2f}<extra></extra>'))
            fig_corr.update_layout(
                title="Pearson Correlation — Pollutants & Meteorology",
                plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=480)
            st.plotly_chart(fig_corr, use_container_width=True, config={'responsive': True})
            st.markdown("""
            <div class='info-box'>
                 <b>Correlation Guide:</b> +1.0 = perfect positive correlation |
                0 = no relationship | -1.0 = perfect negative correlation.
                High PM2.5/PM10 correlation indicates common coarse-particle sources.
            </div>""", unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header animated-fade'>AI Anomaly Detection Engine</div>",
                unsafe_allow_html=True)

    feats = ['PM2.5','PM10','NO2','SO2','CO','O3']
    iso   = IsolationForest(contamination=0.02, n_estimators=200, random_state=42)
    df['anomaly']       = iso.fit_predict(df[feats])
    df['anomaly_score'] = iso.score_samples(df[feats])   # lower = more anomalous

    spikes = df[df['anomaly']==-1].copy()
    n_sp   = len(spikes)
    n_sev  = int((spikes['PM2.5']>250).sum()) if n_sp else 0
    asp    = round(spikes['PM2.5'].mean(),1)  if n_sp else 0
    maff   = (spikes['city_name'].mode()[0]   if n_sp and 'city_name' in spikes.columns else 'N/A')

    c1,c2,c3,c4 = st.columns(4)
    for col,num,lbl in [(c1,n_sp,"Anomalies Detected"),
                        (c2,n_sev,"Severe (PM2.5>250)"),
                        (c3,asp,"Avg Spike PM2.5"),
                        (c4,maff,"Most Affected City")]:
        col.markdown(f"""
        <div class='stat-box'>
            <div class='stat-number' style='font-size:{"38px" if str(num).replace(".","").isdigit() else "24px"};'>
                {num}
            </div>
            <div class='stat-label'>{lbl}</div>
        </div>""", unsafe_allow_html=True)

    if n_sp:
        spikes['severity']   = spikes['PM2.5'].apply(classify_severity)
        spikes['root_cause'] = spikes.apply(advanced_root_cause, axis=1)

        st.markdown("#### Anomaly Timeline")
        t_x = 'timestamp' if 'timestamp' in spikes.columns else spikes.index
        fig_tl = px.scatter(
            spikes.sort_values('timestamp') if 'timestamp' in spikes.columns else spikes,
            x=t_x, y='PM2.5', color='predicted_source',
            size='confidence' if 'confidence' in spikes.columns else None,
            size_max=18,
            hover_data=[c for c in ['city_name','severity','root_cause','aqi'] if c in spikes.columns],
            color_discrete_sequence=['#2196F3','#f44336','#FF9800','#4CAF50','#9C27B0'],
            title=f"Pollution Spike Timeline — {selected_city}")
        fig_tl.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=460,
            xaxis=dict(title='Date/Time',gridcolor='#e0e0e0'),
            yaxis=dict(title='PM2.5 Level (µg/m³)',gridcolor='#e0e0e0'))
        st.plotly_chart(fig_tl, use_container_width=True, config={'responsive': True})

        st.markdown("####  Anomaly Score Distribution")
        fig_asd = px.histogram(df, x='anomaly_score', nbins=60,
                               color='anomaly',
                               color_discrete_map={1:'#4CAF50',-1:'#f44336'},
                               labels={'anomaly_score':'Anomaly Score','anomaly':'Class'},
                               title="Normal vs Anomalous Score Distribution")
        fig_asd.update_layout(plot_bgcolor='#ffffff',paper_bgcolor='#ffffff',height=360)
        st.plotly_chart(fig_asd, use_container_width=True, config={'responsive': True})

        st.markdown("#### Top 10 Critical Pollution Events")
        dcols = [c for c in ['city_name','timestamp','PM2.5','PM10','NO2',
                              'predicted_source','severity','confidence','root_cause','aqi']
                 if c in spikes.columns]
        top10 = spikes.sort_values('PM2.5', ascending=False).head(10).copy()

        if 'timestamp' in top10.columns:
            top10['timestamp'] = pd.to_datetime(top10['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        fmt   = {k:v for k,v in {'PM2.5':'{:.1f}','PM10':'{:.1f}',
                                   'NO2':'{:.1f}','confidence':'{:.1%}',
                                   'aqi':'{:.1f}'}.items() if k in dcols}
        st.dataframe(
            top10[dcols].style.background_gradient(subset=['PM2.5'], cmap='Reds').format(fmt),
            use_container_width=True, height=400)

        with st.expander(" Full Anomaly Investigation Log", expanded=False):
    
            spikes_log = spikes[dcols].copy()
            if 'timestamp' in spikes_log.columns:
                spikes_log['timestamp'] = pd.to_datetime(spikes_log['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(spikes_log.reset_index(drop=True),
                         use_container_width=True, height=500)
    else:
        st.markdown("<div class='success-box'> No significant pollution anomalies detected in selected data.</div>",
                    unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


    st.markdown("<div class='section-header animated-fade'>Automatic Probable Cause Analysis</div>",
                unsafe_allow_html=True)

    causes = []
    ws_mean = df['wind_speed'].mean() if 'wind_speed' in df.columns else 5
    rh_mean = df['humidity'].mean()   if 'humidity'   in df.columns else 50
    tp_mean = df['temperature'].mean()if 'temperature' in df.columns else 25

    if ws_mean < 1.5:
        causes.append("Near-zero wind speed causing severe pollutant trapping")
    elif ws_mean < 2.5:
        causes.append("Low wind speed limiting pollutant dispersion")
    if rh_mean > 78:
        causes.append("High relative humidity (>78%) increasing fine-particle suspension")
    if tp_mean < 15:
        causes.append("Low ambient temperature driving temperature-inversion layering")
    if dominant_source == "Vehicular":
        causes.append("Traffic emission patterns confirm vehicular dominance")
    if dominant_source == "Industrial":
        causes.append("Combustion signatures match industrial emission profiles")
    if dominant_source == "Agricultural":
        causes.append("Seasonal crop-residue burning or dust transport active")
    if dominant_source == "Burning":
        causes.append("Open-waste or biomass combustion detected")
    if dominant_source == "Natural":
        causes.append("Natural sources (dust storms, pollen) contributing")
    if 'hour' in df.columns:
        pk = df.groupby('hour')['PM2.5'].mean().idxmax()
        causes.append(f"Peak pollution hour identified: {pk:02d}:00 — targeted intervention window")
    if 'is_weekend' in df.columns:
        we = df[df['is_weekend']==1]['PM2.5'].mean()
        wd = df[df['is_weekend']==0]['PM2.5'].mean()
        if we < wd*0.80:
            causes.append("~20%+ weekend reduction confirms weekday traffic/industry as major driver")
        elif we > wd*1.20:
            causes.append(" Weekend spike detected — investigate construction/leisure burning")
    if 'distance_to_road_km' in df.columns and df['distance_to_road_km'].mean() < 1:
        causes.append("Monitoring sites close to road (<1 km) — direct vehicular exposure")
    if not causes:
        causes.append("🔍 Mixed urban emission pattern — multi-factor analysis required")

    st.markdown("<div class='feature-highlight'>AI-Identified Probable Drivers of Elevated Pollution:</div>",
                unsafe_allow_html=True)
    for c in causes:
        st.markdown(f"<div class='info-box'>{c}</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header animated-fade'>AI Insights & Policy Recommendations</div>",
                unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("####  Key Findings")
        findings = list(causes)
        findings.append(f"Average AQI: {avg_aqi:.1f} → {aqi_label}")
        findings.append(f"Model Confidence: {avg_confidence*100:.1f}%")
        findings.append(f"Anomaly Rate: {n_sp}/{len(df)} ({n_sp/len(df)*100:.1f}%)")
        findings.append(f"Health Index: {df['health_index'].mean():.2f} (weighted exposure)")
        if 'is_weekend' in df.columns:
            we = df[df['is_weekend']==1]['PM2.5'].mean()
            wd = df[df['is_weekend']==0]['PM2.5'].mean()
            findings.append(f"Weekday PM2.5: {wd:.1f} vs Weekend: {we:.1f}")
        for f in findings:
            st.markdown(f"<div class='info-box'>{f}</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("#### Data-Driven Policy Recommendations")
        for i,r in enumerate(recs[:12], 1):
            st.markdown(f"<div class='success-box'><b>{i}.</b> {r}</div>",
                        unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header animated-fade'>Export Environmental Reports</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='feature-highlight'>
         Official reports for environmental agencies, urban planners &amp; policy makers
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        if 'timestamp' in df.columns:
            daily_agg = df.groupby(df['timestamp'].dt.date).agg(
                Avg_PM25=('PM2.5','mean'), Avg_PM10=('PM10','mean'),
                Avg_NO2=('NO2','mean'),    Avg_SO2=('SO2','mean'),
                Avg_CO=('CO','mean'),      Avg_O3=('O3','mean'),
                Avg_AQI=('aqi','mean'),    Max_AQI=('aqi','max'),
                Avg_Temp=('temperature','mean'), Avg_Humidity=('humidity','mean'),
                Dom_Source=('predicted_source', lambda x: x.mode()[0] if len(x) else 'N/A'),
                Anomalies=('anomaly', lambda x: (x==-1).sum())
            ).reset_index()
            daily_agg.rename(columns={'timestamp':'Date'}, inplace=True)
            st.download_button(
                "Daily Report (CSV)",
                daily_agg.round(2).to_csv(index=False).encode(),
                f"daily_{selected_city}_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv", use_container_width=True)


    with c2:
        if 'timestamp' in df.columns:
            df['_week']  = df['timestamp'].dt.isocalendar().week
            df['_wyear'] = df['timestamp'].dt.isocalendar().year
            wk_agg = df.groupby(['_wyear','_week']).agg(
                Avg_PM25=('PM2.5','mean'), Avg_NO2=('NO2','mean'),
                Avg_AQI=('aqi','mean'),    Max_AQI=('aqi','max'),
                Dom_Source=('predicted_source',lambda x: x.mode()[0] if len(x) else 'N/A'),
                Anomalies=('anomaly',lambda x:(x==-1).sum())
            ).reset_index().rename(columns={'_wyear':'Year','_week':'Week_No'})
            st.download_button(
                "Weekly Report (CSV)",
                wk_agg.round(2).to_csv(index=False).encode(),
                f"weekly_{selected_city}_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv", use_container_width=True)


    with c3:
        if n_sp:
            acols = [c for c in ['city_name','timestamp','PM2.5','PM10','NO2',
                                  'predicted_source','severity','root_cause',
                                  'confidence','aqi','anomaly_score'] if c in spikes.columns]
          
            spikes_csv = spikes[acols].copy()
            if 'timestamp' in spikes_csv.columns:
                spikes_csv['timestamp'] = pd.to_datetime(spikes_csv['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            st.download_button(
                "Anomaly Report (CSV)",
                spikes_csv.round(3).to_csv(index=False).encode(),
                f"anomaly_{selected_city}_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv", use_container_width=True)
        else:
            st.info("No anomalies to export")


    with c4:
        ts_min = str(df['timestamp'].min()) if 'timestamp' in df.columns else 'N/A'
        ts_max = str(df['timestamp'].max()) if 'timestamp' in df.columns else 'N/A'
        src_breakdown = df['predicted_source'].value_counts().to_string()
        causes_text   = "\n".join(f"  • {c}" for c in causes)
        recs_text     = "\n".join(f"  {i}. {r}" for i,r in enumerate(recs[:12],1))
        summary = f"""
{'='*80}
               ENVIRONMENTAL ASSESSMENT REPORT
      EnviroScan Elite Pro — AI-Powered Intelligence Platform
{'='*80}
Report ID   : ENV-{datetime.now().strftime('%Y%m%d-%H%M%S')}
Generated   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Location    : {selected_city}
Period      : {ts_min}  →  {ts_max}
Total Recs  : {len(df):,}
Analyst     : AI Engine 

{'─'*80}
EXECUTIVE SUMMARY
{'─'*80}
Average AQI    : {avg_aqi:.1f}
Maximum AQI    : {max_aqi:.1f}
AQI Category   : {aqi_label}
Health Message : {aqi_desc}
Health Index   : {df['health_index'].mean():.2f} (PM2.5 40% | NO2 20% | SO2 20% | CO+O3 20%)

{'─'*80}
AI POLLUTION SOURCE ANALYSIS
{'─'*80}
Dominant Source     : {dominant_source}  {SOURCE_EMOJI.get(dominant_source,'')}
Average Confidence  : {avg_confidence*100:.1f}%
High-Conf Preds     : {high_conf_count:,} ({high_conf_count/len(df)*100:.1f}%)

Source Distribution:
{src_breakdown}

{'─'*80}
AVERAGE POLLUTANT CONCENTRATIONS (µg/m³)
{'─'*80}
PM2.5  : {df['PM2.5'].mean():.2f}   (Guideline: WHO ≤5 / NAAQS ≤60)
PM10   : {df['PM10'].mean():.2f}    (Guideline: WHO ≤15 / NAAQS ≤100)
NO2    : {df['NO2'].mean():.2f}     (Guideline: WHO ≤10 / NAAQS ≤40)
SO2    : {df['SO2'].mean():.2f}     (Guideline: WHO ≤40)
CO     : {df['CO'].mean():.2f}      (mg/m³)
O3     : {df['O3'].mean():.2f}      (Guideline: WHO ≤60)

{'─'*80}
METEOROLOGICAL CONDITIONS
{'─'*80}
Avg Temperature  : {df['temperature'].mean():.1f} °C
Avg Humidity     : {df['humidity'].mean():.1f} %
Avg Wind Speed   : {df['wind_speed'].mean():.2f} m/s

{'─'*80}
ANOMALY DETECTION SUMMARY
{'─'*80}
Total Anomalies    : {n_sp}
Severe Events      : {n_sev}  (PM2.5 > 250 µg/m³)
Most Affected City : {maff}
Avg Spike PM2.5    : {asp} µg/m³

{'─'*80}
AI-IDENTIFIED PROBABLE CAUSES
{'─'*80}
{causes_text}

{'─'*80}
DATA-DRIVEN POLICY RECOMMENDATIONS
{'─'*80}
{recs_text}

{'─'*80}
NATIONAL STANDARDS COMPLIANCE
{'─'*80}
PM2.5 vs NAAQS (60 µg/m³)  : {' Within limit' if df['PM2.5'].mean()<=60 else ' EXCEEDS NAAQS'}
PM10  vs NAAQS (100 µg/m³) : {' Within limit' if df['PM10'].mean()<=100  else ' EXCEEDS NAAQS'}
NO2   vs NAAQS (40 µg/m³)  : {' Within limit' if df['NO2'].mean()<=40    else ' EXCEEDS NAAQS'}

{'─'*80}
DISCLAIMER
{'─'*80}
This report is AI-generated for informational purposes.
Consult certified environmental scientists before regulatory action.
AI Confidence: {avg_confidence*100:.1f}% | Engine: IsolationForest + RandomForest

{'='*80}
        END OF REPORT — EnviroScan Elite Pro
{'='*80}
"""
        st.download_button(
            "Full Summary (TXT)",
            summary.strip(),
            f"report_{selected_city}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            "text/plain", use_container_width=True)

    if len(st.session_state.predictions_log) > 0:
        with st.expander(f"Analysis Session History ({len(st.session_state.predictions_log)} runs)",
                         expanded=False):
            st.dataframe(pd.DataFrame(st.session_state.predictions_log),
                         use_container_width=True)

    st.markdown(f"""
    <div style='text-align:center;padding:48px 20px;color:#5a6c7d;margin-top:30px;
                border-top:2px solid #e1e8ed;'>
        <p style='font-size:18px;font-weight:700;color:#1a1a1a;'>
             EnviroScan Elite Pro
        </p>
        <p style='font-size:14px;margin-top:8px;'>
            Real-time Monitoring &nbsp;•&nbsp; AI Source Prediction &nbsp;•&nbsp;
            Geospatial Intelligence &nbsp;•&nbsp; Anomaly Detection<br>
            City Comparison &nbsp;•&nbsp; Root Cause Analysis &nbsp;•&nbsp;
            Policy Recommendations &nbsp;•&nbsp; Full Report Export
        </p>
        <p style='font-size:12px;margin-top:14px;color:#94a3b8;'>
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} &nbsp;|&nbsp;
            Session analyses: {st.session_state.analysis_count} &nbsp;|&nbsp;
            Alerts fired: {len(st.session_state.alert_history)}
        </p>
    </div>""", unsafe_allow_html=True)
    
else:
    st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Title Glow */
.title {
    text-align:center;
    font-size:52px;
    font-weight:700;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation: fadeIn 1.5s ease-in-out;
}

/* Subtitle */
.subtitle {
    text-align:center;
    font-size:20px;
    color:#34495e;
    margin-bottom:30px;
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    border-radius:18px;
    padding:25px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition:0.4s;
}

.card:hover {
    transform: translateY(-10px) scale(1.03);
}

/* KPI Glow */
.kpi {
    text-align:center;
    padding:20px;
    border-radius:15px;
    background: rgba(255,255,255,0.05);
    box-shadow:0 0 20px rgba(0,198,255,0.3);
}

/* CTA */
.cta {
    text-align:center;
    padding:18px;
    border-radius:12px;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    font-size:18px;
    margin-top:20px;
}

/* Animation */
@keyframes fadeIn {
    from {opacity:0; transform:translateY(30px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)


st.markdown("<div class='title'>EnviroScan Elite Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Environmental Intelligence & Pollution Analysis System</div>", unsafe_allow_html=True)


k1, k2, k3, k4 = st.columns(4)

k1.markdown("<div class='kpi'><h3>90+</h3><p>Model Accuracy</p></div>", unsafe_allow_html=True)
k2.markdown("<div class='kpi'><h3>10+</h3><p>Environmental Parameters</p></div>", unsafe_allow_html=True)
k3.markdown("<div class='kpi'><h3>98%</h3><p>AI Anomalies Detection</p></div>", unsafe_allow_html=True)
k4.markdown("<div class='kpi'><h3>4</h3><p>Map Modes and Reports</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

progress = st.progress(0)
for i in range(100):
    time.sleep(0.003)
    progress.progress(i + 1)

st.markdown("<div style='text-align:center;color:#00e5ff;'>SYSTEM INITIALIZED ✓</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)



c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class='card'>
    <h3 style='color:#00c6ff;'> Core Features</h3>
    <ul>
    <li>AI Source Prediction (5 classes)</li>
    <li>Real-time Email Alerts</li>
    <li>SMS Alert System</li>
    <li>Interactive Geo Maps</li>
    <li>Trend Forecasting</li>
    <li>Manual Simulation Input</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='card'>
    <h3 style='color:#00c6ff;'> Advanced Analytics</h3>
    <ul>
    <li>3D Pollution Surface</li>
    <li>Correlation Heatmaps</li>
    <li>Radar Multi-Metric Charts</li>
    <li>City Comparison Engine</li>
    <li>Anomaly Detection AI</li>
    <li>Export Engine (4 formats)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<div class='cta'>Upload Dataset from Sidebar to Begin Analysis</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


i1, i2 = st.columns(2)

with i1:
    st.markdown("""
    <div class='card'>
    <h3 style='color:#00c6ff;'> Email Setup</h3>
     <br>
    Gmail → 2FA → App Password → Paste in Sidebar
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class='card'>
      <h3 style='color:#00c6ff;'> SMS Setup</h3><br>
    Fast2SMS → API Key → Paste in Sidebar
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class='card' style='margin-top:20px;'>
  <h4 style='color:#00c6ff;'> Dataset Required</h4><br><br>
PM2.5, PM10, NO2, SO2, CO, O3, temperature, humidity,
wind_speed, latitude, longitude, city, year, month, day, hour
</div>
""", unsafe_allow_html=True)
   

if auto_refresh and uploaded_file:
    time.sleep(30)
    st.rerun()
