# EnviroScan: Milestone 1 - Data Collection

## Overview
This repository contains the dataset preparation for Week 1 of the EnviroScan project: AI-Powered Pollution Source Identification. The objective of this phase is strictly data collection, preprocessing, and dataset organization. No machine learning models, dashboards, or Docker setups are included at this stage.

## Data Sources & APIs 
The datasets were built using the sources specified in the project requirements:
1. **OpenAQ:** Used to collect air pollution metrics (PM2.5, PM10, NO₂, CO, SO₂, O₃).
2. **OpenWeatherMap:** Used to collect meteorological data (Temperature, Humidity, Wind speed, Wind direction).
3. **OpenStreetMap:** Used to identify nearby physical features (proximity to roads, industrial zones, dump sites, agricultural fields).

## Cities Selected & Time Range
* **Selected Locations:** [Insert City 1], [Insert City 2], [Insert City 3]
* **Time Range of Data:** [Insert the dates your data covers, e.g., February 15 - February 18, 2026]

## How the Data Was Collected
1. **Pollution Data:** CSV data was extracted directly from the OpenAQ Explorer for the selected monitoring stations, capturing the required pollutant levels and timestamps.
2. **Weather Data:** Historical weather data (temperature, humidity, wind speed/direction) was gathered for the exact coordinates and timestamps matching the pollution records to ensure temporal alignment.
3. **Location Features:** Spatial analysis was conducted using map data to determine the presence of roads, industrial zones, landfills, and farmland within the immediate vicinity of the coordinate points.
4. **Dataset Merging:** The individual raw datasets were merged into a single structured dataset (`combined_dataset.csv`) aligned by City, Latitude, Longitude, and Timestamp.

## Folder Structure
The repository is organized exactly as requested:
* `data/raw/` 
  * `pollution_data.csv` (Contains raw OpenAQ exports)
  * `weather_data.csv` (Contains aligned meteorological data)
  * `location_features.csv` (Contains geospatial booleans)
* `data/processed/`
  * `combined_dataset.csv` (The final merged dataset ready for future modeling)

## Missing Values Handling
During the data collection process, any missing API readings for specific pollutants or weather metrics at a given timestamp were left blank (NaN). These missing values have been preserved in the raw and processed datasets and will be explicitly handled (e.g., via imputation or dropping) during the data preprocessing phase in Milestone 2.
