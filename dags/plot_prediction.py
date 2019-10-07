"""This DAG has the goal to plot a graph of the computed predictions.
"""
from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from src.model_toolbox import plot_forecast


default_args = {
                "start_date": "2019-10-01",
                "email": ["airflow_notification@thisisadummydomain.com"],
                "email_on_failure": False,
                "email_on_retry": False,
                "retries": 2,
                "retry_delay": timedelta(minutes=5)
                }


dag = DAG("plot_prediction",
          description="Plot Predictions",
          # Generate the plot prediction graph
          schedule_interval= "@once",
          default_args=default_args
          )


def call_plot_function():
    # Pass to the function `plot_forecast` the Host of the sqlite_ml connection
    # (Taken from the Web UI from Admin/Connection/)
    db_host = '/tmp/sqlite_default.db'
    plot_forecast(db_host)


with dag:

    get_plot_forecast_pathfile = PythonOperator(
        task_id="get_plot_forecast_pathfile",
        python_callable=call_plot_function
        )

    get_plot_forecast_pathfile
