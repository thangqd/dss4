import streamlit as st
# import os
import pandas as pd
import geopandas as gpd
import numpy as np
# import json
# import requests
from streamlit_folium import st_folium, folium_static
# from pandas.api.types import is_numeric_dtype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from dss1 import dss1_final
from dss2 import dss2_final
from dss3 import dss3_final
import leafmap.foliumap as leafmap
import folium
from folium.plugins import MarkerCluster, FastMarkerCluster, Fullscreen
import webcolors


# from streamlit_extras.buy_me_a_coffee import button
from datetime import timedelta
st.set_page_config(
            page_title="DSS Calculation Module",
            page_icon=":aquarius:",
            layout="centered",
            initial_sidebar_state="auto",
            menu_items={
                'Report a bug': "https://github.com/thangqd/dss",
                'About': "https://thangqd.github.io"
            }
)

class dss():    
    def __init__(self):
        st.header("DSS Calculation Module")
        st.subheader("©2023 by watertech.vn")    
    def gui(self):    
        DSS_list = ['DSS1','DSS2','DSS3','DSS4','DSS6']
        DSS_url = ['./data/dss1.csv','./data/dss2.csv','./data/dss3.csv','./data/dss3.csv','./data/dss3.csv']                
        self.dss_calc = st.selectbox('Choose a DSS to calculate',DSS_list)
        self.selected_index = DSS_list.index(self.dss_calc)
        self.url = st.text_input(
            "Enter DSS data URL",
            DSS_url[self.selected_index]
        )
        self.uploaded_file = st.file_uploader("Or upload a CSV file")
        dss1, dss2, dss3 = None, None, None
        form = st.form(key="form_settings")
        with form:           
            # self.uploaded_file = os.path.join(os.path.dirname(__file__), '../data/dss1.csv')
            if (self.url or self.uploaded_file):
                if self.dss_calc == 'DSS1':
                    self.fromdate  = st.date_input("From date", pd.to_datetime('today')- timedelta(days=1000))
                    self.todate = st.date_input("To date", pd.to_datetime('today'))                
            submitted = st.form_submit_button("Calculate DSS")
            
            if submitted:
                self.status_lable ="Calculation progress"
                status_bar = st.progress(0, text=self.status_lable)
                self.status_bar= status_bar
                if self.url:  
                    if self.dss_calc == 'DSS1': 
                        # self.dss_result = self.calculate_dss(self.url,self.fromdate,self.todate, self.dss_status_callback) 
                        dss1 = dss1_final(self.url,self.fromdate,self.todate,self.dss_status_callback)
                        dss1["Date"] = pd.to_datetime(dss1["Date"]).dt.date
                        try:
                            st.dataframe(dss1.style.applymap(self.color,subset=['WQI_Color']))          
                        except: st.write(dss1)
                        # self.download_csv(dss1,self.dss_status_callback)
                        # self.download_geojson(dss1,self.dss_status_callback)
                        # self.viewmap_dss1(dss1,dss_status_callback = None)
                    
                    elif self.dss_calc == 'DSS2': 
                        # self.dss_result = self.calculate_dss(self.url,self.fromdate,self.todate, self.dss_status_callback) 
                        dss2 = dss2_final(self.url,self.dss_status_callback)
                        try:
                            st.dataframe(dss2.style.applymap(self.color,subset=['W_SCI1_Color','W_SCI2_Color','W_SCI3_Color']))          
                        except: st.write(dss2)
                        # self.download_csv(dss2,self.dss_status_callback)
                        # self.download_geojson(dss2,self.dss_status_callback)
                        # self.viewmap_dss2(dss2,dss_status_callback = None)       

                    elif self.dss_calc == "DSS3":
                        dss3 = dss3_final(self.url,self.dss_status_callback)
                        try:
                            st.dataframe(dss3.style.applymap(self.color,subset=['Risk_Color']))          
                        except: st.write(dss3)
                        # self.download_csv(dss3,self.dss_status_callback)
                        # self.download_geojson(dss3,self.dss_status_callback)
                        # self.viewmap_dss3(dss3,dss_status_callback = None)

                elif self.uploaded_file:
                    # self.dss_result = self.calculate_dss(self.uploaded_file,self.fromdate,self.todate, self.dss_status_callback)
                    if self.dss_calc == 'DSS1': 
                        # self.dss_result = self.calculate_dss(self.url,self.fromdate,self.todate, self.dss_status_callback) 
                        dss1 = dss1_final(self.uploaded_file,self.fromdate,self.todate,self.dss_status_callback)
                        dss1["Date"] = pd.to_datetime(dss1["Date"]).dt.date
                        try:
                            st.dataframe(dss1.style.applymap(self.color,subset=['WQI_Color']))          
                        except: st.write(dss1)
                        # self.download_csv(dss1,self.dss_status_callback)
                        # self.download_geojson(dss1,self.dss_status_callback)
                        # self.viewmap_dss1(dss1,dss_status_callback = None)
                
                elif self.dss_calc == 'DSS2': 
                        # self.dss_result = self.calculate_dss(self.url,self.fromdate,self.todate, self.dss_status_callback) 
                        dss2 = dss2_final(self.uploaded_file,self.dss_status_callback)
                        try:
                            st.dataframe(dss2.style.applymap(self.color,subset=['W_SCI1_Color','W_SCI2_Color','W_SCI3_Color']))          
                        except: st.write(dss2)
                        # self.download_csv(dss2,self.dss_status_callback)
                        # self.download_geojson(dss2,self.dss_status_callback)
                        # self.viewmap_dss2(dss2,dss_status_callback = None)   
                
                elif self.dss_calc == "DSS3":
                    dss3 = dss3_final(self.uploaded_file,self.dss_status_callback)
                    try:
                        st.dataframe(dss3.style.applymap(self.color,subset=['Risk_Color']))          
                    except: st.write(dss3)
                    # self.download_csv(dss3,self.dss_status_callback)
                    # self.download_geojson(dss3,self.dss_status_callback)
                    # self.viewmap_dss3(dss3,dss_status_callback = None)
                    # st.button('Calculate DSS', on_click=self.dss_result)  
        if dss1 is not None:
            self.viewmap_dss1(dss1,self.dss_status_callback)
            self.download_csv(dss1,self.dss_status_callback)
            self.download_geojson(dss1,self.dss_status_callback)
            
        
        if dss2 is not None:
            self.viewmap_dss2(dss2,self.dss_status_callback)
            self.download_csv(dss2,self.dss_status_callback)
            self.download_geojson(dss2,self.dss_status_callback)

        if dss3 is not None:
            self.viewmap_dss3(dss2,self.dss_status_callback)
            self.download_csv(dss3,self.dss_status_callback)
            self.download_geojson(dss3,self.dss_status_callback)


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
    
    def viewmap_dss1(self, df,dss_status_callback = None):        
        # st.map(df)
        # try:
        #     if not df.empty:
        #         st.write('Select a date range to view map')
        #         fd  = st.date_input("From date", pd.to_datetime(min(df['Date'])))
        #         td = st.date_input("To date", pd.to_datetime(max(df['Date']))  ) 
        #         # selected_date = pd.to_datetime(selected_date)
        #         df["Date"] = pd.to_datetime(df["Date"]).dt.date  
        #         df_filter = df.loc[(df['Date'] >= fd) & (df['Date']<= td)]
        #         # st.write(selected_date)
        #         if not df_filter.empty:
        #             st.write(df_filter)
        #             m = leafmap.Map(center=[10.045180, 105.78841], zoom=8, tiles = 'Stamen Toner')
        #             m.add_points_from_xy(
        #                 df_filter,
        #                 x="longitude",
        #                 y="latitude",
        #                 # color_column='WQI_Color',
        #                 # icon_names=['gear', 'map', 'leaf', 'globe'],
        #                 spin=True,
        #                 # add_legend=True,
        #             )
        #             m.to_streamlit(height=700)
        # except: pass
        def get_color_name_dss1(rgb):
            if rgb == 'RGB(126,0,35)':
                color_name = 'darkred'
            elif rgb == 'RGB(255,0,0)':
                color_name = 'red'
            elif rgb == 'RGB(255,126,0)' :
                color_name = 'orange'
            elif rgb == 'RGB(255,255,0)' :
                color_name = 'beige'
            elif rgb == 'RGB(0,228,0)' :
                color_name = 'green'
            elif rgb == 'RGB(51,51,255)' :
                color_name = 'blue'
            else: color_name = 'black'
            return color_name        

        if not df.empty:
            tiles="https://maps.becagis.vn/tiles/basemap/light/{z}/{x}/{-y}.png",    
            m = folium.Map(tiles = "https://maps.becagis.vn/tiles/basemap/light/{z}/{x}/{-y}.png", attr="BecaGIS Maps", location = [10.045180, 105.78841], zoom_start =8)
            Fullscreen(                                                         
                position                = "topright",                                   
                title                   = "Open full-screen map",                       
                title_cancel            = "Close full-screen map",                      
                force_separate_button   = True,                                         
            ).add_to(m)             
            cluster = MarkerCluster()
            for lat, long, Matram, Date, WQI, WQI_Level, WQI_Color in zip(df.latitude, df.longitude, df.Matram, df.Date, df.WQI, df.WQI_Level, df.WQI_Color):
                color = get_color_name_dss1(WQI_Color)
                # color = 'purple'
                icon=folium.Icon(color=color, icon='ok-circle')
                popContent = ("ID: " + str(Matram) + '<br>' +\
                                            "Date : " + str(Date) + '<br>'+\
                                            "WQI " + str(WQI) + '<br>'+\
                                            "WQI_Level : " +  "<font color=" + color + ">" + str(WQI_Level) + "</font> ")
                                            #   "Risk Level: {}".format(Risk_Level))
                iframe = folium.IFrame(popContent)
                popup = folium.Popup(iframe,
                                    min_width=200,
                                    max_width=200)   
                folium.Marker(location=[lat, long], icon=icon, popup=popup).add_to(cluster)    
            m.add_child(cluster)            
            folium_static(m, width = 550)

    def viewmap_dss2(self, df,dss_status_callback = None):        
        # st.map(df)
        # try:
        #     if not df.empty:
        #         m = leafmap.Map(center=[10.045180, 105.78841], zoom=8, tiles = 'Stamen Toner')
        #         m.add_points_from_xy(
        #             df,
        #             x="longitude",
        #             y="latitude",
        #             spin=True,
        #         )
        #         m.to_streamlit(height=700)
        # except: pass
        def get_color_name_dss2(rgb):
            if rgb == 'RGB(255,0,0)':
                color_name = 'red'
            elif rgb == 'RGB(255,126,0)' :
                color_name = 'orange'
            elif rgb == 'RGB(255,255,0)' :
                color_name = 'beige'
            elif rgb == 'RGB(0,228,0)' :
                color_name = 'green'
            elif rgb == 'RGB(51,51,255)':
                color_name = 'blue'
            else: color_name = 'black'
            return color_name
        
           
        
        if not df.empty:
            tiles="https://maps.becagis.vn/tiles/basemap/light/{z}/{x}/{-y}.png",    
            m = folium.Map(tiles = "https://maps.becagis.vn/tiles/basemap/light/{z}/{x}/{-y}.png", attr="BecaGIS Maps", location = [10.045180, 105.78841], zoom_start =8)
            Fullscreen(                                                         
                position                = "topright",                                   
                title                   = "Open full-screen map",                       
                title_cancel            = "Close full-screen map",                      
                force_separate_button   = True,                                         
            ).add_to(m)             
            cluster = MarkerCluster()
            for lat, long, ID, W_SCI1, W_SCI2, W_SCI3, W_SCI3_Level, W_SCI3_Color in zip(df.latitude, df.longitude, df.ID, df.W_SCI1, df.W_SCI2, df.W_SCI3, df.W_SCI3_Level, df.W_SCI3_Color):
                color = get_color_name_dss2(W_SCI3_Color)
                # color = 'purple'
                icon=folium.Icon(color=color, icon='ok-circle')
                popContent = ("ID: " + str(ID) + '<br>' +\
                                              "W_SCI1 : " + str(round(W_SCI1,2)) + '<br>'+\
                                              "W_SCI2 " + str(round(W_SCI2,2)) + '<br>'+\
                                              "W_SCI3 : " + str(round(W_SCI3,2)) + '<br>'+\
                                              "W_SCI3_Level : " +  "<font color=" + color + ">" + str(W_SCI3_Level) + "</font> ")
                                            #   "Risk Level: {}".format(Risk_Level))
                iframe = folium.IFrame(popContent)
                popup = folium.Popup(iframe,
                                    min_width=150,
                                    max_width=150)   
                folium.Marker(location=[lat, long], icon=icon, popup=popup).add_to(cluster)    
            m.add_child(cluster)            
            folium_static(m, width = 550)


    def viewmap_dss3(self, df,dss_status_callback = None):        
        # st.map(df)
        # try:
        def get_color_name(rgb):
            if rgb == 'RGB(255,0,0)':
                color_name = 'red'
            elif rgb == 'RGB(255,126,0)' :
                color_name = 'orange'
            elif rgb == 'RGB(255,255,0)' :
                color_name = 'beige'
            elif rgb == 'RGB(0,228,0)' :
                color_name = 'green'
            else: color_name = 'purple'
            return color_name
    
        if not df.empty:
            # m = leafmap.Map(center=[10.045180, 105.78841], zoom=8, tiles = 'Stamen Toner')
            # m.add_points_from_xy(
            #     df,
            #     x="longitude",
            #     y="latitude",
            #     spin=True,
            # )
            # m.to_streamlit(height=700)
            tiles="https://maps.becagis.vn/tiles/basemap/light/{z}/{x}/{-y}.png",    
            # m = folium.Map(tiles="stamenterrain", location = [10.045180, 105.78841], zoom_start =8)
            m = folium.Map(tiles = "https://maps.becagis.vn/tiles/basemap/light/{z}/{x}/{-y}.png", attr="BecaGIS Maps", location = [10.045180, 105.78841], zoom_start =8)
            Fullscreen(                                                         
                position                = "topright",                                   
                title                   = "Open full-screen map",                       
                title_cancel            = "Close full-screen map",                      
                force_separate_button   = True,                                         
            ).add_to(m) 
            
            # locations = list(zip(df.latitude, df.longitude))
            # popups = list(zip(df.ID, df.Risk, df.Risk_Level, df.Risk_Color))
            # cluster = MarkerCluster(locations= locations, popups=popups)
            cluster = MarkerCluster()
            for lat, long, ID, Risk, Risk_Level, Risk_Color in zip(df.latitude, df.longitude, df.ID, df.Risk, df.Risk_Level, df.Risk_Color):
                color = get_color_name(Risk_Color)
                icon=folium.Icon(color=color, icon='ok-circle')
                # popup = 'ID: {}, Risk Value: {:2.0f}, Risk Level: {}'.format(ID, Risk, Risk_Level)
                popContent = ("ID: " + str(ID) + '<br>' +\
                                              "Risk Value : " + str(Risk) + '<br>'+\
                                              "Risk Level : " +  "<font color=" + color + ">" + str(Risk_Level) + "</font> ")
                                            #   "Risk Level: {}".format(Risk_Level))
                iframe = folium.IFrame(popContent)
                popup = folium.Popup(iframe,
                                    min_width=150,
                                    max_width=150)   
                folium.Marker(location=[lat, long], icon=icon, popup=popup).add_to(cluster)    
            m.add_child(cluster)            
            folium_static(m, width = 550)
        # except: pass       
  
     
    def download_csv(self, df,dss_status_callback = None):  
        if not df.empty:
            if 'Date' in df.columns:  
                df['Date'] =  df["Date"].astype(str)
            # csv = df.to_csv(index=False).encode('UTF-8') 
            csv = df.to_csv(encoding ='utf-8')        
            click = st.download_button(
            label= "Download CSV " + self.dss_calc,
            data = csv,
            file_name= self.dss_calc + ".csv",
            mime = "text/csv",
            key='download-csv')        

        
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
            st.download_button(
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