# README — Project Dataset Collection

## Project Overview  
This project focuses on collecting and preparing air pollution, weather, and location-based environmental data for major Indian cities. The dataset is used for analysis and prediction of air quality patterns.

## APIs Used  

1.**Air Pollution Data**
- Source: OpenAQ API  
- Website/API: https://api.openaq.org/  
- Pollutants Collected: 
  - PM2.5  
  - PM10  
  - NO₂  
  - CO  
  - SO₂  
  - O₃  

 2.**Weather Data**
- Source: OpenWeatherMap API  
- Website/API: https://openweathermap.org/api  
- Weather Features Collected:
  - Temperature  
  - Humidity  
  - Wind Speed  
  - Pressure  
  - Weather Conditions  

 3.**Location-Based Features**
- Source: OpenStreetMap (OSM) using OSMnx  
- Tool Used: OSMnx + Overpass API  
- Features Extracted: 
  - Roads  
  - Industrial areas  
  - Green spaces  
  - Dumping sites  
  - Land use patterns  

## Cities / Locations Selected  

The following 6 Indian cities were chosen for the dataset:

1. Pune  
2. Mumbai  
3. Delhi  
4. Srinagar  
5. Ahmedabad  
6. Nagaur  

These cities represent different geographic regions and pollution levels across India.

## Time Range of Data  

- **Duration:** 1 Year  
- The dataset contains air pollution and weather data collected over a full one-year period.

## How the Data Was Collected  

1. Air Pollution Collection  
- Pollution measurements were downloaded city-wise using the OpenAQ API.  
- Data was saved in CSV format for each city.  
- Required pollutants were filtered and merged into one main dataset.

2. Weather Data Collection  
- Weather readings were collected every few minutes/hours using OpenWeatherMap API.  
- Weather data was stored in a separate CSV file.

3. OSM Feature Extraction  
- Location-based environmental features were extracted using OpenStreetMap data with OSMnx.  
- Distances to roads, green zones, and dumping areas were calculated for each city.

### Data Cleaning  
- All datasets were cleaned by handling missing values and removing unrealistic zeros.  
- Final cleaned dataset was saved for machine learning and analysis.

##  Folder Structure  

Air Pollution Project/
│
├── city_pollution/
│   ├── Pune.csv
│   ├── Mumbai.csv
│   ├── Delhi.csv
│   ├── Srinagar.csv
│   ├── Ahmedabad.csv
│   └── Nagaur.csv
│
├── scripts/
│   ├── pollution_collection.py
│   ├── weather_collection.py
│   ├── location_collection.py
│  
├── Main_Pollution_Dataset_Cleaned.csv
├── Final_Dataset_Environ.csv
├── weather_Dataset.csv
├── Merge.py
├── location_Dataset.csv
│
└── README.md