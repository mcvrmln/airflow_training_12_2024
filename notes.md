# Notes

## Day 1
Different ways to create a DAG
 - With DAG ... (context manager)
 - my_dag = DAG() (Class instance)
 - @dag (decorator)

 There is an operator to trigger a different DAG.

 There is an Airflow CLI. Connections can be made programmaticly (is even better than by using the UI).

 Idempotency is very important for tasks in Airflow. Atomic & Idempotent.

 Airflow scheduler (inside docker) >> airflow help 
 Shows all the commands in the Airflow CLI. 

 Airflow UI:
 Docs > Swagger UI > REST API's. 

 
