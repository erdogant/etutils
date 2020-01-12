""" This function computes the age and years-months-weeks-hours from date to NOW or a second array of dates.
	A= time_diff(data, <optional>)

 INPUT:
   dates:        Pandas array of strings containing dates with format such as dd/mm/yyyy

 OPTIONAL

   'dates2':       Pandas array of strings containing dates that are compared with the input-dates
                   ['now'] (default)
                   

   'dateformat':   String
                   "%m/%d/%Y" (default)
                   "%a %b %d %H:%M:%S %Y"
                   "" : infer

                   
   'method':       Float: Compute the difference for:
                   "age"    (default)
                   "years"  (difference in years)
                   "months" (difference in months)
                   "days"   (difference in weeks)
                   "hours"  (difference in hours)


 OUTPUT
	output

 DESCRIPTION
   This function computes the age and years-months-weeks-hours from date to now.

 EXAMPLE
   from etutils.time_diff import time_diff

   data=['1983-05-29 00:00:00.000','1978-01-06 00:00:00.000','1980-08-29','1980-07-29 00:00:00.000','hallo']
   dateformat="%Y-%m-%d %H:%M:%S.%f"
   A = time_diff(data, dateformat=dateformat, method="age")
   A = time_diff(data, method="age")
   
   data=['11/09/2017','15/3/2013','26/2/1980']
   A = time_diff(data, dateformat="%d/%m/%Y", method="age")
   A = time_diff(data, dateformat="%d/%m/%Y", method="days")
   W
   data=['11/09/2017','15/3/2013','26/2/1980']
   data2=['11/01/2017','12/02/2017','13/03/2017','14/04/2017','15/05/2017','16/06/2017','17/07/2017','18/08/2017','19/09/2017','20/10/2017','21/11/2017','22/12/2017']
   A1 = time_diff(data, data2=data2, dateformat="%d/%m/%Y", method="age")
   A2 = time_diff(data, data2=data2, method="age")

 SEE ALSO
   cat2radius
   
"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : time_diff.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Sep. 2017
#--------------------------------------------------------------------------

#%% Libraries
import pandas as pd
import numpy as np
import datetime as dt
from dateutil import relativedelta
from tqdm import tqdm

#%% Main
def time_diff(data, data2=['now'], method="age", dateformat="", verbose=1):
    # Make dictionary to store Parameters
    Param = {}
    Param['method']       = method
    Param['dateformat']   = dateformat
    Param['verbose'] = verbose
    out =[];

    # Make empty matrix
    out = pd.DataFrame(index=np.arange(len(data)), columns=np.arange(len(data2)))
    gettimenow=dt.datetime.now()

   # Find difference in time
    for i in tqdm(range(0,len(data)), disable=(True if param['verbose']==0 else False)):
        OK=1

        for j in range(0,len(data2)):
            #Try dataformat
            try:
                if Param['dateformat']=="":
                    # Infer automatically
                    getdate1 = pd.to_datetime(data[i])
                else:
                    getdate1 = dt.datetime.strptime(data[i], dateformat)
                #end
            except:
                # if error, store none
                OK=0
                print('error in date1')
    
                # Get now time
            try:
                if data2==['now']:
                    getdate2=gettimenow
                else:
                    if Param['dateformat']=="":
                        getdate2=pd.to_datetime(data2[j])
                    else:
                        getdate2=dt.datetime.strptime(data2[j], dateformat)
            except:
                # if error, store none
                OK=0
                print('error in date2')

            if OK==1:   
                # Compute difference between dates
                r = relativedelta.relativedelta(getdate2,getdate1)
                
                # Store whatever is asked
                if Param['method']=="age":
                    out.iloc[i,j] = r.years + (r.months/12)
                elif Param['method']=="years":
                    out.iloc[i,j] = r.years
                elif Param['method']=="months":
                    out.iloc[i,j] = r.months + (r.years*12)
                elif Param['method']=="days":
                    out.iloc[i,j] = r.days + (r.months*30) + (r.years*365)
                elif Param['method']=="hours":
                    out.iloc[i,j] = r.hours + r.days*24 + (r.months*30*24) + (r.years*365*24)
            else:
                out.iloc[i,j] = None

    return(out)
