import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd

# Connexion au serveur MLflow
mlflow.set_tracking_uri("http://votre-serveur-mlflow:5001")

client = MlflowClient()

# Récupérer la dernière version validée (champion) d'un modèle
model_name = "predict_meteo"
champion = client.get_latest_versions(model_name, stages=["Production"])[0]

# Charger le modèle champion avec pyfunc
model_uri = f"models:/{model_name}/Production"
model = mlflow.pyfunc.load_model(model_uri)

# Utiliser le modèle pour faire des prédictions
data = pd.read_csv("/home/roulito/mlops_project/data/processed/2025-07-31.csv")  # Remplacez par vos données

predictions = model.predict(data)
print(predictions)
