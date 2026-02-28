import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("🚀 Starting EnviroScan Model Training Pipeline...")
INPUT_FILE_1 = "data/processed/labeled_india_part1.zip"
INPUT_FILE_2 = "data/processed/labeled_india_part2.zip"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

print("⏳ Loading labeled datasets...")
df1 = pd.read_csv(INPUT_FILE_1)
df2 = pd.read_csv(INPUT_FILE_2)
df = pd.concat([df1, df2], ignore_index=True)

print(f"📊 Original dataset size: {len(df)} rows. Sampling 200,000 rows for efficient training...")
df, _ = train_test_split(df, train_size=200000, random_state=42, stratify=df['pollution_source'])

features = [
    'pm25', 'pm10', 'no2', 'so2', 'temperature', 'humidity', 'wind_speed', 
    'distance_to_road', 'distance_to_industry', 'distance_to_dump', 'distance_to_farmland'
]

df[features] = df[features].fillna(df[features].median())

X = df[features]
y = df['pollution_source']

print("✂️ Splitting data (80% Train, 20% Test)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

print("🌲 Training baseline Decision Tree...")
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)
print(f"   Baseline Decision Tree Accuracy: {accuracy_score(y_test, dt_pred):.4f}")

print("🌳 Tuning Random Forest Classifier (This may take 2-3 minutes)...")
rf_base = RandomForestClassifier(random_state=42, n_jobs=-1)

param_dist = {
    'n_estimators': [50, 100],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5]
}

rf_random = RandomizedSearchCV(
    estimator=rf_base, param_distributions=param_dist, 
    n_iter=5, cv=3, verbose=1, random_state=42, n_jobs=-1
)

rf_random.fit(X_train, y_train)
best_rf = rf_random.best_estimator_
print(f"✅ Best Parameters Found: {rf_random.best_params_}")

print("\n🧪 Evaluating Best Model on Test Data...")
y_pred = best_rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n🏆 Final Model Accuracy: {accuracy * 100:.2f}%\n")

print("📄 Classification Report (Precision, Recall, F1-Score):")
report = classification_report(y_test, y_pred)
print(report)

plt.figure(figsize=(10, 7))
cm = confusion_matrix(y_test, y_pred, labels=best_rf.classes_)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=best_rf.classes_, yticklabels=best_rf.classes_)
plt.title('Confusion Matrix - Pollution Source Prediction')
plt.ylabel('Actual Source')
plt.xlabel('Predicted Source')
plt.tight_layout()
cm_path = os.path.join(MODEL_DIR, 'confusion_matrix.png')
plt.savefig(cm_path)
print(f"✅ Confusion Matrix saved to: {cm_path}")

print("\n🔍 Analyzing Feature Importance...")
importances = best_rf.feature_importances_
feature_names = X.columns
feat_imp_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(feat_imp_df['Feature'], feat_imp_df['Importance'], color='teal')
plt.title('Feature Importance for Pollution Source Prediction')
plt.xlabel('Importance Score')
plt.tight_layout()
fi_path = os.path.join(MODEL_DIR, 'feature_importance.png')
plt.savefig(fi_path)
print(f"✅ Feature Importance chart saved to: {fi_path}")

print("\n💾 Exporting the trained model...")
model_path = os.path.join(MODEL_DIR, 'random_forest_enviroscan.joblib')
joblib.dump(best_rf, model_path)
print(f"✅ SUCCESS! Model saved to: {model_path}")
print("🎉 Week 4 Coding Complete!")