# Environ Scan - Week 1 Data Collection

## APIs Used
1. Open-Meteo Air Quality API
2. Open-Meteo Weather Archive API
3. OpenStreetMap (OSMnx)

## Cities Selected
Delhi, Mumbai, Kolkata, Chennai, Bangalore

## Time Range
January 1, 2025 – January 31, 2026

## Data Collected
Pollution Parameters:
- PM2.5
- PM10
- NO2
- CO
- SO2
- O3

Weather Parameters:
- Temperature
- Humidity
- Wind Speed
- Wind Direction

Location Features:
- Distance to nearest road
- Industrial zones
- Landfill
- Farmland

## Folder Structure
data/raw → individual datasets
data/processed → final merged dataset

## Notes
- Missing values appear where API returned null.
- Location features computed using 5km radius.
- All timestamps are hourly and aligned.