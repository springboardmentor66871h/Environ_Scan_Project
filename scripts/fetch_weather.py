import requests
import pandas as pd
import os
from datetime import datetime

print("Collecting Stable Weather Dataset...")

API_KEY = "6e93c0031119104d7eab5769d628dd5e"

cities = [
    "Delhi","Mumbai","Chennai","Kolkata","Bengaluru",
    "Hyderabad","Pune","Jaipur","Lucknow","Ahmedabad",
    "Surat","Indore","Nagpur","Bhopal","Patna",
    "Coimbatore","Visakhapatnam","Vadodara","Kanpur","Agra",
    "Madurai","Thiruvananthapuram","Chandigarh","Mysore","Guwahati",
    "Ranchi","Dehradun","Shimla","Gwalior","Varanasi",
    "Amritsar","Jodhpur","Raipur","Vijayawada","Rajkot",
    "Noida","Faridabad","Gurgaon","Nashik","Aurangabad",
    "Tiruchirappalli","Salem","Tirunelveli","Jamshedpur","Udaipur",
    "Kochi","Kozhikode","Allahabad","Meerut","Srinagar"
]

records = []

for city in cities:

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed for:", city)
        continue

    data = response.json()

    records.append({
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "wind_degree": data["wind"].get("deg"),
        "clouds": data["clouds"]["all"],
        "timestamp": datetime.utcnow()
    })

df = pd.DataFrame(records)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_path = os.path.join(base_dir, "data", "raw")

os.makedirs(raw_path, exist_ok=True)

file_path = os.path.join(raw_path, "weather_200.csv")

df.to_csv(file_path, index=False)

print("✅ Weather dataset saved at:")
print(file_path)