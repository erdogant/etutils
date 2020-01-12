from etutils.asciiart import asciiart
from etutils.ismember import ismember
from etutils.zip_extract import zip_extract
from etutils.time_extract import time_extract
from etutils.time_diff import time_diff
from etutils.strdiff import strdiff
from etutils.tictoc import tic, toc
from etutils.slice_array import slice_array
from etutils.set_dtypes import set_dtypes, set_y, is_DataFrame
from etutils.panel2dataframe import panel2dataframe
from etutils.nanunique import nanunique
from etutils.list2flatten import list2flatten
from etutils.internet_status import internet_status
from etutils.dummyvar import dummyvar
from etutils.dict2flatten import dict2flatten
from etutils.df2onehot import df2onehot
from etutils.colormap import colormap

# Import function in new level
import etutils.ones2idx
import etutils.picklefast
import etutils.path
import etutils.strfun
import etutils.filefun

# Import functions that are build on functions above
from etutils.mmap_readfile import mmap_readfile
from etutils.sql_readfile import sql_readfile

from etutils import viz
#from etutils import text

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'


# module level doc-string
__doc__ = """
etutils
=====================================================================

**etutils** 
See README.md file for more information.

"""
