"""Dataset Link: https://www.kaggle.com/datasets/kimjihoo/coronavirusdataset?select=TimeProvince.csv

This file is used to combine the data (the csv files) in the data folder into one dataset, clean it, turn it into a
dataframe object, and save it both as a csv and a dataframe. The process of feature selection will be semi-automated
using Scikit Learn's feature selection to find the most variable features, and semi-manual to ensure that no poor
features are selected, and no important features are missed.
"""

import pickle
import pandas as pd
import os


def save_dataframe(dataframe: pd.DataFrame, directory: str, filename: str, df_list):
    """This method is used to save a dataframe as both a pickle and a csv to the given directory.

    :param dataframe - the dataframe to save
    :param directory - the directory to save it to
    :param filename - the name of the dataframe's file
    :param df_list - the name of the list to store the dataframe in
    """

    # Make the directory if it doesn't exist
    if not os.path.exists('../data/clean_csvs/' + directory):
        os.mkdir('../data/clean_csvs/' + directory)
    if not os.path.exists('../data/dataframes/' + directory):
        os.mkdir('../data/dataframes/' + directory)

    # Store the dataframe as a csv
    dataframe.to_csv('../data/clean_csvs/' + directory + '/' + filename + '.csv')

    # Pickle the dataframe
    dataframe.to_pickle('../data/dataframes/' + directory + '/' + filename + '.pkl')

    # Save the dataframe in the provided list
    if df_list is not None: df_list += [dataframe]


def get_rolling_average(dataframe: pd.DataFrame, cols: list, n):
    """This method returns a new dataframe which is the save as the provided dataframe, except that all specified rows
    have a n-rolling average applied to them, backwards. Elements which are too close to the start to be averaged are
    averaged as to as close to n as they can.

    :param dataframe - the dataframe to copy
    :param cols: a list of column names to apply a rolling average to
    :param n: the size of the rolling average to apply
    """

    # Get a copy of the given dataframe
    df_copy = dataframe.copy()

    # Starting at the lowest possible value, find the rolling average of all rows
    for index in range(n-1, dataframe.shape[0]):

        # For all columns specified...
        for col in cols:

            # Find the sum of the previous n values
            col_sum = 0
            for prev in range(index-(n-1), index): col_sum += dataframe.iloc[prev][col]

            # Set the average as the new value for the copied dataframe
            df_copy.iloc[index][col] = col_sum / n

    # Deal with all indices prior to the n-1th index
    for index in range(n-1):

        # For all columns specified...
        for col in cols:

            # Find the sum of the previous n values
            col_sum = 0
            for prev in range(index+1): col_sum += dataframe.iloc[prev][col]

            # Set the average as the new value for the copied dataframe
            df_copy.iloc[index][col] = col_sum / (index+1)

    # Return the new dataframe
    return df_copy


def get_regional_total(dataframes: list, cols: list):
    """Returns a dataframe who's columns are the total values of"""


if __name__ == '__main__':

    # region Open the files of each dataset

    case_df = pd.read_csv('../data/raw_csvs/Case.csv')
    patient_df = pd.read_csv('../data/raw_csvs/PatientInfo.csv')
    policy_df = pd.read_csv('../data/raw_csvs/Policy.csv')
    region_df = pd.read_csv('../data/raw_csvs/Region.csv')
    search_trend_df = pd.read_csv('../data/raw_csvs/SearchTrend.csv')
    #seoul_df = pd.read_csv('../data/raw_csvs/SeoulFloating.csv')
    test_df = pd.read_csv('../data/raw_csvs/Time.csv')
    age_df = pd.read_csv('../data/raw_csvs/TimeAge.csv')
    gender_df = pd.read_csv('../data/raw_csvs/TimeGender.csv')
    province_df = pd.read_csv('../data/raw_csvs/TimeProvince.csv')
    weather_df = pd.read_csv('../data/raw_csvs/Weather.csv')

    # endregion Open the files of each dataset

    # region Features Extraction
    """Create a dataset for each region, wherein each day of time is one datapoint."""

    # region Regional Features

    # Find the number of unique regions
    regions = province_df['province'].unique()

    # Store the list of regions as a pickled list
    with open('../data/region_list.pkl', 'wb') as file: pickle.dump(regions, file)

    # Create a list of regional dataframes for each feature
    daily_counts = []
    daily_rates = []
    daily_rates_3dra = []
    daily_rates_7dra = []

    # Extract features from each region
    for region in regions:

        # region Get Daily Covid Counts
        
        # Create a new dataframe from the province dataframe
        df_counts = province_df[province_df['province'] == region].drop(['province', 'date', 'time'], axis=1)
        df_counts.reset_index(drop=True, inplace=True)
        df_counts.index.name = 'index'

        # Save the dataframe
        save_dataframe(df_counts, 'daily_counts', region, daily_counts)

        # endregion Get Daily Covid Counts

        # region Daily Covid Rates

        # Change the dataframe into changes in cases over time
        df_rates = df_counts.copy()
        for i in range(1, df_counts.shape[0]): df_rates.iloc[i, :] = df_counts.iloc[i, :] - df_counts.iloc[i-1, :]
        df_rates.iloc[0, :] = df_rates.iloc[1, :]

        # Save the dataframe
        save_dataframe(df_rates, 'daily_rates', region, daily_rates)

        # endregion Daily Covid Rates

        # region 3 Day Rolling Average Covid Rates

        # Get the 3 day rolling average of the covid rates
        df_ra_rates = get_rolling_average(df_rates, df_rates.columns, 3)

        # Save the dataframe
        save_dataframe(df_ra_rates, '3_day_rolling_average_rates', region, daily_rates_3dra)

        # endregion 3 Day Rolling Average Covid Rates

        # region 7 Day Rolling Average Covid Rates

        # Get the week-long rolling average of covid rates
        df_ra_rates = get_rolling_average(df_rates, df_rates.columns, 7)

        # Save the dataframe
        save_dataframe(df_ra_rates, '7_day_rolling_average_rates', region, daily_rates_7dra)

        # endregion 7 Day Rolling Average Covid Rates

    # region Total Regional Features

    # Find and store the total daily counts
    daily_count_total = pd.DataFrame()
    for df in daily_counts: daily_count_total = daily_count_total.add(df, fill_value=0)
    save_dataframe(daily_count_total, 'daily_counts', 'Total', None)

    # Find and store the total daily counts
    daily_rates_total = pd.DataFrame()
    for df in daily_rates: daily_rates_total = daily_rates_total.add(df, fill_value=0)
    save_dataframe(daily_rates_total, 'daily_rates', 'Total', None)

    # Find and store the total daily counts
    daily_rates_3dra_total = pd.DataFrame()
    for df in daily_rates_3dra: daily_rates_3dra_total = daily_rates_3dra_total.add(df, fill_value=0)
    save_dataframe(daily_rates_3dra_total, '3_day_rolling_average_rates', 'Total', None)

    # Find and store the total daily counts
    daily_rates_7dra_total = pd.DataFrame()
    for df in daily_rates_7dra: daily_rates_7dra_total = daily_rates_7dra_total.add(df, fill_value=0)
    save_dataframe(daily_rates_7dra_total, '7_day_rolling_average_rates', 'Total', None)

    # endregion Total Regional Features

    # endregion Regional Features

    # endregion Feature Extraction
