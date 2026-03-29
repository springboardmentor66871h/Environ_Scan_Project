# EnviroScan: AI-Based Pollution Source Identification System

**EnviroScan** is a high-fidelity environmental intelligence platform designed to identify pollution sources across **50 Indian cities**. It leverages machine learning to classify emission origins and uses geospatial analytics to provide a real-time command-and-control dashboard for air quality management.

---

## Problem Statement
Air pollution monitoring systems globally provide "what" and "when" (pollutant levels), but fail to provide the "where" and "why" (source identification). 

**Key Challenges:**
* **Attribution:** Difficulty in determining if a specific spike is due to vehicle density or industrial discharge.
* **Ground Truth Scarcity:** No large-scale, publicly available labeled datasets exist for automated source classification.
* **Complex Overlaps:** Multiple pollution sources often interact in urban environments, making manual identification impossible at scale.

---

## Objectives
* **Source Attribution:** Automate the classification of pollution into 5 key categories using Random Forest models.
* **Geospatial Hotspot Mapping:** Visualize city-wide pollution density using interactive Folium heatmaps.
* **Real-Time Warning System:** Implement automated alerts for AQI threshold breaches.
* **Multi-City Intelligence:** Analyze trends across a diverse set of 50 urban centers in India.

---

## Dataset Description
* **Data Sources:** * **OpenAQ & OpenWeatherMap APIs:** High-frequency pulls for pollutants and meteorology.
    * **OSMnx (OpenStreetMap):** Extracted infrastructure data for 50 cities.
* **Cities Selected:** **50 Major Indian Cities** (including Tier-1 hubs like Delhi/Mumbai and Tier-2 regions) to ensure geographic and climatic diversity.
* **Features:** * **Primary Pollutants:** PM25, PM10, NO2, SO2, CO, O3.
    * **Weather:** Temperature, Humidity, Wind Speed, Wind Direction.
    * **Engineered Proximity:** `Dist_Road_km`, `Dist_Industry_km`, `Dist_Dump_km`, `Dist_Farmland_km`.

---

## Data Preprocessing
* **Cleaning:** Dropped null values and duplicates using Pandas to ensure high data integrity.
* **Variable Normalization:** Consolidated all pollutant formats (e.g., PM2.5) into a uniform **`PM25`** naming convention.
* **Gaussian Noise Injection:** Introduced **0.05 standard deviation Gaussian noise** to simulate real-world sensor drift and environmental variance.
* **Feature Engineering:** Calculated **AQI** based on Indian National Air Quality Standards (NAAQS).

---

## Detailed Exploratory Data Analysis (EDA)
Comprehensive analysis revealed high-value insights across the 50 cities:
* **The "Urban Corridor" Effect:** Cities with high road density (`Dist_Road_km` < 0.3) showed a **42% higher baseline for NO2**.
* **The Inverse Weather Law:** A strong negative correlation (**-0.68**) was observed between Wind Speed and PM25; low-wind cities acted as "pollutant traps."
* **Signature Consistency:** Industrial cities (e.g., Ahmedabad) exhibited high SO2 spikes regardless of traffic patterns.
* **Diurnal Variation:** Pollution levels peaked between **7:00 AM – 10:00 AM**, correlating with peak traffic and morning temperature inversions.

---

## Source Labeling Methodology
In the absence of physical ground truth, a robust **Logic-Heuristic Rule Engine** was developed in `source_labeling.py`:

| Source Category | Rule Logic | Signature Features |
| :--- | :--- | :--- |
| **VEHICULAR** | High PM25 + High NO2 | `Dist_Road_km` < 0.5 & `NO2` > 40 |
| **INDUSTRIAL** | High SO2 + Proximity to Industry | `Dist_Industry_km` < 1.0 & `SO2` > 20 |
| **AGRICULTURAL** | High PM10 + Farmland Proximity | `Dist_Farmland_km` < 2.0 & `PM10` > 80 |
| **BURNING** | Extreme PM25 + Proximity to Dumps | `Dist_Dump_km` < 1.0 & `PM25` > 200 |
| **NATURAL** | Low Pollutants Across All Categories | `Dist_Features` > 5.0 km & `AQI` < 50 |

