The focus of this phase is on:
1.Collecting air pollution data
2.Collecting weather data
3.Extracting location-based geospatial features
4.Combining datasets into a unified structured format
5.Organizing files properly for further processing

1.OpenAQ API:
Used to collect real-time air pollution data.
->Parameters collected:
    PM2.5,PM10,NO₂,CO,SO₂,O₃
->Each record includes:
    City,Latitude,Longitude,Timestamp,Pollutant Name,Pollutant Value

2.OpenStreetMap (OSM) / OSMnx
Used to extract geospatial location-based features near pollution data points.
->Extracted Features:
    Roads,Industrial Zones,Dump Sites,Agricultural Fields
->Derived Features:
    Distance to nearest road,Distance to nearest industrial area,Distance to nearest dump site,Distance to nearest agricultural land
->Library Used:
    OSMnx,GeoPandas,Shapely

3.Cities / Locations Selected
Example Cities (Modify as per your implementation):
    Hyderabad,Delhi,Mumbai,Bangalore
Coordinates were obtained directly from API responses.

4.Time Range of Data
Example (modify accordingly):
    Start Date: 2026-02-01
    End Date: 2026-02-07
    Data Interval: Hourly observations
All timestamps were standardized to UTC format for consistency.

5.Final Dataset Structure (Processed)
The final combined dataset contains:
    city,latitude,longitude,timestamp,pm25,pm10,no2,co,so2,o3,temperature
    humidity,wind_speed,wind_direction,distance_to_road
    distance_to_industry,distance_to_dump,distance_to_farmland