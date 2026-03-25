
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Pollution Monitor",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

CITY_MAPPING = {
    0: "Ahmedabad",
    1: "Bengaluru",
    2: "Chennai",
    3: "Delhi",
    4: "Hyderabad",
    5: "Jaipur",
    6: "Kolkata",
    7: "Lucknow",
    8: "Mumbai",
    9: "Pune"
}

CITY_COORDS = {
    "Ahmedabad": (23.0225, 72.5714),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Delhi": (28.6139, 77.2090),
    "Hyderabad": (17.3850, 78.4867),
    "Jaipur": (26.9124, 75.7873),
    "Kolkata": (22.5726, 88.3639),
    "Lucknow": (26.8467, 80.9462),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567)
}

st.markdown("""
<style>
    .main { padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .header { font-size: 2.5rem; font-weight: 800; color: #1a1a2e; }
    .subheader-custom { font-size: 1.1rem; color: #555; margin: 2rem 0 1rem 0; font-weight: 600; }
    .metric-box { background: white; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #1f77b4; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1f77b4; }
    .metric-label { font-size: 0.8rem; color: #666; text-transform: uppercase; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); }
</style>
""", unsafe_allow_html=True)

def convert_cities(df):
    """Convert city numbers (0-9) to city names"""
    if 'city' not in df.columns:
        df['city'] = 'Unknown'
    
    try:
        
        df['city'] = pd.to_numeric(df['city'], errors='coerce').map(CITY_MAPPING).fillna(df['city'])
        df['city'] = df['city'].fillna('Unknown')
    except:
        pass
    
    return df

def classify_risk(pm):
    """Classify pollution risk level"""
    if pm >= 150:
        return "Severe"
    elif pm >= 100:
        return "High"
    elif pm >= 60:
        return "Moderate"
    else:
        return "Low"

def get_risk_color(risk):
    """Get color for risk level"""
    colors = {
        'Low': '#2ca02c',
        'Moderate': '#ffbb78',
        'High': '#ff7f0e',
        'Severe': '#d62728'
    }
    return colors.get(risk, '#808080')

@st.cache_resource
def get_data():
    """Load or generate data - only once"""
    try:
        
        if os.path.exists('book2.csv'):
            df = pd.read_csv('book2.csv')
            st.success(" Data loaded from book2.csv")
        elif os.path.exists('data.csv'):
            df = pd.read_csv('data.csv')
            st.success(" Data loaded from data.csv")
        else:
            df = generate_data()
    except:
        df = generate_data()
    
   
    df = convert_cities(df)
    

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['date'].fillna(pd.Timestamp.now(), inplace=True)
    else:
        df['date'] = pd.date_range(start='2024-01-01', periods=len(df), freq='H')
    
  
    for col in ['PM2.5', 'PM10', 'NO2', 'SO2', 'pollution_source', 'latitude', 'longitude']:
        if col not in df.columns:
            df[col] = 0
    
    return df

def generate_data(n=2000):
    
    np.random.seed(42)
    data = []
    
    for _ in range(n):
        city_num = np.random.randint(0, 10)
        city_name = CITY_MAPPING[city_num]
        lat, lon = CITY_COORDS[city_name]
        
       
        lat += np.random.normal(0, 0.1)
        lon += np.random.normal(0, 0.1)
        
        
        pm25 = np.random.gamma(3, 20) + np.random.normal(0, 5)
        pm25 = max(10, min(300, pm25))
        
        sources = ['Industrial', 'Vehicular', 'Agricultural', 'Burning', 'Natural']
        source = np.random.choice(sources)
        
        if source == 'Industrial':
            pm25 *= 1.3
        elif source == 'Vehicular':
            pm25 *= 1.2
        elif source == 'Burning':
            pm25 *= 1.5
        
        data.append({
            'date': datetime.now() - timedelta(days=np.random.randint(0, 120)),
            'city': city_name,
            'latitude': lat,
            'longitude': lon,
            'PM2.5': pm25,
            'PM10': pm25 * 1.5,
            'NO2': np.random.gamma(2, 8),
            'SO2': np.random.gamma(2, 6),
            'pollution_source': source
        })
    
    return pd.DataFrame(data)


