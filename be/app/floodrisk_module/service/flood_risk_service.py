import joblib
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()  # Đọc biến môi trường từ file .env

MODEL_PATH = os.getenv("FLOOD_MODEL_PATH")
SCALER_PATH = os.getenv("FLOOD_SCALER_PATH")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
# Nhãn phân loại
labels = ['an toàn', 'chú ý', 'nguy hiểm', 'khẩn cấp']

last_water_level = None

# Ngưỡng để phân loại từ giá trị flood_risk liên tục
def classify_risk(value):
    if value < 0.2:
        return 0  # an toàn
    elif value < 0.4:
        return 1  # chú ý
    elif value < 0.6:
        return 2  # nguy hiểm
    else:
        return 3  # khẩn cấp


def predict_flood_risk(sensor_data):
    # sensor_data = SensorData(**sensor_data)
    global last_water_level

    if last_water_level is None:
        prev_water_level = sensor_data["water_level"]
    else:
        prev_water_level = last_water_level

    water_level_rate = sensor_data["water_level"] - prev_water_level

    # Đưa water_level_rate vào đặc trưng đầu vào
    features = np.array([
        water_level_rate,
        sensor_data["water_level"],
        sensor_data["rainfall"],
        sensor_data["soil_humidity"],
    ]).reshape(1, -1)

    # features = np.array([
    #     2.0,
    #     95.0,
    #     680,
    #     75
    # ]).reshape(1, -1)

    # print("water_level_rate:", water_level_rate)
    # print("sensor_data:", sensor_data)

    # Chuẩn hóa đặc trưng đầu vào
    features_scaled = scaler.transform(features)
    risk_score = model.predict(features_scaled)[0]  # Giá trị dự đoán liên tục
    class_idx = classify_risk(risk_score)           # Phân loại theo ngưỡng
    risk_label = labels[class_idx]

    # Log dữ liệu đầu vào và kết quả dự đoán
    # print("== DỰ ĐOÁN LŨ ==")
    # print("sensor_data:", sensor_data)
    # print("features:", features)
    # print("risk_score:", risk_score)
    # print("class_idx:", class_idx)
    # print("risk_label:", risk_label)

    last_water_level = sensor_data["water_level"]
    return {
        "risk_score": float(risk_score),
        "label": risk_label,
        "class_idx": int(class_idx)
    }