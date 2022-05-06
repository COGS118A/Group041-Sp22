"""Dataset Link: https://www.kaggle.com/datasets/kimjihoo/coronavirusdataset?select=TimeProvince.csv

This file is used to combine the data (the csv files) in the data folder into one dataset, clean it, turn it into a
dataframe object, and save it both as a csv and a dataframe. The process of feature selection will be semi-automated
using Scikit Learn's feature selection to find the most variable features, and semi-manual to ensure that no poor
features are selected, and no important features are missed.
"""

import csv
import pickle
import pandas as pd
from sklearn.feature_selection import VarianceThreshold


if __name__ == '__main__':

    # region Open the files of each dataset

    case_df = pd.read_csv('data/raw_csvs/Case.csv')
    patient_df = pd.read_csv('data/raw_csvs/PatientInfo.csv')
    policy_df = pd.read_csv('data/raw_csvs/Policy.csv')
    region_df = pd.read_csv('data/raw_csvs/Region.csv')
    search_trend_df = pd.read_csv('data/raw_csvs/SearchTrend.csv')
    #seoul_df = pd.read_csv('data/raw_csvs/SeoulFloating.csv')
    test_df = pd.read_csv('data/raw_csvs/Time.csv')
    age_df = pd.read_csv('data/raw_csvs/TimeAge.csv')
    gender_df = pd.read_csv('data/raw_csvs/TimeGender.csv')
    province_df = pd.read_csv('data/raw_csvs/TimeProvince.csv')
    weather_df = pd.read_csv('data/raw_csvs/Weather.csv')

    # endregion Open the files of each dataset

    # region Create Regional Datasets
    """Create a dataset for each region, wherein each day of time is one datapoint."""

    # Find the number of unique regions
    regions = province_df['province'].unique()

    # Store the list of regions as a pickled list
    with open('data/region_list.pkl', 'wb') as file: pickle.dump(regions, file)

    # For each region, make a dataframe, a file, and save each
    for region in regions:
        
        # Create a new dataframe from the province dataframe
        df = province_df[province_df['province'] == region].drop(['province', 'date', 'time'], axis=1)
        df.reset_index(drop=True, inplace=True)
        df.index.name = 'index'
        
        # Store the case counts over time as a csv
        df.to_csv('data/clean_csvs/absolute/' + region + '.csv')

        # Pickle the case counts over time
        df.to_pickle('data/dataframes/absolute/' + region + '.pkl')

        # Change the dataframe into changes in cases over time
        for i in range(1, df.shape[0]):
            
            # Set the columns

    # Create a dataframe of all summed cases
    total_df = test_df.loc[:,'confirmed':'deceased']
    total_df.reset_index(drop=True, inplace=True)
    total_df.index.name = 'index'

    # Store the dataframe as a csv
    total_df.to_csv('data/clean_csvs/absolute/Total.csv')

    # Pickle the dataframe
    total_df.to_pickle('data/dataframes/absolute/Total.pkl')

    # region Create Regional Datasets