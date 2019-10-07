"""This DAG has the goal to create the SQLite Database and the tables to store
the training and the predictions results
Prerequisite:
- SQLite DB connection named `sqlite_ml` in the UI Connections section
"""
from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.sqlite_operator import SqliteOperator
from airflow.utils.dates import days_ago


# Variables are stored in the Metadata DB
# Instead of hardcoding the tablenames, you can take it from
# Variable.get("training_table") and Variable.get("prediction_table")
# created with the 1st Exercise
TRAINING_TABLE = 'training' #Variable.get("training_table")
PREDICTION_TABLE = 'prediction' #Variable.get("prediction_table")


# default_args when passed to a DAG, it will apply to any of its operators
default_args = {
                "start_date": days_ago(1),
                "email": ["airflow_notification@thisisadummydomain.com"],
                "email_on_failure": False,
                "email_on_retry": False,
                "retries": 2,
                "retry_delay": timedelta(minutes=1)
                }


dag = DAG("create_ml_tables",
          description="Create ML tables",
          default_args=default_args,
          # run only once
          schedule_interval= "@once"
          )


with dag:
    # SqliteOperator execute SQL into the SQLite DB using the
    # 'sqlite_ml' connection
    create_training_table = SqliteOperator(
        task_id="create_training_table",
        # triple-quoted spans code on multiple lines
        sql=f"""
                CREATE TABLE IF NOT EXISTS {TRAINING_TABLE}(
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                mape_test REAL,
                rmse_test REAL,
                days_in_test REAL
                );
            """,
        # 'sqlite_ml' is the connection created from the Connection View UI
        sqlite_conn_id="sqlite_ml"
        )

    create_prediction_table = SqliteOperator(
        task_id="create_prediction_table",
        # triple-quoted spans code on multiple lines
        sql=f"""
                CREATE TABLE IF NOT EXISTS {PREDICTION_TABLE}(
                date_to_predict DATE,
                run_date DATE,
                yhat REAL,
                yhat_upper REAL,
                yhat_lower REAL
                );
            """,
        # 'sqlite_ml' is the connection created from the Connection View UI
        sqlite_conn_id="sqlite_ml"
        )

    # Create an unique index on the column date_to_predict of
    # PREDICTION_TABLE table. When inserting a new prediction,
    # if a prediction with a same date_to_predict already exists,
    # it updates that particular row with the new values,
    # otherwise it inserts a new record.
    create_prediction_index = SqliteOperator(
        task_id="create_prediction_index",
        sql=f"""
                CREATE UNIQUE INDEX idx_date_to_predict
                ON {PREDICTION_TABLE} (date_to_predict) --!!! FIXME add a ) parenthesis
                ;
            """,
        sqlite_conn_id="sqlite_ml"
        )


    # create_prediction_index task will only be executed after
    # create_training_table and create_prediction_table
    [create_training_table , create_prediction_table] >> create_prediction_index
