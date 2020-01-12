'''
 This function contains a set of functions related to file
>
> [nrows, headerline]   = filerows        : Returns number of rows in file
> [ncols, headerline]   = filecols        : Returns number of columns in file and header row
> [headlines, line_skip] = filehead        : Returns head of the file
> [lines, line_skip]     = fileread        : Returns file
> [types per column]     = filedtypes      : Returns whether row is [STRING] or [NUMERICAL]

-----------------------------------------------------------------------------
 INPUT:
   filename:       String: pathname of the file
                   'c:\temp\data.csv'
 OPTIONAL

   delim          : String: Delimiter
                   ',' (default)
-----------------------------------------------------------------------------

 EXAMPLE
   from etutils.filefun import filefun

   filename='startups2.csv'
   A = filefun.filerows(filename)
   print("Number of rows: [%d]" %(A))

   [B,_] = filefun.filecols(filename,delim=';')
   print("Number of cols: [%d]" %(B))


   [out,line_skip,outSplitWrong,line_skip] = filefun.fileread(filename,delim=';',header=1,delrows=1)
   [out,line_skip,outSplitWrong,line_skip] = filefun.filehead(filename,delim=';',header=1, lines=10)
   print("Number of cols: [%d]" %(B))

   #EXAMPLE READ FILE FROM-TO
   filename = 'marketing_data_online_retail_small.csv'
   [out,line_skip,outSplitWrong,line_skip] = filefun.fileread(filename, delim=';', header=0, startpos=100, lines=5)

   #EXAMPLE READ FILE FROM-TO
   filename = 'marketing_data_online_retail_small.csv'
   data=pd.read_csv(filename,sep=';')
   [ncols,headerline]=filefun.filecols(filename,delim=';')
   nrows=1000
   [out,line_skip,outSplitWrong,line_skip] = filefun.fileread(filename, delim=';', header=1, startpos=0, lines=5, nrows=nrows, ncols=ncols, headerline=headerline)


'''

#--------------------------------------------------------------------------
# Name        : strfun.py
# Version     : 0.1.2
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Sep. 2017
#--------------------------------------------------------------------------

#%% Libraries
from itertools import takewhile, repeat
import pandas as pd
import numpy as np
from tqdm import tqdm
import etutils.strfun as strfun
from etutils.slice_array import slice_array

#%% fix wrong column names
def quoteCorrect(inputstr, quote='"', delim=','):
    # Get line
    getline=inputstr
    line_sep=[]

    if getline!='':
        # replace double quotes by a single quote
        getline=getline.replace(quote+quote,quote)
        # Remove start-stop quote
        if getline[0]==quote and (getline[-2]==quote or getline[-1]==quote):
            getline=getline[1:-2]
        # get indexes of quotes, and slice in groups of 2
        getidx=slice_array(strfun.find(getline,quote),2)
        getlineOK=getline
        for k in range(0,len(getidx)):
            if len(getidx[k])==2:
                # Get part between quote
                linepart_o=getline[getidx[k][0]:getidx[k][1]+1]
                # Replace seperator with space between the quotes
                linepart_n=linepart_o.replace(quote,'').replace(delim,' ').replace('  ',' ')
                # Correct the line
                getlineOK=getlineOK.replace(linepart_o,linepart_n)

        # Replace any remaining quotes with space
        getline=getlineOK.replace(quote,'')
        # sepearte on delimiter
        line_sep = str.split(str(getline),delim)
    
    return(getline,line_sep)
    
#%% Number of rows in file
def filerows(filename):
	# DECLARATIONS
    out =[];

    # Open file
    fopen = open(filename, 'rb')
    # read large memory chucks
    bufgen = takewhile(lambda x: x, (fopen.raw.read(1024*1024) for _ in repeat(None)))
    # Sum
    out = sum( buf.count(b'\n') for buf in bufgen if buf )
    # return
    return(out)

