""" This function makes a scatter plot

    from etutils.viz.scatter import scatter

	A=scatter(x, y, <optional>)

 INPUT:
   x:           numpy-array
   y:           numpy-array

 OPTIONAL

   labx=           list of strings of length [x] -> Coloring of the coordinates is based on input labels. LEGEND TEXT is based on this input
                   [] (default)

   labx_txt=       list of strings of length [x] -> this text is plotted for the coordinates
                   ['aap','boom','mies','etc']: Use custom text
                   []                         : if empty, use text from [labx] (default)
   
   density_labx=   list of strings of length [x], note that density_type is disabled. This option can be used for e.g., Cluster labels
                   [] (default)

   labx_type=      String: Plot textlabels from [labx]: LEGEND text is adjusted based on this input
                   'all'   : (default) Plot all txt labels in the plot
                   'unique': Plot unique text labels per group
                   ''      : Do not plot txt labels in the plot

   size=           numpy array of values. Can be either string such as 'k' for all points or of length [x] with values
                   25 (default)
   
   density=        Integer: Plot density over the points:
                   [0]: No (default)
                   [1]: Density borders
                   [2]: Density borders filled with colors

   density_levels= Integer: Thickness of the density. Small number limits the density
                   [30]: (default)

   density_type=    String: Plot density based on:
                   'match' (default) Match with [labx_type]
                   'all':   Density over all samples
                   'unique': Density per labx-type

   colors=         list of values. Can be either string such as 'k' for all points or of length [x] with values
                   [] (default)                     Colors are generated based on labx
                   ['#000000']                      All points will get this color
                   ['#000000','#000FFF','#FFF000']  Specify color for each point
                    
   edgecolors=     list array of values. Can be either string such as 'k' for all points or of length [x] with values
                   [] No color
                   ['#000000'] (default)            All points will get this color
                   ['#000000','#000FFF','#FFF000']  Specify color for each point

   alpha=          Float [0,..,1] 
                   [0.6] (default)
   
   xlabel=         String: x-label
                   "x-axis" (default)
                   
   ylabel=         String: y-label
                   "y-axis" (default)

   title=          String: title
                   "title" (default)

   grid=           Boolean [False,True]
                   [True]: Yes (default)
                   [False]: No

   height=         Integer:  Height of figure
                   [5]: (default)

   width=          Integer:  Width of figure
                   [5]: (default)

   cmap:           String: Colormap  https://matplotlib.org/examples/color/colormaps_reference.html
                   'Set1'       (default)     
                   'Set2'       
                   'rainbow'
                   'bwr'        Blue-white-red
                   'binary' or 'binary_r'
                   'seismic'    Blue-white-red 
                   'Blues'      white-to-blue
                   'Reds'       white-to-red
                   'Pastel1'    Discrete colors
                   'Paired'     Discrete colors
                   'Set1'       Discrete colors

   plottype=       String: Make bokeh plot:
                   'default'
                   'bokeh'
                   'all'

   savepath=       String: pathname of the file, for bokeh, it replaces .* by .html
                   'c:/temp/heatmap.png'


 OUTPUT
	output

 DESCRIPTION
    Makes scatterogram in matplotlib
    https://matplotlib.org/devdocs/gallery/shapes_and_collections/scatter.html#sphx-glr-gallery-shapes-and-collections-scatter-py
    https://matplotlib.org/users/text_intro.html
    
 EXAMPLE
   %reset -f
   %matplotlib auto
   import numpy as np
   from CLUSTER.DBSCAN import DBSCAN
   from TRANSFORMERS.coord2density import coord2density
   from sklearn.datasets.samples_generator import make_blobs

   from etutils.viz.scatter import scatter

   #EXAMPLE
   N=750
   [coord, labx] = make_blobs(n_samples=N, centers=[[1, 1], [-1, -1], [1, -1], [-1, 1]], cluster_std=0.4,random_state=0)
   clustlabx = DBSCAN(coord, showfig=0, min_samples=0)['labx']
   size = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radii
   labx_txt=np.arange(0,len(coord)).astype(str)
   labx_txt = ['labx_'+x for x in labx_txt]
   dens=coord2density(coord)
   x=coord[:,0]
   y=coord[:,1]
   

   out = scatter(x,y)
   out = scatter(x,y,density=1)
   out = scatter(x,y,density=2)
   out = scatter(x,y, size=100)
   out = scatter(x,y, colors=dens, size=100)
   out = scatter(x,y,size=size, plottype='bokeh', labx_type='', savepath='c:/temp/test.html')

   out = scatter(x,y, labx=labx_txt, size=size, labx_type='all',    plottype='default')

   out = scatter(x,y, labx=labx, labx_txt=labx_txt, size=size, labx_type='all',    plottype='all')
   out = scatter(x,y, labx=labx, labx_txt=labx_txt, size=size, labx_type='unique', plottype='default', cmap='Pastel1')
   out = scatter(x,y, labx=labx, labx_txt=labx_txt, size=size, labx_type='',       plottype='all')

   out = scatter(x,y, labx=labx.astype(str), labx_txt=labx_txt, size=size, labx_type='', plottype='all')

   out = scatter(x,y, labx=labx, labx_txt=labx_txt, size=size, plottype='bokeh')
   out = scatter(x,y, labx=labx, size=size, density_labx=clustlabx)
   out = scatter(x,y, labx=labx, size=size, density_labx=clustlabx)
   out = scatter(x,y, labx=labx, size=size, density_labx=clustlabx, density=2)
   
   out = scatter(x,y, labx=labx, size=size, labx_type='unique')
   out = scatter(x,y, labx=labx, size=size, labx_type='unique', cmap='Pastel1')
   out = scatter(x,y, labx=labx, size=size, labx_type='unique', cmap='Set1', density=1)
   out = scatter(x,y, labx=labx, size=size, labx_type='unique', cmap='Set1', density=2, density_levels=15)
   out = scatter(x,y, labx=labx, size=size, labx_type='unique', cmap='Set1', density=2, density_levels=15, density_type='unique')
   out = scatter(x,y, labx=np.arange(0,len(x)).astype(str), size=size, labx_type='unique', cmap='Set1', density=1, density_levels=15)
   out = scatter(x,y, labx=np.arange(0,len(x)).astype(str), size=size, labx_type='unique', cmap='Set1', density=1, density_levels=15, density_type='match')

   out = scatter(x,y,xlim=[5,10],ylim=[2,4])

   from bokeh.plotting import show
   show(out['bokeh'])
 
  SEE ALSO
   hist_bokeh, hist, imagesc, donutchart
"""

