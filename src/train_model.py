import pandas as pd
import numpy as np
import datetime as dt
import mlflow
import mlflow.sklearn

from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from datetime import datetime, UTC

path = "/home/roulito/mlops_project/mlruns"
mlflow.set_tracking_uri("file://" + path)
experiment_name = 'predict_meteo'

date = datetime.now(UTC).strftime("%Y-%m-%d")


experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    experiment_id = mlflow.create_experiment(experiment_name)
else:
    experiment_id = experiment.experiment_id
df = pd.read_csv(f'/home/roulito/mlops_project/data/processed/{date}.csv')
run_name = f"drift_target_{date}"

def feature_eng( df ):
    if len(df) < 2:
        # Remove the Y target column if it exists
        if 'temperature_2m' in df.columns:
            df = df.drop(columns=['temperature_2m'])
        # Return the DataFrame as is or adapt according to your model
        return df
    # Création des features laggées (décalées d'une heure) pour toutes les colonnes sauf 'time' et 'temperature_2m'
    features = [col for col in df.columns if col not in ['time', 'temperature_2m']]
    df_lagged = df.copy()

    for col in features:
        df_lagged[f'{col}_lag1'] = df_lagged[col].shift(1)

    # On décale aussi la température cible d'une heure pour l'aligner avec les features laggées
    df_lagged['temperature_2m_target'] = df_lagged['temperature_2m']

    # On retire la première ligne qui contient des valeurs NaN à cause du décalage
    df_lagged = df_lagged.dropna().reset_index(drop=True)

    # On sélectionne uniquement les colonnes laggées et la cible
    X = df_lagged[[f'{col}_lag1' for col in features]]
    y = df_lagged['temperature_2m_target']

    return(X, y)



def mlflow_log_model(X, y, experiment_id, run_name):
    """
    Enregistre un modèle de régression linéaire dans MLflow et log les métriques de performance.
    """
    # Démarrage d'une nouvelle run MLflow
    with mlflow.start_run(experiment_id=experiment_id, run_name=run_name):
        mlflow.log_param("model_type", "SVM")
        mlflow.log_param("features", X.columns.tolist())
        mlflow.log_param("target", "temperature_2m_target")

        # Entraînement du modèle
        svm_model = SVR()
        svm_model.fit(X, y)

        # Enregistrement du modèle dans MLflow
        mlflow.sklearn.log_model(svm_model, "model")
        y_pred = svm_model.predict(X)
        mlflow.log_metric("model_score", svm_model.score(X, y))    

        # Affichage des métriques de performance
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R2 Score: {r2:.2f}")
        
        mlflow.log_metric("mean_squared_error", mse)
        mlflow.log_metric("r2_score", r2)
        print("Model training and logging completed successfully.")
        
        # Follow drift Y models 
        mlflow.log_metric("target_mean", y.mean())
        mlflow.log_metric("target_std", y.std())
        mlflow.log_metric("target_skew", y.skew())
        mlflow.log_metric("target_kurtosis", y.kurtosis())

    
    

if __name__ == "__main__":
    X, y = feature_eng(df)
    mlflow_log_model(X, y, experiment_id, run_name)
    print("Model training and logging completed successfully.")