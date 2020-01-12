""" This function creates a wordcloud.

    import etutils.viz.wordcloud as wordcloud

	A= wordcloud(data, <optional>)

 INPUT:
   data:           List or numpy array of strings
                   ['hello this is sentence 1','how are you doing','back to the 80ties']

 OPTIONAL

   verbose:        Boolean [True,False]
                   False: No (default)
                   True: Yes

 OUTPUT
	output

 DESCRIPTION
   Create wordcloud

 EXAMPLE
   import etutils.viz.wordcloud as wordcloud

   wordcloud(data)

"""

#--------------------------------------------------------------------------
# Name        : wordcloud.py
# Version     : 1.0
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : March. 2019
#--------------------------------------------------------------------------

import matplotlib.pyplot as plt

#%% Load libraries
def loadlibs():
    # To avoid loading/installing many heavy packages, load when required.
    from wordcloud import WordCloud as wc

#%%
def wordcloud(data, title = None):
    # Load libraries
    loadlibs()
    # Make the plot
    cloudtxt = wc(
        background_color = 'white',
        max_words = 200,
        max_font_size = 40, 
        scale = 3,
        random_state = 42
    ).generate(str(data))

    fig = plt.figure(1, figsize = (20, 20))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize = 20)
        fig.subplots_adjust(top = 2.3)

    plt.imshow(cloudtxt)
    plt.show()