df = get_data()
df['risk_level'] = df['PM2.5'].apply(classify_risk)

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='color: #00d4ff; margin: 0;'> </h1>
        <h2 style='color: white; margin: 0.5rem 0 0 0;'>POLLUTION</h2>
        <h2 style='color: white; margin: 0;'>MONITOR</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
 
    page = st.radio(
        "Navigation",
        ["Dashboard", "Map", "Cities", "Analysis", "Export"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("**Filters**")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.slider(
        "Date Range",
        min_date, max_date,
        (min_date, max_date),
        format="YYYY-MM-DD"
    )
    
    cities = ['All'] + sorted(df['city'].unique().tolist())
    selected_city = st.selectbox("City", cities)
  
    sources = ['All'] + sorted(df['pollution_source'].unique().tolist())
    selected_source = st.selectbox("Source", sources)
    

    selected_risk = st.selectbox("Risk", ['All', 'Low', 'Moderate', 'High', 'Severe'])
    
    st.markdown("---")

    filtered_df = df[
        (df['date'].dt.date >= date_range[0]) & 
        (df['date'].dt.date <= date_range[1])
    ].copy()
    
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['city'] == selected_city]
    if selected_source != 'All':
        filtered_df = filtered_df[filtered_df['pollution_source'] == selected_source]
    if selected_risk != 'All':
        filtered_df = filtered_df[filtered_df['risk_level'] == selected_risk]
    

    st.markdown("**Dataset**")
    st.metric("Records", len(filtered_df))
    st.metric("Cities", filtered_df['city'].nunique())
    st.metric("Sources", filtered_df['pollution_source'].nunique())

if page == "Dashboard":
    st.markdown('<div class="header">Pollution Monitor Dashboard</div>', unsafe_allow_html=True)
    st.markdown("Real-time monitoring and analysis")
    
    st.markdown("---")
    st.markdown('<div class="subheader-custom">Key Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Avg PM2.5</div>
            <div class="metric-value">{filtered_df['PM2.5'].mean():.1f}</div>
            <div style="font-size: 0.75rem; color: #999;">μg/m³</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Avg PM10</div>
            <div class="metric-value">{filtered_df['PM10'].mean():.1f}</div>
            <div style="font-size: 0.75rem; color: #999;">μg/m³</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        severe = len(filtered_df[filtered_df['risk_level'] == 'Severe'])
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: #d62728;">
            <div class="metric-label">Severe</div>
            <div class="metric-value" style="color: #d62728;">{severe}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        high = len(filtered_df[filtered_df['risk_level'].isin(['High', 'Severe'])])
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: #ff7f0e;">
            <div class="metric-label">Critical</div>
            <div class="metric-value" style="color: #ff7f0e;">{high}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        low = len(filtered_df[filtered_df['risk_level'] == 'Low'])
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: #2ca02c;">
            <div class="metric-label">Healthy</div>
            <div class="metric-value" style="color: #2ca02c;">{low}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="subheader-custom">Risk Distribution</div>', unsafe_allow_html=True)
        risk_data = filtered_df['risk_level'].value_counts().reindex(['Low', 'Moderate', 'High', 'Severe'], fill_value=0)
        fig = go.Figure([go.Bar(
            x=risk_data.index,
            y=risk_data.values,
            marker=dict(color=['#2ca02c', '#ffbb78', '#ff7f0e', '#d62728']),
            text=risk_data.values,
            textposition='auto'
        )])
        fig.update_layout(
            title="Risk Levels",
            height=350,
            template="plotly_white",
            showlegend=False,
            xaxis_title="Risk Level",
            yaxis_title="Count"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="subheader-custom">Pollution Sources</div>', unsafe_allow_html=True)
        source_data = filtered_df['pollution_source'].value_counts()
        colors = {'Industrial': '#d62728', 'Vehicular': '#1f77b4', 'Agricultural': '#2ca02c', 'Burning': '#ff7f0e', 'Natural': '#17a2b8'}
        fig = go.Figure([go.Pie(
            labels=source_data.index,
            values=source_data.values,
            hole=0.3,
            marker=dict(colors=[colors.get(x, '#999') for x in source_data.index])
        )])
        fig.update_layout(
            title="Sources Distribution",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown('<div class="subheader-custom"> Trend Analysis</div>', unsafe_allow_html=True)
    
    try:
        trend = filtered_df.groupby(filtered_df['date'].dt.date)['PM2.5'].mean().reset_index()
        fig = go.Figure([go.Scatter(
            x=trend['date'],
            y=trend['PM2.5'],
            mode='lines+markers',
            line=dict(color='#1f77b4', width=3),
            name='PM2.5'
        )])
        fig.update_layout(
            title="PM2.5 Trend Over Time",
            height=350,
            xaxis_title="Date",
            yaxis_title="PM2.5 (μg/m³)",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Insufficient data for trend")

elif page == "Map":
    st.markdown('<div class="header">Interactive Pollution Map</div>', unsafe_allow_html=True)
    st.markdown("Heatmap, source markers & high-risk zones")
    
    st.markdown("---")
    
    if len(filtered_df) == 0:
        st.error("No data available")
    else:
      
        map_data = filtered_df.dropna(subset=['latitude', 'longitude', 'PM2.5']).copy()
        
        if len(map_data) == 0:
            st.error("No valid coordinates")
        else:
            try:
               
                center_lat = map_data['latitude'].mean()
                center_lon = map_data['longitude'].mean()
                
                m = folium.Map(
                    location=[center_lat, center_lon],
                    zoom_start=11,
                    tiles="OpenStreetMap",
                    prefer_canvas=True
                )
                
            
                max_pm = map_data['PM2.5'].max()
                heat_data = [
                    [row['latitude'], row['longitude'], row['PM2.5'] / max_pm]
                    for _, row in map_data.iterrows()
                ]
                
                HeatMap(
                    heat_data,
                    name="Heatmap",
                    radius=20,
                    blur=25,
                    gradient={0.0: 'green', 0.5: 'yellow', 0.75: 'orange', 1.0: 'red'},
                    max_zoom=15,
                    min_opacity=0.3
                ).add_to(m)
                
                
                marker_colors = {
                    'Industrial': 'red',
                    'Vehicular': 'blue',
                    'Agricultural': 'green',
                    'Burning': 'darkred',
                    'Natural': 'lightgreen'
                }
                
                marker_icons = {
                    'Industrial': 'industry',
                    'Vehicular': 'car',
                    'Agricultural': 'leaf',
                    'Burning': 'fire',
                    'Natural': 'tree'
                }
                
                for source in sorted(map_data['pollution_source'].unique()):
                    source_df = map_data[map_data['pollution_source'] == source]
                    fg = folium.FeatureGroup(name=f"{source} ({len(source_df)})")
                    
                    for _, row in source_df.iterrows():
                        color = marker_colors.get(source, 'gray')
                        icon = marker_icons.get(source, 'info-sign')
                        
                        popup = f"""<b>{row['pollution_source']}</b><br>
                        City: {row['city']}<br>
                        PM2.5: {row['PM2.5']:.1f}<br>
                        PM10: {row['PM10']:.1f}<br>
                        Risk: {row['risk_level']}<br>
                        Date: {row['date'].strftime('%Y-%m-%d')}"""
                        
                        folium.Marker(
                            location=[row['latitude'], row['longitude']],
                            popup=folium.Popup(popup, max_width=250),
                            icon=folium.Icon(color=color, icon=icon, prefix='fa'),
                            tooltip=f"{row['city']}"
                        ).add_to(fg)
                    
                    fg.add_to(m)
                
             
                high_risk = map_data[map_data['PM2.5'] > 150]
                if len(high_risk) > 0:
                    fg_risk = folium.FeatureGroup(name="High-Risk Zones (>150)")
                    
                    for _, row in high_risk.iterrows():
                        radius = (row['PM2.5'] / max_pm) * 500
                        folium.Circle(
                            location=[row['latitude'], row['longitude']],
                            radius=radius,
                            popup=f"CRITICAL<br>PM2.5: {row['PM2.5']:.1f}",
                            color='darkred',
                            fill=True,
                            fillColor='darkred',
                            fillOpacity=0.6,
                            weight=3
                        ).add_to(fg_risk)
                    
                    fg_risk.add_to(m)
                
              
                folium.LayerControl(collapsed=False).add_to(m)
                
             
                st_folium(m, width=1400, height=700)
                
                st.success(f"Map loaded: {len(heat_data)} points | {len(high_risk)} high-risk zones")
                
            
                st.markdown("---")
                st.markdown('<div class="subheader-custom">Export Map</div>', unsafe_allow_html=True)
                
                try:
                    map_html = m._repr_html_()
                    st.download_button(
                        "Download Map (HTML)",
                        map_html,
                        f"map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        "text/html"
                    )
                except:
                    st.info("Map export available")
                
     
                st.markdown("---")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Data Points", len(map_data))
                with col2:
                    st.metric("Cities", map_data['city'].nunique())
                with col3:
                    st.metric("Sources", map_data['pollution_source'].nunique())
                with col4:
                    st.metric("High-Risk", len(high_risk))
                with col5:
                    st.metric("Coverage km", f"{(map_data['latitude'].max()-map_data['latitude'].min())*111:.1f}")
            
            except Exception as e:
                st.error(f"Map Error: {str(e)}")

elif page == "Cities":
    st.markdown('<div class="header">City Analysis</div>', unsafe_allow_html=True)
    st.markdown("City-wise pollution comparison")
    
    st.markdown("---")
    
    city_stats = filtered_df.groupby('city').agg({
        'PM2.5': ['mean', 'max', 'min', 'count']
    }).round(2)
    
    city_stats.columns = ['Avg', 'Max', 'Min', 'Count']
    city_stats = city_stats.sort_values('Avg', ascending=False).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="subheader-custom">Average PM2.5</div>', unsafe_allow_html=True)
        fig = px.bar(
            city_stats,
            x='city',
            y='Avg',
            color='Avg',
            color_continuous_scale='Reds',
            title="Avg Pollution by City",
            text='Avg'
        )
        fig.update_layout(height=380, template="plotly_white", showlegend=False)
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="subheader-custom">Monitoring Locations</div>', unsafe_allow_html=True)
        fig = px.bar(
            city_stats,
            x='city',
            y='Count',
            color='Count',
            color_continuous_scale='Blues',
            title="Locations per City",
            text='Count'
        )
        fig.update_layout(height=380, template="plotly_white", showlegend=False)
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown('<div class="subheader-custom"> City Rankings</div>', unsafe_allow_html=True)
    
    rankings = city_stats[['city', 'Avg', 'Max', 'Min', 'Count']].copy()
    rankings.insert(0, 'Rank', range(1, len(rankings) + 1))
    
    st.dataframe(
        rankings.style.background_gradient(subset=['Avg'], cmap='Reds'),
        use_container_width=True,
        hide_index=True
    )

elif page == "Analysis":
    st.markdown('<div class="header">Pollution Analysis</div>', unsafe_allow_html=True)
    st.markdown("Statistical analysis & distributions")
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(filtered_df))
    with col2:
        st.metric("Unique Cities", filtered_df['city'].nunique())
    with col3:
        days = (filtered_df['date'].max() - filtered_df['date'].min()).days
        st.metric("Days", max(1, days))
    with col4:
        st.metric("Avg PM2.5", f"{filtered_df['PM2.5'].mean():.1f}")
    
    st.markdown("---")
    st.markdown('<div class="subheader-custom">Pollutant Distributions</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fig = go.Figure([go.Histogram(x=filtered_df['PM2.5'], nbinsx=30, marker_color='#ff7f0e')])
        fig.update_layout(title="PM2.5", height=300, template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure([go.Histogram(x=filtered_df['PM10'], nbinsx=30, marker_color='#1f77b4')])
        fig.update_layout(title="PM10", height=300, template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        fig = go.Figure([go.Histogram(x=filtered_df['NO2'], nbinsx=30, marker_color='#2ca02c')])
        fig.update_layout(title="NO2", height=300, template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        fig = go.Figure([go.Histogram(x=filtered_df['SO2'], nbinsx=30, marker_color='#d62728')])
        fig.update_layout(title="SO2", height=300, template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown('<div class="subheader-custom">Source-wise Analysis</div>', unsafe_allow_html=True)
    
    source_analysis = filtered_df.groupby('pollution_source')['PM2.5'].agg(['mean', 'max', 'count']).round(2).sort_values('mean', ascending=False)
    
    fig = px.bar(
        source_analysis.reset_index(),
        x='pollution_source',
        y='mean',
        color='mean',
        color_continuous_scale='Reds',
        title="Average PM2.5 by Source",
        text='mean'
    )
    fig.update_layout(height=350, template="plotly_white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Export":
    st.markdown('<div class="header">Data Export</div>', unsafe_allow_html=True)
    st.markdown("Download filtered data")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(filtered_df))
    with col2:
        st.metric("Cities", filtered_df['city'].nunique())
    with col3:
        st.metric("Sources", filtered_df['pollution_source'].nunique())
    
    st.markdown("---")
    st.markdown('<div class="subheader-custom">Data Preview</div>', unsafe_allow_html=True)
    
    st.dataframe(
        filtered_df[['date', 'city', 'PM2.5', 'PM10', 'pollution_source', 'risk_level']].head(100),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.markdown('<div class="subheader-custom">Download Options</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            f"pollution_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with col2:
        json_data = filtered_df.to_json(orient='records', date_format='iso')
        st.download_button(
            "Download JSON",
            json_data,
            f"pollution_{datetime.now().strftime('%Y%m%d')}.json",
            "application/json"
        )

st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #999; font-size: 0.85rem; padding: 2rem 0;'>
    <p>s Pollution Monitoring Dashboard | All Features Working <</<p<>
    <p>Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