#--------------------------------------------------------------------------
# Name        : hist.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Nov. 2017
#--------------------------------------------------------------------------

# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Load libraries
def loadlibs():
    # To avoid loading/installing many heavy packages, load when required.
    import seaborn as sns

#%%
def scatter(xcoord, ycoord, labx=[], labx_txt=[], labx_type='all', colors=[], size=25, edgecolors=['#000000'], alpha=0.6, density=0, density_levels=30, density_type='match', density_labx=[], xlabel="x-axis", ylabel="y-axis", title="Title", xlim=[], ylim=[], width=10, height=10, grid=True, cmap='Set1', newfig=1, ax=[], savepath="", plottype='default'):
	#%% DECLARATIONS
    loadlibs()
    
    fig =[]
    # Make dictionary to store Parameters
    Param = {}
    # Labels
    Param['title']        = title
    Param['xlabel']       = xlabel
    Param['ylabel']       = ylabel
    Param['width']        = width
    Param['height']       = height
    Param['grid']         = grid
    Param['alpha']        = alpha
    Param['xlim']         = xlim
    Param['ylim']         = ylim

    Param['density']        = density
    Param['density_levels'] = density_levels
    Param['density_type']   = density_type
    Param['density_labx']   = density_labx

    Param['colors']       = colors # All black
    Param['size']         = size
    Param['labx']         = labx
    Param['labx_type']    = labx_type
    Param['labx_txt']     = labx_txt

    Param['edgecolors']   = edgecolors
    Param['cmap']         = cmap
    Param['newfig']       = newfig
    
    Param['savepath']     = savepath
    Param['plottype']     = plottype

    #%% Check type
    if 'numpy' in str(type(Param['labx'])):
        if 'str' not in str(type(Param['labx'][0])):
            Param['labx']=list(Param['labx'])

    if Param['density_labx']!=[] and Param['density']==0:
        Param['density']=1
    if Param['density_labx']!=[]:
        Param['density_type']='unique'
    if Param['labx_txt']==[]:
        Param['labx_txt']=Param['labx']
    if Param['labx']==[]:
        Param['labx']=Param['labx_txt']
    
    # Set extra paramters
    if Param['density_type']=='match':
        Param['density_type'] = Param['labx_type']
    if Param['density']==1:
        Param['density_shade'] = False
    elif Param['density']==2:
        Param['density_shade'] = True
    
    Param['density sequential_colors'] = ['Reds', 'Blues', 'Greens', 'Purples', 'Oranges', 'Greys', 'BuGn', 'BuPu', 'gist_yarg',
                             'GnBu', 'OrRd','PuBu', 'PuBuGn', 'PuRd', 'RdPu', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']
    # Get color schemes
    if Param['cmap']!=None:
        getcolors=sns.color_palette(Param['cmap'],len(np.unique(Param['labx']))).as_hex()
    
    #%% Make Figure
    SMALL_SIZE  = 14
    MEDIUM_SIZE = 14
    BIGGER_SIZE = 14
    
    plt.rc('font',  size      = SMALL_SIZE)   # controls default text sizes
    plt.rc('axes',  titlesize = SMALL_SIZE)   # fontsize of the axes title
    plt.rc('xtick', labelsize = SMALL_SIZE)   # fontsize of the tick labels
    plt.rc('ytick', labelsize = SMALL_SIZE)   # fontsize of the tick labels
    plt.rc('legend',fontsize  = SMALL_SIZE)   # legend fontsize
    plt.rc('axes',  labelsize = MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('figure',titlesize = BIGGER_SIZE)  # fontsize of the figure title
    axis_font = {'fontname':'Arial'}
    # axis_font = {'fontname':'Calibri Light', 'size':'14'}
    #plt.style.use('ggplot')
    plt.style.use('default')
    

    #%% Use labx to create colors
    if len(Param['colors'])==0 and Param['labx']!=[]:
        # Default all black
        Param['colors'] = np.repeat('#000000',len(Param['labx']))

        # Colors are determined by LABX
        uilabx = np.unique(Param['labx'])
        for i in range(0,len(uilabx)):
            I = uilabx[i]==Param['labx']
            Param['colors'][I]=getcolors[i]
        #end
        
#        [_,labxBIN]=dummyvar(Param['labx'])
#        Param['colors'] = np.repeat('#000000',len(labx))
#        for i in range(0,labxBIN.shape[1]):
#            Param['colors'][labxBIN.iloc[:,i]]=getcolors[i]
#        #end
        
    elif len(Param['colors'])==1:
        # Colors are the same as specified by user
        Param['colors'] = np.repeat(Param['colors'],len(xcoord))
    elif len(Param['colors'])==0:
        # Colors are all black
        Param['colors'] = np.repeat('#000000',len(xcoord))
    #end

    # EDGE-COLORS
    if len(Param['edgecolors'])==0:
        Param['edgecolors']=None
    elif len(Param['edgecolors'])==1:
        Param['edgecolors'] = np.repeat(Param['edgecolors'],len(xcoord))
    #end
        
    #%% Make figure with properties
    if Param['plottype']=='default' or Param['plottype']=='all':

        if Param['newfig']==1:
            [fig,ax]=plt.subplots(figsize=(Param['width'],Param['height']))
            plt.style.use('ggplot')
        #end

        #%% Add density map
        if Param['density']>0:
            if Param['density_type']=='all':
                # Draw density plot over ALL points in space
                ax = sns.kdeplot(xcoord, ycoord, cmap=Param['density sequential_colors'][0], n_levels=Param['density_levels'], shade=Param['density_shade'], shade_lowest=False)
                #end
            elif Param['density_type']=='unique':
                # Get labx
                if Param['density_labx']!=[]:
                    uilabx=np.unique(Param['density_labx'])
                else:
                    uilabx=np.unique(Param['labx'])
                #end
    
                for i in range(0,len(uilabx)):
                    # Get labx
                    if Param['density_labx']!=[]:
                        getX=xcoord[uilabx[i]==Param['density_labx']]
                        getY=ycoord[uilabx[i]==Param['density_labx']]
                    else:
                        getX=xcoord[uilabx[i]==Param['labx']]
                        getY=ycoord[uilabx[i]==Param['labx']]
                    #end
        
                    # Draw density plot
                    if len(getX)>1:
                        idx_color = np.mod(i, len(Param['density sequential_colors']))
                        ax = sns.kdeplot(getX, getY, cmap=Param['density sequential_colors'][idx_color], n_levels=Param['density_levels'], shade=Param['density_shade'], shade_lowest=False)
                    else:
                        print('WARNING: Density plot requires >1 values! Set [density_type="all"]')

        #%% Add text labels from Param['labx_txt']
    #    labxnew=pd.DataFrame(index=range(0,len(labx)), columns=['labx','x','y'])
        if Param['labx_type']=='all':
    #        labxnew.labx=labx
    #        labxnew.x=xcoord
    #        labxnew.y=ycoord
            # Write text label in plot
            for i in range(0,len(Param['labx'])):
                ax.annotate(Param['labx_txt'][i], (xcoord[i]+xcoord[i]*0.005, ycoord[i]+ycoord[i]*0.005))
            #end
    #        # Draw density plot
    #        if Param['density']>0:
    #            ax = sns.kdeplot(xcoord, ycoord, cmap=Param['density sequential_colors'][0], n_levels=Param['density_levels'], shade=Param['density_shade'], shade_lowest=False)
    #        #end
        elif Param['labx_type']=='unique':
            #print('WARNING: THE UNIQUE TEXT LABEL IS BASED ON [LABX]')
            [uilabx, idx] = np.unique(np.array(Param['labx']), return_index=True)
            uilabx_txt    = np.array(Param['labx_txt'])[idx]
    #        labxnew=pd.DataFrame(index=range(0,len(uilabx)), columns=['labx','x','y'])
            for i in range(0,len(uilabx)):
                getX=xcoord[uilabx[i]==Param['labx']]
                getY=ycoord[uilabx[i]==Param['labx']]
    
    #            # Draw density plot
    #            if Param['density']>0:
    #                if len(getX)>1:
    #                    idx_color = np.mod(i, len(Param['density sequential_colors']))
    #                    ax = sns.kdeplot(getX, getY, cmap=Param['density sequential_colors'][1], n_levels=Param['density_levels'], shade=Param['density_shade'], shade_lowest=False)
    #                else:
    #                    print('WARNING: Density plot requires >1 values!')
    #                #end
    #            #end
    
                # Write text label in plot
                xm=np.mean(getX)
                ym=np.mean(getY)
                # Draw white circles at cluster centers
                # ax.scatter(xm, ym, marker='o', c="white", alpha=1, s=200, edgecolor='k')
                # Add text labels
                #ax.annotate(uilabx[i], (xm, ym))
                ax.annotate(uilabx_txt[i], (xm, ym))
                # Store labx
    #            labxnew.labx[i]=uilabx[i]
    #            labxnew.x[i]=xm
    #            labxnew.y[i]=ym
            #end
        #end
            
        #%% Scatter-plot
        # https://matplotlib.org/devdocs/gallery/lines_bars_and_markers/scatter_with_legend.html
        # Make scatter plot
        plt.scatter(xcoord, ycoord, s=Param['size'], c=Param['colors'], marker=None, linewidth=None, edgecolors=Param['edgecolors'], alpha=Param['alpha'])
    #    ax.legend()
    
        #% Limit axis
        if Param['xlim']!=[]:
            plt.xlim(xmin=Param['xlim'][0], xmax=Param['xlim'][1])
        #end
        if Param['ylim']!=[]:
            plt.ylim(ymin=Param['ylim'][0], ymax=Param['ylim'][1])
        #end
    
        #% SETTINGS
        #plt.rcParams['axes.facecolor']='white'
        plt.xlabel(Param['xlabel'], **axis_font)
        plt.ylabel(Param['ylabel'], **axis_font)
        plt.title(Param['title'], **axis_font)
    #    plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    #    plt.axis([40, 160, 0, 0.03])
        plt.grid(Param['grid'])
        
        if Param['newfig']==1:
            plt.show()
            plt.draw()
        #end
    #    https://matplotlib.org/users/legend_guide.html
    #    if Param['labx_type']=='unique':
    #        plt.legend([red_dot, (red_dot, white_cross)], ["Attr A", "Attr A+B"])
    #    #end
    
        #%% Set the tick labels font
    #    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    #        label.set_fontname('Arial')
            #label.set_fontsize(14)
        #end
        #%% Write figure to path
        if Param['savepath']!='':
            from savefig import savefig
            savefig(fig, Param['savepath'])
        #end
    #end

    #%% Make bokeh plot
    # https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html
    # https://bokeh.pydata.org/en/latest/docs/user_guide/tools.html
    p=[]
    if Param['plottype']=='bokeh' or Param['plottype']=='all':
        try:
            from bokeh.plotting import figure, show, save, output_file
            from bokeh.models import ColumnDataSource, HoverTool, LabelSet
            flag_legend=1
            
            # Scale data between [0-1] using zero-mean, unit variance approach
            if 'int' in str(type(Param['size'])):
                X_scaled = np.repeat(Param['size'],len(xcoord))
            else:
                X_scaled = (size-np.mean(size)) / np.std(Param['size'])
                X_scaled = (X_scaled+np.abs(np.min(X_scaled))+1)*2

            if Param['labx_txt']==[]:
                Param['labx_txt'] = np.repeat('',len(xcoord))
                Param['labx_txt'] = np.arange(0,len(xcoord))
                flag_legend=0

            if Param['labx']==[]:
                Param['labx'] = np.repeat('',len(xcoord))
                Param['labx'] = np.arange(0,len(xcoord))
                flag_legend=0
            
            # Make dataframe to be used in the bokeh plot
            df = pd.DataFrame(index=range(0,len(xcoord)), columns=['x','y','labx_txt','labx','color','size'])
            df['x']        = xcoord
            df['y']        = ycoord
            df['labx_txt'] = Param['labx_txt']
            df['labx']     = Param['labx']
            df['color']    = Param['colors']
            df['size']     = X_scaled

            # Make hover tooltip text
            source = ColumnDataSource(df)
            hover  = HoverTool(tooltips=[("(x,y)", "($x, $y)"),("desc: ", "@labx_txt"),])
    
    #        TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select"
    #        p = figure(tools=TOOLS, title = Param['title'])
#            p = figure(tools=[hover,"crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select"])
            p = figure(tools=[hover,"crosshair,wheel_zoom,reset,lasso_select"])
            p.xaxis.axis_label = Param['xlabel']
            p.yaxis.axis_label = Param['ylabel']

            # Make scatter plot
            if flag_legend==1:
                p.circle(x='x', y='y', color='color', fill_alpha=Param['alpha'], size='size', legend='labx', source=source)
            else:
                p.circle(x='x', y='y', color='color', fill_alpha=Param['alpha'], size='size', source=source)

#            p.circle(x='index', y='tmp1_y1', width=0.75, height='tmp2_y1', source=source)
#            p.circle(xcoord, ycoord, color=Param['colors'], fill_alpha=Param['alpha'], size=X_scaled, legend='labx', source=source)

            # Add text labels
            if Param['labx_type']=='all':
                labels = LabelSet(x='x', y='y', text='labx_txt', level='glyph',x_offset=5, y_offset=5,render_mode='canvas', text_font_size="8pt", source=source)
                p.add_layout(labels)
            
            # Make output file
            if Param['savepath']!='':
#                output_file(Param['title']+".html", title=Param['title'])
                output_file(Param['savepath'].split(sep='.')[0]+'.html', title=Param['title'])

            # Show in browser
            show(p)

            # Save on disk
            if Param['savepath']!='':
                save(p)

        except:
            print("Oops! BOKEH plot failed! pip install bokeh or try to close browser, and Try again...")

    #%% END
    output = {}
    output['ax']=ax
    output['plt']=plt
    output['fig']=fig
    output['bokeh']=p
    
    return(output)
