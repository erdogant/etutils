""" This function extracts the content of a zipfile into a tmp directory

	A= zip.extract(path_of_file, <optional>)

 INPUT:
   path_of_file:  String, e.g., 
                  './my_directory/deeper/myfile.zip'

 OPTIONAL

   verbose:        Boolean [True,False]
                   False: No (default)
                   True: Yes

 OUTPUT
	output

 DESCRIPTION
   Extracts the content of a zipfile into a tmp directory

 EXAMPLE

   A = extract_files('./mydir/files.zip')

 SEE ALSO
   NAME OF FUNCTIONS THAT ARE CLOSELY ASSOCIATED WITH IT
"""

#--------------------------------------------------------------------------
# Name        : zip.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Aug. 2018
#--------------------------------------------------------------------------

import os
import zipfile
import RWSlearn.GENERAL.path as path
import tempfile

#%%
def zzip(filepath, storepath=None, verbose=3):
    if os.path.isdir(filepath):
        # calling function to get all file paths in the directory
        file_paths=path.dirwalk(filepath)
    elif os.path.isfile(filepath):
        # Store at location
        file_paths=[filepath]
    else:
        print('[ZIP] Filepath is not valid.')
        return None

    if storepath==None:
        pathsplit=path.split(filepath)
        storepath=path.correct(filepath, filename=pathsplit[1], ext='.zip')
    else:
        storepath=path.correct(filepath, filename='tmpfile', ext='.zip')
    
    # printing the list of all files to be zipped 
    print('Following files will be zipped:') 
    for file_name in file_paths: 
        if verbose>=3: print(file_name) 


    # writing files to a zipfile 
    with zipfile.ZipFile(storepath,'w') as zip: 
        # writing each file one by one 
        for file in file_paths: 
            zip.write(file) 
  
    print('All files zipped successfully!')      

#%% Make extraction
def extract(path_of_file, tmpdir='input', verbose=3):
    '''

    Parameters
    ----------
    path_of_file : String
        filepath of the zip file.
    tmpdir : String, optional
        path of the files to extract. 
        None: System temp directory.
        'input': In the same directory as the input.
        './path/to/extract/': Path of choice
    verbose : Int, optional
        Printing messages. The default is 3.

    Returns
    -------
    dictionary containing various information.

    '''
    # DECLARATIONS
    out = dict()
    config = dict()
    config['verbose'] = verbose

    # Setting up tempdirectory to unzip files
    if tmpdir is None:
        pathname=tempfile.gettempdir()
        pathname = os.path.join(pathname,'tmp')
    elif tmpdir=='input':
        [pathname, filenameRAW]=os.path.split(path_of_file)
        filename = filenameRAW[0:filenameRAW.find('.')]
        pathname = os.path.join(pathname,'tmp')
    else:
        pathname=tmpdir

    # Make tempdirectory
    if not os.path.isdir(pathname):
        os.mkdir(pathname)
        if verbose>=3: print('[EXTRACT FILES] Directory is created: %s' %pathname)
    else:
        if verbose>=3: print('[EXTRACT FILES] Directory already exists and will be used: %s' %pathname)
    
    # Extracting files
    if verbose>=3: print('[EXTRACT FILES] Extracting %s..' %(filenameRAW))
    zip_ref = zipfile.ZipFile(path_of_file, 'r')
    zip_ref.extractall(pathname)
    zip_ref.close()
        
    # Return info
    out['dir']=pathname
    out['file']=filenameRAW
    out['file_clean']=filename
    out['path']=path_of_file
    out['extracted_files']=path.dirwalk(pathname)
    
    if verbose>=3: print('[EXTRACT FILES] Done!')
    return(out)
