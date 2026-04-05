# EnviroScan: Environmental Pollution Monitoring and Analysis Project

## Overview

EnviroScan is a comprehensive environmental monitoring system designed to analyze air pollution levels across various locations in India. This project integrates real-time weather data, pollution measurements, and machine learning models to provide insights into environmental quality and pollution sources. The system includes data collection, preprocessing, predictive modeling, and interactive visualization components.

Developed by Swapna Gajula as part of environmental research to promote sustainable urban development and public health awareness.

## Project Structure

```
EnviroScan_Run/
├── dashboard.py                 # Main dashboard application
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── assets/                      # Static assets for dashboard
├── dashboard/
│   ├── app.py                   # Flask web application
│   └── pollution_map.html       # Interactive pollution map
├── data/
│   ├── stations.csv             # Monitoring station information
│   ├── stations_with_coordinates.csv    # Stations with GPS coordinates
│   ├── stations_with_spatial_features.csv  # Stations with spatial features
│   ├── weather_today.csv        # Current weather data
│   ├── processed/               # Cleaned and processed datasets
│   │   ├── cleaned_data.csv
│   │   ├── final_environment_dataset.csv
│   │   ├── final_labeled_dataset.csv
│   │   ├── final_labeled_with_weather.csv
│   │   ├── labeled_dataset.csv
│   │   └── pollution_with_levels.csv
│   └── raw/                     # Raw data files
│       ├── india_air_pollution_cleaned.csv
│       ├── india_weather_dataset_new.csv
│       ├── location_features.csv
│       ├── location.csv
│       ├── pollution_data.csv
│       ├── pollution.csv
│       ├── weather_data.csv
│       └── weather.csv
├── models/
│   └── pollution_model.joblib   # Trained machine learning model
└── scripts/
    ├── calculate_distance_to_road.py    # Road proximity calculations
    ├── clean_data.py           # Data cleaning utilities
    ├── collect_pollution.py    # Pollution data collection
    ├── collect_weather.py      # Weather data collection
    ├── combine_datasets.py     # Dataset merging
    ├── extract_location_features.py    # Feature extraction
    ├── generate_pollution_levels.py   # Pollution level categorization
    ├── get_station_coordinates.py     # GPS coordinate retrieval
    ├── label_pollution_source.py      # Source labeling
    ├── map_city.py             # City mapping utilities
    ├── plot_stations_on_map.py # Station visualization
    ├── pollution_map.py        # Pollution mapping
    └── train_model.py          # Model training script
```

## Key Features

### 1. Data Collection and Integration
- **Pollution Data**: Automated collection of air quality metrics including PM2.5, PM10, NO2, SO2, CO, and O3 levels
- **Weather Data**: Real-time weather information integration (temperature, humidity, wind speed, precipitation)
- **Geospatial Data**: GPS coordinates and spatial features for monitoring stations
- **Location Features**: Proximity to roads, urban areas, and industrial zones

### 2. Data Processing Pipeline
- **Data Cleaning**: Removal of duplicates, handling missing values, outlier detection
- **Feature Engineering**: Extraction of spatial features, temporal patterns, and environmental indicators
- **Data Labeling**: Automatic classification of pollution sources (traffic, industrial, residential)
- **Dataset Merging**: Integration of pollution, weather, and location data into unified datasets

### 3. Machine Learning Model
- **Predictive Modeling**: Classification model to predict pollution levels and sources
- **Model Training**: Using scikit-learn with joblib serialization for deployment
- **Performance Evaluation**: Model validation and accuracy assessment

### 4. Interactive Dashboard
- **Web Application**: Flask-based dashboard for data visualization
- **Pollution Maps**: Interactive geographical visualization of pollution levels
- **Real-time Monitoring**: Live data updates and trend analysis
- **Data Exploration**: Charts and graphs for environmental insights

## Work Done in This Project

### Problem Identification and Solution Design
The project began with identifying a critical gap in existing air pollution monitoring systems: while they provide pollutant concentration values, they fail to identify the specific sources of pollution (vehicular, industrial, agricultural, or waste burning). This limitation hinders effective policy-making and targeted interventions.

**My Approach**: I designed EnviroScan as an AI-powered system that combines environmental data with machine learning to predict pollution sources and visualize them geographically through an interactive dashboard.

### Data Acquisition and Preparation
Due to API access limitations, I utilized a comprehensive Kaggle dataset containing static environmental data. The dataset included:
- Pollutant measurements (PM10, NO2, SO2, CO, O3)
- Weather parameters (temperature, humidity, wind speed)
- Location features (distance to roads, industries, farmlands, dump sites)

**Key Challenges Faced**:
- Missing values in raw data
- Inconsistent data formats across different sources
- Lack of labeled data for supervised learning

**Solutions Implemented**:
- Developed robust data cleaning scripts to handle missing values and duplicates
- Created pivot operations to transform pollutant data from rows to columns
- Implemented reverse geocoding to obtain city names from latitude/longitude coordinates
- Built comprehensive dataset merging utilities to combine pollution, weather, and location data

