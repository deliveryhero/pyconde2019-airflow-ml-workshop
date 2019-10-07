"""The `hello_world` Direct Acyclic Graph (DAG)"""
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


# default_args passed to DAG. It's a dictionary of default parameters to be
# used when initialising operators. It will apply to any of its operators
default_args = {
    # Scheduler triggers the task soon after the
    # start_date + scheduler_interval is passed
    # In this case, the DAG will run the first time the 6th October 2019, 5pm
    # with the execution date 5th October 2019, 5pm
    'start_date': datetime(2019, 10, 5),
    'email': ['airflow_notification@thisisadummydomain.com'],
    'email_on_failure': False
}


# `hello_world` is the dag_id that uniquely identifies a dag in Airflow
dag = DAG('hello_world',
          description='Hello world DAG',
          default_args=default_args,
          # The DAG run the 1st time on `start_date` + `schedule_interval`.
          # Idea: run the dag when the schedule period is ended.
          # e.g. if daily run: process today the data of yesterday.
          # schedule_interval defines the frequency you want to run a dag.
          # In this case every day at 5pm (cron notation)
          schedule_interval='0 17 * * *'
          )


# function called by the PythonOperator when `python_task` will be executed
def print_hello():
    print('Hello world :)')


# binds the tasks to the dag using `with dag` context manager
with dag:
    # task `dummy_task_id` is an instance of DummyOperator.
    # An Operator creates objects that become nodes in the dag.
    dummy_task = DummyOperator(task_id='dummy_task_id',
                               retries=5
                               )

    # task `hello_task_id` is an instance of PythonOperator.
    # PythonOperator executes a Python callable, in this case the
    # `print_hello` function
    python_task = PythonOperator(task_id='hello_task_id',
                                 python_callable=print_hello
                                 )

    # Define tasks dependencies (using the bitshift operator `>>`)
    # tasks execution order: the first to be executed is the dummy_task.
    # If dummy_task succeeded, then `python_task` will be triggered
    dummy_task >> python_task
