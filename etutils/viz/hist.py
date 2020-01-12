""" This function provides...

    from etutils.viz.hist import hist

	A=hist(data, <optional>)

 INPUT:
   data:           datamatrix
                   rows    = features
                   colums  = samples
 OPTIONAL

   bins:           Integer:  Number of bins
                   [50]: (default)

   xlabel:         String: strings for the xlabel
                   'Xlabel'

   ylabel:         String: strings for the ylabel
                   'Ylabel'

   title:         String: strings for the title
                   ''

   height:         Integer:  Height of figure
                   [10]: (default)

   width:          Integer:  Width of figure
                   [10]: (default)

   grid:           Boolean [0,1]: Grid in figure
                   'True' (default)
                   'False'

   facecolor:      String: strings for the facecolor
                   'k' (default)

   savepath:       String: pathname of the file
                   'c:/temp/heatmap.png'

   dpi:            Integer: Resolution of the figure
                   [100] (default)

   verbose    Boolean [0,1]
                   [0]: No (default)
                   [1]: Yes

 OUTPUT
	[fig, plt, ax]


 DESCRIPTION
   Makes histogram in matplotlib
   https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.hist.html
   https://matplotlib.org/api/matplotlib_configuration_api.html

 EXAMPLE
   from etutils.viz.hist import hist

   import numpy as np
   savepath = "c:/fig.png"
   data=np.random.normal(0, 0.5, 1000)
   [plt,fig, ax] = hist(data,savepath=savepath)

 SEE ALSO
   hist_bokeh, scatter, imagesc, donutchart
"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : hist.py
# Version     : 0.1.0
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Sep. 2017
#--------------------------------------------------------------------------

#%% Libraries
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

#%%
def hist(data, bins=50, xlabel="x-axis", ylabel="Frequency", title="", width=10, height=10, savepath="", facecolor='k', grid=True, dpi=100, normed=False, verbose=0):
	#%% DECLARATIONS
    fig =[];
    # Make dictionary to store Parameters
    Param = {}
    Param['verbose'] = verbose
    Param['bins']         = bins
    # Labels
    Param['title']        = title
    Param['xlabel']       = xlabel
    Param['ylabel']       = ylabel
    Param['width']        = width
    Param['height']       = height
    Param['facecolor']    = facecolor
    Param['grid']         = grid
    Param['dpi']          = dpi
    Param['normed']       = normed
    Param['savepath']     = savepath

    
    #%% Make Figure
    SMALL_SIZE  = 14
    MEDIUM_SIZE = 14
    BIGGER_SIZE = 14
    
    plt.rc('font',  size       = SMALL_SIZE)   # controls default text sizes
    plt.rc('axes',  titlesize  = SMALL_SIZE)   # fontsize of the axes title
    plt.rc('xtick', labelsize  = SMALL_SIZE)   # fontsize of the tick labels
    plt.rc('ytick', labelsize  = SMALL_SIZE)   # fontsize of the tick labels
    plt.rc('legend', fontsize  = SMALL_SIZE)   # legend fontsize
    plt.rc('axes',  labelsize  = MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('figure', titlesize = BIGGER_SIZE)  # fontsize of the figure title

#    title_font = {'fontname':'Calibri Light', 'size':'16', 'color':'black', 'weight':'normal', 'verticalalignment':'bottom'} # Bottom vertical alignment for more space
    axis_font = {'fontname':'Arial'}
    # axis_font = {'fontname':'Calibri Light', 'size':'14'}

    #%% Make figure with properties
    [fig,ax]=plt.subplots()

    # specify dimensions
    fig.set_size_inches(Param['width'], Param['height'])

    #%% Histogram plot
    [n, bins, patches] = plt.hist(data, Param['bins'], normed=Param['normed'], facecolor=Param['facecolor'], alpha=0.5)
    
    #%% Fig settings
    plt.xlabel(Param['xlabel'], **axis_font)
    plt.ylabel(Param['ylabel'], **axis_font)
    plt.title(Param['title'])
#    plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#    plt.axis([40, 160, 0, 0.03])
    plt.grid(Param['grid'])
    plt.show()

    #%% Set the tick labels font
#    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
#        label.set_fontname('Arial')
        #label.set_fontsize(14)
    #end

    #%% Write figure to path
    etutils.viz.savefig(fig, Param['savepath'], dpi=Param['dpi'])

    #%% END
    return(fig, ax)
