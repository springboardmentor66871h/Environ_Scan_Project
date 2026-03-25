🌍 EnviroScan: AI-Powered Pollution Source Identification System
Geospatial Analytics & Machine Learning for Environmental Monitoring

1. Project Title
EnviroScan — An end-to-end AI framework designed to identify and categorize pollution sources using real-time atmospheric data, meteorological conditions, and geospatial mapping.

2. Problem Statement
Air pollution monitoring typically focus on levels (how much) rather than sources (where from). Identifying whether a spike in PM2.5 is caused by local traffic, a nearby factory, or agricultural burning is critical for effective intervention.Importance: Targeted source identification allows for precise policy-making and faster public health alerts.
Limitations: Existing systems often rely on static sensors and lack the integration of real-time geospatial features (like proximity to roads or factories) to explain why pollution is occurring.

3. Objectives
Predict Pollution Sources: Use Machine Learning to classify pollution causes (Industrial, Vehicular, etc.).
Visualize Hotspots: Map real-time data onto an interactive geospatial heatmap.
Real-time Alerts: Provide dynamic warning banners when pollutant levels cross safety thresholds.

4. Dataset Description
This project utilizes 100% real-world, live data fetched dynamically via global APIs across ~350 unique geographic coordinates in India.
Data Sources:OpenAQ (v3): Live pollutant concentrations ($PM_{2.5}, PM_{10}, NO_2, CO, SO_2, O_3$).
OpenWeatherMap: Current Temperature, Humidity, and Wind Speed/Direction.
OSMnx (OpenStreetMap): Calculated precise geographic distances (in meters) to infrastructure.
Features Collected: Pollutant values, weather parameters, and proximity distances to highways, industrial zones, agricultural lands, and waste dumps.

5. System Architecture
EnviroScan follows a modular, three-tier architecture to ensure scalability and separation of concerns.
Architecture Components:Data Ingestion Layer: Foundational layer using custom scripts to fetch data from OpenAQ, OpenWeatherMap, and OSMnx APIs.
Processing & Machine Learning Layer: The core intelligence hub handling missing value imputation, spatial coordinate mapping (projected CRS), and feature encoding. It houses the Random Forest classifier for real-time inference.
Presentation Layer: User-facing Streamlit dashboard rendering model predictions, real-time alerts, Folium geospatial heatmaps, and Plotly analytics.

6. Data Preprocessing
Handling Missing Values: Imputation strategies were applied to sensor gaps.
Filtering: Old or broken sensor data (e.g., pre-2020) was strictly removed to ensure temporal accuracy.
Feature Engineering: Calculation of "Distance to Source" using OSMnx and encoding wind direction into cyclical features.Data Architecture: Replaced synthetic spatial data with real-world geographic features to ensure the model learns actual spatial relationships.

7. Exploratory Data Analysis (EDA)
Key Observations: Strong correlation between $NO_2$ levels and proximity to major highways.
Patterns: High $SO_2$ concentrations were consistently mapped within a 5km radius of designated industrial zones.Visualizations: Distribution plots revealed a heavy right-tail in PM10 values during low-wind conditions.

8. Source Labeling Methodology
IMPORTANT: Because real-world ground-truth labels for specific sources are unavailable, labels are simulated using deterministic heuristic rules.
Labeling Logic:
Industrial: Distance to industry < 5000m AND (pollutant is $SO_2$ or $NO_2$).
Vehicular: Distance to road < 4000m AND (pollutant is $NO_2$ or $CO$).
Agricultural: Distance to farmland < 5000m AND (pollutant is $PM_{10}$ or $PM_{2.5}$).
Limitations: These rules are approximations and do not account for complex atmospheric chemical dispersion.

9. Model Development
Models Evaluated: XGBoost and Random Forest Classifier.
Feature Selection: Included pollutant type, value, weather metrics, and four proximity distance features.
Hyperparameter Tuning: Performed using GridSearchCV on n_estimators and max_depth.
Selected Model: Random Forest Classifier, chosen for its robustness against noise and non-linear geospatial relationships.

10. Model Evaluation
Accuracy: 90.50%Precision/Recall: Consistently strong across Industrial and Vehicular categories.
Interpretation: To avoid overfitting (which initially showed 99% accuracy), "Real-World Noise" (10% random glitch rate) was injected. This forced the model to learn complex relationships rather than just memorizing rules.

11. Geospatial Visualization
Tools: Folium and GeoPandas.Heatmap 
Layer: Visualizes overall pollution intensity across the map.
Marker Logic: Custom FontAwesome icons (Factories, Cars, Leaves) indicate the predicted source of pollution at specific coordinates.

12. Dashboard Implementation
The Streamlit dashboard serves as the central interface:Real-Time 
Alerts: Triggers warning banners when values exceed safety thresholds (e.g., > 150).
Interactive Controls: Checkbox layers to isolate specific pollution sources (e.g., "Show only Industrial").
Trend Analytics: Interactive Plotly pie charts and bar charts for national source distribution.

13. Results & Outputs
Key Outcome: Successfully created a PoC that maps live API data to predicted pollution causes with high visual clarity.

14. Limitations
Rule-based Labeling: The model is trained on simulated labels, not verified ground-truth "on-the-ground" data.API Rate Limits: Dataset size is constrained to respect free-tier limits of live APIs.
Atmospheric Complexity: Current logic doesn't fully account for regional background pollution drift.

15. Future Enhancements
Satellite Data: Integration of Sentinel-5P satellite imagery for broader coverage.
Advanced ML: Implementation of LSTM models for temporal forecasting.
Real-time API Expansion: Expanding data collection to international cities.

16. Project Structure
PlaintextEnviroScan_Project/
├── data/
│   ├── raw/                # Raw API downloads
│   └── processed/          # Merged and labeled datasets
├── models/                 # Exported .pkl models
├── collect_pollution.py    # Fetch OpenAQ data
├── collect_weather.py      # Fetch OpenWeatherMap data
├── extract_location_features.py # Fetch OSMnx spatial distances
├── train_model.py          # Model training & tuning
├── app.py                  # Main Streamlit Dashboard
└── README.md               # Project documentation

17. How to Run the Project
Clone the repository: git clone <repo-link>
Install dependencies: pip install -r requirements.txtRun 
the dashboard: streamlit run app.py

18. Technologies Used
Languages & Libraries: Python, Pandas, NumPy, Scikit-learn, XGBoost.
Geospatial: Folium, OSMnx, GeoPandas.
APIs: OpenAQ, OpenWeatherMap.