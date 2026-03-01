# 🌍 EnviroScan – AI-Powered Pollution Source Identification using Geospatial Analytics

## 📌 Project Overview
EnviroScan is an AI-driven system designed to identify dominant pollution sources using environmental data, weather conditions, and geospatial proximity features.

The system integrates:
- Air pollution measurements
- Weather parameters
- Geospatial distance features
- Rule-based source labeling

This project is being developed in milestone phases.

---

# 🚀 Milestone 1 – Week 1  
## Data Collection & Dataset Preparation

### Objective
Collect and structure environmental data for model development.

### Data Sources
- OpenWeatherMap API (Air Pollution & Weather Data)
- OpenStreetMap (OSMnx) for geospatial feature extraction

### Cities Selected
- Delhi
- Mumbai
- Hyderabad
- Chennai
- Kolkata

### Data Collected
Pollution Parameters:
- PM2.5
- PM10
- NO₂
- CO
- SO₂
- O₃

Weather Parameters:
- Temperature
- Humidity
- Wind Speed
- Wind Direction

Geospatial Features:
- Distance to nearest road
- Distance to nearest industrial zone
- Distance to nearest farmland
- Distance to nearest dump site

### Folder Structure
data/
├── raw/
└── processed/



# 🌐 Milestone 1 – Week 2  
## Geospatial Feature Engineering & Data Merging

### Key Improvements
- Created multiple spatial sampling points per city
- Computed realistic distance-based features using OSMnx
- Merged pollution, weather, and geospatial datasets
- Ensured no missing values
- Verified class balance across cities

### Final Dataset
- 14,255 rows
- Balanced city distribution
- Cleaned coordinate handling
- Structured features ready for labeling

# 🏷 Milestone 2 – Week 3  
## Pollution Source Labeling (Simulated)

### Objective
Create a target variable `pollution_source` using environmental heuristics.

Since real-world ground truth labels were unavailable, rule-based labeling was implemented using pollutant thresholds and proximity indicators.

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
- OR peak traffic hours with moderate NO₂

**Agricultural**
- PM2.5 > 120
- Distance to farmland < 6000m
- Winter / Post-Monsoon season

**Natural**
- Assigned when none of the above conditions were satisfied

### Assumptions
- Thresholds were chosen based on AQI standards and environmental research.
- Proximity to emission sources increases likelihood of source contribution.
- Seasonal context influences agricultural burning patterns.

### Limitations
- Labels are simulated due to absence of verified source-level ground truth.
- Rule-based logic may introduce bias.
- Real-world deployment would require validated emission inventory data.


 📊 Label Distribution
A visualization of source distribution is included in: data/processed/label_distribution.png


🔒 Security Update
API keys are stored using environment variables and are not included in this repository.


📅 Next Phase
Milestone 3 (Week 4):
- Model Training
- Classification using ML algorithms
- Performance Evaluation
- Feature Importance Analysis

# 🤖 Milestone  3– Week 4  
## Model Training & Source Prediction

### Objective
To train and evaluate machine learning models capable of predicting the `pollution_source` variable.


### Models Trained
- Decision Tree
- Random Forest
- XGBoost

Hyperparameter tuning was performed using GridSearchCV with 5-fold cross-validation.



### Train-Test Split
- 80% Training Data
- 20% Testing Data
- random_state = 42
- Stratified sampling used



### Best Model Selected
XGBoost

Selected based on highest cross-validation weighted F1-score.

### Model Performance (Test Set)

- Accuracy: 99.02%
- Weighted F1-score: 0.99

All classes achieved strong precision and recall.


### Interpretation

The high performance is expected because the dataset was labeled using deterministic rule-based heuristics. Tree-based models such as XGBoost are highly effective at learning threshold-based decision boundaries.

No significant overfitting was observed as training and testing performance were similar.



### Feature Importance

Most influential features:
- SO₂
- PM2.5
- Distance to Industry
- Distance to Dump
- NO₂
- Distance to Road

This aligns with environmental logic used during rule-based labeling.

### Model Export

The trained model is saved as:
models/best_model.joblib

This model will be integrated into the dashboard in the next milestone.

👩‍💻 Author
Rushda – CSE (Data Science)

