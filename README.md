# 🌍 EnviroScan: AI-Based Pollution Source Identification System

## 📌 Project Overview

EnviroScan is an end-to-end data science and machine learning project designed to analyze air pollution data, identify possible pollution sources, and visualize pollution patterns using geospatial analytics and an interactive dashboard.

The system collects environmental data such as pollutant levels, geographic coordinates, and engineered features (like distance from roads or industries). Using this data, it predicts pollution sources like **traffic, industrial, Agriculutral, and natural causes**, helping users better understand pollution patterns.

---

## ❗ Problem Statement

Air pollution is a serious issue that affects human health, climate, and the environment. Although many systems can measure pollution levels, they do not provide information about **where the pollution is coming from**.

### Challenges:

* No labeled dataset for pollution sources
  → There is no real dataset that directly tells the source of pollution

* Difficulty in identifying source contribution
  → Multiple sources contribute to pollution at the same location

* Lack of interactive visualization tools
  → Most systems do not provide maps or dashboards for easy understanding

This project solves these problems using **machine learning models and visual tools**.

---

## 🎯 Objectives

* Predict pollution sources using ML models
  → Classify pollution into categories like traffic or industrial

* Identify pollution hotspots
  → Detect areas with high pollution concentration

* Visualize pollution data on maps
  → Show pollution levels geographically

* Build an interactive dashboard
  → Allow users to explore data easily

* Provide easy-to-understand environmental insights
  → Help users and authorities make decisions

##

---

## 📊 Dataset Description

### Data Sources:

* OpenAQ – Provides air pollution data (PM2.5, PM10, etc.)
* OpenWeatherMap – Provides weather data like temperature and humidity
* OpenStreetMap (OSMnx) – Provides geographic features like roads and industries

### Features:

* Pollutants: PM2.5, PM10, NO₂, CO
  → These values represent pollution levels

* Location: City, Latitude, Longitude
  → Used for mapping and geospatial analysis

* Distance Features:
  → Helps identify possible sources

  * Distance to roads (traffic source)
  * Distance to industries (industrial source)

* Additional environmental parameters
  → Includes weather-related data if available

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

### Dataset Type:

* Combined and processed dataset
* Includes labeled pollution sources (generated using rules)

---

## 🧹 Data Preprocessing
# Handling Missing Values
* Missing or null values were removed to ensure data quality and avoid errors during model training.

# Removing Duplicates
* Duplicate records were identified and removed to prevent repeated data from biasing the model.

# Data Cleaning Steps
* Column names were standardized for consistency.
* Data types were corrected where necessary.
* Irrelevant or noisy data entries were cleaned.

# Feature Engineering
* Created new features such as distance from roads and industries.
* These features help the model understand the impact of location on pollution levels.

# Normalization / Scaling
* Basic formatting and standardization were applied where required.
* Scaling can be applied in future to improve model performance further.
---

## 📈 Exploratory Data Analysis (EDA)

### Key Observations:

* PM2.5 is the most dominant pollutant
  → It appears most frequently and in high values

* High pollution mostly occurs in urban areas
  → Cities show higher pollution levels

* Pollution increases near roads and industries
  → Indicates major sources of pollution

### Visualizations:

* Distribution plots
  → Show how pollution values are spread

* Correlation heatmaps
  → Show relationships between variables

* City-wise pollution comparison
  → Compare pollution levels across cities

## Correlation Insights
* Strong correlation observed between PM2.5 and PM10.
* Pollution levels show a relationship with proximity to roads and industries.
* Environmental factors such as weather also influence pollution levels.

## Patterns Discovered
* Urban areas consistently show higher pollution trends.
* Areas near traffic and industries are more polluted.
* Pollution patterns vary across cities and depend on location features.  

---

## 🏷️ Source Labeling Methodology

Since real labels are not available, **rule-based labeling** is used.

### Logic:

* High PM2.5 + near roads → Traffic
* High PM10 + near industries → Industrial
* Moderate pollution → Residential/Natural

→ These rules simulate real-world pollution behavior

### Threshold Values Used
* Pollution thresholds (e.g., PM2.5, PM10 levels) are used to determine severity.
* Distance-based thresholds (e.g., proximity to roads or industries) help identify likely sources.

### Assumptions Made
* Pollution sources are inferred based on pollutant type and nearby features.
* Areas close to roads are assumed to be affected by vehicular emissions.
* Areas near industries are assumed to have industrial pollution impact.

### Limitations
* Labels are simulated due to lack of real-world ground truth data.
* Rule-based logic may not capture all real environmental conditions.
* Multiple pollution sources in a single area are simplified into one category.
* Accuracy depends heavily on chosen thresholds and assumptions.

---

## 🤖 Model Development

### Models Used:

