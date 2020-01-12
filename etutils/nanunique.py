""" This function gives a unique list back which can handles None/nan values.

	A= nanunique(data, <optional>)

 INPUT:
   data:           numpy-array or list
                   
 OPTIONAL


 OUTPUT
	unique-values and index

 DESCRIPTION
   This function gives a unique list back which can handles None/nan values. It uses and also outputs the index

 EXAMPLE
   import numpy as np
   from etutils.nanunique import nanunique

   data=[None,'aap','aap','boom',None,'boom','mies','mies',None]
   data=['aap','aap','boom','boom','mies','mies']
   data=np.array([1,1,2,2,3,3,3,None,4,4,4,4,5,5,5,5,5,None],dtype=np.float)
   data=[5,3,1,3,2,3,3,3,4,4,3,4,4,5,None,4,5,5,1,5,5]
   [A,idx] = nanunique(data, sort=0)

   [np.array(data)[idx], A]

 SEE ALSO

"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : unique.py
# Version     : 0.1.0
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Oct. 2017
#--------------------------------------------------------------------------

#%% Libraries
import numpy as np

#%%
def nanunique(data, sort=1):
	# DECLARATIONS
    out =[]
    index=[]
    # Make dictionary to store Parameters
    Param = {}
    Param['sort'] = sort
    
    # Replace None values with 'nan'
    gettype=''
    if 'list' in str(type(data)):
        try:
            # Make type float
            data = np.array(data,dtype=np.float)
            gettype='float'
        except:
            #For string
            data=['None' if i is None else i for i in data]
            gettype='string'

    elif 'numpy' in str(type(data)):
        gettype='float'

    # Make unique
    [out, index] = np.unique(data, return_index=True)

    # Unique without sort
    if Param['sort']==0:
        out=out[index.argsort()]
        index=index[index.argsort()]

    # Get only not NaN values
    if gettype=='float':
        if np.any(np.isnan(out)):
            I=~np.isnan(out)
            out=out[I]
            out=np.append(out,np.nan)
            
            # Get index
            index=index[I]
            I=np.isnan(data)
            index=np.append(index,np.where(I==True)[0][0])

    if gettype=='string':
        out = out.tolist()

    return(out,index)
