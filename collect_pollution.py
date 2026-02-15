import requests

API_KEY = "aba3993b60f3f625b99047cbe7124830828a0ea63df2cf1cca3ff3212f483820"

url = "https://api.openaq.org/v3/locations"

headers = {
    "X-API-Key": API_KEY
}

params = {
    "country": "IN",
    "limit": 5
}

response = requests.get(url, headers=headers, params=params)

print("Status Code:", response.status_code)

data = response.json()

for location in data["results"]:
    print("\nLocation Name:", location["name"])
    print("Country:", location["country"]["code"])