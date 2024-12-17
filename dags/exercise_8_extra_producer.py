from airflow import DAG, Dataset
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

import pendulum

intermediate_dataset = Dataset(
    "s3://my_bucket/intermediate_data.csv",  # URI
)

with DAG(
    dag_id="8_extra_producer",
    start_date=pendulum.today("UTC").add(days=-10),
    schedule_interval=timedelta(minutes=3),
):
    clean = EmptyOperator(task_id="clean")
    fill_blanks = EmptyOperator(task_id="fill_blanks")
    add_additional_info = EmptyOperator(task_id="add_additional_info", outlets=[intermediate_dataset])

    clean >> fill_blanks >> add_additional_info