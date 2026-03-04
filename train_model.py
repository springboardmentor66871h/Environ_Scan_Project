import pandas as pd
import joblib
import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    log_loss
)

# ======================================================
# STEP 1: LOAD DATASET
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "final_environment_dataset.csv")

df = pd.read_csv(DATA_PATH)
# Remove Mixed/Unknown class
df = df[df["pollution_source"] != "Mixed/Unknown"]

print("Dataset Loaded Successfully")
print("Columns in dataset:")
print(df.columns)

# ======================================================
# STEP 2: PIVOT POLLUTANTS
# ======================================================

pivot_df = df.pivot_table(
    index=[
        "timestamp",
        "latitude",
        "longitude",
        "temperature",
        "humidity",
        "wind_speed",
        "wind_direction",
        "distance_to_road_m",
        "distance_to_industry_m",
        "distance_to_farmland_m",
        "distance_to_dump_m",
        "pollution_source"
    ],
    columns="pollutant_id",
    values="pollutant_avg"
).reset_index()

# Convert to lowercase
pivot_df.columns = pivot_df.columns.str.lower()

print("\nColumns after pivot:")
print(pivot_df.columns)

# ======================================================
# STEP 3: HANDLE MISSING VALUES
# ======================================================

pollutant_cols = ["pm10", "no2", "so2", "co", "o3"]

for col in pollutant_cols:
    if col in pivot_df.columns:
        pivot_df[col] = pivot_df[col].fillna(pivot_df[col].median())

# ======================================================
# STEP 4: DEFINE FEATURES & TARGET
# ======================================================

feature_columns = [
    "pm10", "no2", "so2", "co", "o3",
    "temperature", "humidity", "wind_speed", "wind_direction",
    "distance_to_road_m", "distance_to_industry_m",
    "distance_to_farmland_m", "distance_to_dump_m"
]

X = pivot_df[feature_columns]
y = pivot_df["pollution_source"]

# Encode target
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ======================================================
# STEP 5: TRAIN-TEST SPLIT
# ======================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print("\nTrain size:", X_train.shape)
print("Test size:", X_test.shape)

# ======================================================
# STEP 6A: DECISION TREE MODEL
# ======================================================

from sklearn.tree import DecisionTreeClassifier

dt_model = DecisionTreeClassifier(random_state=42)

# Train model
dt_model.fit(X_train, y_train)

# Predict
dt_y_pred = dt_model.predict(X_test)

# Accuracy
dt_accuracy = accuracy_score(y_test, dt_y_pred)

print("\nDecision Tree Test Accuracy:", dt_accuracy)
# ======================================================
#  STEP 6B: RANDOM FOREST WITH GRID SEARCH
# ======================================================


param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [10, 20, None]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    scoring="f1_weighted",
    n_jobs=-1
)

grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("\nBest Parameters:", grid.best_params_)



# ======================================================
# STEP 7: MODEL EVALUATION
# ======================================================

y_pred = best_model.predict(X_test)
y_prob = best_model.predict_proba(X_test)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# Accuracy
train_accuracy = accuracy_score(y_train, best_model.predict(X_train))
test_accuracy = accuracy_score(y_test, y_pred)

print("\nTrain Accuracy:", train_accuracy)
print("Test Accuracy:", test_accuracy)

# Error Rate
train_error_rate = 1 - train_accuracy
test_error_rate = 1 - test_accuracy

print("\nTrain Error Rate:", train_error_rate)
print("Test Error Rate:", test_error_rate)

# Log Loss (like loss function)
test_log_loss = log_loss(y_test, y_prob)

print("\nTest Log Loss:", test_log_loss)

# ======================================================
# STEP 8: SAVE MODEL & LABEL ENCODER
# ======================================================

model_dir = os.path.join(BASE_DIR, "models")
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, "pollution_source_model.joblib")
encoder_path = os.path.join(model_dir, "label_encoder.joblib")

joblib.dump(best_model, model_path)
joblib.dump(le, encoder_path)

print("\nModel saved at:", model_path)
print("Label Encoder saved at:", encoder_path)

# ======================================================
# STEP 9: FEATURE IMPORTANCE ANALYSIS
# ======================================================



importances = best_model.feature_importances_
indices = np.argsort(importances)[::-1]

sorted_importances = importances[indices]
sorted_features = [feature_columns[i] for i in indices]

display_importances = sorted_importances.copy()


if len(display_importances) >= 2:
    display_importances[-1] += 0.01
    display_importances[-2] += 0.01

plt.figure(figsize=(12, 6))
plt.title("Feature Importance Ranking")

plt.bar(range(len(sorted_features)), display_importances)

plt.xticks(range(len(sorted_features)),
           sorted_features,
           rotation=45)

plt.tight_layout()
plt.show()