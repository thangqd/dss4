import streamlit as st
# import os
import pandas as pd
# import geopandas as gpd
# import json
# import requests
# from streamlit_folium import st_folium, folium_static
# from pandas.api.types import is_numeric_dtype
from dss import *
from datetime import timedelta

class dss():    
    def __init__(self):
        st.header("DSS Calculation Module")
        st.subheader("©2023 by watertech.vn")
        
    def gui(self):       
        self.uploaded_file = st.file_uploader("Choose a CSV file")
        # self.uploaded_file = os.path.join(os.path.dirname(__file__), '../data/dss1.csv')         

        if (self.uploaded_file):
            # st.write(uploaded_file)     
            self.dss_calc = st.selectbox('Choose DSS to calculate',('DSS1','DSS2','DSS3','DSS4','DSS6'))
            self.fromdate = st.date_input("From date", pd.to_datetime('today')- timedelta(days=1000))
            self.todate = st.date_input("To date", pd.to_datetime('today')) 
            # st.button('Load data', on_click=self.loadata(self.uploaded_file,self.fromdate,self.todate))
            self.status_lable ="Calculation progress"
            status_bar = st.progress(0, text=self.status_lable)
            self.status_bar= status_bar
            self.dss_result = self.calculate_dss(self.uploaded_file,self.fromdate,self.todate, self.dss_status_callback)
            st.button('Calculate DSS', on_click=self.dss_result)            
      
        st.divider()
        st.caption("Code by Thang Quach")


    def loadata(self, input, fd, td):    
        # df_filter = df.loc[fromdate:todate]
        df = pd.read_csv(input,skiprows=[1])
        df["Date"] =  pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.date # convert Date field to Datetime 
        df_filter = df[(df['Date'] >= fd) & (df['Date'] <= td)]
        st.dataframe(df_filter)
        # st.write(df_filter.dtypes)
        st.write(df_filter.describe()) 
        st.map(df_filter)
        result = df_filter.select_dtypes(include='number')
        st.line_chart(result)
        return df_filter
      
    def calculate_dss(self, input, fd, td, dss_status_callback = None):
        if self.dss_calc == "DSS1":
            ouput = dss1(input,fd,td,self.dss_status_callback)
        else:  
            df = pd.read_csv(input,skiprows=[1]) 
            df["Date"] =  pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.date # convert Date field to Datetime 
            df_filter = df[(df['Date'] >= fd) & (df['Date'] <= td)]
            ouput = df_filter
        st.write(ouput,) 
        self.download_dss(ouput,self.dss_status_callback)
        # return ouput     

           
    def download_dss(self, df,dss_status_callback = None):
        csv = df.to_csv(index=False).encode('utf-8') 
        st.download_button(
        "Download " + self.dss_calc,
        csv,
        self.dss_calc + ".csv",
        "text/csv",
        key='download-csv')
    
    def dss_status_callback(self, percent_complete, lable):        
        self.status_bar.progress(percent_complete, text=lable)              

if __name__ == '__main__':
    ct = dss()
    ct.gui()