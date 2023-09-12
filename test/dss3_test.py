import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from datetime import timedelta

from dss3 import dss3_final

dss3_file = os.path.join(os.path.dirname(__file__), '../data/dss3.csv')
# dss3_df = pd.read_csv(dss3_file)

# fromdate = dss1_df['Date'].min()
# todate =  dss1_df['Date'].max()
print (dss3_final(dss3_file, None))