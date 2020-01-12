''' 
 Make ascii art
 from etutils.asciiart import asciiart


 Name        : asciiart.py
 Version     : 0.1.0
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Jan. 2018

'''

#%% Libraries
import time
import numpy as np

#%% main
def asciiart(message, sleeptime=0.2, newline=True):
    '''

    Parameters
    ----------
    message : String
        String to convert to ascii-art.
        'thea'
        'coffee'
        'hello this is a test message'
    sleeptime : float, optional
        Time in seconds. 
        0.2. (default)
    newline : Bool, optional
        Make new line after showing the estimated time.
        True (default)
        False

    Returns
    -------
    None.

    '''
    # Make dictionary to store Parameters
    Param = {}
    Param['message']   = message
    Param['sleeptime'] = sleeptime
    Param['newline'  ] = newline

    #
    getkeys=np.array(list(ascii_txt.keys()))
    if np.any(getkeys==message):
        ascii_fin=ascii_txt[message]
    else:
        getascii=[]
        for i in range(0,len(message)):
            getchar=np.str.upper(message[i])
            # If char exists, add to array
            if np.any(getkeys==getchar):
                getascii.append(ascii_txt[getchar])
            else:
                getascii.append(ascii_txt['nan'])

        ascii_fin=[]
        getascii=np.array(getascii)
        for i in range(0,getascii.shape[1]):
            tmpnew=''
            for k in range(0,getascii.shape[0]):
                tmpnew=tmpnew+ getascii[k][i]

            ascii_fin.append(tmpnew)

    for i in range(0,len(ascii_fin)):
        print('%s' %ascii_fin[i])
        time.sleep(Param['sleeptime'])

    # End with new-line
    if Param['newline']:
        print("\n")
    
#%% acii chars
ascii_txt={}

ascii_txt['tea']=[
r'             ;,  ',
r'     _o_    ;:;  ',
r' ,-.---`.__ ;    ',
r'((j`=====,-      ',
r' `-\     /       ',
r'    `-=-         ',
r'                 ',
r'  Tea time!      ']
    

ascii_txt['coffee']=[
r'       ( (    ',
r'    ) )       ',
r'  ........    ',
r'  |      |]   ',
r'  \      /    ',
r'   `----      ',
r'              ',
r' Coffee time! ']

#%

ascii_txt['A']=[
r'_______  ',
r'___    | ',
r'__  /| | ',
r'_  ___ | ',
r'/_/  |_| ']

ascii_txt['B']=[
r'________ ',
r'___  __ ) ',
r'__  __  | ',
r'_  /_/ /  ',
r'/_____/   ']

ascii_txt['C']=[
r'_________ ',
r'__  ____/ ',
r'_  /      ',
r'/ /___    ',
r'\____/    ']

ascii_txt['D']=[
r'________  ',
r'___  __ \ ',
r'__  / / / ',
r'_  /_/ /  ',
r'/_____/   ']
          
ascii_txt['E']=[
r'__________ ',
r'___  ____/ ',
r'__  __/    ',
r'_  /___    ',
r'/_____/    ']

ascii_txt['F']=[
r'__________ ',
r'___  ____/ ',
r'__  /_     ',
r'_  __/     ',
r'/_/        ']
          
ascii_txt['G']=[
r'_________ ',
r'__  ____/ ',
r'_  / __   ',
r'/ /_/ /   ',
r'\____/    ']
         
ascii_txt['H']=[
r'______  __ ',
r'___  / / / ',
r'__  /_/ /  ',
r'_  __  /   ',
r'/_/ /_/    ']
          
ascii_txt['I']=[
r'________ ',
r'____  _/ ',
r' __  /   ',
r'__/ /    ',
r'/___/    ']
        
ascii_txt['J']=[
r'_________ ',
r'______  / ',
r'___ _  /  ',
r'/ /_/ /   ',
r'\____/    ']
         
ascii_txt['K']=[
r'______ __ ',
r'___  //_/ ',
r'__  ,<    ',
r'_  /| |   ',
r'/_/ |_|   ']
         
ascii_txt['L']=[
r'______  ',
r'___  /  ',
r'__  /   ',
r'_  /___ ',
r'/_____/ ']
       
ascii_txt['M']=[
r'______  ___ ',
r'___   |/  / ',
r'__  /|_/ /  ',
r'_  /  / /   ',
r'/_/  /_/    ']
           
ascii_txt['N']=[
r'_____   __ ',
r'___  | / / ',
r'__   |/ /  ',
r'_  /|  /   ',
r'/_/ |_/    ']
          
ascii_txt['O']=[
r'_______   ',
r'__  __ \  ',
r'_  / / /  ',
r'/ /_/ /   ',
r'\____/    ']
        
ascii_txt['P']=[
r'________  ',
r'___  __ \ ',
r'__  /_/ / ',
r'_  ____/  ',
r'/_/       ']
         
ascii_txt['Q']=[
r'_______  ',
r'__  __ \ ',
r'_  / / / ',
r'/ /_/ /  ',
r'\___\_\  ']
        
ascii_txt['R']=[
r'________  ',
r'___  __ \ ',
r'__  /_/ / ',
r'_  _, _/  ',
r'/_/ |_|   ']
         
ascii_txt['S']=[
r'________ ',
r'__  ___/ ',
r'_____ \  ',
r'____/ /  ',
r'/____/   ']
        
ascii_txt['T']=[
r'________ ',
r'___  __/ ',
r'__  /    ',
r'_  /     ',
r'/_/      ']
        
ascii_txt['U']=[
r'_____  __ ',
r'__  / / / ',
r'_  / / /  ',
r'/ /_/ /   ',
r'\____/    ']
         
ascii_txt['V']=[
r'___    __ ',
r'__ |  / / ',
r'__ | / /  ',
r'__ |/ /   ',
r'_____/    ']
         
ascii_txt['W']=[
r'___       __ ',
r'__ |     / / ',
r'__ | /| / /  ',
r'__ |/ |/ /   ',
r'____/|__/    ']
            
ascii_txt['X']=[
r'____  __ ',
r'__  |/ / ',
r'__    /  ',
r'_    |   ',
r'/_/|_|   ']
        
ascii_txt['Y']=[
r'__  __ ',
r'_ \/ / ',
r'__  /  ',
r'_  /   ',
r'/_/    ']
      
ascii_txt['Z']=[
r'______ ',
r'___  / ',
r'__  /  ',
r'_  /__ ',
r'/____/ ']

ascii_txt['nan']=[
r'     ',
r'     ',
r'     ',
r'     ',
r'     ']

#%% Main
# if __name__=='__main__':
#     asciiart('etutils',sleeptime=0.3)
#     asciiart("coffee",sleeptime=0.2)
#     asciiart('tea',sleeptime=0.3)
#     asciiart('Hello world',sleeptime=0.3)
