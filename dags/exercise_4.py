from datetime import datetime, timedelta

import requests
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor


with DAG(
    dag_id="is_there_data",\
    start_date=datetime.now() - timedelta(days=7),
    description="Exercise 4 sensor",
    schedule=None,

) as dag:
    

    URL = "https://httpstat.us/200?sleep=20000"

    check_connection = HttpSensor(task_id="check_connection",
                                  http_conn_id="http_delayed",
                                  endpoint="",
                                  method='GET',
                                  response_check=lambda response: response.status_code == 200,
                                  mode="reschedule")

    do_something = PythonOperator(task_id="do_something",
                                  python_callable=lambda: print("It is available.")
                                  )

    check_connection >> do_something