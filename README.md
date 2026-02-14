EnviroScan Project – Week 1
📌 Project Overview
The Environ Scan Project aims to build a structured environmental intelligence dataset by integrating:
1.Air pollution data
2.Weather conditions
3.Geospatial location features
Week 1 :
focuses on creating a complete data pipeline that collects, processes, and merges multi-source environmental data for 10 major Indian cities.
🔌 APIs & Data Sources Used
1️⃣ Air Quality API
    PM2.5,PM10,NO₂,CO,SO₂,O₃
2️⃣ Weather API
    Temperature,Relative Humidity,Wind Speed,Wind Direction
3️⃣ OpenStreetMap (OSM)
Used to extract:
Distance to nearest road,Distance to industrial areas,Distance to dump sites,Distance to farmland

🏙 Cities Covered
  Delhi,Mumbai,Hyderabad,Chennai,Bengaluru,Kolkata,Pune,Ahmedabad,Jaipur,Lucknow

📅 Time Coverage
Environmental data collected dynamically for recent timestamps via API calls.

📊 Final Dataset Information
Total Rows: ~2,000
Total Columns: 17–18
File Name: final_dataset.csv
Location: data/processed/
Dataset Includes:
    Pollution indicators (pivoted format),Weather parameters,Latitude & Longitude,Location-based proximity features,Timestamp column,City column

⚙ Data Pipeline Workflow
Step 1 – Pollution Data Collection
Fetched pollutant concentrations for all 10 cities
Stored in long format
Saved as pollution.csv

Step 2 – Weather Data Collection
Retrieved weather metrics for corresponding city coordinates
Saved as weather.csv

Step 3 – Location Feature Extraction
Extracted geospatial distance-based features using OpenStreetMap
Saved as location_features.csv

Step 4 – Data Cleaning & Transformation
Standardized column names
Converted timestamps
Handled missing values
Pivoted pollution data (long → wide)

Step 5 – Data Merging
Merged pollution + weather + location datasets
Removed duplicates
Generated final processed dataset

📁 Project Folder Structure
Environ_Scan_Project/

│
├── data/
│   ├── raw/
│   │   ├── pollution.csv
│   │   ├── weather.csv
│   │   └── location_features.csv
│   │
│   └── processed/
│       └── final_combined_dataset.csv
│
├── scrip/
│   ├── fetch_pollution.py
│   ├── fetch_weather.py
│   ├── extract_location_features.py
│   └── merge_datasets.py
│
├── .gitignore
├── .env  (not pushed to repository)
└── README.md
