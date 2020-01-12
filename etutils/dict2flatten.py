'''
 Flattens dict
 from etutils.dict2flatten import dict2flatten


 Name        : colormap.py
 Version     : 0.1.0
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Dec. 2019

'''

import pandas as pd
def dict2flatten(d, sep='_'):
    df = pd.io.json.json_normalize(d, sep=sep)
    df = df.to_dict(orient='records')[0]
    return(df)