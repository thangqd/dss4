import streamlit as st
import streamlit_ext as ste
# import os
import pandas as pd
import geopandas as gpd
import numpy as np
# import json
# import requests
from streamlit_folium import st_folium, folium_static
# from pandas.api.types import is_numeric_dtype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'data'))

from dss4 import dss4_final
import folium
from folium.plugins import MarkerCluster, FastMarkerCluster, Fullscreen


# from streamlit_extras.buy_me_a_coffee import button
from datetime import timedelta
st.set_page_config(
            page_title="MKDC DSS 4 - CSI Forecast",
            page_icon=":aquarius:",
            layout="wide",
            initial_sidebar_state="auto",
            menu_items={
                'About': "https://thangqd.github.io"
            }
)

class dss4():    
    def __init__(self):
        st.header("MKDC DSS 4 - Coastal Salinity Index Forecast")
        # st.subheader("©2023 by watertech.vn")    
    def gui(self):     
        col1, col2 = st.columns(2)
        with col1: 
            form = st.form(key="dss4")    
            with form:   
                self.url = st.text_input(
                "Enter DSS data URL",
                "./data/dss4.csv"
                )
                self.uploaded_file = st.file_uploader("Or upload a CSV file")
                dss4 = None                                       
                submitted = st.form_submit_button("Run CSI Forecast")
                    
                    
        if submitted:
            with col2:
                self.status_lable ="Calculation progress"
                status_bar = st.progress(0, text=self.status_lable)
                self.status_bar= status_bar

                if self.url:  
                    dss4 = dss4_final(self.url,self.dss_status_callback)      
                    
                elif self.uploaded_file:                 
                    dss4 = dss4_final(self.url,self.dss_status_callback)       

                st.table(dss4[['S1', 'S2', 'S3', 'S4']].describe())
                st.write (dss4)
                if dss4 is not None:
                    self.download_csv(dss4,self.dss_status_callback)            
        
    def loadata(self, input, fd, td):    
        # df_filter = df.loc[fromdate:todate]
        df = pd.read_csv(input,skiprows=[1])
        df["Date"] =  pd.to_datetime(df["Date"],dayfirst=True) # convert Date field to     
        df_filter = df.loc[(df['Date'] >= fd) & (df['Date']<= td)]
        st.dataframe(df_filter)
        # st.write(df_filter.describe()) 
        st.map(df_filter)
        result = df_filter.select_dtypes(include='number')
        st.line_chart(result)
        return df_filter    
    
   
    def color(self,val):
        return f'background-color: {val}'      
    
     
    def download_csv(self, df,dss_status_callback = None):  
        if not df.empty:
            if 'Date' in df.columns:  
                df['Date'] =  df["Date"].astype(str)
            # csv = df.to_csv(index=False).encode('UTF-8') 
            csv = df.to_csv(encoding ='utf-8')        
            click = ste.download_button(
            label= "Download CSV",
            data = csv,
            file_name= "DSS4.csv",
            mime = "text/csv")        

        
    def dss_status_callback(self, percent_complete, lable):        
        self.status_bar.progress(percent_complete, text=lable)              

# if __name__ == '__main__':
ct = dss4()
ct.gui()