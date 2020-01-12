""" This function saves figures in PNG format.

    from etutils.viz.savefig import savefig

	A=savefig(data, <optional>)

 INPUT:
   data:           fig object

 OPTIONAL


 OUTPUT
	BOOLEAN
    [0]: If not succesful 
    [1]: If succesful 

 DESCRIPTION
   This function saves figures in PNG format.

 EXAMPLE
   from etutils.viz.donutchart import donutchart
   from etutils.viz.savefig import savefig

   A = donutchart([15, 30, 45, 10],['aap','boom','mies','banaan'])
   B = savefig(A,"c://temp//magweg//fig.png")

 SEE ALSO
   
"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : savefig.py
# Version     : 0.1.0
# Author      : E.Taskesen
# Date        : Sep. 2017
#--------------------------------------------------------------------------
# Libraries
from os import mkdir
from os import path

#%%
def savefig(fig, filepath, dpi=100, transp=False):
    out=False # Returns True if succesful
    Param = {}
    Param['filepath']     = filepath
    Param['dpi']          = dpi
    Param['transp']       = transp

    # Write figure to path
    if Param['filepath']!="":
        # Check dir
        [getpath, getfilename] = path.split(Param['filepath'])
        if path.exists(getpath)==False:
            mkdir(getpath)

        #save file
        #print(fig.canvas.get_supported_filetypes())
        fig.savefig(Param['filepath'], dpi=Param['dpi'], transparent=Param['transp'], bbox_inches='tight')
        out=True
        
    return(out)
