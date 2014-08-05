#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/__init__.py - equity master main  package
#
# Standard copyright message
#
#  
#

# Initial version: 2012-04-12
# Author: Amnon Janiv  


"""
.. module:: equity_master
   :synopsis:equity master package

 
The package is organized as follows:

- bootstrap. Allows the package to run once installed
- builder.  implements factory and configuration/builder related functionality
- common.  classes, functions used by other modules and common across the
            package
- config.   configuration module comprised of constants, logging.
- desc.        provides facilities for describing fields and files.  In effect,
                meta data required to parse the files at run time without having
                this knowledge hard coded

- file_util.  File sort and merge algorithms which were adopted from the 
            internet.  These are used to handle merging of multiple files
            and support not to have the files all in memory.
- model     constain business classes and functions.
- process   Process related functionality wrapped in this implementation around 
            the underlying threading package
- refdata    Was intented for doing direct key lookup for values stored on disk,
             or memory.
- regexp     provides support for regular rexpressions for ISIN, CUSIP,
             and the fields.  It is integrated with the desc package
- util       miscellaneous set of utilities
 

.. moduleauthor:: Amnon Janiv  
"""

__revision__ = '$Id: $'
__version__ = '0.0.1'
import bootstrap
from bootstrap import *

import builder
from builder import  *

import config
from config import *

import model
from model import *
__all__ = (bootstrap.__all__,
           config.__all__, 
           builder.__all__,
           model.__all__)