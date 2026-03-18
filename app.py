from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)

# ======================================================
# LOAD MODEL & LABEL ENCODER
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "models", "pollution_source_model.joblib")
encoder_path = os.path.join(BASE_DIR, "models", "label_encoder.joblib")

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)

feature_columns = [
    "pm10", "no2", "so2", "co", "o3",
    "temperature", "humidity", "wind_speed", "wind_direction",
    "distance_to_road_m", "distance_to_industry_m",
    "distance_to_farmland_m", "distance_to_dump_m"
]

# ======================================================
# HOME PAGE
# ======================================================

@app.route("/")
def home():
    return render_template("index.html")

# ======================================================
# PREDICTION ROUTE
# ======================================================

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect form values
        values = [float(request.form[col]) for col in feature_columns]
        input_df = pd.DataFrame([values], columns=feature_columns)

        # Predict
        prediction = model.predict(input_df)
        result = encoder.inverse_transform(prediction)[0]

        # Custom message and color
        if result.lower() == "road":
            message = "🛣 Road Pollution Detected"
            color = "#ff9800"
        elif result.lower() == "industry":
            message = "🏭 Industrial Pollution Detected"
            color = "#f44336"
        elif result.lower() == "farmland":
            message = "🌾 Agricultural Pollution Detected"
            color = "#4caf50"
        elif result.lower() == "dump":
            message = "🗑 Dump Yard Pollution Detected"
            color = "#9c27b0"
        else:
            message = f"Detected: {result}"
            color = "#333"

        return render_template("index.html", prediction=message, color=color)

    except:
        return render_template(
            "index.html",
            prediction="⚠ Invalid Input! Please enter numeric values.",
            color="#000"
        )

# ======================================================

if __name__ == "__main__":
    app.run(debug=True)