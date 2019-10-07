"""
This script runs time-series forecasting via ARIMA. It contains all the methods necessary
to simulate a time series forecasting task. Below simulation uses daily minimum temp. and tries
to predict min. temp. for given date.

Steps to follow:

    1. Pre-processing raw data. `preprocess_raw_data()`
    2. Splitting data into two as train and test.  `split_data(2)`
    3. Fit model to the train dataset and save model object.  `fit_and_save_model()`
    4. Make prediction for test datasets.  `predict_test_wt_arima()`
    5. Measure the accuracy of predictions for test period. Afterwards save it
    to the local.  `measure_accuracy()`
    6. Use forecast function to have a point estimate for a given date.
    `forecast_wt_arima_for_date(input_date)`

What is ARIMA?
ARIMA is the most common method used in time series forecasting. It is an acronym for
AutoregRessive Integrated Moving Average. ARIMA is a model that can be fitted to time series data
in order to better understand or predict future points in the series.

Details of the dataset:
This dataset describes the minimum daily temperatures over 10 years (1981-1990)
in the city Melbourne, Australia.

The units are in degrees Celsius and there are 3650 observations.
The source of the data is credited as the Australian Bureau of Meteorology
"""
import logging
import math
import os
import pandas as pd
import pickle
import sqlite3

from pmdarima import auto_arima
from datetime import date
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def run_training():
    #TODO
    preprocess_raw_data()
    split_data(2)
    fit_and_save_model()
    predict_test_wt_arima()
    measure_accuracy()


def run_prediction():
    #TODO
    forecast_wt_arima_for_date(str(date.today()))


def read_data(df_phase):
    """
    This function reads necessary data from local for the steps of the simulation.
    :param df_phase: Read data for which step of the simulation.
        Options: ['raw_data', 'processed', 'train_model', 'test_model', 'train_predicted',
        'test_predicted']
    :return: DataFrame read from local.
    """

    if df_phase == 'raw_data':
        repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(repo_path, 'data', 'raw_data', 'daily_minimum_temp.csv')
        df = pd.read_csv(data_path, error_bad_lines=False)

    elif df_phase == 'processed':
        repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(repo_path, 'data', 'interim', 'processed_df.csv')
        df = pd.read_csv(data_path, error_bad_lines=False)

    elif df_phase == 'train_model':
        repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(repo_path, 'data', 'interim', 'train_df.csv')
        df = pd.read_csv(data_path, error_bad_lines=False)

    elif df_phase == 'test_model':
        repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(repo_path, 'data', 'interim', 'test_df.csv')
        df = pd.read_csv(data_path, error_bad_lines=False)

    elif df_phase == 'test_predicted':
        repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(repo_path, 'data', 'interim', 'predicted_test.csv')
        df = pd.read_csv(data_path, error_bad_lines=False)

    return df


def preprocess_raw_data():
    """
    Reads raw data from local and makes pre-processing necessary to use dataset with ARIMA.
    Function assumes that the date column is named as 'Date'. It saves prep-processed dataset
    the local.
    """

    raw_df = read_data('raw_data')

    raw_df['Date'] = list(map(lambda x: pd.to_datetime(x), raw_df['Date']))
    raw_df = raw_df.sort_values('Date')

    procesed_df = raw_df.rename(index=str,
                                columns={'Daily minimum temperatures in Melbourne, '
                                         'Australia, 1981-1990': 'y'})

    for sub in procesed_df['y']:
        if '?' in sub:
            procesed_df.loc[procesed_df['y'] == sub, 'y'] = sub.split('?')[1]

    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(repo_path, 'data', 'interim', 'processed_df.csv')

    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    procesed_df.to_csv(path_or_buf=data_path, index=False, header=True)


def split_data(n_weeks_to_test=2):
    """
    Reads preprocessed data from local and splits it to test/train and saves it to
    local. test_df.csv and train_df.csv can be found under `data/interim` path.
    :param n_weeks_to_test: Number of weeks for the test data. Default is 2.
    """
    preprocessed_data = read_data('processed')
    n_days_for_test = n_weeks_to_test * 7

    test_df = preprocessed_data[-n_days_for_test:]
    train_df = preprocessed_data[:-n_days_for_test]

    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join('data', 'interim')

    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    combined_path_test = os.path.join(repo_path, data_path, 'test_df.csv')
    combined_path_train = os.path.join(repo_path, data_path, 'train_df.csv')

    train_df.to_csv(path_or_buf=combined_path_train, index=False, header=True)
    test_df.to_csv(path_or_buf=combined_path_test, index=False, header=True)


def fit_and_save_model():
    """
    Runs Prophet for the train dataframe. It reads data from local and saves the model
    object to the local. Model can be found under `data/model/arima.pkl`
    """
    train_df = read_data('train_model')
    train_df['Date'] = list(map(lambda x: pd.to_datetime(x), train_df['Date']))
    train_df = train_df.set_index('Date')

    model = auto_arima(train_df, start_p=1, start_q=1,
                       test='adf',
                       max_p=1, max_q=1, m=12,
                       start_P=0, seasonal=True,
                       d=None, D=1, trace=True,
                       error_action='ignore',
                       suppress_warnings=True,
                       stepwise=True)

    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(repo_path, 'data', 'model', 'arima.pkl')

    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    with open(model_path, "wb") as f:
        pickle.dump(model, f)


