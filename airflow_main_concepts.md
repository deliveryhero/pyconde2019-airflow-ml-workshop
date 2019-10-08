## Airflow main concepts [:top:](README.md#table-of-contents)

We briefly introduce the **Airflow main concepts** using the **`hello_world.py`** file that you can find in the repository (inside the `dags` folder).

### Example: Hello World DAG

A **workflow** is a **sequence of tasks** organised in a way that reflects their **relationships** and **dependencies**.

In **Airflow** a **workflow is represented** as a **DAG (Direct Acyclic Graph)**.

In the **`hello_world.py`** file the workflow is represented as a **Graph with 2 nodes**: **`dummy_task_id`** and **`hello_task_id`**.

<p align="center">
<img src="/media/airflow_hello_world_graph_dag.png" alt="hello world graph"  width="50%"/>
</p>

The **Python code** that defines the `hello_world` dag is the following:

<p align="center">
<img src="/media/airflow_hello_world_code_dag.png" alt="hello world dag"  width="80%"/>
</p>

In the above code you can see the elements:
- **DAG**:
  - describe **how** to run a workflow
- **TASKS**:
  - determine what actually gets done
  - are parameterised instances of operators
  - have status (e.g. `queued`, `running`, `failed`)
- **OPERATORS**:
  - are the blueprints for defining what tasks have to get done

Examples of [Operators](https://airflow.apache.org/_api/index.html#operators):
- `PythonOperator`, to run a Python callable
- `SqliteOperator`, to execute a query on a SQLite DB
- `BashOperator`, to execute bash commands
- `RedshiftToS3Transfer`, to execute an UNLOAD command to Amazon s3 as a CSV with headers
- `GoogleCloudStorageToBigQueryOperator`, to load files from Google Cloud Storage into BigQuery


After this short explanation we can introduce the [Exercises: Airflow for training and predicting](https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop/blob/master/exercise_intro.md).
