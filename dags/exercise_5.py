import json
from pathlib import Path

import airflow.utils.dates
import requests
from airflow.models import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

API_URL = "https://lldev.thespacedevs.com/2.3.0/launches"


with DAG(
    dag_id="exercise5_xcoms",
    start_date=airflow.utils.dates.days_ago(7),
    schedule_interval="@daily",
    tags=["exercise"],
) as dag:

    def _download_launches(task_instance: TaskInstance, **context):
        templates_dict = context["templates_dict"]
        output_path = Path(templates_dict["output_path"])

        response = requests.get(
            API_URL,
            params={
                "window_start__gte": templates_dict["window_start"],
                "window_end__lt": templates_dict["window_end"],
            },
        )
        response.raise_for_status()

        task_instance.xcom_push(key="data", value=response.text)
                                

    def _print_launch_count(task_instance: TaskInstance, **context):
        # TODO: Finish this task. Should load the launch JSON file
        # and print the 'count' field from it's contents.
        # raise NotImplementedError()

        data = json.loads(task_instance.xcom_pull(key="data", task_ids="download_launches"))

        print(f'Number of lauches {data["count"]}')

    print_date = BashOperator(task_id="print_date", bash_command='echo "{{ logical_date }}"')

    # TODO: Use data interval start and end to define window start/end + file path.
    # Useful https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
    # Format for dates should be following: 2021-12-01T00:00:00Z"
    download_launches = PythonOperator(
        task_id="download_launches",
        python_callable=_download_launches,
        templates_dict={
            "output_path": "/tmp/launches/{{ ds }}.json",
            "window_start": "{{ data_interval_start | ds}}T00:00:00Z",
            "window_end": "{{ data_interval_end | ds}}T00:00:00Z",
        },

    )

    # TODO: Complete this task.
    check_for_launches = PythonOperator(
        task_id="check_for_launches", 
        python_callable=_print_launch_count,
        templates_dict={
            "input_path" :"/tmp/launches/{{ ds }}.json",
        }
    )

    print_date >> download_launches >> check_for_launches