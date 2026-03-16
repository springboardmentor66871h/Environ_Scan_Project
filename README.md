# 🌍 EnviroScan: AI-Powered Pollution Source Identification using Geospatial Analytics

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-LightGBM%20%7C%20XGBoost-orange)
![Data Science](https://img.shields.io/badge/Data%20Science-Pandas%20%7C%20Scikit--Learn-green)
![Status](https://img.shields.io/badge/Status-Milestone%202%20Completed-success)

> **Infosys Springboard Internship Project** | Milestone 1 & 2 (Weeks 1–4)

## 📑 Table of Contents
1. [Project Overview](#-project-overview)
2. [Tech Stack & Tools](#-tech-stack--tools)
3. [Methodology & Pipeline](#-methodology--pipeline)
    - [Phase 1: Data Aggregation](#phase-1-data-aggregation-weeks-1-2)
    - [Phase 2: Heuristic Source Labeling](#phase-2-heuristic-source-labeling-week-3)
    - [Phase 3: Model Training & Evaluation](#phase-3-model-training--evaluation-week-4)
4. [Model Performance](#-model-performance-metrics)
5. [Critical Limitations & Future Scope](#-critical-limitations--future-scope)
6. [Repository Structure](#-repository-structure)
7. [Installation & Usage](#-installation--usage)

---

## 📋 Project Overview
EnviroScan is an AI-driven geospatial analytics ecosystem designed to predict and classify the primary anthropogenic and natural sources of air pollution in specific geographic locations. 

By fusing live atmospheric pollutant concentrations (PM2.5, NO2, etc.), real-time meteorological conditions, and spatial proximity matrices (distance to industrial zones, main roads, etc.), this system utilizes advanced gradient boosting machine learning algorithms to automatically categorize pollution sources into distinct profiles.

---

## 🛠 Tech Stack & Tools
* **Language:** Python 3.x
* **Data Processing:** `pandas`, `numpy`
* **Machine Learning:** `scikit-learn`, `xgboost`, `lightgbm`, `catboost`
* **APIs & Geospatial:** `OpenAQ API` (Air Quality), `OpenWeatherMap API` (Meteorology), `OSMnx` / `OpenStreetMap` (Spatial features)
* **Visualization:** `matplotlib`, `seaborn`
* **Serialization:** `joblib`

---

## ⚙️ Methodology & Pipeline

### Phase 1: Data Aggregation (Weeks 1-2)
The foundational dataset was constructed by pinging multiple external APIs to create a multi-dimensional environmental profile for various geolocations.

| Data Type | Source | Variables Extracted |
| :--- | :--- | :--- |
| **Atmospheric** | OpenAQ API | PM2.5, PM10, NO₂, CO, SO₂, O₃ |
| **Meteorological** | OpenWeatherMap API | Temperature, Humidity, Wind Speed, Wind Direction |
| **Spatial Proximity** | OSMnx / OSM | Distance to Road, Distance to Industry, Distance to Dump Site, Distance to Farmland |

### Phase 2: Heuristic Source Labeling (Week 3)
In the absence of physical ground-truth sensors that explicitly state "This pollution came from a factory," the target variable (`pollution_source`) was engineered using strict, logical environmental heuristics based on established AQI behavior.

**The Labeling Engine Ruleset:**
1. **Vehicular:** High `NO2` + extremely low `distance_to_road`.
2. **Industrial:** High `SO2` and `NO2` + low `distance_to_industry`.
3. **Agricultural:** High Particulate Matter (`PM10`) + low `humidity` (dry season) + low `distance_to_farmland`.
4. **Burning:** High `PM2.5` and `CO` + low `distance_to_dump_site`.
5. **Natural:** Moderate/Background dispersion assigned to all records failing the above anthropogenic thresholds.

### Phase 3: Model Training & Evaluation (Week 4)
We transitioned from deterministic `IF/ELSE` logic to a scalable machine learning approach. The objective was to train an algorithm to recognize the complex, multi-dimensional signatures of these pollution sources automatically.

* **Preprocessing:** The target variable was mapped via `LabelEncoder`. All numerical input features were normalized using `StandardScaler` to ensure uniform weighting across distance-based algorithms.
* **The Gauntlet:** We evaluated **12 different classification algorithms** using 5-fold cross-validation, including Logistic Regression, SVMs, Random Forests, XGBoost, and Neural Networks (MLP).
* **The Winner:** **LightGBM (Light Gradient Boosting Machine)** outperformed all other models, demonstrating exceptional capability in mapping complex feature interactions with rapid convergence.

---

## 📊 Model Performance Metrics

Evaluated on a 20% unseen hold-out test set, the LightGBM classifier achieved near-perfect predictive capabilities.

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | `99.70%` | Model correctly identifies the source 99.7% of the time. |
| **Precision** | `0.9970` | When predicting a specific class, it is correct 99.7% of the time. |
| **Recall** | `0.9970` | Model successfully identifies 99.7% of all actual instances of a class. |
| **F1-Score** | `0.9970` | Harmonic mean indicates perfectly balanced classification across all categories. |

*(Visualizations for the Confusion Matrix and Feature Importances are available in the `/visuals` directory).*

---

## ⚠️ Critical Limitations & Future Scope

While the `99.7%` evaluation metrics demonstrate successful algorithmic training, hyperparameter tuning, and data preprocessing, it is critical to acknowledge the fundamental limitation of this phase:

**The Rule-Based Bias:** Because the training labels were deterministically engineered in Phase 2 using static Python thresholds, the machine learning model has essentially learned to reverse-engineer those exact static rules. It perfectly mapped our human assumptions rather than real-world chaotic dispersion dynamics. 

**Future Scope (Milestone 3 & Beyond):** 1. Retrain the model on authenticated, sensor-verified ground-truth data.
2. Integrate the exported `.joblib` model into a live, interactive web dashboard (Streamlit/Flask) for real-time inference.
3. Containerize the application using Docker for seamless deployment.

### Milestone 3 (Modules 5 & 6): Geospatial Mapping & Real-Time Dashboard

**Overview:**
The final phase of the EnviroScan project integrates the trained predictive models into a centralized, interactive web application built with Streamlit. This dashboard serves as a decision-support platform, transforming raw predictions into actionable geospatial and temporal insights.

**Geospatial Visualization (Folium):**
* **Heatmap Integration:** Utilized `folium.plugins.HeatMap` to visualize PM2.5 intensity gradients across the selected geographic areas.
* **Source-Specific Markers:** Implemented dynamically colored `CircleMarkers` to plot the predicted origin of pollution (e.g., Industrial, Vehicular) at precise coordinates.
* **High-Risk Zones:** Applied threshold logic (`PM2.5 > 50 µg/m³`) to automatically scale marker radius and trigger high-visibility colors for critical zones, allowing rapid identification by stakeholders.
* **Embedding:** Seamlessly embedded the interactive HTML map directly into the Streamlit UI via the `streamlit-folium` bridge.

**Dashboard Features (Streamlit):**
* **Real-Time Alert System:** Conditional UI banners (`st.error`, `st.warning`) trigger automatically when aggregated pollutant levels cross predefined safety thresholds (e.g., PM2.5 > 50 or NO2 > 40).
* **Trend & Distribution Analytics:** Integrated interactive `plotly` charts, including time-series line charts for pollutant tracking and pie charts for source distribution analysis.
* **Interactive Filtering:** Sidebar widgets allow users to slice data by city, date ranges, and specific predicted sources.
* **Reporting:** Built-in export functionality allows users to download the filtered, current-view dataset as a CSV report for offline analysis.
---

## 📂 Repository Structure

```text
EnviroScan/
│
├── data/
│   ├── raw/                            # Raw JSON/CSV data fetched from APIs
│   └── processed/
│       └── final_combined_dataset.csv  # Merged dataset used for modeling
│
├── models/                             # Exported model artifacts (Ready for Deployment)
│   ├── best_pollution_model.joblib     # Trained LightGBM Classification Model
│   ├── label_encoder.joblib            # Target variable encoder
│   └── feature_scaler.joblib           # StandardScaler for numerical inputs
│
├── notebooks/
│   └── Week4_Model_Training.ipynb      # Source code for hyperparameter tuning & evaluation
│
├── visuals/                            # Visual evaluation of the model
│   ├── confusion_matrix.png            # Classification accuracy heatmap
│   └── feature_importance.png          # Predictive weight of each feature
│
└── README.md                           # Project documentation
