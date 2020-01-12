"""
Imports file and stores data into a memmory mapped array 

FUNCTION mmap_readfile: 
	A = mmap_readfile(filename, delim=',', mmappath='')

 INPUT:
   filename:       String: pathname of the file
                   'c:\temp\data.csv'
#
 OPTIONAL

   mmappath        : String: Full pathname to store the memmory mapped file
                   '': default: ./[tmpdir]/mmapdata.dat)

   delim           : String: Delimiter
                   ',' (default)

   dtype          : String:
                   'float32' (default)
                   'uint32'

   header         : Boolean [0,1]: File contains header
                   [0]: No (default)
                   [1]: Yes


 OUTPUT
	output

 DESCRIPTION
   Imports file and stores data into a memmory mapped array 

 EXAMPLE
   from etutils.mmap_readfile import mmap_readfile

   delim=','
   mmappath=''
   dtype='float64'
   header=0

   filename='../DATA/OTHER/startups.csv'
   [dataMmap, runline, headerline]=eta.mmap_readfile(filename, delim=',', mmappath="", dtype="float32", header=1)

   filename='../DATA/OTHER/marketing_data_online_retail.csv'
   [dataMmap, runline, headerline]=eta.mmap_readfile(filename, delim=';', mmappath="", dtype="float32", header=1)

   # Load existing memmory mapped file
   data = np.memmap('C:\\Users\\Erdogan\\AppData\\Local\\Temp\\tmpuzj7i72l\\mmapdata.dat', dtype='float32', mode='r', shape=(541909,8) )

--------------------------------------------------------------------------
 Name        : mmap_readfile.m
 Author      : Erdogan Taskesen
 Version     : 1.0
 Author      : E.Taskesen
 Date        : Sep. 2017
--------------------------------------------------------------------------
"""

#%% Libraries
import numpy as np
import pandas as pd
import os.path as path
from os import mkdir
from tempfile import mkdtemp
# from etutils.tictoc import tic, toc
'''
 Flattens dict
 from etutils.dict2flatten import dict2flatten


 Name        : colormap.py
 Version     : 0.1.0
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Dec. 2019

'''

#%% Libraries
import etutils.filefun as filefun

#%% Main
def mmap_readfile(filename, delim=',', mmappath='', dtype='float32', header=0, verbose=3):
    #%% output
    out        = []
    fp         = []
    headerline = ''
    
	#%% Make dictionary to store Parameters
    Param = {}
    Param['verbose'] = verbose
    Param['delim']        = delim
    Param['filename']     = filename
    Param['mmappath']     = mmappath
    Param['dtype']        = dtype
    Param['header']       = header

    # Use tempdirectory if empty
    if Param['mmappath']=="":
        Param['mmappath'] = path.join(mkdtemp(), 'mmapdata.dat')

    #%% Check file
    if path.exists(Param['filename'])==False:
        print('Pathname does not exist <exit>.')
    
    # Make dir if not exists
    if path.exists(path.dirname(Param['mmappath']))==False:
        mkdir(path.dirname(Param['mmappath']))
    
    #%% Determine #columns
    [nrcol,_] = filefun.filecols(Param['filename'],delim=Param['delim'])
        
    #%% Determine #lines
    nrlines = filefun.filerows(Param['filename'])
    
    #%% Check header
    fopen=open(Param['filename'], "r+")
    if Param['header']==1:
        headerline = fopen.readline()
        headerline = headerline[0:len(headerline)-1]
        headerline = str.split(headerline,Param['delim'])
        nrlines=nrlines-1;
        # Leave file open
    else:
        headerline=''
    
    #%%Create a memmap with dtype and shape that matches data:
    fp = np.memmap(Param['mmappath'], dtype=Param['dtype'], mode='w+', shape=(nrlines,nrcol))

    #%% Read per line and fill memmory-mapped array
    for i in tqdm(range(0,fp.shape[0]), disable=(True if param['verbose']==0 else False)):
        # Extract line
        line = fopen.readline()
        # Remove '\n'
        #line = line[0:len(line)-1]
        
        # sepearte on delimiter
        line=str.split(str(line),Param['delim'])
        # print line
        #print(line)

        # Convert to numerical and set strings to NaN
        line = pd.to_numeric(line,errors='coerce')
        #line = pd.to_numeric(line,errors='ignore')
        
        # Store in memmap-file
        fp[i,:] = line
        
    #%% Close file
    fopen.close()
    # Remove fp from variables so it becomes 'unlocked' again 
    # del fp

    #%% Out
    out = ('data = np.memmap("%s", dtype="%s", mode="r", shape=(%d,%d) )' %(Param['mmappath'], Param['dtype'], nrlines, nrcol))
    
    #%% Return
    return(fp, out, headerline)

    #%% Load the memmap and verify data was stored:
#    newfp = np.memmap(Param['mmappath'], dtype=Param['dtype'], mode='r', shape=(nrlines,nrcol))
#    newfp
 
