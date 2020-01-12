"""
Imports text-file and stores data into a SQLlite3 database

	A = sql_readfile(filename, delim=",")

 INPUT:
   filename:       String: pathname of the file
                   'c:\temp\data.csv'

 OPTIONAL

   dbpath         : String: Full pathname to store the memmory mapped file
                   '' (temp directory, default)

   delim          : String: Delimiter
                   ',' (default)

   header         : Boolean [0,1]: File contains header
                   [0]: No
                   [1]: Yes (default)

   verbose       : Boolean [0,1]
                   [0]: No (default)
                   [1]: Yes (Only visible when multithread=1)

 OUTPUT
	output

 DESCRIPTION
   Imports text-file and stores data into a SQLlite3 database

 EXAMPLE
   from etutils.sql_readfile import sql_readfile

   filename='startups.csv'
   delim=","
   mmappath=""
   dtype="float32"
   header=0
   verbose=1

   [out, Param]=sql_readfile(filename, delim=",", header=1, verbose=3)

--------------------------------------------------------------------------
 Name        : sql_readfile.m
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Sep. 2017
--------------------------------------------------------------------------
"""

#%% Libraries
import pandas as pd
from tempfile import mkdtemp
from os import path
from os import chdir
from os import mkdir
from os import getcwd
import sqlite3
from tqdm import tqdm

# from etutils.tictoc import tic, toc
import etutils.filefun as filefun

#%% Main
def sql_readfile(filename, delim=",", header=1, dbpath="", verbose=3):
    #%% output
    out = []
    
	#%% Make dictionary to store Parameters
    Param = {}
    Param['verbose'] = verbose
    Param['delim']        = delim
    Param['filename']     = filename
    Param['header']       = header
    Param['dbpath']       = dbpath
    Param['curdir']       = getcwd()

    # Use tempdirectory if empty
    if Param['dbpath']=="":
        Param['dbname'] = 'DBdata.db'
        #Param['dbpath'] = path.join(mkdtemp(), Param['dbname'])
        Param['dbpath'] = mkdtemp()
    else:
        [Param['dbpath'], Param['dbname']] = path.split(Param['dbpath'])

    # Check file
    if path.exists(Param['filename'])==False:
        print('Pathname does not exist <exit>.')
    
    # Make dir if not exists
    if path.exists(path.dirname(Param['dbpath']))==False:
        mkdir(path.dirname(Param['dbpath']))

    #%% Determine #columns
    [nrcol, headerline] = filefun.filecols(Param['filename'], delim=Param['delim'])
    
    # Open file and read first line
    if Param['header']==0:
        headerline=''

    # Remove invalid chars
    headerline=strfun.strrep(headerline,' ','_')
    headerline=strfun.strrep(headerline,'&','')
    
    #%% Determine #lines
    nrlines = filefun.filerows(Param['filename'])
        
    #%% Determine datatype for the columns
    header_dtype = filefun.filedtypes(Param['filename'],lines=100,delim=Param['delim'])
    
    # Make dataframe
    df = pd.DataFrame()
    df['header'] = headerline
    df['dtype']  = header_dtype.values()

    # Concatenate rows
    sqltables=strfun.strcat_array(df,' ')
    #Concatenate to one line
    sqltables=strfun.strcat(sqltables,', ')

    #%% Change working directory
    chdir(Param['dbpath'])

    #%% CREATE DB with tables
    # SQL query
    sqlquery = "CREATE TABLE IF NOT EXISTS %s (%s)" %(Param['dbname'],sqltables)
    # 1 - Connect to database
    conn = sqlite3.connect(Param['dbname'])
    # 2 - Set connection
    cur = conn.cursor()
    # 3 Create table with SQL query
    # cur.execute("CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)")
    cur.execute(sqlquery)
    # 4 - Commit
    conn.commit()
    # Close db
    conn.close()

    #%% Read per line and fill the SQLite db
    # 1 Connect
    conn = sqlite3.connect(Param['dbname'])
    # 2 - Set cursor
    cur = conn.cursor()

    # Open file and read first line
    if Param['header']==1:
        fopen = open(Param['filename'], "r+")
        fopen.readline()


    for i in tqdm(range(0,nrlines)):
        # Extract line
        line = fopen.readline()

        # sepearte on delimiter
        line=str.split(str(line),Param['delim'])
        # print line
        #print(line)

        for k in range(0,len(line)):
            if header_dtype[k]=='REAL':
                line[k]=float(line[k])
                
        # Make Query
        makeQ = strfun.repmat('?',len(line),1)
        makeQ = strfun.strcat(makeQ.values.tolist()[0],',')
        sqlquery = "INSERT INTO %s VALUES(%s)" %(Param['dbname'],makeQ)
        
        # Execute query
        cur.execute(sqlquery,(line))
        # cur.execute("INSERT INTO DBdata VALUES(?,?,?,?,?)",(line))

    # Close connections
    conn.commit()
    conn.close()
    fopen.close()
    
    #%% Show records in DB
    # Connect to DB
    conn = sqlite3.connect(Param['dbname'])
    # 2 - Set cursor
    cur = conn.cursor()
    # Make query
    sqlquery = "SELECT * FROM %s" %(Param['dbname'])
    # Execute
    cur.execute(sqlquery)
    # Fetch
    rows = cur.fetchall()
    print(rows)
    # Close
    conn.commit()
    conn.close()

    #%% Restore original working dir
    chdir(Param['curdir'])

    #%% Return
    return(out, Param)
