import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# ------------------------
# Step 1: Load dataset
# ------------------------
df = pd.read_csv("data/processed/final_labeled_with_weather.csv")

print("Original Shape:", df.shape)

# ------------------------
# Step 2: Remove non-numeric columns
# ------------------------
df = df.drop(columns=["timestamp"], errors='ignore')

# (Optional but recommended)
df = df.drop(columns=["latitude", "longitude"], errors='ignore')

# ------------------------
# Step 3: Remove missing values
# ------------------------
df = df.dropna()

print("After Cleaning Shape:", df.shape)

# ------------------------
# Step 4: Define features & target
# ------------------------
target = "pollution_source"

X = df.drop(columns=[target])
y = df[target]

# ------------------------
# Step 5: Train-test split
# ------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------
# Model 1: Decision Tree
# ------------------------
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

# ------------------------
# Model 2: Random Forest + Hyperparameter tuning
# ------------------------
rf = RandomForestClassifier(random_state=42)

param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [5, 10, None]
}

grid = GridSearchCV(rf, param_grid, cv=3)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("\nBest Parameters:", grid.best_params_)

# ------------------------
# Step 6: Model Evaluation
# ------------------------
y_pred = best_model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ------------------------
# Step 7: Feature Importance
# ------------------------
importance = best_model.feature_importances_

features = pd.Series(importance, index=X.columns)
features = features.sort_values(ascending=False)

plt.figure(figsize=(10, 5))
features.head(10).plot(kind="bar")
plt.title("Top Features for Pollution Prediction")
plt.tight_layout()

plt.savefig("data/processed/feature_importance.png")

print("\nFeature importance chart saved!")

# ------------------------
# Step 8: Save Model
# ------------------------
joblib.dump(best_model, "models/pollution_model.pkl")

print("\n✅ Model saved successfully!")