import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import pandas as pd


def hello_world():
    logging.info("Hello World")

#
# TODO: Add a daily `schedule_interval` argument to the following DAG
#
dag = DAG(
        "lesson1.exercise2",
        start_date=datetime.datetime.now() - datetime.timedelta(days=2),
        schedule_interval="@daily",
)

task = PythonOperator(
        task_id="hello_world_task",
        python_callable=hello_world,
        dag=dag)
