## Mac OS X Airflow Setup [:top:](README.md#table-of-contents)

### Download the repository
**Clone the repository** in your **`home`** directory `/Users/<user>/`.
We'll refer this location during the workshop.

```bash
$ git clone https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop
```

To setup an Airflow instance we recommend to use a **Python 3.7+** virtual environment.
If you have already one you can skip the creation and jump to the installation phase, based on your OS.


### 1. Create a 3.7+ Python environment

If you don't have a Python 3.7+, you can use [pyenv](https://github.com/pyenv/pyenv) to install different Python versions on your macOS.

**Install pyenv** with [Homebrew](https://brew.sh) and **Python 3.7.0**
```bash
$ brew install pyenv
$ pyenv install 3.7.0
```

**Create the virtual environment** with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is a plugin that provides features to manage virtual environments for Python.
  - install pyenv-virtualenv with [Homebrew](https://brew.sh)
    ```bash
    $ brew install pyenv-virtualenv
    ```
  - **create** and **activate** a **3.7.0 venv** named **airflow_env**
    ```
    $ pyenv virtualenv 3.7.0 airflow_env
    $ pyenv activate airflow_env
    ```
    (_to deactivate: `pyenv deactivate`_)

  - **export** the **PYTHONPATH** where you cloned the repository
  (it should be in your `home directory` `/Users/<user>/`)
    ```bash
    $ export PYTHONPATH=$PYTHONPATH:/Users/<user>/pyconde2019-airflow-ml-workshop/
    # verify that it contains the path to the repository
    $ echo $PYTHONPATH
    ```

### 2. Install Airflow

Move to the repository directory (it should be in your `home directory` `/Users/<user>/`) for **installing** Airflow:
  ```bash
  $ cd ~/pyconde2019-airflow-ml-workshop
  $ pip install pip --upgrade
  $ pip install -r requirements.txt
  ```

### 3. Initialise Airflow DB

Before launching Airflow, **initialise** the **SQLite Airflow database**.
This is the default option, in production you will probably use another RDBMS like MySQL or PostgreSQL.
SQLite doesn't allow to parallelize tasks.
The AF Database keeps information about dags, tasks, connections, users, etc.
Initialise the database:
```{bash}
$ airflow initdb
```
:pushpin: If you encounter this warning `WARNI [airflow.utils.log.logging_mixin.LoggingMixin] cryptography not found - values will not be stored encrypted.` it's because, for the scope of this tutorial, we didn't install the `cryptography` package. For a production environment you should install it.

### 4. Configure Airflow

**Airflow creates the directory `~/airflow/`** and it stores inside:
  - :mag: the **configuration file `airflow.cfg`**
  - the SQLite DB `airflow.db`
  - the `log` repository

Export the environment variable `AIRFLOW_HOME`
```bash
$ export AIRFLOW_HOME=/Users/<user>/airflow
```

The cloned **repository** has inside a **subfolder** named **`dags`** that contains the **DAGs**, our workflows **python files**, that we'll use during this workshop.

:pencil2: **Modify** the **`/Users/<user>/airflow/airflow.cfg`**:
find in the file the **`dags_folder` parameter** and configure it for loading the python files in the **dags folder repository**.

:white_check_mark: Instead of `dags_folder = /Users/<user>/airflow/dags`
put **`dags_folder = /Users/<user>/pyconde2019-airflow-ml-workshop/dags`**


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

For starting the AF Scheduler, activate a 2nd environment in another terminal (in the ``~/pyconde2019-airflow-ml-workshop` directory) and launch the scheduler.
Note: it's foundamental that both `Scheduler` and `Webserver` have
```bash
$ pyenv activate airflow_env
# Allow to run python script with multithreading in Mac OS X (see note below)
$ export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
$ export PYTHONPATH=$PYTHONPATH:/Users/<user>/pyconde2019-airflow-ml-workshop/
$ export AIRFLOW_HOME=/Users/<user>/airflow
$ airflow scheduler
```

:pushpin: Note regarding the command `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`: this command prevents Mac OS X, when running the Airflow Scheduler, to keep throwing messages like
```
objc[47911]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
```
(for more details see the [Apache Airflow jira ticket AIRFLOW-3326](https://issues.apache.org/jira/browse/AIRFLOW-3326) for details)


:warning: Note: If in the terminal you read this message `ERROR - Cannot use more than 1 thread when using sqlite. Setting parallelism to 1`.
This is because we are using **Airflow with SQLite DB** and the **[SequentialExecutor](https://airflow.apache.org/_modules/airflow/executors/sequential_executor.html)**.

Executors are the mechanism by which task instances get run.
The **Sequential** one allows to run **one task instance at a time** (this is not a setup for production). Consider also that SQLite doesn't support multiple connections.

<p align="center">
<img src="/media/airflow_error_sqlite_parallelism.png" alt="airflow SequentialExecutor sqlitedb" width="80%"/>
</p>

<br />

:trophy: **Great! Now everything is ready for starting the Exercises!**

:white_check_mark: Jump to the [Airflow main concepts](#airflow-main-concepts-top) section for continuing the tutorial.
