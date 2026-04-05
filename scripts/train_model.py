import pandas as pd,joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df=pd.read_csv("data/processed/enviroscan_final_dataset.csv")

X=df[['pm25','no2','o3','temperature','humidity','wind_speed','pressure']]
y=df['source_label']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

model=RandomForestClassifier()
model.fit(X_train,y_train)

joblib.dump(model,"models/pollution_model.joblib")
print("Done")
