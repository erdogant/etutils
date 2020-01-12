'''
from etutils.viz.rocplot import rocplot

#--------------------------------------------------------------------------
# Name        : rocplot.py
# Version     : 1.0
# Author      : E.Taskesen
# Date        : Sep. 2017
#--------------------------------------------------------------------------

'''

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import f1_score

def rocplot(y_true, y_pred, threshold=0.5, ax=None):
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    f1score = f1_score(y_true, y_pred>=thresholds)
    
    if isinstance(ax, type(None)):
        fig,ax=plt.subplots(figsize = (20, 12))

    lw = 2
    plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic. F1score:%.3f' %f1score)
    plt.legend(loc="lower right")
    plt.show()

    out = dict()
    out['auc']=roc_auc
    out['f1']=f1score
    return(out)
    