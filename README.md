EnviroScan: AI-Powered Pollution Source Identification using Geospatial Analytics
Project Overview
EnviroScan is an AI-driven initiative designed to identify and predict the primary sources of air pollution (e.g., Vehicular, Industrial, Agricultural) in specific geographic locations. By combining live atmospheric pollutant data, weather conditions, and geospatial proximity features, this project aims to provide actionable environmental intelligence.

📂 Repository Structure
Plaintext
EnviroScan/
│
├── data/
│   ├── raw/                            # Raw data fetched from APIs
│   └── processed/
│       └── final_combined_dataset.csv  # Merged dataset used for modeling
│
├── models/                             # Exported model artifacts (Week 4)
│   ├── best_pollution_model.joblib     # Trained LightGBM model
│   ├── label_encoder.joblib            # Target variable encoder
│   └── feature_scaler.joblib           # StandardScaler for numerical features
│
├── notebooks/
│   └── Week4_Model_Training.ipynb      # Colab notebook containing model training and evaluation
│
├── visuals/                            # Evaluation charts
│   ├── confusion_matrix.png            
│   └── feature_importance.png          
│
└── README.md                           # Project documentation
📅 Project Progression
Milestone 1 (Weeks 1 & 2): Data Collection & Preparation
Pollution Data: Sourced PM2.5, PM10, NO₂, CO, SO₂, and O₃ levels using the OpenAQ API.

Weather Data: Sourced Temperature, Humidity, Wind Speed, and Wind Direction using the OpenWeatherMap API.

Geospatial Features: Extracted distance metrics (Distance to Road, Industry, Dump Site, Farmland) using OpenStreetMap / OSMnx.

Result: Merged into a unified dataset containing atmospheric, meteorological, and spatial variables.

Milestone 2 (Week 3): Source Labeling & Simulation
Due to the absence of real-world ground-truth labels for pollution sources, we engineered the target variable (pollution_source) using logical, rule-based heuristics.

Categories Simulated: Vehicular, Industrial, Agricultural, Burning, Natural.

Logic Example: NO2 > Threshold + Distance to Road < 1.0km = Vehicular.

Limitation: These labels represent logical environmental assumptions rather than sensor-verified truth.

Milestone 2 (Week 4): Model Training & Source Prediction
This phase focused on training a machine learning classification model to automatically predict the pollution_source variable based on our engineered dataset.

1. Model Selection:
We evaluated 12 different classification algorithms (including Random Forest, XGBoost, Support Vector Machines, and Neural Networks) using 5-fold cross-validation.

Selected Model: LightGBM was chosen as it achieved the highest cross-validation score and handled the complex feature interactions flawlessly.

2. Data Preprocessing:

Categorical targets were mapped using LabelEncoder.

All numerical input features were normalized using StandardScaler prior to training to ensure uniform feature weighting.

3. Performance Metrics (Evaluated on 20% Unseen Test Data):

Accuracy: 0.9970 (99.70%)

Precision: 0.9970

Recall: 0.9970

F1-Score: 0.9970

4. Observations and Project Limitations:
The LightGBM model achieved near-perfect accuracy. While this demonstrates highly successful algorithmic training and hyperparameter tuning, it is critical to acknowledge the primary limitation of this phase: because our training labels were generated deterministically in Week 3 using strict IF/ELSE rules, the model has essentially learned to reverse-engineer those exact static thresholds.

In a real-world deployment scenario, this model would need to be retrained on authenticated, ground-truth data to accurately capture true atmospheric dispersion complexities and avoid propagating rule-based biases.
