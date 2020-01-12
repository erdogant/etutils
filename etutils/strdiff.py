""" This strdiff computes differences in two strings

	from etutils.strdiff import strdiff

	A= strdiff(string1, string2, <optional>)

 INPUT:
   data:           datamatrix
                   rows    = features
                   colums  = samples
 OPTIONAL

 OUTPUT
	output

 DESCRIPTION
   Compute differences in strings

 EXAMPLE
   from etutils.strdiff import strdiff

   string1 = 'MeGaaaaaa-image'
   string2 = 'megaimage'

   string1 = 'IGADKYFHARGNYDAA AWOOH'
   string2 = 'KGADKYFHARGNYEAA  W'
   [out, outstring] = strdiff(string1, string2, methodtype='exact')
   print("%d differences\n\n%s" %(out, outstring))

   string1 = 'MeGaaaaaa-image'
   string2 = 'megaimage'
   [out, _] = strdiff(string1, string2)

   string1 = 'MeGa-image'
   string2 = 'megaimage hyphypehoera'
   [out, _] = strdiff(string1, string2)

   [out, _] = strdiff(string2, string1)

 SEE ALSO
   stringmagnet
"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : strdiff.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Nov. 2017
#--------------------------------------------------------------------------

#%% Libraries
import numpy as np
import difflib

#%%
def strdiff(string1, string2, methodtype='', no_match_c=' ', match_c='|'):
	#%% DECLARATIONS
    # Make dictionary to store Parameters
    outdiff=''
    Param = {}
    Param['methodtype'] = methodtype
    Param['no_match_c'] = no_match_c
    Param['match_c'] = match_c

    #%% Lower
    string1=string1.lower()
    string2=string2.lower()

    #%% Similar characters overall
    if Param['methodtype']=='':
        out=np.sum(np.in1d(list(string1), list(string2))==False)

    #%% Compute number of changes
    if Param['methodtype']=='ratio':
        out=difflib.SequenceMatcher(None, string1, string2).ratio()
    
    #%% Exact matching
    if Param['methodtype']=='exact':
        if len(string2) < len(string1):
            string1, string2 = string2, string1
        result = ''
        n_diff = 0
        
        #% char search
        for c1, c2 in zip(string1, string2):
            if c1 == c2:
                result += Param['match_c']
            else:
                result += Param['no_match_c']
                n_diff += 1
    
        delta = len(string2) - len(string1)
        result += delta * Param['no_match_c']
        n_diff += delta
        out=n_diff
    
        #% Make nice word-difference
        outdiff = string1+'\n'+result+'\n'+string2
    
    return(out,outdiff)
