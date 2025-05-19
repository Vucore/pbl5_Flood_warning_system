from fastapi import APIRouter, Request
from ..service.flood_risk_service import predict_flood_risk

router = APIRouter()

@router.post("/predict-flood-risk")
async def get_flood_risk(request: Request):
    sensor_data = await request.json()
    result = predict_flood_risk(sensor_data)
    return {
        "risk_score": result["risk_score"],
        "label": result["label"],
        "class_idx": result["class_idx"]
    }