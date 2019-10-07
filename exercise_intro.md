## Exercises: Airflow for training and predicting [:top:](README.md#table-of-contents)

<p align="center">
<img src="/media/main_steps_all.png" alt="all exercises" width="90%"/>
</p>

In this part we'll use Airflow for training a Machine Learning model and then do predictions with that.

During the workshop we'll guide you through the steps to complete the exercises.
For each exercise you'll find a description of the operations to perform.

#### Business Problem

**In this tutorial, we want to solve a simple business problem by using a machine learning procedure that will be managed via Apache Airflow**

Our business requires to have daily temperature forecast for forthcoming days.
Moreover, they would like to automate this requirement.

In other words, we are going to try to have an accurate glimpse of the future in an automated way.

In this tutorial, we are going to train a time series model to forecast the minimum temperature at Melbourne,
Australia for the given date interval.

Our data is a [well-known time series](https://www.kaggle.com/paulbrabban/daily-minimum-temperatures-in-melbourne) which consists of 3650 observations.
It records the weather change from 1981 to 1990. The units are in degrees Celsius and observations are in daily granularity.
The source of the data is credited to the Australian Bureau of Meteorology.

The dataset has a trend/seasonality/noise component which is a very common phenomenon that we will face while dealing with **time series problems**.

During model training, we are going to use ARIMA (Autoregressive Integrated Moving Average) model.
In ARIMA we have three main hyperparameters to tune and [pyramid-arima](https://pypi.org/project/pmdarima/) package's `auto_arima()` function is going to handle this task for us.
Parameter selection procedure relies on AIC (Akaike Information Criteria).

**ARIMA Parameters:**
* **p:** Parameter associated with the autoregressive aspect of the model. It determines how many lags to
use at the model. It other words, order of the AR model.

* **d:** Parameter associated with the integrated part of the model which determines the differencing to apply to make data stationary.

* **q:** Parameter to define moving averages. It determines the size of the window for moving average.

For better, more accurate models, it requires proper hyperparameter-tuning and domain expertise BUT having
a better model/forecast is not the real aim of this tutorial.

Go to [EX 1. Preconditions: Variables, Tables and Connection](https://github.com/deliveryhero/pyconde2019-airflow-ml-workshop/blob/master/exercise_1.md).
