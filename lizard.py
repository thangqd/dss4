# try:
#     from osgeo import gdal
# except ImportError:
#     import gdal
#     #from osgeo import ogr
import os
#os.getcwd()
import pandas as pd
# import geopandas as gpd
import requests
import streamlit as st
# import geemap


# csv = os.path.join(os.path.dirname(__file__), 'dss1.csv')
# 3lAj61vj.H5YQXu95lhkyN599SobVaapydeOiU21j
USERNAME = "__key__"
PASSWORD = "3lAj61vj.H5YQXu95lhkyN599SobVaapydeOiU21j"
HEADERS = {
    "username": USERNAME,
    "password": PASSWORD,
    "Content-Type": "application/json"
    }
mn_name= "DSS1-1.0.1"
url = "https://demo.lizard.net/api/v4/monitoringnetworks/?name__icontains=" + mn_name
r = requests.get(url, headers = HEADERS)
# print (r.json())

mn = r.json()["results"]

url2 = "https://demo.lizard.net/api/v4/monitoringnetworks/"+mn[0]['uuid']+"/timeseries/"
querydata = requests.get(url2,headers=HEADERS,params= {'page_size':'10000'}).json()['results']
timeseries_list = pd.DataFrame(querydata)
st.write(timeseries_list[0:4])

# print(timeseries_list[0:4])# print only the first 5 rows of the dataframe
# url3 = timeseries_list['url'][0]
# r = requests.get(url3, headers = HEADERS)
# print(r.json()["code"])
# print(r.json()["location"])

#url4 = timeseries_list['url'][0]+"events/"
# print(url)
#time_series_events = pd.DataFrame(requests.get(url=url4,headers=HEADERS,params= {'page_size':'10000'}).json()['results'])

# print(time_series_events[0:5])
#st.write(time_series_events[0:5])
# st.write(r.json())

# df= pd.read_csv(csv, skiprows=[1], on_bad_lines='skip')
# # print (df)
# gdf = gpd.GeoDataFrame(
#     df, geometry=gpd.points_from_xy(df.E, df.N)
# )
# print (gdf)
# gdf.to_file(os.path.join(os.path.dirname(__file__), 'dss1.geojson'), driver='GeoJSON')  

