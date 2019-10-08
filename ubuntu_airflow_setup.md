## Ubuntu Airflow Setup [:top:](README.md#table-of-contents)

### Download the repository

**Clone the repository** in your **`home`** directory
`/home/<user>/`.
We'll refer this location during the workshop.

```bash
$ git clone https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop
```

### Ubuntu Linux
To proceed with the workshop, it is necessary to have **Python 3.7+** installed on your machine.
:warning: Note: The procedure varies according to your distribution and its version.

:warning:We provide some **basic instructions** for the latest LTS version of **Ubuntu, 18.04**.

Be logged in as a user with **sudo access** for being able to install packages.

### Create a 3.7+ Python environment

Install Pip, Python 3.7+ and [venv](https://docs.python.org/3/library/venv.html)
```bash
$ sudo apt update
$ sudo apt -y upgrade
# Install pip if not already present on your machine
$ sudo apt install python3-pip
# Ubuntu 18.04 ships only Python 3.6. Add this ppa repo to download Python 3.7
$ sudo add-apt-repository ppa:ubuntu-toolchain-r/ppa
# Install Python3.7 and venv for creating virtual environment
$ sudo apt install python3.7 python3.7-dev python3.7-venv
# Create a virtual environment named airflow_env in your home
$ python3.7 -m venv /home/<user>/airflow_env
# Activate it
$ source /home/<user>/airflow_env/bin/activate
```

### 2. Install Airflow

Move to the repository directory (it should be in your `home directory` `/home/<user>/`) for **installing** Airflow:
```bash
# Go to the directory where you download the repo
$ cd /home/<user>/pyconde2019-airflow-ml-workshop
# export the PYTHONPATH
$ export PYTHONPATH=$PYTHONPATH:/home/<user>/pyconde2019-airflow-ml-workshop/
# avoid raise RuntimeError("By default one of Airflow's dependencies installs a GPL "
$ export SLUGIFY_USES_TEXT_UNIDECODE=yes
# upgrade pip
$ pip3.7 install pip --upgrade
# install requirements in the environment
$ pip3.7 install -r requirements.txt
```

### 3. Initialise Airflow DB

Before launching Airflow, **initialise the SQLite Airflow database**.
The AF Database keeps information about dags, tasks, connections, users, etc.
This is the default option, in production you will probably use another RDBMS like MySQL or PostgreSQL.
Note: SQLite doesn't allow to parallelise tasks.

Initialise the database:

```bash
airflow initdb
```

### 4. Configure Airflow

Airflow creates the directory `~/airflow/` and it stores inside:
  - :mag: the **configuration file `airflow.cfg`**
  - the SQLite DB `airflow.db`
  - the `log` repository

Export the environment variable `AIRFLOW_HOME`
```bash
$ export AIRFLOW_HOME=/home/<user>/airflow
```

The cloned **repository** has inside a **subfolder** named **`dags`** that contains the **DAGs**, our workflows **python files**, that we'll use during this workshop.

:pencil2: **Modify** the **`/home/<user>/airflow/airflow.cfg`**: find the **`dags_folder` parameter** and configure it for loading the python files in the **dags folder repository**.
:white_check_mark: Instead of `dags_folder = /home/<user>/airflow/dags`
put **`dags_folder = /home/<user>/pyconde2019-airflow-ml-workshop/dags`**


### 5. Run Airflow webserver

Finally everything is ready for **running** the **Airflow webserver**!

From the `airflow_env` active virtualenv, execute:
```{bash}
$ airflow webserver --port 8080
```
and then open the **browser** to **[localhost:8080](http://localhost:8080/)**.

Check out the Airflow UI:

<p align="center">
<img src="/media/airflow_initdb.png" alt="airflow ui after initdb" width="90%"/>
</p>

### 6. Run Airflow scheduler

The **Airflow Webserver** is running in its virtual environment.
We need to activate the same virtual environment but for the **Scheduler**.

For starting the AF Scheduler, activate a 2nd environment in another terminal (in the `~/pyconde2019-airflow-ml-workshop` directory) and launch the scheduler.
Note: it's foundamental that both `Scheduler` and `Webserver` have

```bash
$ source /home/<user>/airflow_env/bin/activate
$ cd /home/<user>/pyconde2019-airflow-ml-workshop
$ export PYTHONPATH=$PYTHONPATH:/home/<user>/pyconde2019-airflow-ml-workshop/
$ export AIRFLOW_HOME=/home/<user>/airflow
$ airflow scheduler
```

:warning: Note: If in the terminal you read this message `ERROR - Cannot use more than 1 thread when using sqlite. Setting parallelism to 1`.
This is because we are using **Airflow with SQLite** DB and the **[SequentialExecutor](https://airflow.apache.org/_modules/airflow/executors/sequential_executor.html)**.

Executors are the mechanism by which task instances get run.
The **Sequential** one allows to run **one task instance at a time** (this is not a setup for production). Consider also that SQLite doesn't support multiple connections.

<p align="center">
<img src="/media/airflow_error_sqlite_parallelism.png" alt="airflow SequentialExecutor sqlitedb" width="80%"/>
</p>


:trophy: **Great! Now everything is ready for starting the Exercises!**

:white_check_mark: Jump to the [Airflow main concepts](https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop/blob/master/airflow_main_concepts.md) section for continuing the tutorial.
