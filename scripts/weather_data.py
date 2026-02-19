import pandas as pd
weather1 = pd.read_excel("data/raw/Weather data1.xlsx")
weather2 = pd.read_excel("data/raw/Weather data2.xlsx")
print(weather1.head())
print(weather2.head())
weather1.to_csv("weather_data.csv", index=False)
weather2.to_csv("weather_data.csv", index=False)