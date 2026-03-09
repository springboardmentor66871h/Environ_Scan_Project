 HEAD
# AI_Price_Optima – Environmental Data Collection & Processing

##  Project Overview
This project collects, processes, and combines environmental data including air pollution, weather, and location-based features to create a final dataset for analysis and modeling.



## APIs Used

1. Air Pollution API  
   - Used to collect pollutant data such as:
     - PM2.5
     - PM10
     - NO₂
     - CO
     - SO₂
     - O₃  

2. Weather API  
   - Used to collect:
     - Temperature
     - Humidity
     - Wind speed
     - Other weather-related features

3. OpenStreetMap (OSMnx)  
   - Used to extract location-based features such as:
     - Roads
     - Industrial areas
     - Dump sites
     - Agricultural land



##  Cities / Locations Selected

Data was collected for selected Indian cities based on latitude and longitude coordinates.

(You can mention specific city names here if required.)



## Time Range of Data

Data was collected for the selected time period using API queries.  
The time range depends on API availability and request parameters used in the scripts.



##  How the Data Was Collected

1. `collect_pollution.py`
   - Fetches pollution data using API requests.
   - Saves raw data into CSV format.

2. `collect_weather.py`
   - Fetches weather data from weather API.
   - Stores results in CSV format.

3. `extract_location_features.py`
   - Uses OSMnx to extract nearby geographic features.
   - Calculates distance-based features.

4. `combine_datasets.py`
   - Merges pollution, weather, and location datasets.
   - Produces final cleaned dataset.



##  Folder Structure
AI_Price_Optima/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── data/
│   ├── raw/                     # Original collected data
│   │   ├── pollution_data.csv
│   │   ├── weather_data.csv
│   │   └── location_features.csv
│   │
│   └── processed/               # Cleaned & merged dataset
│       └── final_environment_dataset.csv
│
├── src/                         # All Python scripts
│   ├── collect_pollution.py
│   ├── collect_weather.py
│   ├── extract_location_features.py
│   └── combine_datasets.py
│
├── notebooK

# Air Pollution Source Attribution Using AI

## Project Overview
This project aims to identify the likely sources of air pollution using environmental data and machine learning techniques. The goal is to classify pollution sources such as vehicular, industrial, agricultural, burning, and natural sources.



## Dataset
The project uses a combination of datasets:

- Station spatial data (`stations_with_spatial_features.csv`)
- Weather data (`weather_data.csv`)
- Synthetic pollutant concentrations generated for modeling.

Since real-world datasets do not contain labeled pollution sources, pollutant levels were simulated and rule-based labeling was applied.


## Data Processing Pipeline

1. Generate synthetic pollutant concentrations
2. Combine station and spatial data
3. Apply rule-based labeling to assign pollution sources
4. Generate labeled dataset for machine learning models



## Pollution Source Labels

The dataset contains the following classes:

- Vehicular
- Industrial
- Agricultural
- Burning
- Natural



## Labeling Rules

| Condition | Source |
|----------|--------|
| NO₂ > 80 and Distance_to_Nearest_Road < 0.5 | Vehicular |
| SO₂ > 50 | Industrial |
| PM2.5 > 100 and PM10 > 150 | Agricultural |
| PM2.5 > 120 | Burning |
| Otherwise | Natural |



## Generated Outputs
 HEAD
 fdfb9cb2 (Week 3 milestone: pollution labeling and dataset generation)


## Week 4 – Model Training

Model Used:
Random Forest Classifier

Features:
PM2.5, PM10, NO2, CO, SO2, O3
Temperature, Humidity
Wind Speed, Wind Direction
Distance to Road, Industry, Dump Site

Evaluation Metrics:
Accuracy
Precision
Recall
F1-score

Output Files:
models/pollution_model.pkl
feature_importance.png
 fc668669 (Week 4: Model training and evaluation)
