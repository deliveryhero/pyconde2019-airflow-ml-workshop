"""This DAG has the goal to simulate a ML Prediction pipeline.
Run forecast prediction everyday.
"""
from datetime import timedelta, date

from airflow import DAG
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator

from src.model_toolbox import forecast_wt_arima_for_date

# Instead of hardcoding the prediction tablename, you can take it from
# Variable.get("prediction_table") created with the 1st Exercise
PREDICTION_TABLE = 'prediction'


# default_args when passed to a DAG, it will apply to any of its operators
default_args = {
                "start_date": "2019-09-22",
                "email": ["airflow_notification@thisisadummydomain.com"],
                "email_on_failure": False,
                "email_on_retry": False,
                "retries": 2,
                "retry_delay": timedelta(minutes=5)
                }


dag = DAG("prediction_pipeline",
          description="ML Prediction Pipeline",
          # predict every day
          schedule_interval= "30 15 * * *",
          default_args=default_args,
          dagrun_timeout=timedelta(minutes=60*4),
          # set catchup=True to run the dag for the previous days
          # (starting from "start_date")
          catchup=True
          )


def save_prediction(**kwargs):
    # Tasks can pass parameters to downstream tasks through the XCom space.
    # In this example the current task `save_prediction` takes the output of
    # the previous task `run_prediction` "pulling" it from the XCom space
    ti = kwargs['ti']
    prediction_dict = ti.xcom_pull(task_ids='run_prediction')
    # INSERT OR REPLACE guarantees to have unique row for each date_to_predict:
    # it inserts a new prediction if it doesn't exists or replace the existing
    # one due to the index idx_date_to_predict on date_to_predict
    sql_insert = f"""INSERT OR REPLACE INTO {PREDICTION_TABLE} 
                     (date_to_predict, run_date, yhat, yhat_upper, yhat_lower)
                     VALUES ('{prediction_dict["date_to_predict"]}', 
                             '{prediction_dict["run_date"]}',
                             {prediction_dict["yhat"]}, 
                             {prediction_dict["yhat_upper"]},
                             {prediction_dict["yhat_lower"]}
                            )
                     ;"""
    # Hooks are interface to external platforms (e.g. Amazon S3)
    # and DBs (e.g. SQLite DB, PostgreSQL)
    conn_host = SqliteHook(sqlite_conn_id='sqlite_ml').get_conn()
    conn_host.execute(sql_insert)
    conn_host.commit()
    conn_host.close()


def run_prediction(**kwargs):
    # kwargs is a dictionary of keyword arguments passed to the function
    # kwargs['ds'] is the execution_date. It's the date when the task is
    # scheduled to run (it could not correspond to current date, for example
    # when running for past period when catchup=True
    prediction_date = kwargs['ds']
    # save in run_date the day the predition is calculated
    run_date = date.today()
    result = forecast_wt_arima_for_date(str(prediction_date))
    # add execution information
    result['date_to_predict'] = prediction_date
    result['run_date'] = run_date
    print(result)
    return result


with dag:

    # Instantiating a PythonOperator class results in the creation of a
    # task object, which ultimately becomes a node in DAG objects.
    run_prediction = PythonOperator(task_id="run_prediction",
                                    python_callable=run_prediction,
                                    # when provide_context=True pass a set of
                                    # keyword arguments to the called function
                                    provide_context=True
                                    )
    #
    save_prediction = PythonOperator(task_id="save_prediction",
                                     python_callable=save_prediction,
                                     provide_context=True
                                     )

    run_prediction >> save_prediction
