""" This function Extract year-month-day from array of dates
	A= time_extract(data, <optional>)


 INPUT:
   dates:        Pandas array of strings containing dates with format such as dd/mm/yyyy

 OPTIONAL

   'dateformat':   String
                   [] (Default) Try to infer
                   "%m/%d/%Y"
                   "%a %b %d %H:%M:%S %Y"

   'dates2':       Pandas array of strings containing dates that are compared with the input-dates
                   now (default)


 OUTPUT
	output

 DESCRIPTION
   Extract year-month-day from array of dates

 EXAMPLE
   from etutils.time_extract import time_extract

   data=['1983-05-29 00:00:00.000','1978-01-06 00:00:00.000','1980-07-29','1980-07-29 00:00:00.000','hallo']
   dateformat="%Y-%m-%d %H:%M:%S.%f"
   A = time_extract(data, dateformat=dateformat)
   A = time_extract(data)

   data=['1983-05-29 00:00:00.000','1978-01-06 00:00:00.000','1980-07-29','1980-07-29 00:00:00.000','hallo']
   data=pd.DataFrame(data, index=range(0,len(data)),columns=['date'])
   dateformat="%Y-%m-%d %H:%M:%S.%f"
   A = time_extract(data, dateformat=dateformat)
   A = time_extract(data)
   
   data=['11/09/2017','15/3/2013','26/2/1980']
   A = time_extract(data, dateformat="%d/%m/%Y")

 SEE ALSO
   cat2radius, timediff
   
"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : time_extract.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Oct. 2017
#--------------------------------------------------------------------------

#%% Libraries
import pandas as pd
import numpy as np

#%% Main
def time_extract(data, dateformat=None, verbose=3):
    # Make empty matrix
    out = pd.DataFrame(index=np.arange(len(data)), columns=['year','month','day','weekday','weekOfYear','weekday_name','hour','minute','second','date'])
    
    if 'pandas' in str(type(data)):
        if verbose>=3: print("First column is mapped from pandas to list..")
        data=data[data.columns[0]].tolist()
    
    # Convert to date-time object
    getdate=pd.to_datetime(data,errors='coerce', format=dateformat, infer_datetime_format=True)
    
    # Store
    out =[]
    out.year         = getdate.year.values
    out.month        = getdate.month.values
    out.weekday      = getdate.weekday.values
    out.weekOfYear   = getdate.weekofyear.values
    out.weekday_name = getdate.weekday_name.values
    out.day          = getdate.day.values
    out.hour         = getdate.hour.values
    out.minute       = getdate.minute.values
    out.second       = getdate.second.values
    out.date         = getdate
    
    return(out)
