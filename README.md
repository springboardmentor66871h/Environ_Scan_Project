# EnviroScan: AI-Powered Pollution Source Identification 🌍🏭

**EnviroScan** is a machine learning project designed to identify the likely sources of air pollution (e.g., Traffic, Industry, Agriculture) based on real-time air quality readings and meteorological data.

---

## 🚀 Milestone 1: Data Collection & Processing (Completed)

We have successfully built a national-scale dataset covering **241 cities in India** with over **1.9 million hourly data points**. This dataset merges pollution levels with weather conditions and geospatial features to train our Source Identification AI.

### 📂 1. Data Sources
* **Primary Source:** Central Pollution Control Board (CPCB) of India via Kaggle.
* **Pollutants Tracked:** $PM_{2.5}, PM_{10}, NO_2, SO_2, CO, O_3$.
* **Meteorological Data:** Temperature, Humidity, Wind Speed, and **Wind Direction** (Crucial for source tracing).
* **Timeframe:** 2024 (Hourly resolution).

### 🛠️ 2. Data Processing Pipeline
We implemented a robust Python pipeline (`process_all_india.py`) to transform raw state-level files into a single master dataset.

**Key Processing Steps:**
1.  **Crawling:** Automated script traversed directory structures for 31 States/UTs.
2.  **Merging:** Paired "Pollution" files with "Weather" files for each city using hourly timestamps.
3.  **Cleaning:** Standardized column names and removed incomplete records.
4.  **Geospatial Feature Engineering:**
    * Simulated distance metrics for training: `distance_to_road`, `distance_to_industry`, `distance_to_dump`, `distance_to_farmland`.
    * *Note: In Milestone 2, these features help the model distinguish between traffic (near roads) and industrial (near factories) pollution.*

### 💾 3. Dataset Structure
Due to the massive size (**~2 Million rows**), the processed dataset is split into two zipped parts to comply with GitHub storage limits.

**Location:** `data/processed/`
* `india_part1.zip` (~977k rows)
* `india_part2.zip` (~977k rows)

**Columns in Master Dataset:**
| Category | Columns |
| :--- | :--- |
| **Location** | `state`, `city`, `latitude`, `longitude` |
| **Time** | `timestamp` |
| **Pollutants** | `pm25`, `pm10`, `no2`, `co`, `so2`, `o3` |
| **Weather** | `temperature`, `humidity`, `wind_speed`, `wind_direction` |
| **Geospatial** | `distance_to_road`, `distance_to_industry`, `distance_to_dump` |

---

## 🔜 Next Steps (Milestone 2)
* **Data Loading:** Stitching `part1` and `part2` back into a single Dataframe.
* **Model Training:** Training Random Forest / XGBoost classifiers to predict pollution sources.
* **Evaluation:** Assessing model accuracy and feature importance.

## 🏷️ Milestone 2: Source Labeling & Simulation (Week 3)

### 1. The Core Problem & Solution
Our dataset lacks a ground-truth `pollution_source` target variable. To prepare for supervised machine learning in Week 4, we utilized **Rule-Based Weak Supervision** to simulate labels based on environmental logic, chemical signatures, and geospatial proximity. 

**Note: This is simulated labeling due to the absence of real-world ground-truth data.**

### 2. Rule-Based Labeling Logic & Thresholds
To ensure the machine learning model has sufficient positive examples to learn from, we used **Expanded Dynamic Quantile Thresholding**. We lowered pollutant thresholds (35th–40th percentiles) and expanded distance radiuses to capture moderate-to-high pollution events across all 241 cities.

**The Rules:**
1. **Vehicular:** `NO2 >= 35th percentile` AND `Distance to Road <= 700m`
   * *Logic:* Combustion engines produce NO2; proximity confirms local traffic.
2. **Industrial:** `SO2 >= 35th percentile` AND `Distance to Industry <= 4500m`
   * *Logic:* Fossil fuel/smelting produces SO2; industrial zones have wider dispersion radiuses.
3. **Agricultural:** `PM10 >= 40th percentile` AND `NO2 <= 60th percentile` AND `Distance to Farmland <= 3500m`
   * *Logic:* Coarse dust without combustion gases signifies soil resuspension or harvest activity.
4. **Burning:** `PM2.5 >= 40th percentile` AND `Distance to Dump <= 8000m`
   * *Logic:* Fine particulate matter spikes indicate biomass or waste burning.
5. **Natural:** `PM10 >= 40th percentile` AND `PM2.5 <= 60th percentile`
   * *Logic:* High coarse dust but lower fine particles signifies windblown soil or pollen.

### 3. Label Distribution & Validation
The expanded heuristic script successfully categorized ~80% of the dataset into distinct pollution events, providing a robust training ground for the classification model.

* **Vehicular:** 938,940 (48.0%)
* **Industrial:** 409,137 (20.9%)
* **Burning:** 127,048 (6.5%)
* **Agricultural:** 47,688 (2.4%)
* **Natural:** 11,555 (0.6%)
* **Mixed/Unknown:** 421,536 (21.6%) *(Retained to represent baseline/mixed background air).*