def predict_test_wt_arima():
    """
    Reads test dataframe and model object from local and makes prediction.
    Data with predicted values for test dataframe will be saved to local.
    """
    test_df = read_data('test_model')

    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(repo_path, 'data', 'model', 'arima.pkl')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    fitted, confint = model.predict(n_periods=len(test_df), return_conf_int=True)

    predicted_test = pd.merge(
        pd.DataFrame(fitted), pd.DataFrame(confint), right_index=True, left_index=True)

    predicted_test = predicted_test.rename(index=str,
                                           columns={'0_x': 'yhat',
                                                    '0_y': 'yhat_lower',
                                                    1: 'yhat_upper'})

    data_path = os.path.join(repo_path, 'data', 'interim')
    combined_path_test = os.path.join(data_path, 'predicted_test.csv')

    predicted_test.to_csv(path_or_buf=combined_path_test, index=False, header=True)


def calculate_mape(y, yhat):
    """
    Calculates Mean Average Percentage Error.
    :param y: Actual values as series
    :param yhat: Predicted values as series
    :return: MAPE as percentage
    """

    y = y.replace(0, np.nan)

    error_daily = y - yhat
    abs_daily_error = list(map(abs, error_daily))
    relative_abs_daily_error = abs_daily_error / y

    mape = (np.nansum(relative_abs_daily_error) / np.sum(~np.isnan(y)))*100

    return mape


def calculate_rmse(y, yhat):
    """
    Calculates Root Mean Square Error
    :param y: Actual values as series
    :param yhat: Predicted values as series
    :return: RMSE value
    """
    error_sqr = (y - yhat)**2
    error_sqr_rooted = list(map(lambda x: math.sqrt(x), error_sqr))
    rmse = sum(error_sqr_rooted) / len(error_sqr_rooted)

    return rmse


def measure_accuracy():
    """
    Uses the above defined accuracy metrics and calculates accuracy for both test series in
    terms of MAPE and RMSE. Saves those results to local as a csv file.
    :return: A dictionary with accuracy metrics for test dataset.
    """
    test_df = read_data('test_model')

    predicted_test = read_data('test_predicted')

    mape_test = calculate_mape(test_df['y'], predicted_test['yhat'])

    rmse_test = calculate_rmse(test_df['y'], predicted_test['yhat'])

    days_in_test = len(test_df)

    accuracy_dict = {'mape_test': [mape_test],
                     'rmse_test': [rmse_test],
                     'days_in_test': [days_in_test]}

    acc_df = pd.DataFrame(accuracy_dict)

    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    acc_path = os.path.join(repo_path, 'data', 'model', 'accuracy.csv')

    acc_df.to_csv(path_or_buf=acc_path, index=False, header=True)

    return acc_df.to_dict('index')[0]


def forecast_wt_arima_for_date(input_date):
    """
    :param input_date: A date as a string in ISO format (yyyy-mm-dd).
    :return: Dictionary with the forecasted values.
            `yhat`: Forecasted value for given date.
            `yhat_upper`: Forecasted upper value for given date & confidence intervals.
            `yhat_lower`: Forecasted lower value for given date & confidence intervals.
    """
    logging.info("Computing forecast for %s", input_date)
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(repo_path, 'data', 'model', 'arima.pkl')

    test_df = read_data('test_model')
    min_test_date = pd.to_datetime(test_df.index.min())

    date_diff = pd.to_datetime(input_date) - min_test_date

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    fitted, confint = model.predict(n_periods=date_diff.days, return_conf_int=True)

    forecast_results = pd.merge(
        pd.DataFrame(fitted), pd.DataFrame(confint), right_index=True, left_index=True)

    forecast_results = forecast_results.rename(
        index=str, columns={'0_x': 'yhat', '0_y': 'yhat_upper', 1: 'yhat_lower'})

    final_forecast = forecast_results[-1:]
    final_forecast['Date'] = input_date
    final_forecast = final_forecast.set_index('Date')

    return final_forecast.to_dict('index')[input_date]


def plot_forecast(sqlite_path='/tmp/sqlite_default.db'):
    """
    Reads DB created by Airflow while making forecasts and generate graph. Afterwards,
    it saves the graph to the local.
    :param sqlite_path: This is the string where Airflow stores the SQLite db file to keep record
    of forecasts. eg: /tmp/sqlite_default.db
    """
    conn = sqlite3.connect(sqlite_path)
    df = pd.read_sql_query("SELECT * FROM prediction;", conn)

    plt.figure(figsize=(20, 10))
    sns.set(style="darkgrid")

    df['date'] = pd.to_datetime(df['date_to_predict'], format='%Y-%m-%d')

    df = df.sort_values('date').reset_index(drop=True)

    plt.plot(df['date_to_predict'], df['yhat'], ls='-', c='#0072B2')

    plt.xlabel('Dates')
    plt.ylabel('Temperature in Celsius')
    plt.title('Graph for Expected Temperature', fontsize=20)
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    figure_path = os.path.join(repo_path, 'plots')

    os.makedirs(figure_path, exist_ok=True)

    plt.savefig(os.path.join(os.path.abspath(figure_path), 'forecasts.png'))


if __name__ == "__main__":
   #run_training()
   #run_prediction()
   preprocess_raw_data()
   split_data(2)
   fit_and_save_model()
   predict_test_wt_arima()
   measure_accuracy()
   print(forecast_wt_arima_for_date(str(date.today())))
