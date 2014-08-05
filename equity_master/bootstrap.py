#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# router/calc.py - router journey calculator
#
# standard copy right text
#

# Initial version: 2012-04-12
# Author: Amnon Janiv  

"""

.. module:: router/bootstrap
   :synopsis: router package bootstrap

Handle package initialization tasks including retrieving
required data, ensuring that dependent packages/applications
have a valid run time  environment

.. moduleauthor:: Amnon Janiv  

"""

__revision__ = '$Id: $'
__version__ = '0.0.1'

import os

_log_dir='./logs'


__all__ = ['create_workflow', 'log_dir']


def create_workflow(root_dir,
                    wf_dir,
                    log_dir,
                    data_dir, 
                    *data_files):
    """Create directory structure required to support
    the workflow
    """
    def create_dir(name):
        try:
            os.stat(name)
        except:
            os.mkdir(name)
    global _log_dir
    create_dir(root_dir)
    create_dir(root_dir + wf_dir)
    _log_dir = root_dir+log_dir
    create_dir(_log_dir)
    
    from equity_master import config
    config.log_init(_log_dir)
    from equity_master import builder
    
    return builder.create_workflow(root_dir, wf_dir, data_dir, *data_files)

def log_dir():
    """provide support to other modules with logging configuration
    """
    return _log_dir