#%% Number of rows in file
def filecols(filename, delim=',', quote='', encoding="utf-8"):
	# DECLARATIONS
   # [_,header]=filefun.filecols('example_dataset.csv')
   # OUT: header=np.array(header)
   # header[[2,4,6]]

    out            = [];
    headerline     = '';
    Param          = {}
    Param['delim'] = delim
    
    # Determine nr. Columns of file
    fopen = open(filename, "r+", encoding=encoding)
    line  = fopen.readline()
    
    # sepearte on delimiter
    headerline = line[0:len(line)-1]
    if quote!='':
        [a, headerline]=quoteCorrect(headerline, delim=Param['delim'], quote=quote)
    else:
        headerline = str.split(str(headerline),Param['delim'])
    
    out = len(headerline)
    
    # Close file
    fopen.close()
    
    return(out, headerline)

#%% Number of rows in file
def fileread(filename, delim=',', header=1, startpos=0, lines=0, delrows=0, showlineskip=0, nanfill=1, quote='', ncols=None, nrows=None, headerline=[], encoding="utf-8", verbose=3):
    # PARAMETERS
    out              = []
    line_skip        = []
    Param            = {}
    Param['delim']   = delim    # Delimiter
    Param['header']  = header   # Header 1=yes, 0=No
    Param['lines']   = lines    # Import X lines
    Param['delrows']      = delrows  # Keep only not-empty rows 
    Param['verbose'] = verbose # Progresbar
    Param['showlineskip'] = showlineskip # Print lines to screen that are skipped
    Param['nanfill']      = nanfill # 1=yes, 0=no, replace empty fields with nan
    Param['startpos']     = startpos # start position to read file
    Param['encoding']     = encoding # start position to read file
    Param['quote']     = quote # quote fix
    lineNr = 1
    
    # Get #columns if not specified
    if ncols==None:
        [ncols, _] = filecols(filename, delim=Param['delim'], encoding=Param['encoding'], quote=Param['quote'])
    
    if header==1:
        [_, headerline] = filecols(filename, delim=Param['delim'], encoding=Param['encoding'], quote=Param['quote'])
    elif headerline==[]:
        headerline = strfun.repmat("col",1,ncols).values.ravel()+np.char.mod('%d', np.arange(1,ncols+1))

    # Get rows of file
    if nrows==None:
        nrows=filerows(filename)
    
    # Import all rows
    if Param['lines']==0:
        Param['lines'] = nrows
    else:
        # lines to read can not be more then total number of lines in file
        Param['lines'] = min(Param['lines'],nrows)

    
    # Make empty pandas dataframe
    #index = list(range(0, Param['lines']))
    out   = pd.DataFrame(index=np.arange(Param['lines']), columns=headerline)
    outSplitWrong = pd.DataFrame(index=np.arange(0), columns={'WrongSplit'})
    
    #Skip lines
    if Param['startpos']>0:
        Param['header']=0
        Param['delrows']=0
        fopen = open(filename, "r", encoding=Param['encoding'])
        for i in range(Param['startpos']-1):
            fopen.readline()
            lineNr=lineNr+1 # Increase linenumber

        stoppos = out.shape[0]+Param['startpos']
        out.index = np.arange(Param['startpos'],stoppos)

    if Param['header']==1:
        fopen = open(filename, "r", encoding=Param['encoding'])
        fopen.readline()
        lineNr=lineNr+1 # Increase linenumber
    elif Param['startpos']==0:
        fopen = open(filename, "r", encoding=Param['encoding'])


    # Determine nr. Columns of file
    colsperline = np.zeros(Param['lines'])

    count=0
    for i in tqdm(range(0,out.shape[0]), disable=(True if param['verbose']==0 else False)):
        # Read line
        getline   = fopen.readline()
        getline_o = getline # Original line

        # Fix the quotes
        if Param['quote']!='':
            getline=getline.replace(Param['quote'],'')
