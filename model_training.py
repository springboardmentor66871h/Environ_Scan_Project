# ============================================
# EnviroScan - Final Pollution Source Model
# ============================================

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


print("🚀 Step 1: Loading Dataset")

# Load Dataset (use ONE correct path only)
file_path = r"C:\Users\shrij\OneDrive\文档\Air Pollution Project\Final_Labeled_Pollution_Dataset.csv"
df = pd.read_csv(file_path)

print("Dataset Shape:", df.shape)

# -----------------------------------------
# Step 2: Data Cleaning
# -----------------------------------------
print("\n🔍 Checking Missing Values")
print(df.isnull().sum())

df = df.dropna()
print("✅ Missing values removed")

# -----------------------------------------
# Step 3: Feature Selection
# -----------------------------------------

features = ['co','no2','o3','pm10','pm25','so2',
            'Temperature','Humidity','Wind Speed','Wind Direction',
            'dist_road','dist_industry','dist_dump','dist_farmland']

X = df[features]
y = df['pollution_source']

# Encode target
le = LabelEncoder()
y_encoded = le.fit_transform(y)

print("\nClass Mapping:")
for index, class_name in enumerate(le.classes_):
    print(f"{class_name} --> {index}")
# -----------------------------------------
# Add Noise HERE 
# -----------------------------------------

import numpy as np

noise_level = 0.15   

for col in features:
    std_dev = X[col].std()
    noise = np.random.normal(0, noise_level * std_dev, X.shape[0])
    X[col] = X[col] + noise

print("✅ Noise added to features")    

# -----------------------------------------
# Step 4: Train-Test Split
# -----------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print("\nTrain size:", X_train.shape)
print("Test size:", X_test.shape)

# -----------------------------------------
# Step 5: Random Forest(Gridsearch)
# -----------------------------------------

param_grid = {
    'n_estimators': [100],
    'max_depth': [4, 6, 8],
    'min_samples_split': [8, 12],
    'min_samples_leaf': [5, 8]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1
)

print("\n🔎 Running GridSearch...")
grid.fit(X_train, y_train)

print("Best Parameters:", grid.best_params_)

model = grid.best_estimator_

# -----------------------------------------
# Step 6: Evaluation
# -----------------------------------------

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print("\n✅ Training Accuracy:", accuracy_score(y_train, y_train_pred))
print("✅ Testing Accuracy:", accuracy_score(y_test, y_test_pred))

print("\n📊 Classification Report:")
print(classification_report(y_test, y_test_pred, target_names=le.classes_))

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=le.classes_,
            yticklabels=le.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# -----------------------------------------
# Step 7: Feature Importance
# -----------------------------------------

importances = model.feature_importances_

importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importance:")
print(importance_df)

plt.figure()
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.gca().invert_yaxis()
plt.title("Feature Importance - Random Forest")
plt.tight_layout()
plt.show()

# -----------------------------------------
# Step 8: Save Model
# -----------------------------------------

import os
os.makedirs("Models", exist_ok=True)

joblib.dump(model, "Models/pollution_source_model.joblib")
joblib.dump(le, "Models/label_encoder.joblib")

print("🎉 Model and Encoder Saved Successfully!")
# ============================================
# Decision Tree Model
# ============================================

from sklearn.tree import DecisionTreeClassifier

print("\n🌳 Training Decision Tree Model")

dt_param_grid = {
    'max_depth': [3, 5, 7],
    'min_samples_split': [10, 20],
    'min_samples_leaf': [5, 10],
    'criterion': ['gini']
}

dt_grid = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    dt_param_grid,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1
)

dt_grid.fit(X_train, y_train)

print("Best Decision Tree Parameters:", dt_grid.best_params_)

dt_model = dt_grid.best_estimator_

# Evaluation
y_train_pred_dt = dt_model.predict(X_train)
y_test_pred_dt = dt_model.predict(X_test)

print("\n🌳 Decision Tree Results")
print("Training Accuracy:", accuracy_score(y_train, y_train_pred_dt))
print("Testing Accuracy:", accuracy_score(y_test, y_test_pred_dt))

print("\nClassification Report:")
print(classification_report(y_test, y_test_pred_dt, target_names=le.classes_))

# -----------------------------------------
# Confusion Matrix - Decision Tree
# -----------------------------------------
cm_dt = confusion_matrix(y_test, y_test_pred_dt)

plt.figure(figsize=(6,5))
sns.heatmap(cm_dt, annot=True, fmt='d',
            xticklabels=le.classes_,
            yticklabels=le.classes_)
plt.title("Confusion Matrix - Decision Tree")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# Save Decision Tree Model
joblib.dump(dt_model, "Models/decision_tree_model.joblib")
print("✅ Decision Tree Model Saved!")
# ============================================
# XGBoost Model
# ============================================

from xgboost import XGBClassifier

print("\n🚀 Training XGBoost Model")

xgb_model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_lambda=5,
    reg_alpha=2,
    random_state=42,
    eval_metric='mlogloss'
)

xgb_model.fit(X_train, y_train)

# Evaluation
y_train_pred_xgb = xgb_model.predict(X_train)
y_test_pred_xgb = xgb_model.predict(X_test)

print("\n🚀 XGBoost Results")
print("Training Accuracy:", accuracy_score(y_train, y_train_pred_xgb))
print("Testing Accuracy:", accuracy_score(y_test, y_test_pred_xgb))

print("\nClassification Report:")
print(classification_report(y_test, y_test_pred_xgb, target_names=le.classes_))

# -----------------------------------------
# Confusion Matrix - XGBoost
# -----------------------------------------
cm_xgb = confusion_matrix(y_test, y_test_pred_xgb)

plt.figure(figsize=(6,5))
sns.heatmap(cm_xgb, annot=True, fmt='d',
            xticklabels=le.classes_,
            yticklabels=le.classes_)
plt.title("Confusion Matrix - XGBoost")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# Save XGBoost Model
joblib.dump(xgb_model, "Models/xgboost_model.joblib")
print("✅ XGBoost Model Saved!")