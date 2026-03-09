import pandas as pd
import joblib

# Load dataset
data = pd.read_csv("data/processed/final_dataset.csv")

# Load trained model
model = joblib.load("models/pollution_model.pkl")

# Features used during training
features = [
    "pollutant_min",
    "pollutant_max",
    "pollutant_avg",
    "Nearest_Road_km",
    "Nearest_Industry_km",
    "Nearest_Dump_km",
    "Nearest_Farm_km"
]

# Remove rows with missing values
data = data.dropna(subset=features)

# Predict pollution source
data["pollution_source"] = model.predict(data[features])

# Save dataset for map
data.to_csv("data/processed/final_map_dataset.csv", index=False)

print("Final map dataset created successfully!")