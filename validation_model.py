from pydantic import BaseModel

class weather_hour_data(BaseModel):
    date: str
    hour: str
    temperature: float
    feels_like: float
    dew: float
    precipitation: float
    precip_prob: float
    snow: float
    snow_depth: float
    precip_type: str
    wind_gust: float
    wind_speed: float
    wind_direction: float
    pressure: float
    visibility: float
    cloud_cover: float
    solar_radiation: float
    uv_index: float
    severe_risk: float


class date_data(BaseModel):
    data: str