import pandas as pd
from pandas.api.types import is_numeric_dtype
pd.options.mode.copy_on_write = True
from datetime import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Calculate DSS1
def dss4_preprocessing (input):
    ######### remove NULL value   
    df = pd.read_csv(input,encoding = "UTF-8") # depend on exisitng dss4.csv file
    df["Date"] =  pd.to_datetime(df["Date"],dayfirst=True)
    print('Before processing: ', len(df)) 
    # print('Before remove NULL values', len(df)) 
    df = df.dropna(subset=['S1','S2','S3','S4']) 
    print('After remove NULL values', len(df)) 
   
    ######### Detect and delete outliers of S1
    Q1 = df['S1'].quantile(0.25)
    Q3 = df['S1'].quantile(0.75)
    IQR = Q3 - Q1
    # identify outliers
    threshold = 1.5
    outliers = df[(df['S1'] < Q1 - threshold * IQR) | (df['S1'] > Q3 + threshold * IQR)]
    # print ('outliers: ', outliers)
    df = df.drop(outliers.index)
    # print('After remove NULL values', len(df))

    ######## Detect and delete outliers of S2
    Q1 = df['S2'].quantile(0.25)
    Q3 = df['S2'].quantile(0.75)
    IQR = Q3 - Q1
    # identify outliers
    threshold = 1.5
    outliers = df[(df['S2'] < Q1 - threshold * IQR) | (df['S2'] > Q3 + threshold * IQR)]
    df = df.drop(outliers.index)

    ######## Detect and delete outliers of S3
    Q1 = df['S3'].quantile(0.25)
    Q3 = df['S3'].quantile(0.75)
    IQR = Q3 - Q1
    # identify outliers
    threshold = 1.5
    outliers = df[(df['S3'] < Q1 - threshold * IQR) | (df['S3'] > Q3 + threshold * IQR)]
    df = df.drop(outliers.index)

    ######## Detect and delete outliers of S3
    Q1 = df['S4'].quantile(0.25)
    Q3 = df['S4'].quantile(0.75)
    IQR = Q3 - Q1
    # identify outliers
    threshold = 1.5
    outliers = df[(df['S4'] < Q1 - threshold * IQR) | (df['S4'] > Q3 + threshold * IQR)]
    df = df.drop(outliers.index)

    print('After remove outliers: ', len(df))
    print('Statistics of processed data:')  
    print('S1:',  df['S1'].describe())  
    print('S2:',  df['S2'].describe())  
    print('S3:',  df['S3'].describe())  
    print('S4:',  df['S4'].describe())  

    return df

def dss4_final (input, status_callback):
    i = 0
    steps =1    
    df = dss4_preprocessing (input)
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Preprocessing Data'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    return df