---

## Model Development & Evaluation
* **Final Selected Model:** Random Forest Classifier (Tuned).
* **Metrics Post-Noise Injection:**
    * **Decision Tree:** 93.22% Accuracy.
    * **Random Forest:** **94.89% Accuracy** (Selected for final deployment).
* **Feature Importance:** Proximity features (`Dist_Road_km`) and `Wind Speed` were the most influential variables.

---

## Geospatial Visualization
* **Folium Heatmaps:** Dynamic rendering of PM25 concentrations.
* **Marker Clusters:** Grouped pollution sources across 50 cities to prevent UI clutter.
* **Hotspot Logic:** Dark red circular icons highlight stations where current AQI > 150.

---

## Dashboard Implementation (Streamlit)
* **Real-Time API Sync:** Connects to OpenWeather API for live data fetching.
* **Multi-Tab Interface:** * **Map:** Geospatial visual data.
    * **Sources:** Pie and bar charts of source distribution.
    * **AI Model:** Performance metrics and confusion matrices.
    * **Download:** Exporting city-specific CSV reports.

---

## Results & Outputs

### Dashboard Overview
<img width="1919" height="1019" alt="Dashboard" src="https://github.com/user-attachments/assets/69fd4edd-2641-46f8-85bc-023e6e1852c6" />


### Map Visualization
<img width="1920" height="1080" alt="Heatmap" src="https://github.com/user-attachments/assets/9b11fb39-2881-4cb1-923d-7094ddcb8992" />


### Analytics & Charts
<img width="1920" height="1080" alt="Charts" src="https://github.com/user-attachments/assets/74038b8a-167e-4c1b-a7a1-b58a0ab1fb42" />


---

## Project Structure

```text
Environ_Scan_Project/
│
├── Models/                        # Machine Learning Assets
│   ├── pollution_model.pkl        # Final Random Forest model (94.89% Accuracy)
│   └── label_encoder.pkl          # Source class mappings
│
├── Processed/                     # Cleaned & Labeled Datasets
│   ├── dataset_with_predictions.csv # Master file for 50 cities
│   ├── training_data.zip          # 80% Training split
│   ├── testing_data.zip           # 20% Evaluation split
│   └── Final_Labeled_Dataset.csv  # Generated from labeling logic
│
├── raw/                           # Original API Pulls (50 Cities)
│   ├── Delhi.csv
│   ├── Mumbai.csv
│   └── ... [48 other city CSV files]
│
├── Scripts/                       # Core Python Logic
│   ├── app.py                     # Main Dashboard App
│   ├── train_data.py              # Training script with noise injection
│   ├── source_labeling.py         # Heuristic logic engine
│   ├── Split_data.py              # Train-Test splitter
│   ├── generate_geospatial_data.py # Data normalizer
│   └── generate_map.py            # Folium HTML generator
│
├── Visualizations/                # Generated Plots & Maps
│   ├── pollution_map.html         # Interactive Map
│   ├── feature_importance.png     # Model importance chart
│   └── confusion_matrix_rf.png    # Final performance matrix
│
├── LICENSE                        # Project License
└── README.md                      # Project Documentation
```

---

## 🛠️ Technologies Used

* **Backend:** Python (`Pandas`, `NumPy`, `Scikit-Learn`, `Joblib`)
* **Visualization:** `Plotly`, `Folium`
* **UI Framework:** `Streamlit`
* **Data APIs:** OpenAQ, OpenWeatherMap, OSMnx

---

**Developed by:** Venkata Ajay Kilaru  
**Internship:** Infosys Springboard Virtual Internship 2026
