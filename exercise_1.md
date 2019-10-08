### EX 1. Preconditions: Variables, Tables and Connection [:top:](README.md#table-of-contents)

<p align="center">
<img src="/media/main_steps_exercise_1.png" alt="ex1" width="90%"/>
</p>

Now that both **Scheduler** and **Webserver** are running, we can start **getting familiar** with the Airflow User Interface at [http://localhost:8080](http://localhost:8080) and create the preconditions for orchestrating our ML pipelines.

#### 1.1 Add Variables

Let's start to **customise Airflow** adding two **Variables** that store the **tablenames: `training` and `prediction`**:

:white_check_mark: go to **`Admin/Variables`** and **create** a new **Key** **`training_table`** with the value **`training`**.

:white_check_mark: Do the same for prediction: add the **Key** **`prediction_table`** with the value **`prediction`**.

<p align="center">
<img src="/media/airflow_add_variables.png" alt="add variables" width="90%"/>
</p>


#### 1.2 Create SQLite DB Connection

:white_check_mark: Go to **`Admin/Connections`** and **search** the connection with `Conn Id` **`sqlite_default`**.

:pushpin: The connections that you see are examples, are not in use.

:pencil2: Edit the **`Conn Id`** value from `sqlite_default` to **`sqlite_ml`**.

<p align="center">
<img src="/media/airflow_edit_sqlite_ml_connection.png" alt="toggle dag" width="60%"/>
</p>


#### 1.3 DAG Table Creation and Connection

Now that you have:
- saved the variables with the table names, one for training and one for prediction
- created the SQLite DB connection

let's activate the **DAG create_ml_tables** to let the **Scheduler pick it up** and create the Database and the tables in it.

:white_check_mark: go to **`DAGS`** section and **toggle `ON`** the button of the **`create_ml_tables`** dag.

<p align="center">
<img src="/media/airflow_toggle_create_ml_tables.png" alt="toggle dag" width="70%"/>
</p>

The **Scheduler** will pickup the DAG and it will run it (there aren't dependecies that prevent the execution).

**Click on the DAG name `create_ml_tables`**: we are now in the **`Graph View`**.
With the **`Graph View`** you can visualise the task dependencies and the current status.

:clock11: The **`create_ml_tables` dag is running**.
Refresh the status clicking on the :repeat: `REFRESH` button.

<p align="center">
<img src="/media/airflow_create_tables.png" alt="create tables" width="85%"/>
</p>

:white_check_mark: If you click on the `Code` button on the DAG menu, **you can see (but not modify) the Python code**:

<p align="center">
<img src="/media/airflow_dag_code.png" alt="dag code" width="85%"/>
</p>

:pushpin: Note: for **running the SQL** that creates the tables and the index we instantiated the **`SqliteOperator`** that makes use of the **`sqlite_ml` connection** we have previously created.

```sql
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
```

:pushpin: Note: To define the execution order we use the **bitshift operator >>**.
You can see it at the bottom of the code:
```python
[create_training_table , create_prediction_table] >> create_prediction_index
```
the `create_prediction_index` task is executed only after `create_training_table` and `create_prediction_table` have been successfully executed.

:heavy_exclamation_mark: Let's **go back to the DAG View**: **something bad happened**!
The task **`create_prediction_index` is having some issues**.
The previous 2 tasks, `create_training_table` and `create_prediction_table`, finished in `success`.

<p align="center">
<img src="/media/airflow_debug_index.png" alt="retry index view log" width="70%"/>
</p>

Let's **DEBUG using Airflow**: **click on the task `create_prediction_index`**: it will open a new window.

<p align="center">
<img src="/media/airflow_retry_index_view_log.png" alt="retry index view log" width="60%"/>
</p>

:heavy_exclamation_mark: **Click** on **`View Log`**, you can see the error message:

<p align="center">
<img src="/media/airflow_index_sql_error.png" alt="create index error log" width="70%"/>
</p>

:pencil2: We need to fix the bug in the code (**we CAN'T do it** in the Airflow UI).<br />
:white_check_mark: **Open with the editor** the file **`/dags/create_ml_tables.py`** in the repository.<br />
Go through the code and find the **SQL** where we created the **index**.

```sql
CREATE UNIQUE INDEX idx_date_to_predict
ON {PREDICTION_TABLE} (date_to_predict --!!! FIXME add a ) parenthesis
;
```
:heavy_exclamation_mark: Is missing the closing parenthesis `)` after `date_to_predict`. Add it: `date_to_predict)`.

:white_check_mark: Save the file and **go back to the Web UI**, in the `Graph View` of the `create_ml_tables` dag.

:white_check_mark: **Click again on the task `create_prediction_index`**, but this time, on the open window, **click** on the **`Clear` button** and in the next window confirm the operation clicking on `OK!`.

<p align="center">
<img src="/media/airflow_retry_index_view_log.png" alt="retry index view log" width="60%"/>
</p>

:pushpin: You are now **resetting the task status**.
:clock11: Wait some seconds to let the **scheduler pickup the task and re-run it**.

:trophy: Once all the tasks will have been executed and terminated in `success`, we'll have 2 tables: **training** and **prediction**.

<p align="center">
<img src="/media/airflow_create_ml_success.png" alt="success create tables" width="60%"/>
</p>

:trophy: We have also created an **index** for the **`prediction` table** on the column `date_to_predict`: this will guarantee to save only one prediction per day that we want to predict.

Go to [EX 2. Train the model](https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop/blob/master/exercise_2.md).