* Random Forest
  → Ensemble model, gives better accuracy

* Decision Tree
  → Simple and interpretable model

### Process:

* Feature selection
  → Selected important columns for prediction

* Train-test split (80:20)
  → 80% data for training, 20% for testing

* Model training
  → Model learns patterns from data

---

## 📊 Model Evaluation

# Metrics
* Accuracy
→ Measures overall correctness of the model predictions
* Precision
→ Indicates how many predicted values are actually correct
* Recall
→ Measures how many actual values are correctly * identified
* F1-score
→ Provides a balance between precision and recall
* Confusion Matrix
→ Shows detailed comparison of actual vs predicted values for each class

# Results
* Model achieved good accuracy on the labeled dataset
* Random Forest performed better compared to other models
* XGBoost also provided competitive performance

# Interpretation of Results
* The model is able to predict pollution sources effectively
* Performance depends on the quality of rule-based labeling
* Some variation occurs due to simulated data and assumptions
---

## 🗺️ Geospatial Visualization

### Tools:
* Folium (for interactive map visualization)

# Heatmap Generation
* Heatmaps are created using pollution values to represent intensity
* Darker regions indicate higher pollution levels

# Marker Logic for Pollution Sources
* Different markers/colors are used to represent different pollution sources
* Markers are placed based on predicted pollution source at each location

# High-Risk Zone Identification
* Areas with high pollutant values are identified as high-risk zones
* These zones are highlighted using darker heatmap regions and dense markers

---

## 📊 Dashboard Implementation

Built using Streamlit to create an interactive and user-friendly interface.

### Features

* Streamlit Dashboard Features
> Displays pollution data in real-time or from the dataset
> Provides interactive UI components for easy navigation
> Integrates charts and maps in a single interface

* User Inputs
> Users can select city or location
> Input options allow filtering and exploring specific data

* Prediction Display
> Shows predicted pollution source based on model output
> Displays pollutant values along with prediction

* Charts and Map Integration
> Plotly charts are used for visual analysis of pollution trends
> Folium maps are embedded to show heatmaps and source markers

---

## 📸 Results & Outputs

## Screenshots (to be added in GitHub)
* Dashboard view
* Heatmap visualization
* Charts and graphs

## Key Outcomes Achieved
* Successfully predicted pollution sources using ML models
* Visualized pollution hotspots on maps
* Built an interactive dashboard for analysis
* Integrated machine learning with real-world data visualization
---

## ⚠️ Limitations

## Rule-Based Labeling Limitations
* Labels are generated using predefined rules and may not reflect real conditions accurately

## Lack of Real-World Ground Truth
* No actual labeled dataset is available for validation

## Data Constraints
* Limited dataset size may affect model performance
* Results depend on assumptions and selected thresholds
---

## 🚀 Future Enhancements

* Real-time API integration
  → Live pollution tracking

* Advanced ML models ( Deep Learning)
  → Improve accuracy

* Satellite data usage
  → Better environmental analysis
---

##  Project Structure  

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
├── Dataset/
│   ├── Final_Dataset_Environ.csv
│   ├── location_Dataset.csv
│   ├── Main_pollution_Dataset.csv
│   ├── Weather_Dataset.csv
│   
├── Image/
│   ├── Matrix-Decision_tree.png
│   ├── Matrix-XGBoost.png
│   ├── Matrix.png
│   ├── Random_forest.png
│   ├── visualization_Bar.png
│   
├── Models/
│   ├── decision_tree_model.joblib
│   ├── label_encoder.joblib
│   ├── pollution_source_model.joblib
│   ├── xgboost_model.joblib
│  
│
├── scripts/
│   ├── pollution_collection.py
│   ├── weather_collection.py
│   ├── location_collection.py
│   ├── Merge.py
│   ├── model_training.py
│   ├── pollution_map.py
│   ├── source_labeling.py
│   └── test_model.py
│   
├── Final_Labeled_pollution_Dataset.csv
├── dashboard.py
├── pollution_map.html
│
└── README.md
 ---

## ▶️ How to Run the Project

### Install dependencies:

```bash
pip install pandas numpy streamlit scikit-learn plotly folium joblib
```

### Run dashboard:

```bash
streamlit run dashboard.py
```
---

## 🛠️ Technologies Used

* Python
* Pandas, NumPy
* Scikit-learn
* XGBoost
* Streamlit
* Plotly
* Folium
* Joblib
* OpenAQ API
* OpenWeatherMap API
* OpenStreetMap (OSMnx)

---

## 📌 Conclusion

EnviroScan provides an effective way to analyze air pollution and predict its sources. It combines machine learning with geospatial visualization to create a powerful and user-friendly system that helps in understanding pollution patterns and supports better environmental decision-making.

---
