import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib


df = pd.read_csv("farmer_advisor_dataset.csv", sep='\t')

le_crop = LabelEncoder()

df['Crop_Type'] = le_crop.fit_transform(df['Crop_Type'])

x = df[['Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm', 'Crop_Type', 'Fertilizer_Usage_kg', 'Pesticide_Usage_kg', 'Crop_Yield_ton']]
y = df['Sustainability_Score']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(x_train, y_train)

joblib.dump(model, 'model.pkl')
joblib.dump(le_crop, 'crop_encoder.pkl')

def predict_sustainability(pH, moisture, temp, rainfall, crop_type, fert_usage, pest_usage, yield_ton):
    crop_encoded = le_crop.transform([crop_type])[0]
    input_data = [[pH, moisture, temp, rainfall, crop_encoded, fert_usage, pest_usage, yield_ton]]
    score = model.predict(input_data)[0]
    return round(score, 2)

result = predict_sustainability(6.5, 22, 30, 120, "Wheat", 50, 10, 2.5)
print("Predicted Sustainability Score: " , result)
