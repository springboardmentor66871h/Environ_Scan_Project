EnviroScan: AI-Powered Pollution Source Identification 🌍🏭

This project focuses on collecting and organizing environmental datasets required for pollution source analysis. The datasets include air pollution measurements, weather information, and location-based geographical features. These datasets are combined into a unified dataset for further AI model development in later stages.

APIs and Data Sources Used
1. Air Pollution Data

Air pollution data was collected from publicly available datasets containing pollutant measurements across Indian cities.

Pollutants included:

PM2.5

PM10

NO₂

CO

SO₂

O₃

Each record contains:

City

Latitude

Longitude

Timestamp

Pollutant Name

Pollutant Value

Dataset stored as:

data/raw/pollution_data.csv
2. Weather Data

Weather data includes environmental conditions corresponding to the same locations as pollution measurements.

Collected parameters:

Temperature

Humidity

Wind Speed

Wind Direction

Each record contains:

City

Latitude

Longitude

Timestamp

Dataset stored as:

data/raw/weather_data.csv
3. Location-Based Features (OpenStreetMap / OSMnx)

Geographical features were extracted using OpenStreetMap data through Python libraries.

Extracted nearby physical features:

Roads

Industrial Zones

Waste Disposal Sites

Agricultural/Farmland Areas

Distance-based features were calculated:

Distance to nearest road

Distance to nearest industry

Distance to nearest dump site

Distance to nearest farmland

Dataset stored as:

data/raw/location_features.csv
Cities / Locations Selected

The following Indian cities were selected for analysis:

Amaravati,
Bhopal,
Indore,
Chittoor,
Guntur

Locations were selected based on dataset consistency and data availability.

Time Range of Data:

The data corresponds to timestamps available in the collected datasets.

Pollution and weather datasets were aligned using available timestamp and location information to maintain consistency.

Data Collection Process:

Pollution datasets were collected and cleaned to include latitude, longitude, and pollutant values.

Weather datasets were collected for the same cities and formatted to match pollution dataset structure.

Location-based features were extracted using geographical coordinates.

Distances to nearby environmental features were calculated using geospatial analysis.

All datasets were merged using common columns:

City

Latitude

Longitude

Folder Structure

EnviroScan/
│
├── cache/
│
├── data/
│   │
│   ├── processed/
│   │     └── final_dataset.csv
│   │
│   └── raw/
│         ├── pollution_data.csv
│         ├── weather_data.csv
│         ├── location_features.csv
│         ├── Weather data1.xlsx
│         └── Weather data2.xlsx
│
├── scripts/
│     ├── build_location_dataset.py
│     ├── location_features.py
│     ├── merge_data.py
│     ├── pollution_data.py
│     └── weather_data.py
│
└── README.md

Output

Final dataset saved as:

data/processed/final_dataset.csv

🌍 EnviroScan – Week 3: Rule-Based Pollution Source Labeling
📌 Objective of Week 3

The objective of this phase is:

To assign pollution source labels to the dataset using logical, rule-based heuristics and prepare a final labeled dataset for machine learning training.

Since real-world ground-truth pollution source labels were not available, we implemented a scientifically motivated rule-based labeling system using pollutant intensity and environmental proximity features.

📊 Problem Statement

The dataset contains:

🔬 Pollutant Concentrations

PM2.5

PM10

NO₂

CO

SO₂

O₃

🌦 Weather Features

Temperature

Humidity

Wind Speed

Wind Direction

📍 Distance Features

Distance to nearest road

Distance to nearest industrial zone

Distance to nearest farmland

Distance to nearest dump site
🏷 Defined Pollution Categories

🚗 Vehicular

🏭 Industrial

🌾 Agricultural

🔥 Burning

🌍 Natural
Labeling Rules Implemented
1️⃣ Vehicular Pollution

Condition:

Pollutant = NO₂ or CO

Concentration > 40 µg/m³

Distance to road ≤ 5 km

Logic:
High traffic emissions are associated with elevated NO₂ and CO near major roads.

2️⃣ Industrial Pollution

Condition:

Pollutant = SO₂

Concentration > 30 µg/m³

Distance to industry ≤ 20 km

Logic:
SO₂ is commonly linked to industrial combustion and power plants.

3️⃣ Agricultural Pollution

Condition:

Pollutant = PM2.5 or PM10

Concentration > 50 µg/m³

Distance to farmland ≤ 30 km

Logic:
Crop burning and agricultural activities elevate particulate matter levels.

4️⃣ Burning (Waste Burning)

Condition:

Pollutant = PM2.5 or PM10

Concentration > 60 µg/m³

Distance to dump site ≤ 15 km

Logic:
Open waste burning produces high particulate matter concentrations.

5️⃣ Natural

Condition:

Assigned when none of the above conditions are met.

Logic:

Represents background pollution, dust, or mixed atmospheric sources not strongly linked to anthropogenic activities.

Visualization file generated:

Source_Labeling/label_distribution.png

📁 Output Files

✅ Final Labeled Dataset

data/processed/final_labeled_dataset.csv

✅ Visualization

Source_Labeling/label_distribution.png

Run labeling script:

