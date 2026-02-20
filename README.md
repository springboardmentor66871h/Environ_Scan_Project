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
Because this is a national dataset spanning 241 cities, static thresholds (e.g., exactly 40 µg/m³) fail due to regional baselines. Instead, we used **Dynamic Quantile Thresholding** to capture "High" and "Low" spikes relative to the overall dataset.

**The Rules:**
1. **Vehicular:** `NO2 >= 60th percentile` AND `Distance to Road <= 500m`
   * *Logic:* Combustion engines produce high NO2; proximity confirms local traffic.
2. **Industrial:** `SO2 >= 60th percentile` AND `Distance to Industry <= 3000m`
   * *Logic:* Fossil fuel/smelting produces SO2; industrial zones have wider dispersion radiuses.
3. **Agricultural:** `PM10 >= 60th percentile` AND `NO2 <= 40th percentile` AND `Distance to Farmland <= 2500m`
   * *Logic:* Coarse dust without combustion gases signifies soil resuspension or harvest activity.
4. **Burning:** `PM2.5 >= 75th percentile` AND `Distance to Dump <= 6000m`
   * *Logic:* Fine particulate matter spikes indicate biomass or waste burning.
5. **Natural:** `PM10 >= 60th percentile` AND `PM2.5 <= 40th percentile`
   * *Logic:* High coarse dust but low fine particles signifies windblown soil or pollen, not combustion.

### 3. Label Distribution & Validation
The heuristic script successfully categorized over 800,000 distinct pollution events. 

* **Vehicular:** ~399k
* **Industrial:** ~247k
* **Burning:** ~102k
* **Agricultural:** ~54k
* **Natural:** ~19k
* **Mixed/Unknown:** ~1.13M *(Kept to represent background/mixed air, but will be filtered/downsampled during model training to ensure strong signal learning).*

### 4. Assumptions & Limitations
* **Assumptions:** We assume that a chemical spike occurring near a known geospatial feature is caused by that feature. 
* **Limitations:** Wind direction was not fully integrated into this specific rule engine due to the complexity of reverse-trajectory mapping at a national scale, leading to a high number of "Mixed/Unknown" tags. The simulated geospatial distances act as placeholders to establish the ML pipeline schema.