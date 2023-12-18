import pandas as pd
from pandas.api.types import is_numeric_dtype
pd.options.mode.copy_on_write = True
from datetime import datetime


# Calculate DSS1
def dss4_final (input, status_callback):
    df = pd.read_csv(input,encoding = "UTF-8") # depend on exisitng dss4.csv file   
    # date_format = "%m/%d/%Y %I:%M:%S %p"
    # df['Date'] = datetime.strptime(df['Date'], date_format)
    return df