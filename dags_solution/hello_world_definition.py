from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'start_date': datetime(2019, 10, 5),
    'email': ['airflow_notification@thisisadummydomain.com'],
    'email_on_failure': False
}

dag = DAG('hello_world',
          description='Hello world DAG',
          default_args=default_args,
          schedule_interval='0 17 * * *'
          )

def print_hello():
    print('Hello world :)')

with dag:

    dummy_task = DummyOperator(task_id='dummy_task_id',
                               retries=5
                               )

    python_task = PythonOperator(task_id='hello_task_id',
                                 python_callable=print_hello
                                 )

    dummy_task >> python_task
