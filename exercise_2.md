### EX 2. Train the model [:top:](README.md#table-of-contents)

<p align="center">
<img src="/media/main_steps_exercise_2.png" alt="ex2" width="90%"/>
</p>

After creating the `training` table for saving the model accuracy, let's have a look a the **training pipeline dag**.

:white_check_mark: **Open** with the editor the file **`/dags/training_pipeline.py`**.

#### 2.1 Add training_table variable
At the **top of the file**, find the variable **`TRAINING_TABLE`**.
Instead of having the tablename hardcoded
`TRAINING_TABLE = 'training_table'`
 let's take it from the Variable we have setup before:
`TRAINING_TABLE = Variable.get("training_table")`


#### 2.2 Add remaining training tasks

:pencil2: We need to **complete the training dag**:

:white_check_mark: **Complete** the PythonOperator tasks for **each function** that we need to call.

The functions are already imported in the module.
The **functions and the executions order** is the following:
1) preprocess_raw_data (already created)
2) split_data  (already created)
3) **fit_and_save_model**
4) **predict_test_wt_arima**
5) measure_accuracy  (already created)
6) save_model_accuracy (already created)


To complete the tasks, you can look at the `preprocess_raw_data` task:

```python
preprocess_raw_data = PythonOperator(task_id="preprocess_raw_data",
                                     python_callable=preprocess_raw_data
                                     )
```

:white_check_mark: Complete the execution order, at the bottom of the file, inside the `dag context manager`, to reflect the expected execution.

Use the **bitshift operators >>** we have met before.

:white_check_mark: When code is completed, **go back** to the **Web UI DAGs View** and **activate the DAG**, clicking on the `ON` button of the **`training_pipeline`** dag.

:clock11: Wait some seconds to let the **scheduler pickup the task and re-run it**.

:clock11: The **`training_pipeline` dag is running**.
Refresh the status clicking on the :repeat: `REFRESH` button until all the tasks become green:

<p align="center">
<img src="/media/airflow_training.png" alt="training" width="80%"/>
</p>

:trophy: The **training pipeline** is completed: all the tasks are terminated in **success**.

Go to [EX 3. Prediction](https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop/blob/master/exercise_3.md).
