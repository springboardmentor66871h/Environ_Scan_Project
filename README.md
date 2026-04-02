

## ENVIROSCAN
An AI-based environmental analytics system developed to analyze air quality data, identify probable pollution sources, and visualize pollution hotspots using machine learning and geospatial techniques.

---

## 1. Problem Statement

Air pollution is a major environmental and public health challenge, especially in urban regions where industrial activities, vehicular emissions, and population growth contribute to poor air quality. Traditional air quality monitoring systems mainly report pollutant concentration values such as PM2.5, PM10, NO2, and SO2, but they do not identify the likely sources of pollution.

Identifying pollution sources is important because it helps authorities and stakeholders take targeted actions for pollution control, urban planning, and public health protection. Without source identification, it is difficult to know whether the pollution is mainly caused by traffic, industrial activity, open burning, or mixed urban factors.

Existing systems also have certain limitations:
- They focus mainly on pollutant levels and not source attribution
- They do not effectively combine pollution, weather, and spatial data
- They offer limited predictive insights
- They often lack interactive visualization for hotspot analysis

EnviroScan addresses these limitations by integrating environmental data, machine learning, and geospatial visualization into one system.

---

## 2. Objectives

The main objectives of the EnviroScan project are:

- Predict probable pollution sources using machine learning
- Analyze pollution trends using historical data
- Integrate pollution, weather, and location-based features
- Visualize pollution hotspots using maps and heatmaps
- Build an interactive dashboard for users
- Support better environmental analysis and decision-making

---

## 3. Dataset Description

EnviroScan uses a multi-source dataset that combines pollution data, weather data, and location-based features. This allows the system to capture both environmental conditions and spatial context.

### 3.1 Data Sources

- **Pollution Data:** CPCB datasets collected from monitoring stations
- **Weather Data:**
  - Historical weather data from NASA LARC
  - Real-time weather data from Open-Meteo
- **Location Data:**
  - Simulated distance-based features due to difficulty in extracting accurate data from OpenStreetMap/OSMnx

### 3.2 Monitoring Stations Used

**Delhi**
- DELHI_CHANDINI_CHOWK
- DELHI_ANANT_VIHAR
- DELHI_ITO

**Bhopal**
- BHOPAL
- BHOPAL_PARYAVARAN_PARK
- BHOPAL_IDGAH_HILLS

**Mumbai**
- MUMBAI
- MUMBAI_BYCULLA
- MUMBAI_CHAKALA_ANDHERI

**Kolkata**
- KOLKATA
- KOLKATA_BALLYGUNGE
- KOLKATA_JADAVPUR

**Bengaluru**
- BENGELURU
- BENGALURU_HEBBAL
- BENGALURU_RAILWAY_STATION

**Chennai**
- CHENNAI
- CHENNAI_ALANDUR_BUS_DEPOT
- CHENNAI_VELACHERY

**Lucknow**
- LUCKNOW
- LUCKNOW_TALKATORA
- LUCKNOW_LALBAGH

**Hyderabad**
- HYDERABAD
- HYDERABAD_PATENCHERU
- HYDERABAD_SOMAJIGUDA

**Ahmedabad**
- AHEMEDABAD
- AHMEDABAD_SOMAJIGUDA
- AHMEDABAD_SVPT

### 3.3 Features Collected

**Pollutant Features**
- PM2.5
- PM10
- NO2
- SO2
- CO
- Ozone

**Weather Features**
- Temperature
- Humidity
- Wind Speed
- Wind Direction

**Location-Based Features**
- distance_to_major_road_km
- distance_to_industrial_zone_km
- distance_to_dump_site_km
- distance_to_farmland_km

### 3.4 Time Range of Data

- Historical pollution and weather data were collected for the period from **January 2025 to 17 February 2026**
- Real-time weather data was fetched using **Open-Meteo**
- Real-time pollution-related integration was also explored during implementation

---

## 4. Data Preprocessing

Data preprocessing was performed to convert raw data from different sources into a clean and structured format suitable for model development.

### Preprocessing steps performed

