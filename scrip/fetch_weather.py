import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

cities = [
    {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"city": "Delhi", "lat": 28.6139, "lon": 77.2090},
    {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"city": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"city": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"city": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"city": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"city": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"city": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"city": "Lucknow", "lat": 26.8467, "lon": 80.9462}
]


weather_data = []

for city in cities:
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={city['lat']}&lon={city['lon']}"
        f"&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error {response.status_code} for {city['city']}")
        print(response.text)
        continue

    data = response.json()

    weather_data.append({
        "city": city["city"],
        "latitude": city["lat"],
        "longitude": city["lon"],
        "timestamp": datetime.utcfromtimestamp(data["dt"]).isoformat(),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "wind_direction": data["wind"]["deg"]
    })

df = pd.DataFrame(weather_data)

df.to_csv("../data/raw/weather/weather_data.csv", index=False)

print("Weather Data Saved Successfully")
