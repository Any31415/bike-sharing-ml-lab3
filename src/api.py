from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import load_model, predict
from src.db import save_prediction

app = FastAPI(title="Bike Sharing Prediction API")
model = load_model()


class BikeFeatures(BaseModel):
    season: int
    holiday: int
    workingday: int
    weather: int
    temp: float
    humidity: float
    windspeed: float
    hour: int
    dayofweek: int
    month: int


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def get_prediction(features: BikeFeatures):
    result = predict(model, features.model_dump())
    save_prediction(features.model_dump(), result)  # сохраняем запрос+результат в БД
    return {"predicted_count": result}