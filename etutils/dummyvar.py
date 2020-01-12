""" 
 Converts to catagorical and binairy values
 from etutils.dummyvar import dummyvar


 EXAMPLE
 
   import pandas as pd
   import numpy as np
   from etutils.dummyvar import dummyvar
 
   X  = pd.DataFrame(['aap','None','mies','aap','boom','mies',None,'mies','mies','pies',None])
   [df_list, df_onehot] = dummyvar(X)

   X  = pd.DataFrame([1,2,3,1,1,2,2,3,4,None,None])
   [df_list, df_onehot] = dummyvar(X)

   X  = pd.DataFrame([1,2,3,1,1,2,2,3,4])
   [df_list, df_onehot] = dummyvar(X)

   X  = np.array([1,2,3,1,1,2,2,3,4,None,None])
   [df_list, df_onehot] = dummyvar(X)

   X  = [1,2,3,1,1,2,2,3,4,None,None]
   [df_list, df_onehot] = dummyvar(X)
 
"""
 
#--------------------------------------------------------------------------
# Name        : dummyvar.py
# Author      : Erdogan Taskesen
# Version     : 0.1.0
# Copyright   : E.Taskesen
# Date        : Aug 2017
#--------------------------------------------------------------------------

#%% Libraries
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np
import pandas as pd

#%% Main
def dummyvar(data):
    '''

    Parameters
    ----------
    data : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    # DECLARATIONS
    out_cat  = []
    out_bin  = []
    out_labx = []
    getdtype=float
    
    # Check type
    if 'str' in str(type(data)):
        getdtype=str

    # If object
    if 'numpy' in str(type(data)) and data.dtype=='O':
        data = pd.DataFrame(data,dtype=getdtype)
    
    if 'numpy' in str(type(data)) or 'list' in str(type(data)):
        #data = pd.DataFrame(data,dtype=getdtype)
        data = pd.DataFrame(data)
    
    # Reset indexing
    data.index = np.arange(0,data.shape[0])
    
    # Replace None values with 'nan'
    I=data.isnull()==True
    if np.any(I):
        data.values[I.values]='NaN'
    
    # Unique with numpy
    out_labx=np.unique(data)
    
    # Convert to catagorical values
    labelencoder = LabelEncoder()
    out_cat      = labelencoder.fit_transform(data)
    out_cat      = out_cat.reshape(-1, 1) # This is required for the onehotencoder
    
    # Convert to binairy values
    onehotenc = OneHotEncoder() # Specify the index in X that requires onehotencoding = [0]
    out_bin   = onehotenc.fit_transform(out_cat).toarray()
    out_bin   = pd.DataFrame(data=out_bin,columns=out_labx)
    out_bin   = out_bin.astype(bool)
    
    # Re-arrange dataframe for NaN values
    I = out_bin.columns.isnull()
    if np.any(I):
        tmpNaN = out_bin.iloc[:,I].sum(axis=1)
        tmpNaN = tmpNaN.astype(bool)
    
        # Drop columns with NaN
        out_bin.drop(out_bin.columns[np.where(I)], inplace=True, axis=1)
        # Add combined column of NaN
        out_bin[None]=tmpNaN
    
    # Make dataframe and add label
    out_cat      = pd.DataFrame(data=out_cat,columns={'labx_num'})
    # Add original data column   
    out_cat = out_cat.assign(labx=data)

    # Combine NaN values
    I = out_cat.labx.isnull()
    if np.any(I):
        out_cat.labx_num.values[I]=min(out_cat.labx_num[I])
    
    return(out_cat, out_bin)
