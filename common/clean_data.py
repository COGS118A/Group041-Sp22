"""Dataset Link: https://www.kaggle.com/datasets/kimjihoo/coronavirusdataset?select=TimeProvince.csv

This file is used to combine the data (the csv files) in the data folder into one dataset, clean it, turn it into a
dataframe object, and save it both as a csv and a dataframe. The process of feature selection will be semi-automated
using Scikit Learn's feature selection to find the most variable features, and semi-manual to ensure that no poor
features are selected, and no important features are missed.
"""

