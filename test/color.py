import pandas as pd
import numpy as np
import matplotlib as mpl
import streamlit as st

df = pd.DataFrame({"col1": ['1', '2', '3'], "col2": ['RGB(255,0,0)', 'RGB(0,255,0)', 'RGB(0,0,255)']})
# st.dataframe(df)
def color2(val):
    c1 = 'background-color: %s' % val
    c2 = ' & color: %s' % val
    return (c1+c2)

def color(row):
    if row['col2'] == 'RGB(255,0,0)':        
        return ['background-color:red'] * len(row)
    elif row['col2'] == 'RGB(0,255,0)':        
        return ['background-color:green']* len(row)
    elif row['col2'] == 'RGB(0,0,255)':        
        return ['background-color:blue']* len(row)
    
# st.dataframe(df.style.apply(color, axis=1))
st.dataframe(df.style.applymap(color2,subset=['col2']))
