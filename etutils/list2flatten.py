'''
 Flattens list
 from etutils.list2flatten import list2flatten


 Name        : colormap.py
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Dec. 2019
'''

import numpy as np

def list2flatten(l):
    assert isinstance(l, list), 'Input must be of type list'
    return(np.array(list(np.concatenate(l))))