### Exploratory Data Analysis (EDA)
I conducted thorough EDA to understand data patterns and distributions:
- Analyzed pollution distribution across different locations
- Identified dominant pollutant types and their correlations
- Discovered imbalances in pollution source categories
- Visualized spatial patterns using geographical plotting

### Source Labeling Methodology
Since real-world labeled data was unavailable, I developed a rule-based labeling system to simulate pollution source classification:

**Pollution Sources Identified**:
- **Vehicular**: High NO2 levels near roads
- **Industrial**: High SO2 levels or proximity to industrial areas
- **Agricultural**: Elevated PM10 levels in farming regions
- **Burning**: Moderate PM10 levels near waste dump sites

**Implementation**: Created automated labeling scripts that apply these rules to generate training labels for the machine learning model.

### Machine Learning Model Development
I implemented and compared multiple classification algorithms:
- Decision Tree
- Random Forest (selected as final model)

**Training Process**:
- 80/20 train-test split for model validation
- Hyperparameter tuning using GridSearchCV
- Feature importance analysis using Random Forest

**Model Performance**: Achieved high accuracy due to well-defined rule-based patterns, with strong precision and recall metrics across pollution source categories.

### Geospatial Visualization
Developed interactive maps using Folium library:
- Pollution heatmaps based on PM10 concentrations
- Source-specific markers for different pollution types
- High-risk zone identification
- Interactive features for location-based filtering

### Dashboard Development
Built a comprehensive web dashboard using Streamlit with the following features:
- City/location-based search functionality
- Real-time pollution source prediction
- Interactive heatmap visualization
- Trend charts and data analysis
- Dataset download capabilities
- Voice-enabled AQI output using text-to-speech (pyttsx3)

### Technical Implementation Details
**Data Processing Scripts**:
- `clean_data.py`: Handles data cleaning and preprocessing
- `extract_location_features.py`: Calculates spatial features
- `label_pollution_source.py`: Applies rule-based labeling
- `combine_datasets.py`: Merges multiple data sources
- `train_model.py`: Model training and evaluation

**Dashboard Components**:
- `dashboard/app.py`: Main Streamlit application
- `pollution_map.html`: Folium-generated interactive maps

**Model Persistence**: Used joblib for model serialization and deployment.

## Results and Achievements

### Successful Outcomes
- **Accurate Predictions**: Model successfully predicts pollution sources with high confidence
- **Interactive Visualization**: Created user-friendly dashboard for environmental insights
- **Comprehensive Dataset**: Built integrated environmental dataset with 15+ features
- **Scalable Architecture**: Modular code structure for easy maintenance and extension

### Key Insights Discovered
- Urban areas show significantly higher pollution levels
- Weather conditions strongly correlate with pollution dispersion
- Traffic and industrial sources contribute to majority of pollution
- Seasonal patterns affect pollution accumulation

## Technologies and Tools Used

- **Programming Language**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, Joblib
- **Visualization**: Folium, Matplotlib, Streamlit
- **Geospatial**: Geopy, Shapely
- **Web Framework**: Flask, Streamlit
- **Version Control**: Git

## Installation and Usage

### Prerequisites
- Python 3.8 or higher
- Git
- Internet connection for data collection

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/swapnagajula16/Environ_Scan_Project.git
   cd Environ_Scan_Project
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # Windows: env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

1. **Data Processing**:
   ```bash
   # Clean and process data
   python scripts/clean_data.py
   python scripts/extract_location_features.py
   python scripts/combine_datasets.py
   ```

2. **Model Training**:
   ```bash
   python scripts/train_model.py
   ```

3. **Launch Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

The dashboard will be available at `http://localhost:8501`

## Limitations and Future Work

### Current Limitations
- Reliance on static Kaggle dataset due to API access constraints
- Rule-based labeling instead of real ground-truth data
- Limited real-time data integration

### Planned Enhancements
- Integrate real-time pollution and weather APIs
- Implement advanced deep learning models
- Improve labeling accuracy with actual sensor data
- Add mobile application for field data collection
- Implement automated alert systems for pollution spikes

## Project Impact

This project demonstrates the potential of combining environmental data with machine learning to:
- Identify pollution sources more accurately
- Enable targeted environmental interventions
- Provide actionable insights for policymakers
- Raise public awareness about air quality issues
- Support sustainable urban planning decisions

## Acknowledgments

- Central Pollution Control Board (CPCB) for air quality data
- OpenWeatherMap for weather API services
- Kaggle community for dataset contributions
- Mentors and peers for guidance and feedback

## Author

**Swapna Gajula**
- GitHub: [swapnagajula16](https://github.com/swapnagajula16)
- Project Repository: [Environ_Scan_Project](https://github.com/swapnagajula16/Environ_Scan_Project)

---

*Developed as part of environmental monitoring research to promote sustainable development and public health.*