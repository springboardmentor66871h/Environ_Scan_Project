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