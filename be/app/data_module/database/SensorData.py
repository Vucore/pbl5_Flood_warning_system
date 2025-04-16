from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime

class SensorData(BaseModel):
    timestamp: Optional[datetime] = None 
    rainfall: Union[float, str]       # Cho phép cả số (mm) và chuỗi (phân loại)
    soil_humidity: Union[float, str]  # Cho phép cả số (%) và chuỗi (phân loại)
    air_humidity: float               # Luôn là số
    air_pressure: float               # Luôn là số
    temperature: float                 # Luôn là số
    water_level: float  