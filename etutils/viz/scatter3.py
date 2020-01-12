""" This function creates a 3d scatterplot

    from etutils.viz.scatter3 import scatter3

	A= scatter3(x,y,z <optional>)

 INPUT:
   data:           numpy array
                   x
                   y
                   z
 OPTIONAL

   verbose:        Integer [0..5] if verbose >= DEBUG: print('debug message')
                   0: (default)
                   1: ERROR
                   2: WARN
                   3: INFO
                   4: DEBUG
                   

 OUTPUT
	output

 DESCRIPTION
   Plot 3d scatterplot

 EXAMPLE
   from etutils.viz.scatter3 import scatter3

   data='hallo'
   A = scatter3(data,verbose=1)

 SEE ALSO
   scatter
"""

#--------------------------------------------------------------------------
# Name        : scatter3.py
# Version     : 1.0
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : April. 2019
#--------------------------------------------------------------------------

#%% Libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#%% Main
def scatter3(x, y, z, dtypes=[None,None,None], xlabel='X-axis', ylabel='Y-axis', zlabel='Z-axis', colors='b', verbose=3):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x_num = checktype(x, dtypes[0])
    y_num = checktype(y, dtypes[1])
    z_num = checktype(z, dtypes[2])
    
    if not 'str' in str(type(colors)):
        colors = checktype(colors, dtypes=None)
    
    # Plot the values
    ax.scatter(x_num, y_num, z_num, c=colors, marker='.')
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    plt.show()

    return

#%% Check type
def checktype(data, dtypes=None):
    if isinstance(dtypes, type(None)):
        score = np.isnan(pd.to_numeric(data,errors='coerce')).sum()/len(data)
        if score>=0.1:
            dtypes='cat'
        else:
            dtypes='num'

    if dtypes=='num':
        if 'pandas' in str(type(data)):
            out = pd.to_numeric(data,errors='coerce').values
        if 'numpy' in str(type(data)):
            out = data.astype(float)
    
    if dtypes=='cat':
        data = data.astype(str)
        if 'numpy' in str(type(data)):
            _,out = etutils.ismember(data, np.unique(data))
        if 'pandas' in str(type(data)):
            data = data.astype('category')
            out = data.cat.codes.values
    
    return(out)