# 🌍 EnviroScan – AI-Powered Pollution Source Identification using Geospatial Analytics

EnviroScan is an AI-based system designed to identify dominant pollution sources using environmental data, weather conditions, and geospatial features. It combines machine learning and geospatial analytics to provide insights into pollution patterns and sources.

---

## 📌 Problem Statement

Air pollution monitoring systems typically measure pollutant levels but fail to identify the **source of pollution** (vehicular, industrial, agricultural, etc.).

Without source identification, it becomes difficult to take targeted corrective actions. EnviroScan addresses this gap by predicting pollution sources using environmental and spatial data.

---

## 🎯 Objectives

- Predict pollution sources using machine learning  
- Visualize pollution trends and hotspots  
- Provide pollution alerts based on thresholds  
- Build an interactive dashboard for monitoring  

---

## 📊 Dataset Description

### Data Sources
- OpenWeatherMap API (Pollution + Weather)
- OpenStreetMap (OSMnx) for geospatial features

### Cities Covered
- Delhi  
- Mumbai  
- Hyderabad  
- Chennai  
- Kolkata  

### Features

#### Pollution Parameters
- PM2.5, PM10, NO₂, CO, SO₂, O₃  

#### Weather Parameters
- Temperature  
- Humidity  
- Wind Speed  
- Wind Direction  

#### Geospatial Features
- Distance to road  
- Distance to industry  
- Distance to farmland  
- Distance to dump site  

### Dataset Summary
- ~14,255 records  
- Balanced across cities  
- ~4 months of data  

---

## 🧹 Data Preprocessing

- Converted timestamps into datetime format  
- Removed missing values and duplicates  
- Cleaned city names  
- Generated distance-based features  
- Structured dataset for modeling  

---

## 📈 Exploratory Data Analysis (EDA)

- Identified pollution trends across cities  
- Observed temporal variations in pollutants  
- Analyzed relationships between weather and pollution  
- Visualized pollutant distributions  

---

## 🏷️ Source Labeling Methodology

Pollution sources were labeled using rule-based logic based on pollutant thresholds and spatial proximity.

### Label Categories
- Vehicular  
- Industrial  
- Agricultural  
- Burning  
- Natural  

### Labeling Logic

**Burning**
- PM2.5 > 180  
- Distance to dump < 5000m  

**Industrial**
- SO₂ > 25  
- Distance to industry < 4000m  

**Vehicular**
- NO₂ > 50 & Distance to road < 3000m  

**Agricultural**
- PM2.5 > 120  
- Distance to farmland < 6000m  

**Natural**
- Default category  

⚠️ **Important Note**:  
Labels are **simulated** due to lack of real-world ground truth data.

---

## 🤖 Model Development

### Models Used
- Decision Tree  
- Random Forest  
- XGBoost  

### Training Setup
- Train-test split: 80/20  
- Stratified sampling  
- GridSearchCV for tuning  

### Best Model
XGBoost (highest F1-score)

---

## 📊 Model Evaluation

- Accuracy: **99.02%**  
- Weighted F1-score: **0.99**  

### Interpretation
High accuracy is expected due to rule-based labeling. Tree-based models effectively learn threshold-based decision rules.

---

## 🗺️ Geospatial Visualization

- Used **Folium** for mapping  
- Created pollution heatmaps  
- Added location markers  
- Highlighted high pollution areas  

---

## 📊 Dashboard Implementation

The dashboard was built using **Streamlit**.

### Features

- City selection  
- Pollution source prediction  
- Confidence score display  
- AQI status indicator  
- Pollution alerts  
- Trend charts  
- Source distribution visualization  
- Interactive map with controls  
- Downloadable pollution reports  

---

## 📌 Results & Outputs

- Successfully predicted pollution sources  
- Visualized pollution trends and hotspots  
- Provided alert system for unsafe conditions  
- Built a user-friendly dashboard  

---

## ⚠️ Limitations

- Rule-based labeling (not real-world verified)  
- No ground truth data  
- Limited dataset (~4 months)  
- Static dataset (not real-time APIs)  

---

## 🚀 Future Enhancements

- Integration with real-time APIs  
- Advanced ML/DL models  
- Mobile-based alert system  
- Satellite data integration  
- Improved labeling techniques  

---

## 📁 Project Structure


ENVIRON-SCAN/
│
├── data/
│ └── processed/
│ └── final_dataset.csv
│
├── models/
│ └── best_model.joblib
│
├── dashboard.py
├── README.md


---

## ▶️ How to Run the Project

### Install Dependencies

        pip install -r requirements.txt


### Run Dashboard

        streamlit run dashboard.py


---

## 🛠️ Technologies Used

- Python  
- Pandas, NumPy  
- Scikit-learn  
- XGBoost  
- Plotly  
- Folium  
- Streamlit  

---

## 📸 Screenshots

(Add screenshots here)

- Dashboard UI  
- Pollution Map  
- Charts  

---

## 🙌 Conclusion

EnviroScan demonstrates how machine learning and geospatial analytics can be combined to identify pollution sources and provide actionable insights for environmental monitoring.

---

## 👩‍💻 Author

Rushda  
