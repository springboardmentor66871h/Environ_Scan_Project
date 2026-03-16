import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")

st.title("🌍 EnviroScan – Air Pollution Intelligence Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../data/processed/final_labeled_dataset.csv")
    return df

df = load_data()

# Remove rows with missing coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("Filters")

# STATE FILTER
if "state" in df.columns:
    states = ["All"] + sorted(df["state"].dropna().unique())
    selected_state = st.sidebar.selectbox("Select State", states)
else:
    selected_state = "All"

# CITY FILTER
if "city" in df.columns:
    if selected_state != "All":
        cities = ["All"] + sorted(df[df["state"] == selected_state]["city"].dropna().unique())
    else:
        cities = ["All"] + sorted(df["city"].dropna().unique())
    selected_city = st.sidebar.selectbox("Select City", cities)
else:
    selected_city = "All"

# POLLUTION SOURCE FILTER
sources = sorted(df["pollution_source"].dropna().unique())
selected_sources = st.sidebar.multiselect("Pollution Source", sources, default=sources)

# SEARCH FILTER
search_location = st.sidebar.text_input(
    "Search Area / City / State",
    placeholder="Type Chennai, Delhi, Mumbai..."
)

# -------------------------
# APPLY FILTERS
# -------------------------
filtered_df = df.copy()

# Source filter
filtered_df = filtered_df[filtered_df["pollution_source"].isin(selected_sources)]

# State filter
if selected_state != "All" and "state" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["state"] == selected_state]

# City filter
if selected_city != "All" and "city" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["city"] == selected_city]

# Search filter
if search_location:
    search_location = search_location.lower()

    if "city" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["city"].str.lower().str.contains(search_location, na=False)
        ]

    if "state" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["state"].str.lower().str.contains(search_location, na=False)
        ]

# -------------------------
# CHECK DATA
# -------------------------
if filtered_df.empty:
    st.warning("No pollution data available for this location.")
    st.stop()

# -------------------------
# METRICS
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))
col2.metric("Average PM2.5", round(filtered_df["PM2.5"].mean(), 2))
col3.metric("Pollution Sources", filtered_df["pollution_source"].nunique())

st.divider()

# -------------------------
# MAP
# -------------------------
st.subheader("🗺 Pollution Map")

center_lat = filtered_df["Latitude"].mean()
center_lon = filtered_df["Longitude"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

# Heatmap
heat_data = filtered_df[["Latitude", "Longitude", "PM2.5"]].dropna().values.tolist()
HeatMap(heat_data).add_to(m)

# Source markers
color_map = {
    "Vehicular": "blue",
    "Industrial": "red",
    "Agricultural": "green",
    "Burning": "orange",
    "Natural": "purple"
}

for _, row in filtered_df.iterrows():

    color = color_map.get(row["pollution_source"], "gray")

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=6,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=f"""
        Source: {row['pollution_source']}<br>
        PM2.5: {row.get('PM2.5','N/A')}<br>
        NO2: {row.get('NO2','N/A')}<br>
        SO2: {row.get('SO2','N/A')}
        """
    ).add_to(m)

# High risk zones
threshold = 120
high_risk = filtered_df[filtered_df["PM2.5"] > threshold]

for _, row in high_risk.iterrows():

    folium.Circle(
        location=[row["Latitude"], row["Longitude"]],
        radius=5000,
        color="darkred",
        fill=True,
        fill_opacity=0.4,
        popup=f"High Risk Zone PM2.5={row['PM2.5']}"
    ).add_to(m)

st_folium(m, width=1100, height=550)

st.divider()

# -------------------------
# DATA TABLE
# -------------------------
st.subheader("📊 Pollution Data")

columns_to_show = [
    "Latitude",
    "Longitude",
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3",
    "pollution_source"
]

available_cols = [c for c in columns_to_show if c in filtered_df.columns]

st.dataframe(filtered_df[available_cols], use_container_width=True)

st.caption("EnviroScan – AI Based Pollution Source Detection Dashboard")