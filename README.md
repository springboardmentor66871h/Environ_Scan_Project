# 🌍 EnviroScan: AI-Powered Pollution Source Identification

> **Infosys Springboard Internship Project** | Milestone 1 & 2 (Weeks 1–4)

## 📋 Project Overview
EnviroScan is an AI-driven geospatial analytics project designed to identify and predict the primary sources of air pollution in specific locations. By integrating atmospheric pollutant levels, meteorological data, and spatial proximity features, this project utilizes machine learning to classify pollution sources (e.g., Vehicular, Industrial, Agricultural) automatically.

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
├── models/                             # Exported model artifacts
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
