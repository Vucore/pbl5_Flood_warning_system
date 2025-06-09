from fastapi import APIRouter
from ..service.flood_risk_service import predict_flood_risk
from ..service.prepare_data import control_prepare_data_rainfall
from pydantic import BaseModel

router = APIRouter()

class PredictRequest(BaseModel):
    rainfall: float
    soil_humidity: float
    air_humidity: float
    air_pressure: float
    temperature: float

@router.post("/predict-flood-risk")
async def get_flood_risk(request: PredictRequest):
    try:
        # Lấy dữ liệu cảm biến từ request
        sensor_data = {
            "rainfall": request.rainfall,
            "soil_humidity": request.soil_humidity,
            "air_humidity": request.air_humidity,
            "air_pressure": request.air_pressure,
            "temperature": request.temperature
        }

        # Tính các đặc trưng lượng mưa
        features = control_prepare_data_rainfall(rainfall=sensor_data["rainfall"])
        sensor_data.update(features)  # Cập nhật các đặc trưng vào sensor_data

        # Gọi hàm dự đoán từ service
        result = predict_flood_risk(sensor_data)

        # Trả về kết quả dự đoán
        return {
            "class_idx": result["class_idx"],
            "label": result["label"]
        }
    except Exception as e:
        return {"error": str(e)}