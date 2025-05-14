from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime

class SensorData(BaseModel):
    timestamp: Optional[datetime] = None 
    rainfall: Union[float, str]      
    soil_humidity: Union[float, str]
    air_humidity: Union[float, str]               
    air_pressure: Union[float, str]              
    temperature: Union[float, str]                
    water_level: Union[float, str]