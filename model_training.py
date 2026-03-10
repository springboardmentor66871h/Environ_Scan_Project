import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

print("STEP 1: Loading and Verifying the Labeled Dataset...")
df = pd.read_csv("data/Labeled_Master_Dataset.csv")

# Verify no missing values
if df.isnull().sum().sum() == 0:
    print("Dataset verified: 0 missing values.")
else:
    print("Warning: Missing values detected! Please clean data.")

print("\nSTEP 2: Defining Features (X) and Target (y)...")
# Using the exact features specified for the model
features = [
    'pm25', 'pm10', 'no2', 'co', 'so2', 'o3', 
    'temperature_c', 'humidity_percent', 'wind_speed_mps', 'wind_direction_deg',
    'dist_to_road_m', 'dist_to_industry_m', 'dist_to_farm_m', 'dist_to_waste_m',
    'hour', 'is_weekend' # Crucial temporal context
]

X = df[features]
y_raw = df['pollution_source']

# XGBoost requires the target variable to be numeric (0, 1, 2, etc.)
# We use LabelEncoder to convert the text labels into numbers, and save it so we can decode later!
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)
print(f" Target encoded. Classes mapped to: {dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))}")

print("\nSTEP 3: Train-Test Split (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
print(f"  -> Training on {len(X_train)} rows.")
print(f"  -> Testing on {len(X_test)} rows.")

print("\nSTEP 4 & 5: Training and Tuning Models (Random Forest & XGBoost)...")
# --- MODEL 1: Random Forest ---
print("  -> Tuning Random Forest...")
rf_params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None]
}
rf_model = RandomForestClassifier(random_state=42, n_jobs=-1)
rf_search = RandomizedSearchCV(rf_model, rf_params, n_iter=5, cv=3, random_state=42, n_jobs=-1)
rf_search.fit(X_train, y_train)
print(f"     Best RF Params: {rf_search.best_params_}")

# --- MODEL 2: XGBoost ---
print("  -> Tuning XGBoost...")
xgb_params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 6, 10],
    'learning_rate': [0.01, 0.1, 0.2]
}
xgb_model = XGBClassifier(random_state=42, n_jobs=-1, eval_metric='mlogloss')
xgb_search = RandomizedSearchCV(xgb_model, xgb_params, n_iter=5, cv=3, random_state=42, n_jobs=-1)
xgb_search.fit(X_train, y_train)
print(f"     Best XGB Params: {xgb_search.best_params_}")

# --- SELECT BEST MODEL ---
rf_acc = rf_search.best_estimator_.score(X_test, y_test)
xgb_acc = xgb_search.best_estimator_.score(X_test, y_test)

print("\nModel Accuracies:")
print(f"  -> Random Forest: {rf_acc * 100:.2f}%")
print(f"  -> XGBoost:       {xgb_acc * 100:.2f}%")

if xgb_acc > rf_acc:
    print("\nOverall Winner: XGBoost")
    best_model = xgb_search.best_estimator_
else:
    print("\nOverall Winner: Random Forest")
    best_model = rf_search.best_estimator_

print("\n STEP 6: Model Evaluation on Test Data...")
y_pred = best_model.predict(X_test)

print("\n--- Classification Report ---")
# Use the label_encoder to print the actual category names instead of 0, 1, 2
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
print(report)

# Generate and Save Confusion Matrix Image
os.makedirs("visualisation", exist_ok=True)
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.title('Confusion Matrix - Pollution Source Prediction', fontsize=14, fontweight='bold')
plt.ylabel('Actual Source', fontsize=12)
plt.xlabel('Predicted Source', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
cm_path = "visualisation/confusion_matrix.png"
plt.savefig(cm_path, dpi=300)
print(f" Confusion Matrix saved to: {cm_path}")

print("\nSTEP 7: Feature Importance Analysis...")
# Extract feature importance from the best model
importances = best_model.feature_importances_
feature_imp_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=True)

plt.figure(figsize=(10, 8))
plt.barh(feature_imp_df['Feature'], feature_imp_df['Importance'], color='#2a9d8f')
plt.title('Feature Importance in Predicting Pollution Source', fontsize=14, fontweight='bold')
plt.xlabel('Relative Importance Score', fontsize=12)
plt.tight_layout()
feat_path = "visualisation/feature_importance.png"
plt.savefig(feat_path, dpi=300)
print(f"Feature Importance chart saved to: {feat_path}")

print("\n STEP 8: Exporting Final Model...")
os.makedirs("models", exist_ok=True)

# Save the Best Model