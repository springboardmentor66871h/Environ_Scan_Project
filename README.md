# AI_Price_Optima – Environmental Data Collection & Processing

## Project Overview
This project collects, processes, and combines environmental data including air pollution, weather, and location-based features to create a final dataset for analysis and modeling.

## APIs Used

1. Air Pollution API  
   - PM2.5  
   - PM10  
   - NO₂  
   - CO  
   - SO₂  
   - O₃  

2. Weather API  
   - Temperature  
   - Humidity  
   - Wind speed  

3. OpenStreetMap (OSMnx)  
   - Roads  
   - Industrial areas  
   - Dump sites  
   - Agricultural land  

## Cities / Locations Selected
Data was collected for selected Indian cities based on latitude and longitude coordinates.

## Time Range of Data
Data was collected for the selected time period using API queries.

---

# Data Collection Pipeline

### 1. collect_pollution.py
Fetches pollution data using API requests.

### 2. collect_weather.py
Fetches weather data.

### 3. extract_location_features.py
Uses OSMnx to extract geographic features.

### 4. combine_datasets.py
Merges pollution, weather, and location datasets.

---

# Air Pollution Source Attribution Using AI

## Project Overview
This project identifies likely sources of air pollution using machine learning.

### Pollution Sources
- Vehicular  
- Industrial  
- Agricultural  
- Burning  
- Natural  

---

# Dataset

The project combines:

- Station spatial data  
- Weather data  
- Synthetic pollutant concentrations  

Since real datasets do not contain labeled sources, pollutant levels were simulated and rule-based labeling was applied.

---

# Labeling Rules

| Condition | Source |
|----------|--------|
| NO₂ > 80 and Distance_to_Road < 0.5 | Vehicular |
| SO₂ > 50 | Industrial |
| PM2.5 > 100 and PM10 > 150 | Agricultural |
| PM2.5 > 120 | Burning |
| Otherwise | Natural |

---

# Week 4 – Model Training

Model Used:  
Random Forest Classifier

### Features
- PM2.5, PM10, NO2, CO, SO2, O3  
- Temperature, Humidity  
- Wind Speed, Wind Direction  
- Distance to Road, Industry, Dump Site  

### Evaluation Metrics
- Accuracy  
- Precision  
- Recall  
- F1-Score  

### Output Files
- models/pollution_model.pkl  
- feature_importance.png  

---

# Week 5 – Geospatial Mapping

Tools Used:
- Folium  
- HeatMap plugin  

### Features
- Pollution heatmap using PM2.5 values  
- Source-specific markers  
- High-risk zone highlighting  
- Interactive map exported as HTML