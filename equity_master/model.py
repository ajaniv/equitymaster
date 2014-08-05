#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/file_sort - merge and sort
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  

"""

.. module:: equity_master/model
   :synopsis: basic abstractions



.. moduleauthor:: Amnon Janiv  

"""
__revision__ = '$Id: $'
__version__ = '0.0.1'



import datetime

from equity_master import config

__all__ = ['process_state'
           ] 
class FileProcesState(object):
    """
    Class to model the process state
    """
    
    def __init__(self, state_id, next_state_id, error, name):
        self.state_id = state_id
        self.next_state_id = next_state_id
        self.name = name
        self.error = error
   

_cl = FileProcesState
process_states = { 
   config.WAIT : _cl(config.WAIT, config.ARRIVED, config.ERROR,'wait'),
   config.ARRIVED : _cl(config.ARRIVED, config.VALIDATED, config.ERROR,'arrived'),
   config.VALIDATED : _cl(config.VALIDATED, config.SORTED, config.ERROR,'validated'),
   config.SORTED : _cl(config.SORTED, config.MERGED, config.ERROR,'sorted'),
   config.MERGED : _cl(config.MERGED, config.DONE, config.ERROR,'merged'),
   config.DONE : _cl(config.DONE, None, None,'done'),
   config.ERROR : _cl(config.ERROR, None, None,'error'),
              }

def process_state(state_id):
    """
    process state lookup funciton
    """
    return process_states [state_id]


class Request(object):
    """
    Class designed to support process request description
    It is a base class for all request types
    """
    class Priority:
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        DEFAULT = MEDIUM
    default_priority = Priority.MEDIUM
    
    def __init__(self):
        self.created = datetime.datetime.now()
        
    def is_system(self):
        return False;
        
class Response(object):
    """
    Class to handle process response
    It is a base class for all responses
    """
    default_priority = Request.Priority.MEDIUM
    def __init__(self):
        self.error_app = None
        self.error_sys = None
        self.created = datetime.datetime.now()
        self.completed = None

class FileResponse(Response):
    """
    Response with details on a file
    """
    def __init__(self, file_name, file_state):
        super(FileResponse,self).__init__()
        self.file_name = file_name
        self.file_state = file_state
    


class FileRequest(Request):
    """
    Class designed to allow specification of class related requests
    """
    def __init__(self, 
                 input_file_names, 
                 output_file_names,
                 error_file_names,
                 input_file_state,
                 input_file_desc,
                 output_file_desc,
                 ):
        super(FileRequest,self).__init__()
        self.input_file_names = input_file_names
        self.output_file_names = output_file_names
        self.error_file_names = error_file_names
        self.input_file_state = input_file_state
        self.input_file_desc = input_file_desc
        self.output_file_desc = output_file_desc

        
        
class Workflow (object):
    """
    minimal abstraction designed to model the transition
    """
    def __init__(self, 
                 dir,
                 ):
        self.dir = dir
        self.created = datetime.datetime.now()
        self.end_time = None


        
        
class SystemRequest(Request):
    """
    Very basic construct to provide process support
    """
    class RequestType:
        SHUTDOWN=1
    
    default_priority = Request.Priority.HIGH
    
    def __init__(self, request_type):
        super(SystemRequest,self).__init__()
        
    def is_system(self):
        return True


