# AI_Price_Optima – Environmental Data Collection & Processing

##  Project Overview
This project collects, processes, and combines environmental data including air pollution, weather, and location-based features to create a final dataset for analysis and modeling.

---

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

---

##  Cities / Locations Selected

Data was collected for selected Indian cities based on latitude and longitude coordinates.

(You can mention specific city names here if required.)

---

## Time Range of Data

Data was collected for the selected time period using API queries.  
The time range depends on API availability and request parameters used in the scripts.

---

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

---

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