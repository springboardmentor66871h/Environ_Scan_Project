import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.utils import resample
from sklearn.preprocessing import LabelEncoder
df = pd.read_csv(r"C:\Users\admin\Environ_Scan_Project\data\processed\labeled_dataset.csv")

target = "pollution_source"

classes = df[target].unique()
dfs = {c: df[df[target]==c] for c in classes}

natural_down = resample(
    dfs["Natural"],
    replace=False,
    n_samples=3500,
    random_state=42
)

balanced_parts = [natural_down]

for cls in classes:
    if cls == "Natural":
        continue
    temp = dfs[cls]
    temp_up = resample(
        temp,
        replace=True,
        n_samples=3500,
        random_state=42
    )
    balanced_parts.append(temp_up)

balanced_df = pd.concat(balanced_parts)

X = balanced_df.drop(columns=[target])
y = balanced_df[target]

for col in X.select_dtypes(include="object").columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
smote = SMOTE(k_neighbors=3, random_state=42)
X_res, y_res = smote.fit_resample(X, y)

final_df = pd.concat([X_res, y_res], axis=1)

final_df.to_csv(r"C:\Users\admin\Environ_Scan_Project\data\processed\final_training_dataset.csv", index=False)

print("Balanced Dataset Shape:", final_df.shape)
print(final_df[target].value_counts())
