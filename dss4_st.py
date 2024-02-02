import streamlit as st
import streamlit_ext as ste
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'data'))

from dss4 import dss4_final



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
    selected_plot, x_axis, y_axis = None, None, None

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
                submitted = st.form_submit_button("Run CSI Forecast")                    
                    
        if submitted:
            with col2:
                self.status_lable ="Calculation progress"
                status_bar = st.progress(0, text=self.status_lable)
                self.status_bar= status_bar
                df = pd.read_csv(self.url,encoding = "UTF-8") # depend on exisitng dss4.csv file
                df["Datetime"] =  pd.to_datetime(df["Datetime"],dayfirst=True)
                # df.set_index('Datetime', inplace=True)
                st.table(df[['S1']].describe())
                if self.url:                     
                   trainScore, testScore, Train, testPredict = dss4_final(self.url,self.dss_status_callback)        
                    
                elif self.uploaded_file:                 
                   trainScore, testScore, Train, testPredict = dss4_final(self.url,self.dss_status_callback)     
                st.write('Train Score: %.2f RMSE' % (trainScore))
                st.write('Test Score: %.2f RMSE' % (testScore))
                # Visualize the results
                st.write(Train)
                st.write(Train.describe())
                st.write(testPredict)
                st.write(testPredict.describe())
                st.line_chart(Train)
                st.line_chart(testPredict)
                # if testPredict is not None:
                #     self.download_csv(testPredict,self.dss_status_callback)            
    
    
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