#            getline=quoteCorrect(getline, delim=Param['delim'], quote=Param['quote'])
        
        # sepearte on delimiter
        line = str.split(str(getline),Param['delim'])
        # Count columns per row
        colsperline[i] = len(line)
        
        if len(line)!=out.shape[1]:
            # Append skipped line
            line_skip.append(lineNr)
            if Param['showlineskip']==1:
                if Param['verbose']>=3: print("[FILEREAD] Skipping in file the line [%d] > [%s]" %(lineNr,line))

            df = pd.DataFrame(data=getline_o, index=range(0,1), columns={'WrongSplit'})
            outSplitWrong = outSplitWrong.append(df,ignore_index=True)
        else:
            # Store in pandas dataframe
            out.values[i,:] = line
            count=count+1

        # Increase Line number
        lineNr=lineNr+1
    
    # set index correct for wrong split
    outSplitWrong.index=np.where(out.iloc[:,0].isnull())[0]
    
    # Close file
    fopen.close()
    
    # Fix the quotes
    if Param['quote']!='':
#        out2 = pd.DataFrame(index=np.arange(outSplitWrong.shape[0]), columns=headerline)
        count=0
        dropid=[]
        if Param['verbose']>=3: print('[FILEREAD]\nCorrecting for quotes ', end='')
        
        for i in tqdm(range(0, outSplitWrong.shape[0]), disable=(True if param['verbose']==0 else False)):
            # Get line
            getline=outSplitWrong.WrongSplit.iloc[i]
            if getline!='':
                # Correct line
                [_, linesep]=quoteCorrect(getline, delim=Param['delim'], quote=Param['quote'])
                if len(linesep)==out.shape[1]:
                    # Store value
#                    out.iloc[outSplitWrong.index[i],:]  = linesep
                    out.values[outSplitWrong.index[i],:] = linesep
                    # Remove from wrongsplit
#                    outSplitWrong.drop(outSplitWrong.index[i],axis=0)
                    dropid.append(outSplitWrong.index[i])
                    count=count+1


        if dropid!=[]:
            outSplitWrong=outSplitWrong.drop(dropid, axis=0)
            
        if Param['verbose']>=3: print('[FILEREAD] %d rows were rescued!' %(count))
    
    # Remove empty rows ([take] function is faster then [drop])
    if Param['delrows']==1:
        I   = out.iloc[:,0].isnull()==False
        out = out.take(out.index[I])
        #Reset index
        out.index=range(out.shape[0])
    
    if Param['nanfill']==1:
        if Param['verbose']>=3: print("[FILEREAD] Replacing empty fields to NaN..")
        out=strfun.strrep_to_nan(out,'')         # Replace empty fields with NaN
        out=strfun.strrep_to_nan(out,'NULL')     # Replace fields with NULl as NaN
        
    if Param['verbose']>=3: print("[FILEREAD] Lines imported: [%d]" %out.shape[0])
    
    return(out, colsperline, outSplitWrong, line_skip)

#%% Number of rows in file
def filehead(filename, delim=',',header=1, lines=10, verbose=3):
    # PARAMETERS
    out                   = []
    line_skip             = []
    Param                 = {}
    Param['delim']        = delim
    Param['header']       = header
    Param['lines']        = lines

    # Read data
    [out, _, line_skip]=filefun.fileread(filename, lines=Param['lines'], delim=Param['delim'],header=Param['header'], verbose=verbose)
    
    return(out, line_skip)

#%% Determine column data-types
def filedtypes(filename, delim=',', lines=10):
    # PARAMETERS
    out  = {}
    Param           = {}
    Param['delim']  = delim
    Param['lines']  = lines
    
    # Check whether String
    if 'str' in str(type(filename)):
        [data,_] = filefun.filehead(filename, delim=Param['delim'], lines=Param['lines'])
    
    #Param['lines'] = np.min([Param['lines'],data.shape[0]])
    
    
    for i in range(0,data.shape[1]):
        # Get data for column
        getdata = data.iloc[:,i]
        # Convert to numerical values
        getdata = pd.to_numeric(getdata,errors='coerce')
        
        # Get data-types
        if getdata.dtype=='float64':
            out[i] = "REAL"
        elif getdata.dtype=='int64':
            out[i] = "INTEGER"
        
        # If majority is NaN, then make STRING
        if sum(getdata.isnull()) >= (data.shape[0]/2):
            out[i] = "TEXT"

        # Convert to apporiate
        if out[i]=='REAL' or out[i]=='INTEGER':
            data[data.columns[i]] = getdata
    
    # Return
    return(data,out)