- Removed duplicate records
- Handled missing values using suitable cleaning methods
- Cleaned inconsistent entries and standardized column formats
- Processed each dataset separately:
  - Pollution dataset
  - Weather dataset
  - Location feature dataset
- Combined data across multiple cities and stations
- Merged pollution, weather, and location datasets into one unified dataset
- Organized the final dataset with features such as:
  - date
  - temperature
  - humidity
  - wind_speed
  - wind_direction
  - city
  - station
  - latitude
  - longitude
  - pm25
  - pm10
  - no2
  - so2
  - co
  - ozone
  - distance_to_major_road_km
  - distance_to_industrial_zone_km
  - distance_to_dump_site_km
  - distance_to_farmland_km

### Feature Engineering

Feature engineering mainly focused on:
- Integrating pollution, weather, and spatial context
- Creating synthetic location-based distance features
- Preparing labeled data for supervised learning

### Normalization / Scaling

Normalization or scaling can be applied depending on the selected model, though tree-based models such as Random Forest and XGBoost generally do not require heavy feature scaling.

---

## 5. Exploratory Data Analysis (EDA)

Exploratory Data Analysis was carried out to understand patterns in pollution levels, relationships between features, and spatial influence on air quality.

### Key Observations

- High PM2.5 values were commonly associated with areas closer to major roads
- High NO2 and SO2 values were more strongly associated with industrial regions
- Spatial features had a strong impact on source prediction
- Weather conditions affected the spread of pollutants, though their direct importance was lower than key spatial features

### Important Visualizations

- Trend plots for pollutant levels
- Feature importance chart
- Confusion matrix
- Heatmap visualization on map
- Source distribution chart

### Correlation Insights

EDA showed that:
- Distance-based features are strong indicators for pollution source classification
- NO2 and SO2 help indicate industrial influence
- PM2.5 and PM10 are useful indicators for traffic-related pollution

### Patterns Discovered

- Proximity to industrial zones had the strongest impact on model decisions
- Road proximity was also highly significant
- Weather features such as humidity and wind speed had comparatively lower influence on source classification

---

## 6. Source Labeling Methodology

Since no ground-truth dataset was available that directly labels pollution source categories, a **rule-based labeling methodology** was used.

### Labeling Logic

The following logic was used to assign pollution source labels:

- **Traffic:** High PM2.5 values combined with close distance to major roads
- **Industrial:** High NO2 and SO2 values combined with industrial influence
- **Mixed:** Cases where pollution indicators did not strongly belong to a single source
- Additional categories were also supported based on dataset distribution and logic used during implementation

### Assumptions Made

- High PM2.5 near roads likely indicates vehicular pollution
- High NO2 and SO2 indicate industrial contribution
- Distance-based features help represent environmental source influence
- Pollution sources can be approximated using pollutant levels and spatial context

### Limitations of Labeling

- Labels are **simulated** and not based on verified real-world ground truth
- The rule-based approach can introduce bias
- Real environmental conditions can be more complex than predefined threshold rules
- Variations in predicted results may occur due to simplified assumptions

---

## 7. Model Development

The model development phase focused on training machine learning models to classify pollution sources using the processed and labeled dataset.

### Models Used

- Random Forest
- Decision Tree
- XGBoost

### Feature Selection

The features used for model training included:
- Pollutant values
- Weather features
- Latitude and longitude
- Distance-based features

Feature importance analysis was used to understand which variables influenced the model most strongly.

### Train-Test Split

- The dataset was divided using an **80:20 train-test split**

### Hyperparameter Tuning

Model comparison and tuning were performed during experimentation. Training and evaluation were mainly carried out in a **Kaggle notebook environment**, which provided convenient compute resources for testing multiple models.

### Model Training Environment

- Model training was performed on **Kaggle**
- The final trained model was downloaded and stored in the project folder for integration into the application

---

## 8. Model Evaluation

The trained models were evaluated using classification metrics and comparison of overall performance.

### Model Accuracy

- **Random Forest Accuracy:** 0.9914
- **XGBoost Accuracy:** 0.9919

