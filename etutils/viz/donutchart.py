""" This function makes a donut/pie chart.
    
	from etutils.viz.donutchart import donutchart

	A=donutchart(data, labels, <optional>)

 INPUT:
   data:           List of integers

   labels:         List of strings

 OPTIONAL

   colors:         List of strings
                   e.g., ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

   explode:        List of integers


   chart           String
                   'donut': (default)
                   'pie': 

   height:         Integer:  Height of figure
                   [10]: (default)

   width:          Integer:  Width of figure
                   [10]: (default)

   filepath:       String: pathname of the file
                   'c:/temp/heatmap.png'

   shadow          Boolean [True,False]
                   True (default)
                   False


 OUTPUT
	output

 DESCRIPTION
   This function makes a donut/pie chart

 EXAMPLE
   from etutils.viz.donutchart import donutchart

   labels   = ['Frogs', 'Hogs', 'Dogs', 'Logs']
   data     = [15, 30, 45, 10]
   explode  = [0.1, 0, 0.2, 0]
   filepath = "c://temp//magweg//fig.png"
   
   A = donutchart(data,labels, chart='donut', filepath=filepath)
   A = donutchart(data,labels, chart='pie', explode=explode, filepath=filepath)

 SEE ALSO
   imagesc, hist

"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : donutchart.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Sep. 2017
#--------------------------------------------------------------------------

#%% Libraries
import matplotlib.pyplot as plt

#%%
def donutchart(data, labels, colors=None, explode=None, filepath='', chart='donut', width=10, height=10, shadow=True):
	#%% DECLARATIONS
    fig =[];
    # Make dictionary to store Parameters
    Param = {}
    Param['colors']       = colors
    Param['explode']      = explode
    Param['chart']        = chart
    Param['height']       = height
    Param['width']        = width
    Param['filepath']     = filepath
    Param['shadow']       = shadow

    #%% Make Pie-chart
    [fig,ax]=plt.subplots()
    [patches, texts, autotexts] = plt.pie(data, explode=Param['explode'], labels=labels, colors=Param['colors'],autopct='%1.1f%%', shadow=Param['shadow'])
    
    #%% Make the labels on the plot easier to read.
    for t in texts:
        t.set_size('larger')
    for t in autotexts:
        t.set_size('x-large')
    #autotexts[0].set_color('y')

    #%% Remove hart of the pie to create donut-chart
    if Param['chart']=='donut':
        #draw a circle at the center of pie to make it look like a donut
        centre_circle = plt.Circle((0,0),0.75,color='black', fc='white',linewidth=1.25)
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
    #end
    
    #%% get figure (usually obtained via "fig,ax=plt.subplots()" with matplotlib)
    fig = ax.get_figure()
    # specify dimensions
    fig.set_size_inches(Param['width'], Param['height'])

    #%% Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.show()

    #%% Write figure to path
    etutils.viz.savefig(fig, Param['filepath'])
            
    #%% END
    return(fig)
