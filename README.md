# 1. Project Title
**EnviroScan: AI-Based Pollution Source Identification System using Geospatial Analytics**

An end-to-end machine learning pipeline and interactive dashboard designed to analyze environmental data, predict likely pollution sources, and visualize high-risk hotspots.

---

# 2. Problem Statement
Identifying the exact sources of urban air pollution is critical for public health interventions and environmental policy. However, existing monitoring systems often rely on sparse sensor networks and fail to integrate real-time meteorological conditions with local geospatial features (like proximity to factories or highways). This project addresses this gap by merging air quality metrics, weather data, and physical map features to intelligently estimate and visualize where pollution is originating.

---

# 3. Objectives
* **Predict pollution sources** based on the convergence of air quality, weather, and proximity data.
* **Visualize pollution hotspots** and high-risk zones using interactive geospatial heatmaps.
* **Provide an interactive dashboard** with real-time alerts and user-driven data exploration to assist decision-makers.

---

# 4. Dataset Description
The dataset was custom-built using the following APIs and sources:
* **OpenAQ (Pollution Data):** Collected metrics for PM2.5, PM10, NO₂, CO, SO₂, and O₃.
* **OpenWeatherMap (Weather Data):** Collected Temperature, Humidity, Wind speed, and Wind direction.
* **OpenStreetMap / OSMnx (Location Features):** Extracted distance-based geospatial features (proximity to roads, industrial zones, dump sites, and agricultural fields).

* **Cities Selected:** Bangalore, Chennai, Tirupati
* **Time Range of Data:** January 2026 - February 2026

---

# 5. Data Preprocessing
To prepare the raw data for machine learning, the following steps were executed:
* **Handling Missing Values:** Missing API readings were addressed using forward-filling for time-series consistency and dropping rows with missing spatial coordinates.
* **Removing Duplicates:** Ensured all timestamp-location pairings were strictly unique.
* **Data Cleaning:** Standardized column names and formatted timestamps into datetime objects.
* **Feature Engineering:** Combined wind direction and proximity tags to create contextual features.
* **Normalization/Scaling:** Applied `StandardScaler` to numerical weather and pollution values to ensure equal feature weighting for the models.

---

# 6. Exploratory Data Analysis (EDA)
* **Key Observations:** PM2.5 and PM10 levels showed significant spikes during specific wind directions pointing from industrial zones.
* **Important Visualizations:** Generated correlation heatmaps and time-series line charts for pollutant trends across the three cities.
* **Patterns Discovered:** High NO₂ concentrations were strongly correlated with the 'Near_Road' boolean feature, indicating heavy vehicular traffic impact.

---

# 7. Source Labeling Methodology
**Important Note:** Due to the lack of real-world ground truth data identifying exact emission sources, the target labels for this dataset were simulated.
* **Rule-Based Logic:** A synthetic labeling function was created based on environmental domain knowledge.
* **Thresholds Used:** For example, if NO₂ > 30.0 and `Near_Road` == True, the source was labeled "Vehicular". If SO₂ was high and `Near_Industry` == True, it was labeled "Industrial".
* **Assumptions & Limitations:** These labels are simulated logic approximations meant to prove the system architecture and pipeline, not definitive real-world source confirmations.

---

# 8. Model Development
* **Models Evaluated:** Random Forest Classifier, Decision Tree, and XGBoost.
* **Feature Selection:** Dropped highly collinear variables and non-predictive identifiers (like raw City strings) before training.
* **Train-Test Split:** Data was split using an 80/20 ratio for training and validation.
* **Hyperparameter Tuning:** Applied `GridSearchCV` to optimize tree depth and estimators for the best-performing model.

---

# 9. Model Evaluation
The final selected model (Random Forest) yielded the following results on the test set:
* **Accuracy:** 92%
* **Precision:** 90%
* **Recall:** 91%
* **F1-Score:** 90.5%

*Interpretation:* The confusion matrix revealed that the model was highly successful at classifying Industrial and Vehicular sources, but occasionally confused minor local sources due to overlapping threshold parameters in the simulated data.

---

# 10. Geospatial Visualization
* **Tools Used:** Folium and GeoPandas.
* **Heatmap Generation:** Created density heatmaps based on PM2.5 and PM10 concentrations across the selected city coordinates.
* **Marker Logic:** Color-coded map markers were deployed to signify predicted pollution sources (e.g., Red for Industrial, Blue for Vehicular).
* **High-Risk Zones:** Zones exceeding safe AQI thresholds were visually highlighted on the interactive map.

---

# 11. Dashboard Implementation
The final deliverable is an interactive web application built with **Streamlit**.
* **User Inputs:** Users can select specific cities or input custom weather/pollution metrics via the sidebar.
* **Prediction Display:** The dashboard outputs the AI-predicted pollution source instantly based on the loaded `.joblib` model.
* **Charts & Map Integration:** Embeds the Folium interactive map and renders real-time EDA charts.
* **Alert System:** Displays dynamic warning banners if inputted PM2.5/PM10 levels exceed standard safety limits.

---

# 12. Results & Outputs
*(Note to evaluator: Screenshots can be found in the repository root directory)*

* **Dashboard Interface:** See `Screenshot 2026-03-04 024708.png`
* **Geospatial Heatmap:** See `Screenshot 2026-03-04 024720.png`
* **Model Evaluation Charts:** See `Screenshot 2026-03-04 024738.png`

**Outcomes Achieved:** Successfully built a reproducible pipeline that transforms disparate environmental APIs into a unified, predictive geospatial dashboard.

---

# 13. Limitations
* **Simulated Target Data:** The rule-based labeling approach is a proxy; it does not represent verified ground truth.
* **Data Constraints:** Relies heavily on the historical uptime and sensor accuracy of the OpenAQ and OpenWeather APIs.
* **Static Distances:** OSMnx radius searches represent static proximity, not dynamic real-world wind dispersion modeling.

---

# 14. Future Enhancements
* **Real-time API Integration:** Upgrading the dashboard to automatically pull live data on a cron schedule rather than relying on static CSVs.
* **Advanced ML Models:** Implementing Deep Learning (CNNs) or sequential models (LSTMs) for time-series forecasting.
* **Satellite Data Usage:** Integrating satellite imagery (e.g., Sentinel-5P) to track emission plumes visually.
* **Better Alert Systems:** Adding SMS or email notification integrations for critical pollution spikes.

---

# 15. Project Structure
For ease of access and deployment, all project files are housed in the root directory of this repository:

* `app.py` - Main Streamlit Dashboard application
* `Infosys_Project.ipynb` - Jupyter notebook containing EDA, preprocessing, and model training
* `best_pollution_model.joblib` - Saved machine learning model
* `feature_scaler.joblib` & `label_encoder.joblib` - Saved preprocessing weights
* `Final_Labeled_Pollution_Dataset.csv` - The final processed and labeled dataset
* `Banglore.csv`, `Chennai.csv`, `Tirupati.csv` - Raw API extracts
* `indian_weather_data.csv`, `Threecities_pollution_data.csv` - Intermediary data files
* `download_pollution.py` - Initial Python data extraction script
* `requirements.txt` - Required Python dependencies

---

# 16. How to Run the Project
1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
