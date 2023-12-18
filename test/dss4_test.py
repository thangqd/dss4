import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from datetime import timedelta

from dss4 import dss4_final

dss4_file = os.path.join(os.path.dirname(__file__), '../data/dss4.csv')
# dss3_df = pd.read_csv(dss3_file)

# fromdate = dss1_df['Date'].min()
# todate =  dss1_df['Date'].max()
print (dss4_final(dss4_file, None))