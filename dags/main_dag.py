from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


from src import get_data, parse_json_to_csv, train_model


with DAG(
    dag_id="train_predict_meteo_model",
    start_date=datetime(2025, 7, 2),
    schedule_interval="@daily",  # ou None si déclenché manuellement
    catchup=False,
    tags=["ml"]
) as dag:
    
    get_data = PythonOperator(
        task_id="curl_data",
        python_callable=get_data
    ),

    stagging_data = PythonOperator(
        task_id="staging_data",
        python_callable=parse_json_to_csv
    ),
    
    train_model = PythonOperator(
        task_id="train and register model",
        python_callable=train_model
    )
    
get_data >> stagging_data >> train_model