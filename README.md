# EnviroScan: AI-Based Pollution Source Identification System

EnviroScan is an AI-based system that analyzes environmental data to identify pollution sources using machine learning and geospatial analytics.

---

## 1. Problem Statement

Air pollution is a major environmental issue that affects human health and ecosystems. Identifying pollution sources is difficult because:

- Data is collected from different sources and not integrated  
- Existing systems only monitor pollution levels  
- There is no direct mapping between pollution and its sources  

This project aims to solve these problems by combining multiple datasets and predicting pollution sources.

---

## 2. Objectives

- Predict pollution sources using machine learning  
- Analyze environmental and weather data  
- Visualize pollution hotspots  
- Build an interactive dashboard  
- Provide alerts for high pollution levels  

---

## 3. Dataset Description

### Raw Dataset (data/raw)

- india_air_pollution_cleaned.csv contains pollution data  
- india_weather_dataset_new.csv contains weather data  
- location.csv contains geographical data  

### Processed Dataset (data/processed)

- final_environment_dataset.csv is the combined dataset after preprocessing  

### Features Used

- Pollution parameters such as PM2.5, PM10, NO2  
- Weather parameters such as temperature, humidity, wind speed  
- Location features such as latitude and longitude  
- Additional engineered features  

---

## 4. Data Preprocessing

The following steps were performed:

- Handling missing values  
- Removing duplicate records  
- Cleaning inconsistent data  
- Merging pollution, weather, and location datasets  
- Feature engineering  

Final dataset location:
data/processed/final_environment_dataset.csv

---

## 5. Exploratory Data Analysis

Key observations:

- PM2.5 and PM10 show strong correlation  
- Pollution levels increase when wind speed is low  
- Some locations consistently show higher pollution  

Visualizations include:

- Correlation analysis  
- Distribution plots  
- Trend analysis  

---

## 6. Source Labeling Methodology

Since real-world labels are not available, rule-based labeling is used.

Example logic:

- High PM2.5 values indicate industrial sources  
- Medium pollution indicates vehicular sources  
- Low pollution indicates natural sources  

Important note:

Labels are simulated and not based on real ground truth data.

---

## 7. Model Development

### Model Files (models)

- pollution_source_model.joblib contains the trained model  
- label_encoder.joblib is used for encoding labels  

### Models Used

- Random Forest  
- Decision Tree  

### Process

- Feature selection  
- Train-test split using 80:20 ratio  
- Model training using scikit-learn  
- Saving the model using joblib  

---

## 8. Model Evaluation

Evaluation metrics used:

- Accuracy  
- Precision  
- Recall  
- F1 Score  

Result:

The model performs well on simulated data and provides good classification of pollution sources.

---

## 9. Geospatial Visualization

Tools used:

- Folium  

Features:

- Pollution heatmaps  
- Location markers  
- Identification of high-risk areas  

Files:

- map_visualization.py  
- pollution_map.html  

---

## 10. Dashboard Implementation

The dashboard is developed using Streamlit.

Features:

- User input for location  
- Pollution prediction display  
- Charts and graphs  
- Map visualization  
- High pollution alert system  

Files:

- dashboardd.py  
- templates/index.html  

<img width="1897" height="721" alt="image" src="https://github.com/user-attachments/assets/5d6f6367-773c-4ea0-a3f1-2b89caf10d04" />


<img width="1423" height="522" alt="image" src="https://github.com/user-attachments/assets/2db16bb9-e05e-41f2-89e9-c22745f5b491" />


<img width="1479" height="542" alt="image" src="https://github.com/user-attachments/assets/37a69dfb-951e-44d8-8b05-81795e66c106" />


<img width="1467" height="842" alt="image" src="https://github.com/user-attachments/assets/331bcfab-beef-46dc-9854-c76c01af4e40" />


<img width="1465" height="824" alt="image" src="https://github.com/user-attachments/assets/bb57a936-2786-42d7-9046-4d899d500bca" />







































































---

## 11. Results and Outputs

Outputs generated:

- Pollution prediction system  
- Interactive dashboard  
- Heatmap visualization  
- Processed dataset  

Screenshots to include:

- Dashboard interface  
- Maps  
- Graphs  

---

## 12. Limitations

- Rule-based labeling is not fully accurate  
- No real-world labeled dataset  
- Limited data availability  
- Model performance depends on simulated labels  

---

## 13. Future Enhancements

- Integration with real-time APIs  
- Use of advanced machine learning models  
- Integration of satellite data  
- Improved alert system  
- Deployment on cloud platforms  

---

## 14. Project Structure

AI_Price_Optima/
│
├── data/
│   ├── raw/
│   │   ├── india_air_pollution_cleaned.csv
│   │   ├── india_weather_dataset_new.csv
│   │   └── location.csv
│   │
│   └── processed/
│       └── final_environment_dataset.csv
│
├── models/
│   ├── pollution_source_model.joblib
│   └── label_encoder.joblib
│
├── templates/
│   └── index.html
│
├── app.py
├── collect_pollution.py
├── collect_weather.py
├── combine_datasets.py
├── extract_location_features.py
├── map_visualization.py
├── predict.py
├── train_model.py
├── dashboardd.py
├── pollution_source.py
│
└── README.md
## 15. How to Run the Project

Step 1: Install dependencies
        pip install pandas numpy scikit-learn streamlit folium joblib

Step 2: Run data processing
        python combine_datasets.py

Step 3: Train model
        python train_model.py

Step 4: Run prediction
        python predict.py

Step 5: Run dashboard
        python -m streamlit run dashboardd.py

## 16.TECHNOLOGIES USED

* Python
* Pandas
* NumPy
* Scikit learn
* Folium
* Streamlit
* OpenAQ API
* OpenWeatherMap API
* OSMnx

---

## CONCLUSION

* EnviroScan provides a complete pipeline from data collection to prediction and visualization
* It helps in understanding pollution patterns and possible sources
* The system supports environmental monitoring and analysis


