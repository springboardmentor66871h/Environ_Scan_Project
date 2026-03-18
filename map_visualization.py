import folium
import pandas as pd
from folium.plugins import HeatMap

# Load dataset
data = pd.read_csv("C:/projects/AI_Price_Optima/data/processed/final_environment_dataset.csv")

print(data.columns)

# ===============================
# Remove rows with missing values
# ===============================

data = data.dropna(subset=["latitude","longitude","pollutant_avg"])
data = data.sample(n=300, random_state=42)

# ===============================
# Pollution score
# ===============================

data["pollution_score"] = data["pollutant_avg"]

# ===============================
# Create map
# ===============================

m = folium.Map(
    location=[data["latitude"].mean(), data["longitude"].mean()],
    zoom_start=10
)

# ===============================
# Heatmap layer
# ===============================

heat_data = data[["latitude","longitude","pollution_score"]].values.tolist()

HeatMap(heat_data).add_to(m)

# ===============================
# Pollution markers
# ===============================

for _, row in data.iterrows():

    source = row["pollution_source"]

    if source == "Natural":
        color = "green"
    elif source == "Industry":
        color = "red"
    elif source == "Road":
        color = "orange"
    else:
        color = "blue"

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"""
        Source: {source}<br>
        Pollution Avg: {row["pollutant_avg"]}
        """,
        icon=folium.Icon(color=color)
    ).add_to(m)

# ===============================
# Save map
# ===============================

m.save("C:/projects/AI_Price_Optima/pollution_map.html")

print("Map Created Successfully")