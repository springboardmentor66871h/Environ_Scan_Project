from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

# 1. Initialize FastAPI App
app = FastAPI(title="EnviroScan API")

# 2. Add CORS Middleware (Crucial!)
# This allows your React app (running on port 5173) to securely talk to this Python API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load ML Models
try:
    model = joblib.load("models/pollution_source_classifier.joblib")
    encoder = joblib.load("models/label_encoder.joblib")
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")

# 4. Define the Expected Input Data Format using Pydantic
class PollutionInput(BaseModel):
    pm25: float
    pm10: float
    no2: float
    co: float
    so2: float
    o3: float
    temperature_c: float
    humidity_percent: float
    wind_speed_mps: float
    wind_direction_deg: float
    dist_to_road_m: float
    dist_to_industry_m: float
    dist_to_farm_m: float
    dist_to_waste_m: float
    hour: int
    is_weekend: int

# 5. Create the API Endpoint
@app.post("/api/predict_pollution")
async def predict_pollution(data: PollutionInput):
    try:
        # Convert incoming JSON data into a format the model understands (DataFrame)
        input_dict = data.dict()
        input_df = pd.DataFrame([input_dict])
        
        # Make Prediction
        pred_num = model.predict(input_df)[0]
        pred_text = encoder.inverse_transform([pred_num])[0]
        
        # Get Confidence Score
        probs = model.predict_proba(input_df)[0]
        confidence = float(max(probs) * 100)
        
        # Return the response to React
        return {
            "predicted_source": pred_text,
            "confidence_score": round(confidence, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple health check endpoint
@app.get("/")
def read_root():
    return {"status": "EnviroScan API is running!"}
@app.get("/api/data")
def get_data():
    df = pd.read_csv("Labeled_Master_Dataset.csv")
    return df.head(100).to_dict(orient="records")