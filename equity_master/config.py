#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/config.py - package comfiguration module
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  

"""

.. module:: equity_master/config
   :synopsis: configuration related construct



.. moduleauthor:: Amnon Janiv  

"""
__revision__ = '$Id: $'
__version__ = '0.0.1'





import logging
import time
import Queue

__all__ = ['WAIT',
           'ARRIVED',
           'VALIDATED',
           'SORTED',
           'MERGED']



"""
Constants Section
"""
PROCESS_NAME_ATTR = 'proc_name'

PROCESS_MAX_QUEUE_SIZE = 4
FILE_NAME_SEPARATOR = '_'
FILE_NAME_SUFFIX = '.txt'
FIELD_FILLER = '0Z1Y'
FIELD_TRIM = ' \t\n\r'
ERROR_FILE_NAME='error'
FIELD_CAT_MIN = 3
FIELD_CAT_MAX = 32
DIR_SEP = '/'
FIELD_SEP = ','
#Process Names
FILE_DETECTION = 'file detection'
FILE_VALIDATION = 'file validation'
FILE_SORT = 'file sort'
FILE_MERGE = 'file merge'
FILE_FINAL = 'file final'
WF_PREFIX = 'wf'
proc_names = (
            FILE_DETECTION,
            FILE_VALIDATION,
            FILE_SORT,
            FILE_MERGE,
            FILE_FINAL)
#
#Process States
WAIT=1
ARRIVED=2
VALIDATED=3
SORTED=4
MERGED=5
DONE=6
ERROR=7
START=1
END=DONE

state_ids = (
             WAIT,
             ARRIVED,
             VALIDATED,
             SORTED,
             MERGED
             )
#
work_flow_dir = 'wf/'
file_time_format = '%Y%m%d%H%M%S'

#Logging
def log_init(log_dir):
    logger = logging.getLogger('equity_master')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    # @TODO: configure logger time format to use GMT

    _log_file_name=log_dir + 'equity_master'
    _log_file_suffix='.log'
    file_handler = logging.FileHandler(_log_file_name + '_' + time.strftime(file_time_format) + _log_file_suffix)
    file_handler.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(funcName)s - (%(threadName)-10s) - %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - (%(threadName)-10s) - %(message)s')
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("Logger initialized")


"""
    Queue section
"""




"""
    Data Section
"""
data_dir = 'data/'
data_input_dir = data_dir + 'input/'
error_dir = 'error/'

file_names = ('vendor_a_eq.txt', 'vendor_a_ts.txt')

def data_files():
    return [data_input_dir   + file_name for file_name in file_names]



process_config = dict()
for proc_name, state_id in zip(proc_names, state_ids):
    process_config[proc_name] = dict (
                        proc_name = proc_name,
                        state_id = state_id,
                        input_queue = Queue.Queue(PROCESS_MAX_QUEUE_SIZE),
                        output_queue = Queue.Queue(PROCESS_MAX_QUEUE_SIZE))
    
                                    