### Selected Model

- **XGBoost** was selected as the final model because it achieved the best overall performance

### Precision, Recall, and F1-Score

The classification report indicated:
- High precision across major classes
- High recall for dominant classes
- High weighted F1-score overall
- Lower performance in rare or low-support classes

### Confusion Matrix

The confusion matrix showed that:
- Most predictions were correctly classified along the diagonal
- Only a small number of instances were misclassified
- Rare classes showed minor imbalance and limited support

### Interpretation of Results

- The model achieved very high accuracy
- Classification performance was strong for major source categories
- Minor imbalance in rare classes affected some class-wise performance
- The results confirm that combining pollutant, weather, and spatial features is effective for source prediction

---

## 9. Geospatial Visualization

Geospatial visualization is one of the main components of EnviroScan and was implemented to show pollution distribution across locations.

### Tools Used

- Folium

### Visualization Features

- Interactive map generation
- Pollution heatmap creation
- Station-based hotspot marking
- Spatial visualization using latitude and longitude of monitoring stations

### Heatmap Generation

Heatmaps were generated to visually represent pollution intensity over geographic space. These heatmaps help identify locations with stronger pollution concentration.

### Marker Logic for Pollution Sources

Markers on the map represent station locations and related pollution analysis outputs. They help users understand where pollution hotspots occur and how station-level data varies across regions.

### High-Risk Zone Identification

High-risk pollution zones can be visually identified using the heatmap and station-based geospatial displays. This makes it easier to interpret pollution concentration and source patterns.

---

## 10. Dashboard Implementation

The EnviroScan dashboard was built using **Streamlit** and acts as the main user interface for the project.

### Dashboard Features

- Station selection
- Date and time input for analysis
- Predicted pollution source display
- Confidence score display
- Pollutant metrics display
- Interactive map and heatmap integration
- Trend charts
- Source distribution visualization
- Alert messages based on pollution levels
- Export option for pollution report

### User Inputs

Users can:
- Select a monitoring station
- Select analysis date
- Select analysis time

### Prediction Display

The dashboard displays:
- Predicted pollution source
- Confidence score
- Current pollutant values such as PM2.5, NO2, SO2, and CO

### Charts and Map Integration

The dashboard includes:
- Interactive Folium map
- Heatmap visualization
- Pollution trend analysis chart
- Source distribution chart

### Alert System

The system displays alert messages to indicate pollution condition status, such as safe or concerning pollution levels.

---

## 11. Results & Outputs

The EnviroScan project successfully produced a complete workflow from data collection to prediction and visualization.

### Key Outcomes Achieved

- Successfully integrated pollution, weather, and location-based datasets
- Built machine learning models for source classification
- Selected XGBoost as the best model
- Generated interactive geospatial maps
- Developed a Streamlit dashboard for user interaction
- Displayed pollution metrics, source prediction, and charts in one interface

### Screenshots 

You should include screenshots of:
- Dashboard displaying pollution prediction results
- <img width="1914" height="912" alt="Screenshot 2026-04-02 153037" src="https://github.com/user-attachments/assets/052e91f5-ccbd-4b6f-82d3-dbfb62542ac3" />

- Interactive heatmap showing pollution hotspot
- <img width="1913" height="917" alt="Screenshot 2026-04-02 153131" src="https://github.com/user-attachments/assets/e73412ed-af37-475e-b8b8-477f2f756bc2" />

-Pollution trend analysis chart & Source distribution visualization
- Source distribution chart
- <img width="1907" height="894" alt="Screenshot 2026-04-02 153230" src="https://github.com/user-attachments/assets/58e232be-4695-4346-8fff-1738c938034b" />

- Confusion matrix of final model
- <img width="763" height="559" alt="Screenshot 2026-04-02 160308" src="https://github.com/user-attachments/assets/64294d10-7e21-434a-a610-662bfd8b705b" />

-Feature importance analysis
- <img width="1020" height="573" alt="Screenshot 2026-04-02 160322" src="https://github.com/user-attachments/assets/031c0ebf-c6f2-4e1b-abac-9995a94cef9c" />


