from airflow import DAG, Dataset
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

import pendulum

intermediate_dataset = Dataset(
    "s3://my_bucket/intermediate_data.csv",  # URI
)

with DAG(
    dag_id="8_etl_pipeline",
    start_date=pendulum.today("UTC").add(days=-10),
    schedule_interval=timedelta(minutes=2),
):
    fetch = EmptyOperator(task_id="fetch")
    remove_outliers = EmptyOperator(task_id="remove_outliers")
    update_db = EmptyOperator(task_id="update_db", outlets=[intermediate_dataset])

    fetch >> remove_outliers >> update_db
