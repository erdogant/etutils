""" This function Makes histogram in bokeh
   
    from etutils.viz.hist_bokeh import hist_bokeh

	A= hist_bokeh(data, <optional>)

 INPUT:
   data:           datamatrix
                   rows    = features
                   colums  = samples
 OPTIONAL

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

   filepath:       String: pathname of the file
                   'c:/temp/heatmap.png'

   dpi:            Integer: Resolution of the figure
                   [100] (default)


 OUTPUT
	[fig, plt, ax]

 DESCRIPTION
   Makes histogram in bokeh
   http://bokeh.pydata.org/en/latest/docs/gallery/histogram.html

 EXAMPLE
   import numpy as np
   from etutils.viz.hist_bokeh import hist_bokeh

   data=np.random.normal(0, 0.5, 1000)
   A = hist_bokeh(data,bins=50, title="Hello histogram",density=True, xlabel="x-axis", ylabel="y-axis", width=400, height=400)

 SEE ALSO
   hist, scatter, imagesc, donutchart

print(__doc__)
"""

#--------------------------------------------------------------------------
# Name        : hist_bokeh.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Sep. 2017
#--------------------------------------------------------------------------

#%% Libraries
import numpy as np

#%% Load libraries
def loadlibs():
    # To avoid loading/installing many heavy packages, load when required.
    from bokeh.layouts import gridplot
    from bokeh.plotting import figure, show, output_file
    from bokeh.io import curdoc
    curdoc().clear()
    
#%% Main
def hist_bokeh(data, bins=50, title="", xlabel="x-axis", ylabel="Frequency", density=True, width=400, height=400, filename="histogram.html", filepath=""):
	#%% DECLARATIONS
    
    loadlibs()
    out =[];
    
    # Make dictionary to store Parameters
    Param = {}
    Param['density']      = density
    Param['bins']         = bins
    Param['filename']     = filename
    Param['filepath']     = filepath
    # Labels
    Param['title']        = title
    Param['xlabel']       = xlabel
    Param['ylabel']       = ylabel
    Param['width']        = width
    Param['height']       = height
    # Colors
    Param['fill_color_background']   = "#FFFFFF"
    Param['fill_color_legend']       = "darkgrey"


    #%% Get histogram from data
    [hist, edges] = np.histogram(data, density=Param['density'], bins=Param['bins'])

    #%% Use maximum likelihood to determine distribution with best fit
#        import scipy
#    import scipy.stats

#    dist_names = ['gamma', 'beta', 'rayleigh', 'norm', 'pareto']
#    for i in dist_names:
#        dist = getattr(scipy.stats, i)
#        param = dist.fit(data)
    # here's the parameters of your distribution, scale, location
    
    #    x = np.linspace(-2, 2, 1000)
#    pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
#    cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2

#%%
#    import matplotlib.pyplot as plt
#    import scipy
#    import scipy.stats
#    size = 30000
#    x = scipy.arange(size)
#    y = scipy.int_(scipy.round_(scipy.stats.vonmises.rvs(5,size=size)*47))
#    h = plt.hist(y, bins=range(48), color='w')
#    
#    dist_names = ['gamma', 'beta', 'rayleigh', 'norm', 'pareto']
#    
#    for dist_name in dist_names:
#        dist = getattr(scipy.stats, dist_name)
#        param = dist.fit(y)
#        pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1]) * size
#        plt.plot(pdf_fitted, label=dist_name)
#        plt.xlim(0,47)
#    plt.legend(loc='upper right')
#    plt.show()

    #%% Set figure properties
    p1 = figure(title=Param['title'],tools="save", background_fill_color=Param['fill_color_background'])
    p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],fill_color="#036564", line_color="#033649")
#    p1.line(x, pdf, line_color="#D95B43", line_width=8, alpha=0.7, legend="PDF")
#    p1.line(x, cdf, line_color="white", line_width=2, alpha=0.7, legend="CDF")
 
    p1.legend.location = "center_right"
    p1.legend.background_fill_color = Param['fill_color_legend']
    p1.xaxis.axis_label = Param['xlabel']
    p1.yaxis.axis_label = Param['ylabel']
    
    #%% Output to HTML
    output_file(Param['filename'], title=Param['title'])
    show(gridplot(p1, ncols=1, plot_width=Param['width'], plot_height=Param['height'], toolbar_location=None))
    
    #%% Write figure to path
    #savefig(p1, Param['filepath'])

    #%% END
    return(out)
