# import ellipsis as el
import folium as f 
import streamlit as st
import ellipsis as el
import os
import pandas as pd
import geopandas as gpd
import json
import requests
from streamlit_folium import st_folium, folium_static
from pandas.api.types import is_numeric_dtype


# folium_map = f.Map([9.3, 105.6], zoom_start=9)
# # html_map = folium_map._repr_html_()
# # st.markdown(html_map, unsafe_allow_html =True)
# st_folium(folium_map, width=725)

# #ellipsis
# # pathId = 'aa4b2e7f-4e13-4fa6-9a47-33a3a0067d36'
# # timestampId = 'ac8e7f63-e091-4efc-84ef-bc051919c414'
# # sh = el.path.vector.timestamp.listFeatures(pathId = pathId, timestampId = timestampId)['result']
# # features_geojson = sh.to_json()
# # vector_layer = f.GeoJson(features_geojson, name="geojson")

# vietnam = os.path.join(os.path.dirname(__file__), 'dss2.geojson')
# file = open(vietnam,errors="ignore")
# vietnam_gpd = gpd.read_file(file,encoding="utf8",errors="ignore")
# print(vietnam_gpd)

# url = (
#     "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
# )
# antarctic_ice_edge = f"{url}/antarctic_ice_edge.json"

# m = f.Map(
#     location=[9.3, 105.68],
#     tiles='cartodbdark_matter',#'stamentoner'], #'stamentoner','openstreetmap','cartodbpositron', 'cartodbdark_matter',"stamenterrain", tiles='Mapbox','stamenwatercolor'
#     # tiles="https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/%7Bz%7D/%7Bx%7D/%7By%7D?access_token=pk.eyJ1IjoidGhhbmdxZCIsImEiOiJucHFlNFVvIn0.j5yb-N8ZR3d4SJAYZz-TZA",
#     # API_key="pk.eyJ1IjoidGhhbmdxZCIsImEiOiJucHFlNFVvIn0.j5yb-N8ZR3d4SJAYZz-TZA",
#     zoom_start=8
#     )


# f.LayerControl().add_to(m)
# f.GeoJson(antarctic_ice_edge, name="geojson").add_to(m)

# df = pd.read_csv('dss3.csv', 
#                   usecols=['wlbWellboreName', 'wlbNsDecDeg', 'wlbEwDesDeg'])

# df.columns = ['Well Name', 'latitude', 'longitude']

df = pd.read_csv('dss1.csv',skiprows=[1])
                #   usecols=['Matram', 'E', 'N', 'Date','pH'])
# df.columns = ['matram','longitude', 'latitude', 'date', 'pH']
# print (df)
df["Date"] =  pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.date
fromdate = st.date_input("From date", df["Date"].min())
todate = st.date_input("To date",  df["Date"].max())  

def loadata(df, fromdate, todate):    
    df_date = df[(df['Date'] >= fromdate) & (df['Date'] < todate)]
    st.dataframe(df_date)
    st.write(df_date.dtypes)
    st.write(df_date.describe()) 
    st.map(df_date)
    # df = df.rename(columns={'date':'index'}).set_index('index')
    result = df_date.select_dtypes(include='number')
    # st.line_chart(df,x='Date', y=['pH','COD'])
    st.line_chart(result)
    return df_date

def dss1(df):    
   

if st.button('Load data'):
    df = loadata(df, fromdate, todate)
    # st.write(loadata(fromdate, todate))

if st.button('Calculate DSS1'):
    loadata(df, fromdate, todate)
    # st.write(loadata(fromdate, todate))


# df.columns = ['matram','longitude', 'latitude', 'date', 'pH']
# m =  f.Map(location=[df.latitude.mean(), df.longitude.mean()], 
#                  zoom_start=8, tiles='cartodbdark_matter')

# for i,row in df.iterrows():
#     #Setup the content of the popup
#     htmlstr = 'Mã trạm:' + str(row["matram"])
#     iframe = f.IFrame(htmlstr)
    
#     #Initialise the popup using the iframe
#     popup = f.Popup(iframe, min_width=200, max_width=200)
    
#     #Add each row to the map
#     f.Marker(location=[row['latitude'],row['longitude']],
#                   popup = popup, c=row['matram']).add_to(m)

# # f.GeoJson(vietnam, name="geojson").add_to(m)
# f.TileLayer('stamenwatercolor').add_to(m)
# f.LayerControl().add_to(m)

# st_folium(m, width=700)
# # folium_static(m, width=700)

# m.save("maps.html")

# import plotly.express as px

# fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name='pH', zoom=3)

# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# st.plotly_chart(fig)



