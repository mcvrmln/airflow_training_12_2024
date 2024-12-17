from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from google.cloud import storage


with DAG(
    dag_id="landing",
    start_date=pendulum.today("UTC").add(days=-10),
    schedule_interval=timedelta(minutes=3),
):
    def load_data(task_instance: TaskInstance, **context):
        landing_dataset = task_instance.xcom_pull(key="launches", task_ids="fetch_API")

        storage_client = storage.Client()
        bucket = storage_client.bucket(context["bucket_name"])
        blob = bucket.blob(context["blob_name"])

        with blob.open("w") as f:
            f.write(landing_dataset)


    load_into_bucket = PythonOperator(task_id="load_into_bucket",
            python_callable=load_data,
            templates_dict={"bucket_name": "",
                    "blob_name": ""
                }
            )