python Source_Labeling/labeling_rules.py

Outputs:

Labeled CSV

Distribution visualization.


🌍 EnviroScan – Pollution Source Classification (Week 4)

This model predicts the likely pollution source based on pollutant concentration levels and distance to nearby potential pollution contributors such as roads, 
industries, farms, and dump sites.

This repository contains the Week 4 milestone deliverables, including:

Target label generation (rule-based)

Model training (Random Forest)


Model evaluation

Feature importance analysis

Exported trained model

📊 Dataset Information

Total Records: 3314

Features Used: 7

Train-Test Split: 80% / 20%

🔹 Input Features
Pollutant Features
pollutant_min
pollutant_max
pollutant_avg
Proximity Features
Nearest_Road_km
Nearest_Industry_km
Nearest_Dump_km
Nearest_Farm_km

🎯 Target Variable Creation

The target column pollution_source is generated using rule-based logic:
If distance to industry < 2 km → Industrial
If distance to farm < 2 km → Agricultural
If distance to dump < 2 km → Dump
If distance to road < 2 km → Vehicular
Otherwise → Natural

This labeling approach is deterministic and based on proximity thresholds.
⚙️ Model Details
Model Used
Random Forest Classifier
Model Configuration
n_estimators = 300
class_weight = 'balanced'
random_state = 42
Stratified train-test split

📉 Confusion Matrix
Saved at:
models/confusion_matrix.png
The confusion matrix shows zero misclassifications on the test set.

🔍 Feature Importance
Top contributing features:
Nearest_Industry_km
Nearest_Road_km
Nearest_Farm_km
Pollutant statistics
Saved at:

models/feature_importance.png
📦 Exported Model

The trained model and label encoder are saved using joblib:

models/pollution_model.pkl

models/label_encoder.pkl

These files can be integrated into a dashboard or deployment pipeline.

📂 Project Structure

EnviroScan/
│
├── data/
│   └── processed/
│       └── final_dataset.csv
│
├── models/
│   ├── pollution_model.pkl
│   ├── label_encoder.pkl
│   ├── confusion_matrix.png
│   └── feature_importance.png
│
├── scripts/
│   └── train_model.py
│
└── README.md

🌍EnviroScan – Module 5: Geospatial Pollution Mapping
📌Overview

Module 5 of the EnviroScan project focuses on Geospatial Data Visualization. This module generates an interactive pollution heatmap using geographic coordinates from environmental datasets. The visualization helps identify pollution hotspots and understand the spatial distribution of pollution levels.

The system processes pollution data and displays it on an interactive map using geospatial visualization techniques.

🎯Objectives

Visualize pollution intensity geographically

Identify high pollution zones

Represent pollution data using heatmaps

Provide an interactive map for environmental analysis

🛠Technologies Used

Python

Pandas – Data processing

Folium – Geospatial visualization

Leaflet.js – Interactive map rendering

📂Project Structure
EnviroScan
│
├── data
│   └── processed
│       └── final_map_dataset.csv
│
├── visualization
│   ├── geospatial_map.py
│   └── pollution_map.html
│
└── README.md
🗂Dataset Description

The dataset contains processed pollution information including:

Latitude – Geographic coordinate

Longitude – Geographic coordinate

pollutant_avg – Average pollution level (PM2.5)

pollution_source – Source category (Industrial, Vehicular, Agricultural, Burning)

These fields are used to create the geospatial visualization.

⚙Installation

Install required Python libraries:

pip install pandas folium
▶Running the Module

Run the geospatial visualization script:

python visualization/geospatial_map.py

This will generate the output file:

visualization/pollution_map.html

Open the HTML file in a web browser to view the interactive pollution map.

✨Features

Pollution heatmap visualization

Color gradient representing pollution intensity

Interactive geographic map

Pollution value markers

Legend explaining pollution levels

Zoom and navigation support

📊Output

The generated map displays pollution intensity using a color gradient:

Blue – Very Low Pollution

Green – Moderate Pollution

Yellow – High Pollution

Red – Severe Pollution

Users can zoom and interact with the map to explore pollution levels in different regions.

✅Conclusion

Module 5 successfully visualizes environmental pollution data using geospatial mapping techniques. This interactive visualization helps in identifying pollution hotspots and supports environmental monitoring and analysis.
🗺️ Phase 4: Geospatial Mapping & Dashboard (Week 5-6)
Objective: Create an interactive, user-friendly web interface for real-time monitoring.

Tools Used: Streamlit, Folium, Plotly.

Dashboard Features:

Real-Time Alerts: Dynamic warning banners triggered when pollutant values cross safety thresholds (e.g., > 150 triggers a High-Risk Alert).

Interactive Map: * Heatmap Layer: Visualizes overall pollution intensity.

Source Markers: Custom FontAwesome icons (cars, factories, leaves) indicating predicted sources.

Filter Mechanism: Checkbox layer controls to isolate specific pollution sources.

Trend Analytics: Interactive Plotly pie charts and bar charts displaying national source distribution and top pollutants.

Report Export: A one-click download button allowing users to export the fully labeled and processed dataset as a CSV.
