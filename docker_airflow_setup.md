## Docker Airflow Setup [:top:](README.md#table-of-contents)

### Download the repository

**Clone the repository** in your **`$HOME`** directory
(e.g. for Mac: `/Users/<user>/`, for Windows is `\Users\<user>\`).
We'll refer this location during the workshop.
```bash
$ cd $HOME
$ git clone https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop
```

:white_check_mark: **Download** the **dockerized Airflow** image **`docker pull puckel/docker-airflow:1.10.4`**

:pushpin: For more information about **using Airflow in a Docker container** check the **[puckel docker-airflow project](https://github.com/puckel/docker-airflow)**.

**Move into the directory (`$HOME/pyconde2019-airflow-ml-workshop`)** where you downloaded the repository
```bash
$ cd pyconde2019-airflow-ml-workshop
```

Launch the Airflow Docker container:
```bash
$ docker run -p 8080:8080 -e LOAD_EX=y -e PYTHONPATH="/usr/local/airflow/pyconde2019-airflow-ml-workshop" -v $HOME/pyconde2019-airflow-ml-workshop/requirements.txt:/requirements.txt -v $HOME/pyconde2019-airflow-ml-workshop/:/usr/local/airflow/pyconde2019-airflow-ml-workshop:rw -v $HOME/pyconde2019-airflow-ml-workshop/dags/:/usr/local/airflow/dags:rw puckel/docker-airflow webserver
```

The above command specify:
- `8080:8080`: Airflow is reachable at `localhost:8080`
- `LOAD_EX=y `: load the Airflow examples
- `-v $HOME/pyconde2019-airflow-ml-workshop/requirements.txt:/requirements.txt \`: install the requirements for the workshop exercises
- `-v $HOME/pyconde2019-airflow-ml-workshop/:/usr/local/airflow/pyconde2019-airflow-ml-workshop:rw `: mount the project repository volume
- `-v $HOME/pyconde2019-airflow-ml-workshop/dags/:/usr/local/airflow/dags:rw`: mount the volume that contains the dags (the exercise worflows)
- `puckel/docker-airflow webserver`: run Airflow with `SequentialExecutor`

:pushpin: In **this tutorial** we use **Airflow with SQLite DB** and the **[SequentialExecutor](https://airflow.apache.org/_modules/airflow/executors/sequential_executor.html)**.

Executors are the mechanism by which tasks in workflow get run.
The **Sequential** one allows to run **one task instance at a time** (this is not a production setup). Consider also that SQLite doesn't support multiple connections.

:clock11: Wait 1-2 minutes to let Docker be ready with a **fresh live Airflow instance**!
With this dockerized AF version we run a container that spins up both **Scheduler** and **Webserver**.

:white_check_mark: **Go to [http://localhost:8080](http://localhost:8080)** to see that **Airflow is running**. When it will be ready you should see a screen like this:

<p align="center">
<img src="/media/airflow_docker.png" alt="airflow docker" width="90%"/>
</p>

:trophy: **Great! Now everything is ready for starting the Exercises!**

:white_check_mark: Jump to the [Airflow main concepts](https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop/blob/master/airflow_main_concepts.md) section for continuing the tutorial.
