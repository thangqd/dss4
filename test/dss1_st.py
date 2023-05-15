import streamlit as st
import os
import pandas as pd
import geopandas as gpd
import json
import requests
from streamlit_folium import st_folium, folium_static
from pandas.api.types import is_numeric_dtype
from dss import *
from datetime import timedelta


uploaded_file = st.file_uploader("Choose a CSV file")
# uploaded_file = os.path.join(os.path.dirname(__file__), '../data/dss1.csv')
st.write(uploaded_file)


def loadata(input, fromdate, todate):    
    # df_filter = df.loc[fromdate:todate]
    df = pd.read_csv(uploaded_file,skiprows=[1])
    df["Date"] =  pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.date # convert Date field to Datetime 
    df_filter = df[(df['Date'] >= fromdate) & (df['Date'] < todate)]
    st.dataframe(df_filter)
    st.write(df_filter.dtypes)
    st.write(df_filter.describe()) 
    st.map(df_filter)
    result = df_filter.select_dtypes(include='number')
    st.line_chart(result)
    return df_filter

if uploaded_file is not None:
    fromdate = st.date_input("From date", pd.to_datetime('today')- timedelta(days=1000))
    todate = st.date_input("To date", pd.to_datetime('today')) 

    if st.button('Filter data by date'):
        loadata(input, fromdate, todate)

    if st.button('Calculate DSS1'):       
        st.write(dss1(uploaded_file,fromdate,todate))

