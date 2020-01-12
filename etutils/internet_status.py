''' 
 Make ascii art
 from etutils.asciiart import asciiart


 Name        : asciiart.py
 Version     : 0.1.0
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Jan. 2018

'''

import time
import http.client as httplib
from datetime import datetime, timezone

def internet_status(verbose=3):
    # Check whether server is still alive.
    counter=1
    status=False
    sleepinsec=60
    
    while status==False:
        conn = httplib.HTTPConnection("www.google.com", timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            status=True
        except:
            print('[INTERNET] [ERROR] [%s] No internet connection? Trying again in 60 sec.. [attempt %s]' %(now().strftime('%d-%m-%Y %H:%M'), counter))
            status=False
            time.sleep(sleepinsec)
            counter=counter+1

    if counter>1:
        if verbose>=3:('[INTERNET] [%s] Internet connection re-established after after %s attempts.' %(now().strftime('%d-%m-%Y %H:%M'), counter))
    return(status)


def now():
    return datetime.utcnow().replace(tzinfo=timezone.utc)
    