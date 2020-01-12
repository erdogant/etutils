'''
 Create an N-bin discrete colormap from the specified input map
 from etutils.colormap import colormap


 Name        : colormap.py
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Jan. 2018

'''

#%% Libraries
import matplotlib.pyplot as plt
import numpy as np

#%% Main
def colormap(N, cmap='Set1', method='matplotlib'):
    '''

    Parameters
    ----------
    N : Integer
        Number of colors to be generated.
    cmap : String, optional
        Colormap > https://matplotlib.org/examples/color/colormaps_reference.html
        'Set1'       (default)     
        'Set2'       
        'rainbow'
        'bwr'        Blue-white-red
        'binary' or 'binary_r'
        'seismic'    Blue-white-red 
        'Blues'      white-to-blue
        'Reds'       white-to-red
        'Pastel1'    Discrete colors
        'Paired'     Discrete colors
        'Set1'       Discrete colors

    Returns
    -------
    color_list : TYPE
        Colors.

    '''
    if method=='seaborn':
        import seaborn as sns
        color_list=sns.color_palette(cmap,N).as_hex()
    else:
        base = plt.cm.get_cmap(cmap)
        color_list = base(np.linspace(0, 1, N))[:,0:3]
    return color_list