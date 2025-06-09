import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os

# Load biến môi trường từ file .env
load_dotenv()

# Đường dẫn tới mô hình
MODEL_PATH = os.getenv("FLOOD_MODEL_PATH")

# Load mô hình
model = joblib.load(MODEL_PATH)

# Nhãn phân loại
labels = ['Bình thường', 'Cảnh báo', 'Nguy hiểm']

# Hàm dự đoán rủi ro lũ
def predict_flood_risk(sensor_data):
    feature_df = pd.DataFrame([{
        "soil_humidity": sensor_data["soil_humidity"],
        "temperature": sensor_data["temperature"],
        "air_pressure": sensor_data["air_pressure"],
        "air_humidity": sensor_data["air_humidity"],
        "rainfall": sensor_data["rainfall"],
        "rain_duration": sensor_data["rain_duration"],
        "rain_24h": sensor_data["rain_24h"],
        "rain_48h_avg": sensor_data["rain_48h_avg"],
        "rain_max_24h": sensor_data["rain_max_24h"],
        "rain_acc_week": sensor_data["rain_acc_week"]
    }])

    # Dự đoán với mô hình Random Forest
    class_idx = model.predict(feature_df)[0]
    risk_label = labels[class_idx]

    # Trả về kết quả dự đoán
    return {
        "class_idx": int(class_idx),
        "label": risk_label
    }