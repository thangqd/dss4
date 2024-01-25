import pandas as pd
from pandas.api.types import is_numeric_dtype
pd.options.mode.copy_on_write = True
from datetime import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt


# Calculate DSS1
def dss4_preprocessing (input):
    ######### remove NULL value
    df = pd.read_csv(input,encoding = "UTF-8") # depend on exisitng dss4.csv file
    print('Statistics of original data:',  df['S1'].describe())  
    print('Before remove NULL values', len(df)) 
    df = df.dropna(subset=['S1','S2','S3','S4']) 
    print('After remove NULL values', len(df)) 
   
    ######### Detect outliers of S1
    Q1 = df['S1'].quantile(0.25)
    Q3 = df['S1'].quantile(0.75)
    IQR = Q3 - Q1
    # identify outliers
    threshold = 1.5
    outliers = df[(df['S1'] < Q1 - threshold * IQR) | (df['S1'] > Q3 + threshold * IQR)]
    print ('outliers: ', outliers)
    df = df.drop(outliers.index)
    print('After remove NULL values', len(df))
    return df

def dss4_final (input, status_callback):
   df = dss4_preprocessing (input)
   return df