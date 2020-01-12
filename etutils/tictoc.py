"""
MODULE tictoc
>
> tic()     : Time-start
> toc()     : Time spend from tic()
>

DESCRIPTION
   Measures time between tic and toc

EXAMPLE 1:
   from etutils.tictoc import tic, toc

   tic()
   toc()

EXAMPLE 2:
   import time as time
    for i in range(0,25):
        tic()
        time.sleep(0.1)
        print(toc())
        
--------------------------------------------------------------------------
 Name        : tictoc.py
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 Date        : Sep. 2017
--------------------------------------------------------------------------

"""

#%% Libraries
from time import time
tics = []

#%% start-time
def tic():
    tics.append(time())

#%% stop-time
def toc():
    if len(tics)==0:
        return None
    else:
        return time()-tics.pop()

#%% end
