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
            page_title="DSS Calculation Module",
            page_icon=":aquarius:",
            layout="centered",
            initial_sidebar_state="auto",
            menu_items={
                'About': "https://thangqd.github.io"
            }
)

class dss():    
    def __init__(self):
        st.header("DSS Calculation Module")
        st.subheader("©2023 by watertech.vn")    
    def gui(self):    
        DSS_list = ['DSS4']
        DSS_url = ['./data/dss4.csv']                
        self.dss_calc = st.selectbox('Choose a DSS to calculate',DSS_list)
        self.selected_index = DSS_list.index(self.dss_calc)
        self.url = st.text_input(
            "Enter DSS data URL",
            DSS_url[self.selected_index]
        )
        self.uploaded_file = st.file_uploader("Or upload a CSV file")
        dss4 = None, None, None, None
        form = st.form(key="form_settings")
        with form:           
            # self.uploaded_file = os.path.join(os.path.dirname(__file__), '../data/dss1.csv')
            # if (self.url or self.uploaded_file):
            #     if self.dss_calc == 'DSS1':
            #         self.fromdate  = st.date_input("From date", pd.to_datetime('today')- timedelta(days=1000))
            #         self.todate = st.date_input("To date", pd.to_datetime('today'))                
            submitted = st.form_submit_button("Calculate DSS")
            
            if submitted:
                self.status_lable ="Calculation progress"
                status_bar = st.progress(0, text=self.status_lable)
                self.status_bar= status_bar
                if self.url:  
                    # if self.dss_calc == 'DSS1': 
                    #     # self.dss_result = self.calculate_dss(self.url,self.fromdate,self.todate, self.dss_status_callback) 
                    #     dss1 = dss1_final(self.url,self.fromdate,self.todate,self.dss_status_callback)
                    #     dss1["Date"] = pd.to_datetime(dss1["Date"]).dt.date
                    #     try:
                    #         st.dataframe(dss1.style.applymap(self.color,subset=['WQI_Color']))          
                    #     except: st.write(dss1)
                    #     # self.download_csv(dss1,self.dss_status_callback)
                    #     # self.download_geojson(dss1,self.dss_status_callback)
                    #     # self.viewmap_dss1(dss1,dss_status_callback = None)
                    
                    # elif self.dss_calc == 'DSS2': 
                    #     # self.dss_result = self.calculate_dss(self.url,self.fromdate,self.todate, self.dss_status_callback) 
                    #     dss2 = dss2_final(self.url,self.dss_status_callback)
                    #     try:
                    #         st.dataframe(dss2.style.applymap(self.color,subset=['W_SCI1_Color','W_SCI2_Color','W_SCI3_Color']))          
                    #     except: st.write(dss2)
                    #     # self.download_csv(dss2,self.dss_status_callback)
                    #     # self.download_geojson(dss2,self.dss_status_callback)
                    #     # self.viewmap_dss2(dss2,dss_status_callback = None)       

                    # elif self.dss_calc == "DSS3":
                    #     dss3 = dss3_final(self.url,self.dss_status_callback)
                    #     try:
                    #         st.dataframe(dss3.style.applymap(self.color,subset=['Risk_Color']))          
                    #     except: st.write(dss3)
                    #     # self.download_csv(dss3,self.dss_status_callback)
                    #     # self.download_geojson(dss3,self.dss_status_callback)
                    #     # self.viewmap_dss3(dss3,dss_status_callback = None)
                    if self.dss_calc == "DSS4":
                        dss4 = dss4_final(self.url,self.dss_status_callback)
                        st.write (dss4)
                
                elif self.uploaded_file:
                    # self.dss_result = self.calculate_dss(self.uploaded_file,self.fromdate,self.todate, self.dss_status_callback)
                    # if self.dss_calc == 'DSS1': 
                    #     # self.dss_result = self.calculate_dss(self.url,self.fromdate,self.todate, self.dss_status_callback) 
                    #     dss1 = dss1_final(self.uploaded_file,self.fromdate,self.todate,self.dss_status_callback)
                    #     dss1["Date"] = pd.to_datetime(dss1["Date"]).dt.date
                    #     try:
                    #         st.dataframe(dss1.style.applymap(self.color,subset=['WQI_Color']))          
                    #     except: st.write(dss1)
                    #     # self.download_csv(dss1,self.dss_status_callback)
                    #     # self.download_geojson(dss1,self.dss_status_callback)
                    #     # self.viewmap_dss1(dss1,dss_status_callback = None)
                
                    # elif self.dss_calc == 'DSS2': 
                    #         # self.dss_result = self.calculate_dss(self.url,self.fromdate,self.todate, self.dss_status_callback) 
                    #         dss2 = dss2_final(self.uploaded_file,self.dss_status_callback)
                    #         try:
                    #             st.dataframe(dss2.style.applymap(self.color,subset=['W_SCI1_Color','W_SCI2_Color','W_SCI3_Color']))          
                    #         except: st.write(dss2)
                    #         # self.download_csv(dss2,self.dss_status_callback)
                    #         # self.download_geojson(dss2,self.dss_status_callback)
                    #         # self.viewmap_dss2(dss2,dss_status_callback = None)   
                    
                    # elif self.dss_calc == "DSS3":
                    #     dss3 = dss3_final(self.uploaded_file,self.dss_status_callback)
                    #     try:
                    #         st.dataframe(dss3.style.applymap(self.color,subset=['Risk_Color']))          
                    #     except: st.write(dss3)
                    #     # self.download_csv(dss3,self.dss_status_callback)
                    #     # self.download_geojson(dss3,self.dss_status_callback)
                    #     # self.viewmap_dss3(dss3,dss_status_callback = None)
                    #     # st.button('Calculate DSS', on_click=self.dss_result)  
                    if self.dss_calc == "DSS4":
                        dss4 = dss4_final(self.url,self.dss_status_callback)
                        st.write (dss4)
        # if dss1 is not None:
        #     self.viewmap_dss1(dss1,self.dss_status_callback)
        #     self.download_csv(dss1,self.dss_status_callback)
        #     self.download_geojson(dss1,self.dss_status_callback)
            
        
        # if dss2 is not None:
        #     self.viewmap_dss2(dss2,self.dss_status_callback)
        #     self.download_csv(dss2,self.dss_status_callback)
        #     self.download_geojson(dss2,self.dss_status_callback)

        # if dss3 is not None:
        #     self.viewmap_dss3(dss3,self.dss_status_callback)
        #     self.download_csv(dss3,self.dss_status_callback)
        #     self.download_geojson(dss3,self.dss_status_callback)

        # if dss4 is not None:
        #     self.download_csv(dss4,self.dss_status_callback)


        st.divider()
        st.caption("Coded by [Thang Quach](https://thangqd.github.io)")
        # button(username="quachdongthang", floating=False, width=221)

    
    def loadata(self, input, fd, td):    
        # df_filter = df.loc[fromdate:todate]
        df = pd.read_csv(input,skiprows=[1])
        df["Date"] =  pd.to_datetime(df["Date"],dayfirst=True) # convert Date field to     
        df_filter = df.loc[(df['Date'] >= fd) & (df['Date']<= td)]
        st.dataframe(df_filter)
        # st.write(df_filter.dtypes)
        st.write(df_filter.describe()) 
        st.map(df_filter)
        result = df_filter.select_dtypes(include='number')
        st.line_chart(result)
        return df_filter    
    
   
    def color(self,val):
        return f'background-color: {val}'      
    
    def viewmap_dss4(self, df,dss_status_callback = None):        
       pass
  
     
    def download_csv(self, df,dss_status_callback = None):  
        if not df.empty:
            if 'Date' in df.columns:  
                df['Date'] =  df["Date"].astype(str)
            # csv = df.to_csv(index=False).encode('UTF-8') 
            csv = df.to_csv(encoding ='utf-8')        
            click = ste.download_button(
            label= "Download CSV " + self.dss_calc,
            data = csv,
            file_name= self.dss_calc + ".csv",
            mime = "text/csv")        

        
    def download_geojson(self, df,dss_status_callback = None):
        if not df.empty:
            if 'Date' in df.columns:  
                df['Date'] =  df["Date"].astype(str)
            # st.write(df.dtypes) 
            try: 
                gdf = gpd.GeoDataFrame(
                    df, geometry=gpd.points_from_xy(df.longitude, df.latitude)
                )
            except:
                gdf = gpd.GeoDataFrame(
                    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude)
                )

            # st.write(gdf)
            geojson = gdf.to_json()  
            ste.download_button(
                label="Download GeoJSON",
                file_name= self.dss_calc + ".geojson",
                mime="application/json",
                data=geojson
            ) 
       
             
    def dss_status_callback(self, percent_complete, lable):        
        self.status_bar.progress(percent_complete, text=lable)              

# if __name__ == '__main__':
ct = dss()
ct.gui()