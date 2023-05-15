import pandas as pd
import os
import sys
from dss import *
dss1_file = os.path.join(os.path.dirname(__file__), '../data/dss1.csv')
dss1_df = pd.read_csv(dss1_file,skiprows=[1])
fromdate = dss1_df['Date'].min
todate =  dss1_df['Date'].max
print(dss1(dss1_file,fromdate,todate))
