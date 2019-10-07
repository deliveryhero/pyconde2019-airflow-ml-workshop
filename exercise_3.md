### EX 3. Prediction [:top:](README.md#table-of-contents)

<p align="center">
<img src="/media/main_steps_exercise_3.png" alt="ex3" width="90%"/>
</p>

:trophy: After having trained the model with the dag `training_pipeline`, it's time for making some **`predictions`**. Go to the **`prediction_pipeline` dag**.

:sos: _Note_: in case you skipped the 2nd Exercise and you don't have a model file to use for the inference phase, you can copy the `/model` folder and its content (`arima.pkl.zip`) from the directory `/solution` into the `/data` directory. **Decompress** the file `arima.pkl.zip` **to have `arima.pkl` available**.

In this dag there are **2 tasks**:
- `run_prediction`: calculates the prediction using the model
- `save_prediction`: stores the model in the `prediction table`

In this exercise there aren't changes to apply. Everything should run smoothly :sunglasses:

**Activate the `prediction_pipeline` DAG**, clicking on the `ON` button.

:clock11: Refresh the status clicking on the :repeat: `REFRESH` button and **check the progress** in the :deciduous_tree: **Tree View**.
The **Tree View** shows a tree representation of the DAG that spans across time.

As you can notice we are running the predictions starting from the 22nd of September 2019.

<p align="center">
<img src="/media/airflow_prediction_catchup.png" alt="prediction catchup" width="80%"/>
</p>

If you **look at the code** we have defined the dag with these parameters:
```python
default_args = {
                "start_date": "2019-09-22",
                [ .. ]
                }

dag = DAG("prediction_pipeline",
          [ ... ]
          schedule_interval= "30 15 * * *",
          # set catchup=True to run the dag for the previous days (starting from "start_date")
          catchup=True,
          )
```
We have as `"start_date": "2019-09-22"` and the argument `catchup=True`: the **Scheduler will create a dag run for each completed interval**.

An interval is the period between one run and the next one.

At the end of the execution, we have the **`prediction table` populated with different predictions**.

:white_check_mark: Let's check it! **Select and Click** on the of the bar the **`Data Profiling/Ad Hoc Query`** element:

Select from the menu the `sqlite_ml` option and **write this small query** for verifying that the **predictions** has been **saved into the SQLite database**:
```sql
SELECT * FROM prediction;
```

:trophy: The output will show you the **prediction records**.

<p align="center">
<img src="/media/airflow_ad_hoc_query_prediction.png" alt="ad hoc query" width="70%"/>
</p>

Go to [Bonus EX. Plot Predictions](https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop/blob/master/exercise_4.md).
