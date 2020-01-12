'''
 Flattens dict
 from etutils.dict2flatten import dict2flatten


 Name        : colormap.py
 Version     : 0.1.0
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Dec. 2019

'''

#%% Libraries
import pandas as pd
from datetime import timedelta
import numpy as np

#%% Main
def panel2dataframe(data):
    if isinstance(data, pd.DataFrame):
        return data
    else:
        df=data.to_xarray()
        gettime=pd.to_datetime(df.major_axis.values, utc=True)+timedelta(hours=23,minutes=59, seconds=59)
        df=pd.DataFrame(index=gettime, data=df.values[0], columns=df.minor_axis.values)

        df['close'] = df['close'].astype(float)
        df['low'] = df['low'].astype(float)
        df['high'] = df['high'].astype(float)
        df['open'] = df['open'].astype(float)
        df['volume'] = df['volume'].astype(float)
        return(df)
