import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from fastapi import FastAPI
import pandas as pd
from datetime import datetime

from pydantic import BaseModel


class InputFeatures(BaseModel):
    precipitation: float
    relative_humidity_2m : float
    dew_point_2m: float
    apparent_temperature: float
    cloudcover: float
    windspeed_10m: float
    winddirection_10m: float
    shortwave_radiation: float
    surface_pressure: float

app = FastAPI()

# Connexion au serveur MLflow
mlflow.set_tracking_uri("http://host.docker.internal:5000")
client = MlflowClient()


# Load model from MLflow registry
model_name = "new_predict_meteo"

model = mlflow.sklearn.load_model(f"models:/{model_name}@champion")

# Create api endpoint

@app.post("/predict")
def predict(input_data: InputFeatures):
    """_summary_
    Effectue une prédiction de la température pour l'heure suivante en utilisant le modèle chargé.

    Args:
        input_data (dict): Données à utiliser pour la prédiction. Doit contenir les mêmes colonnes que celles utilisées pour l'entraînement du modèle.

    Returns:
        _type_: Témpérature prédite pour l'heure suivante.
    """
    input_df = pd.DataFrame([input_data.dict()]) 
    input_df.columns = [
        'precipitation_lag1',
        'relative_humidity_2m_lag1',
        'dew_point_2m_lag1',
        'apparent_temperature_lag1',
        'cloudcover_lag1',
        'windspeed_10m_lag1',
        'winddirection_10m_lag1',
        'shortwave_radiation_lag1',
        'surface_pressure_lag1'
    ]
    preds = model.predict(input_df)
    return {"predictions": preds.tolist()}

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API"}