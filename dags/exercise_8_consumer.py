from airflow import DAG, Dataset
from airflow.operators.empty import EmptyOperator

import pendulum

intermediate_dataset = Dataset(
    "s3://my_bucket/intermediate_data.csv",  # URI
)


with DAG(
    dag_id="8_produce_report",
    start_date=pendulum.today("UTC").add(days=-10),
    schedule=[intermediate_dataset],
):
    get_cleaned_data = EmptyOperator(task_id="get_cleaned_data")
    produce_report = EmptyOperator(task_id="produce_report")

    get_cleaned_data >> produce_report