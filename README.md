🌍 EnviroScan – Data Collection (Week 1)

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

🌍 EnviroScan – Milestone 2 (Week 3)
Source Labeling Using Multi-Priority Environmental Logic
📌 Objective

The goal of Week 3 is to assign a pollution source label to each record in the processed environmental dataset.

Since real-world datasets (from Open-Meteo API and OSM) do not provide ground-truth pollution source labels, we simulate labels using:

Pollutant concentration levels

Proximity to pollution-related features

Wind speed conditions

Data-driven percentile thresholds

The final labeled dataset will be used for supervised machine learning in Week 4.

📊 Dataset Description

The dataset contains real-world environmental data including:

🌫 Pollutants

PM2.5 (pm2_5)

NO₂ (no2)

SO₂ (so2)

PM10

CO

O₃

🌦 Weather Features

Temperature

Humidity

Wind Speed (wind_speed)

Wind Direction

📍 Location Feature

nearest_feature_distance_m
(Distance to nearest major pollution-related feature such as roads, industries, farmland, or dump sites)

🧠 Labeling Methodology

Instead of using fixed arbitrary thresholds, the labeling system uses data-driven percentile thresholds, making it adaptive and realistic.

📐 Threshold Strategy (Percentile-Based)
Feature	Threshold Used	Purpose
PM2.5 Moderate	70th percentile	Agricultural detection
PM2.5 High	85th percentile	Burning detection
NO₂ High	70th percentile	Vehicular detection
SO₂ High	70th percentile	Industrial detection
Near Source	35th percentile distance	Moderate proximity
Very Near	20th percentile distance	Strong proximity
Low Wind	40th percentile	Burning (pollution trapping)
High Wind	75th percentile	Natural dust dispersion

This approach ensures thresholds reflect actual data distribution.

🔎 Multi-Priority Rule-Based Logic

Each row is assigned exactly one label based on priority order:

1️⃣ Burning

Assigned if:

PM2.5 > 85th percentile

Very near pollution source

Low wind speed

Rationale:
Burning events produce extreme particulate matter and occur near dump or waste areas. Low wind traps smoke.

2️⃣ Industrial

Assigned if:

SO₂ > 70th percentile

Near pollution source

Rationale:
High SO₂ is a strong indicator of industrial emissions.

3️⃣ Vehicular

Assigned if:

NO₂ > 70th percentile

Near pollution source

Rationale:
NO₂ is strongly associated with traffic emissions.

4️⃣ Agricultural

Assigned if:

PM2.5 > 70th percentile

Not extremely near a major source

Rationale:
Moderate particulate matter at moderate distance may indicate crop burning or field dust.

5️⃣ Natural

Assigned in all remaining cases:

Background pollution

Wind-driven dust