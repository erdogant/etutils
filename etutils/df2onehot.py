""" This function transforms categorical values to one-hot

   from etutils.df2onehot import df2onehot

 EXAMPLE
    import pandas as pd
    nfeat=100
    nobservations=50
    df = pd.DataFrame(np.random.randint(0,2,(nfeat,nobservations)))
    A = df2onehot(df)


 -----------------------------------
  Name        : df2onehot.py
  Author      : E.Taskesen
  Contact     : erdogant@gmail.com
  Date        : April. 2019
 -----------------------------------
"""

#%% Libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
# Custom
from etutils.set_dtypes import set_dtypes
label_encoder = LabelEncoder()
onehot_encoder = OneHotEncoder(sparse=False, categories='auto')

#%% My function
def df2onehot(df, dtypes='pandas', hot_only=True, y_min=None, list_expand=True, perc_min_num=None, excl_background=None, verbose=3):
    '''
                   
    Parameters
    ----------
    df : pd.DataFrame
        rows    = features
        colums  = samples
    dtypes : list of strings. Format: ['cat','num'] with length y. By default the dtype is determiend based on the pandas dataframe.
        ['cat','cat','num',...]
    hot_only : Bool, The output of the onehot matrix exclusively contains categorical values that are transformed to one-hot. All other numerical values are removed
        False: (default)
        True
    y_min : Integer, [0..len(y)] Minimal number of sampels that must be present in a group. All groups with less then y_min samples are labeled as _other_ and are not used in the enriching model.
        DESCRIPTION. The default is None.
        None : (default)
    list_expand : Bool, Expanding of columns that contain lists of strings.
        False
        True (True)
    perc_min_num : Float, Force column (int or float) to be numerical if unique non-zero values are above percentage.
        None (default)
        0.8
    excl_background : list, Remove values/strings that labeled as background. As an example, in a two-class approach with [0,1], the 0 is usually the background and not of interest.
        None (default)
        [0]
        [0, '0.0', 'male', ...]
    verbose : Integer, [0..5] if verbose >= DEBUG: print('debug message')
        0: (default)
        1: ERROR
        2: WARN
        3: INFO
        4: DEBUG

    Returns
    -------
    None.

    '''
    config = dict()
    config['dtypes'] = dtypes
    config['verbose'] = verbose
    config['perc_min_num'] = perc_min_num
    config['list_expand'] = list_expand
    config['excl_background'] = excl_background
    labx=[]
    
    # Determine Dtypes
    [df, dtypes] = set_dtypes(df, config['dtypes'], is_list=config['list_expand'], perc_min_num=config['perc_min_num'], verbose=config['verbose'])
    # If any column is a list, also expand the list!
    [df, dtypes]=expand_column_with_list(df, dtypes, config['verbose'])
    
    # Make empty frames
    out_numeric=pd.DataFrame()
    out_onehot=pd.DataFrame()
    
    # Run over all columns
    for i in np.arange(0,df.shape[1]):
        if verbose>=3: print('[DF2ONEHOT] Working on %s' %(df.columns[i]), end='')
        
        # Do not touch a float
        if 'float' in str(df.dtypes[i]):
            if verbose>=3: print('')
            out_numeric[df.columns[i]] = df.iloc[:,i]
            if hot_only==False:
                out_onehot[df.columns[i]] = df.iloc[:,i]
                labx.append(df.columns[i])
        else:
            integer_encoded = label_encoder.fit_transform(df.iloc[:,i])
            # integer_encoded = set_y(integer_encoded, y_min=y_min, numeric=True, verbose=0)

            out_numeric[df.columns[i]] = integer_encoded
            out_numeric[df.columns[i]] = out_numeric[df.columns[i]].astype('category')
            if verbose>=3: print('.....[%.0f]' %(len(np.unique(integer_encoded))))

            # Contains a single value
            if len(np.unique(integer_encoded))<=1:
                out_onehot[df.columns[i]] = integer_encoded.astype('Bool')
                labx.append(df.columns[i])
            else:
                # binary encode
                onehot_encoded = onehot_encoder.fit_transform(integer_encoded.reshape(-1, 1))
                # Remove columns if it does not fullfill minimum nr. of samples (>=y_min)
                if not isinstance(y_min, type(None)):
                    onehot_encoded=onehot_encoded[:,onehot_encoded.sum(axis=0)>=y_min]
                # Make new one-hot columns
                for k in range(0,onehot_encoded.shape[1]):
                    # Get the colname based on the value in the orignal dataframe
                    label=df.iloc[onehot_encoded[:,k]==1,i].unique().astype(str)[0]
                    
                    # Check whether this is a label that should be excluded.
                    if (isinstance(config['excl_background'], type(None))) or (not np.isin(label, config['excl_background'])):
                        colname=df.columns[i]+'_'+label
                        out_onehot[colname] = onehot_encoded[:,k].astype('Bool')
                        labx.append(df.columns[i])

                # Make numerical vector
                if onehot_encoded.shape[1]>2:
                    out_numeric[df.columns[i]] =(onehot_encoded*np.arange(1,onehot_encoded.shape[1]+1)).sum(axis=1)
    
    out=dict()
    out['numeric'] = out_numeric
    out['onehot']  = out_onehot
    out['labx']    = np.array(labx, dtype=str)
    out['dtypes']  = np.array(dtypes)
    
    return(out)

#%%
def expand_column_with_list(df, dtypes, verbose=3):
    # Check for any lists in dtypes
    Icol=np.isin(dtypes,'list')
    
    # If any
    if np.any(Icol):
        # Empty df
        df_list_to_onehot=pd.DataFrame()
        idxCol=np.where(Icol)[0]

        # Expand columns with lists
        for i in range(0,len(idxCol)):
            if verbose>=3: print('[DF2ONEHOT] Column is detected as list and expanded: [%s]' %(df.columns[idxCol[i]]))
            uielements=np.unique(sum(df.iloc[:,idxCol[i]].to_list(),[]))
            
            A=df.iloc[:,idxCol[i]].apply(findcol, cols=uielements)
            arr = np.concatenate(A).reshape((A.shape[0],A[0].shape[0]))
            df1=pd.DataFrame(index=np.arange(0,df.shape[0]), columns=uielements, data=arr,  dtype='bool')
            
            # Combine in one big matrix
            df_list_to_onehot=pd.concat([df_list_to_onehot.astype(bool),df1], axis=1)
        # Drop columns that are expanded
        df.drop(labels=df.columns[Icol].values, axis=1, inplace=True)
        # Combine new one-hot-colums with 
        df=pd.concat([df,df_list_to_onehot], axis=1)
    
    # Redo the typing
    [df, dtypes] = set_dtypes(df, verbose=0)
    # Return
    return(df, dtypes)

#%%
def findcol(x, cols):
     return(np.isin(cols,x))
