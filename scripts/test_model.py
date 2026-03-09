import joblib
import pandas as pd

# Load model
model = joblib.load("Models/pollution_source_model.joblib")
le = joblib.load("Models/label_encoder.joblib")

# Create sample with column names
sample = pd.DataFrame([{
    'co': 2.1,
    'no2': 30,
    'o3': 40,
    'pm10': 120,
    'pm25': 80,
    'so2': 20,
    'Temperature': 32,
    'Humidity': 65,
    'Wind Speed': 4.5,
    'Wind Direction': 180,
    'dist_road': 0.5,
    'dist_industry': 3.0,
    'dist_dump': 5.0,
    'dist_farmland': 10.0
}])

prediction = model.predict(sample)

print("Predicted Pollution Source:", le.inverse_transform(prediction))