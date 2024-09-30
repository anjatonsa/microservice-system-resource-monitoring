import pandas as pd 
import pickle
from sklearn.preprocessing import StandardScaler 
from sklearn.neighbors import KNeighborsRegressor
from sklearn.impute import SimpleImputer


#data preprocces
df = pd.read_csv("dataset.csv")
split_ratio = 0.8
split_point = int(len(df) * split_ratio)
train_data = df[:split_point]  
simulation_data = df[split_point:]  
simulation_data.to_csv("../MLModelMS/simulation_data.csv", index=False)
print("Preprocessing data finshed.")

 
#CPU_Load model prediction
imputer = SimpleImputer(strategy="mean")

X_train = train_data.drop(columns=["CPU_Load","Series","Time"])
X_train = imputer.fit_transform(X_train)
y_train = imputer.fit_transform(train_data[["CPU_Load"]])
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

model = KNeighborsRegressor(n_neighbors=5)
model.fit(X_train, y_train) 
model_pkl_file = "../MLModelMS/cpu_load_model.pkl"  
with open(model_pkl_file, 'wb') as file:  
    pickle.dump(model, file)

scaler_pkl_file = "../MLModelMS/cpu_scaler.pkl"
with open(scaler_pkl_file, 'wb') as file:  
    pickle.dump(scaler, file)

print("CPU_Load model training finshed.")

#Power model prediction
imputer = SimpleImputer(strategy="mean")

X_train = train_data.drop(columns=["Power","Series","Time"])
X_train = imputer.fit_transform(X_train)
y_train = imputer.fit_transform(train_data[["Power"]])
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

model = KNeighborsRegressor(n_neighbors=5)
model.fit(X_train, y_train)
model_pkl_file = "../MLModelMS/power_model.pkl"  
with open(model_pkl_file, 'wb') as file:  
    pickle.dump(model, file)

scaler_pkl_file = "../MLModelMS/power_scaler.pkl"
with open(scaler_pkl_file, 'wb') as file:  
    pickle.dump(scaler, file)

print("Power model training finshed.")