import joblib
import pandas as pd
import os

# ======================================================
# LOAD SAVED MODEL & LABEL ENCODER
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "models", "pollution_source_model.joblib")
encoder_path = os.path.join(BASE_DIR, "models", "label_encoder.joblib")

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)

print("Model Loaded Successfully!")

# ======================================================
# DEFINE FEATURE COLUMNS (Must Match train_model.py)
# ======================================================

feature_columns = [
    "pm10", "no2", "so2", "co", "o3",
    "temperature", "humidity", "wind_speed", "wind_direction",
    "distance_to_road_m", "distance_to_industry_m",
    "distance_to_farmland_m", "distance_to_dump_m"
]

# ======================================================
# SAMPLE INPUT DATA (Change values to test)
# ======================================================

sample_data = {
    "pm10": [45],
    "no2": [30],
    "so2": [12],
    "co": [0.8],
    "o3": [25],
    "temperature": [32],
    "humidity": [60],
    "wind_speed": [5],
    "wind_direction": [180],
    "distance_to_road_m": [100],
    "distance_to_industry_m": [500],
    "distance_to_farmland_m": [1000],
    "distance_to_dump_m": [200]
}

# Convert to DataFrame
sample_input = pd.DataFrame(sample_data)

# Ensure correct column order
sample_input = sample_input[feature_columns]

# ======================================================
# PREDICT
# ======================================================

prediction_encoded = model.predict(sample_input)
prediction_label = encoder.inverse_transform(prediction_encoded)

print("\nPredicted Pollution Source:", prediction_label[0])