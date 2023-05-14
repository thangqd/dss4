import streamlit as st
import os
import pandas as pd
import geopandas as gpd
import json
import requests
from streamlit_folium import st_folium, folium_static
from pandas.api.types import is_numeric_dtype

df = pd.read_csv('dss1.csv',skiprows=[1])               
df["Date"] =  pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.date
fromdate = st.date_input("From date", df["Date"].min())
todate = st.date_input("To date",  df["Date"].max())  

def loadata(df, fromdate, todate):    
    df_filter = df[(df['Date'] >= fromdate) & (df['Date'] < todate)]
    st.dataframe(df_filter)
    st.write(df_filter.dtypes)
    st.write(df_filter.describe()) 
    st.map(df_filter)
    result = df_filter.select_dtypes(include='number')
    st.line_chart(result)
    return df_filter

BPi_I = [5.5,5.5,6.0,8.5,9.0,9.0]
Qi_I = [10,50,100,100,50,10]
index_labels=['BPi','Qi']

if st.button('Load data'):
    df = loadata(df, fromdate, todate)

params_I = pd.DataFrame(
        {
            "1": [5.5,50],
            "2": [6,100],
            "3": [8.5,100], 
            "4": [9,50]
        },
        index=index_labels
)
st.write(params_I)

def dss1_I(df,pH):
    # st.write(df.describe()) 
    result = 1
    if pH < params_I.iloc[0][0] or pH >params_I.iloc[0][-1]: # pH < 5.5 or pH > 9
        result = 10
        st.write('pH < 5.5 or pH > 9')
    elif (pH >= params_I.iloc[0][0]) and  (pH <params_I.iloc[0][1]): # 5.5 <= pH < 6
        result = params_I.iloc[1][0]+ (params_I.iloc[1][1] - params_I.iloc[1][0])/(params_I.iloc[0][1]-params_I.iloc[0][0])*(pH-params_I.iloc[0][0])
        st.write('5.5 <= pH < 6')
    elif (pH >= params_I.iloc[0][1]) and  (pH <params_I.iloc[0][2]): # 6 <= pH < 8.5
        result = 100
        st.write('6 <= pH < 8.5')
    elif (pH >= params_I.iloc[0][2]) and  (pH <params_I.iloc[0][3]):  # 8.5 <= pH <=9
        result = params_I.iloc[1][3]+ (params_I.iloc[1][2]-params_I.iloc[1][3])/(params_I.iloc[0][3]-params_I.iloc[0][2])*(params_I.iloc[0][3]-pH)  
        st.write('8.5 <= pH <=9')           
    return result


pH = st.number_input('Insert pH value') 

if st.button('Calculate DSS1'):
    st.write('DSS1 for pH:')
    st.write(dss1_I(df,pH))