## 12. Limitations

Although EnviroScan produced strong results, the project has several limitations:

- **Simulated location data:** Real distance values could not be extracted reliably, so location-based features were synthetically generated
- **Synthetic distance features:** Exact distances from stations to roads, industrial zones, dump sites, and farmland were difficult to obtain
- **Rule-based labeling bias:** Since labels were generated using rules, prediction results may vary and may not fully reflect real environmental conditions
- **Lack of real-world ground truth:** There is no verified source-labeled pollution dataset for direct validation
- **Limited real-time data integration:** Real-time system capability is partial and not fully automated
- **Dataset coverage limitations:** The dataset includes selected cities and stations, not all locations
- **Incomplete pollutant availability:** Pollutant values may not be equally available for all places and time periods

---

## 13. Future Enhancements

The following improvements can be made in future versions of EnviroScan:

- **Real geospatial data integration**  
  Replace synthetic location features with real GIS-based spatial distances

- **Satellite data usage**  
  Integrate satellite and remote sensing data for broader environmental analysis

- **Advanced machine learning and deep learning models**  
  Explore neural networks, time-series forecasting, and more advanced classification approaches

- **Better real-time alert systems**  
  Provide automated pollution warnings and health recommendations

- **Voice-based interaction**  
  Support audio-based queries such as:
  - What is the AQI today?
  - What is the pollution source?
  - What precautions should I take?

- **Voice-based response system**  
  Return spoken responses for accessibility and convenience

- **React-based frontend**  
  Upgrade from Streamlit to a more scalable frontend if needed

- **Low-literacy-friendly UI design**  
  Improve accessibility using simple layouts, clearer visuals, large controls, and user-friendly design

- **Automated retraining pipeline**  
  Support future model updates as new data becomes available

---

## 14. Project Structure

```text
ENVIRON_SCAN_PROJECT/
│── data/
│   ├── raw/
│   │   ├── pollution_excels/
│   │   ├── location_features.csv
│   │   ├── pollution_data.csv
│   │   └── weather_data.csv
│   ├── processed/
│   │   ├── enviro_labeled_dataset.csv
│   │   └── enviro_merged_dataset.csv
│
│── scripts/
│   ├── collect_weather.py
│   ├── combined.py
│   ├── label_source.py
│   ├── pollutioncleaned.py
│   └── synthetic_locationdata.py
│
│── map/
│   ├── create_map.py
│   └── outputs/
│       └── pollution_map.html
│
│── model/
│   └── pollution_source_model.pkl
│
│── notebooks/
│   └── enviroscan-model-training.ipynb
│
│── app.py
│── README.md
│── LICENSE

How to Run the Project
Step 1: Clone the Repository

git clone <your-repository-link>

cd ENVIRON_SCAN_PROJECT

Step 2: Install Dependencies

pip install -r requirements.txt

Step 3: Launch the Streamlit Dashboard

streamlit run app.py

Technologies Used
Programming Language
Python
Libraries and Frameworks
Pandas
NumPy
Scikit-learn
XGBoost
Folium
Streamlit
Matplotlib / Seaborn (for analysis visualizations, if used in notebook)
Platforms
Kaggle (model training and experimentation)
APIs / Data Sources
CPCB
NASA LARC
Open-Meteo
OpenAQ / related air quality integration explored during implementation
OpenStreetMap / OSMnx (attempted for distance extraction)
17. Deliverables

This project submission includes:

Complete README file in GitHub
Well-structured project repository
Organized raw and processed datasets
Model file
Notebook used for model training
Dashboard implementation
Geospatial map output
Author

Megha Rajeev
Integrated M.Tech in Artificial Intelligence
VIT Bhopal


A couple of quick fixes before you paste it:
- In your repo structure, make sure `map/` is shown correctly if it is inside `scripts/` or outside it. Use the actual folder layout from your project.
- Add your screenshots under `Results & Outputs` in GitHub using image links or drag-and-drop in the README editor.
