from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 24),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def extract():
    subprocess.run(["python", "extract.py"])

def transform():
    subprocess.run(["python", "transform.py"])

def load():
    subprocess.run(["python", "load.py"])

dag = DAG(
    "etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
)

extract_task = PythonOperator(task_id="extract", python_callable=extract, dag=dag)
transform_task = PythonOperator(task_id="transform", python_callable=transform, dag=dag)
load_task = PythonOperator(task_id="load", python_callable=load, dag=dag)

extract_task >> transform_task >> load_task
