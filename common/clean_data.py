"""Dataset Link: https://www.kaggle.com/datasets/kimjihoo/coronavirusdataset?select=TimeProvince.csv

This file is used to combine the data (the csv files) in the data folder into one dataset, clean it, turn it into a
dataframe object, and save it both as a csv and a dataframe. The process of feature selection will be semi-automated
using Scikit Learn's feature selection to find the most variable features, and semi-manual to ensure that no poor
features are selected, and no important features are missed.
"""

import csv
import pickle
import pandas as pd


if __name__ == 'main':

    # Open the files of each dataset
    case_file = pd.read_csv('../data/raw_data/Case.csv')
    patient_file = pd.read_csv('../data/raw_data/PatientInfo.csv')
    policy_file = pd.read_csv('../data/raw_data/Policy.csv')
    region_file = pd.read_csv('../data/raw_data/Region.csv')
    search_trend_file = pd.read_csv('../data/raw_data/SearchTrend.csv')
    #seoul_file = pd.read_csv('../data/raw_data/SeoulFloating.csv')
    test_file = pd.read_csv('../data/raw_data/Time.csv')
    time_file = pd.read_csv('../data/raw_data/TimeAge.csv')
    gender_file = pd.read_csv('../data/raw_data/TimeGender.csv')
    providence_file = pd.read_csv('../data/raw_data/TimeProvince.csv')
    weather_file = pd.read_csv('../data/raw_data/Weather.csv')