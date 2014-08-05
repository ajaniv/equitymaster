#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/builder.py - equity masger  build pattern utilities
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  

"""

.. module:: equity_master/builder
   :synopsis: object creation and configuration

Required to simplify object creation and configuration

.. moduleauthor:: Amnon Janiv  

"""
__revision__ = '$Id: $'
__version__ = '0.0.1'


import Queue
import os
import shutil
from equity_master import config
from equity_master import process
from equity_master import model
from equity_master import util

from equity_master import desc

__all__ = [
           'create_file_detection_process',
           'create_file_validation_process',
           'create_file_sort_process',
           'create_file_merge_process',
           'create_file_detection_request',
           'create_file_validation_request',
           'create_file_sort_request',
           'create_file_merge_request',
           
           ]
def create_workflow(root_dir, wf_dir, data_dir, input_files):
    """create a workflow environment"""
    
    #create directory structure
    wf_dir_name = (root_dir + 
                wf_dir + 
                config.WF_PREFIX + config.FILE_NAME_SEPARATOR + 
                util.file_time_suffix() +
                config.DIR_SEP)
                
    os.mkdir (wf_dir_name)
    exclude = [config.END]
    for state in model.process_states.itervalues():
        if state.state_id not in exclude:
            sub_dir = wf_dir_name + state.name
            os.mkdir (sub_dir )
    
    #add required files to work flow
    dest_dir = wf_dir_name + model.process_states[config.START].name
    for source_file in input_files:
        shutil.copy(data_dir + source_file, dest_dir)
        
    return model.Workflow(wf_dir_name)

def file_path(state_id,
               file_name,
               wf_dir
               ):
    fname = (wf_dir + 
             model.process_state(state_id).name + 
             config.DIR_SEP + file_name)
    return fname

def error_file_path(state_id, 
                    file_name, 
                    wf_dir):
    input_prefix = os.path.split(file_name)[1].split('.')[0]
    fname = (wf_dir  
             + config.error_dir  
             + input_prefix  
             + config.FILE_NAME_SEPARATOR  
             + model.process_state(state_id).name 
             + config.FILE_NAME_SEPARATOR   
             + config.ERROR_FILE_NAME  
             + config.FILE_NAME_SUFFIX )
    return fname
   
def file_names(
               current_state_id,
               input_file_name, 
               output_file_name, 
               wf_dir):
    
#    sep = config.FILE_NAME_SEPARATOR
#    file_suffix = config.FILE_NAME_SUFFIX
#    error_suffix = config.ERROR_FILE_NAME
#    input_prefix = os.path.split(input_file_name)[1].split('.')[0]
    current_state = model.process_state(current_state_id)
    next_state = model.process_state(current_state.next_state_id)
     
    
    input = file_path(current_state_id, 
                      input_file_name, 
                      wf_dir)
#    input = (wf_dir + current_state.name + 
#             config.DIR_SEP + input_file_name)
   
   
    output = file_path(next_state.state_id, 
                      output_file_name, 
                      wf_dir)
#    output = (wf_dir  + next_state.name 
#               + config.DIR_SEP +  input_file_name
#              )

    error = error_file_path(current_state_id, 
                            input_file_name, 
                            wf_dir)
#    error = (wf_dir + config.error_dir + input_prefix  
#             + sep + current_state.name + sep +  error_suffix  
#             + file_suffix )
    return (input,output, error)



def create_process(cls, proc_name):
    proc_cfg  = config.process_config[proc_name]
    attr_name = proc_cfg[config.PROCESS_NAME_ATTR]
    proc = cls(name=attr_name,
                        kwargs=proc_cfg)
    return proc

def create_file_detection_process():
    """Create and configure a file detection  process
    """
    proc =  create_process(cls = process.FileDetection,
                          proc_name = config.FILE_DETECTION)
    return proc

    
def create_file_validation_process():
    """Create and configure a file validation  process
    """
    proc = create_process(cls = process.FileValidation,
                          proc_name = config.FILE_VALIDATION)
    return proc

def create_file_sort_process():
    """Create and configure a file sort  process
    """
    proc = create_process(cls = process.FileSort,
                          proc_name = config.FILE_SORT)
    return proc

def create_file_merge_process():
    """Create and configure a file merge  process
    """
    proc = create_process(cls = process.FileMerge,
                          proc_name = config.FILE_MERGE)
    return proc

proc_builders  = (create_file_detection_process,
                  create_file_validation_process,
                  create_file_sort_process,
                  create_file_merge_process)

def create_procs():
    procs = [proc() for proc in proc_builders]
    return procs

def create_queue():
    return Queue.Queue(config.PROCESS_MAX_QUEUE_SIZE)

def create_file_desc(vendor=None, file_name=None, field_desc=None):
    return desc.FileDescriptor(vendor, file_name, field_desc)

def create_request(input_file_names, 
                   output_file_names,
                   error_file_names,
                   state_id, 
                   input_desc, 
                   output_desc):
    return model.FileRequest(input_file_names, 
                             output_file_names,
                             error_file_names,
                             state_id, 
                             input_desc,
                             output_desc)
    
def create_file_detection_request(state_id,
                                  input_desc, 
                                  output_desc,
                                  wf_dir):
   
    input, output, error = file_names(state_id,
                                      input_desc.file_name,
                                      input_desc.file_name,
                                      wf_dir
                                      )
    return create_request(
                          input_file_names=(input,),
                          output_file_names=(output,),
                          error_file_names=(error,),
                          state_id = state_id,
                          input_desc=input_desc,
                          output_desc=output_desc)
    
    
def create_file_validation_request(state_id,
                                   input_desc,
                                    output_desc,
                                    wf_dir):
    input, output, error = file_names(state_id,
                                      input_desc.file_name,
                                      input_desc.file_name,
                                      wf_dir
                                      )
    return create_request(
                          input_file_names=(input,),
                          output_file_names=(output,),
                          error_file_names=(error,),
                          state_id = state_id,
                          input_desc=input_desc,
                          output_desc=output_desc)
    
def create_file_sort_request(state_id,
                                input_desc,
                                output_desc,
                                wf_dir):
    input, output, error = file_names(state_id,
                                      input_desc.file_name,
                                      input_desc.file_name,
                                      wf_dir
                                      )
    return create_request(
                          input_file_names=(input,),
                          output_file_names=(output,),
                          error_file_names=(error,),
                          state_id = state_id,
                          input_desc=input_desc,
                          output_desc=output_desc)



def create_file_merge_request(state_id,
                                input_descs,
                                output_desc,
                                wf_dir):
    
    input_names = [file_path(state_id, 
                             fd.file_name, 
                             wf_dir)
                    for fd in input_descs]
    
    output = file_path(
                       model.process_state(state_id).next_state_id,
                       output_desc.file_name,
                       wf_dir)
    
    error = error_file_path(state_id,
                            output_desc.file_name,
                            wf_dir)
    return create_request(
                          input_file_names=input_names,
                          output_file_names=(output,),
                          error_file_names=(error,),
                          state_id = state_id,
                          input_desc=input_descs[0],
                          output_desc=output_desc)
request_builders = ( 
                   create_file_detection_request,
                   create_file_validation_request,
                   create_file_sort_request,
                   create_file_merge_request)

def create_requests():
    reqs = [req() for req in request_builders]
    return reqs
    