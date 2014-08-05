#/usr/bin/env python
# -#- coding: utf-8 -#-

#
#  
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  

"""

.. module:: samples
   :synopsis: Explore equity master package  

Demonstrates how file related processes are pipelined between
cooperating process using input and output queues.



.. moduleauthor:: Amnon Janiv  

"""


import os
import sys

from optparse import OptionParser
root_dir = '../demo/'
log_dir = 'logs/'
wf_dir =  'wf/'
data_dir = '../data/'
input_dir = data_dir + 'input/'
data_files = ( 
              'vendor_a_eq.txt',
              'vendor_b_eq.txt'
              )
def fix_path():
    """
    Configure python sys.path for standalone execution
    """
    _cwd = os.path.dirname(__file__)
    _app_root = os.path.abspath(os.path.join(_cwd, '..'))
    if not _app_root in sys.path:
        sys.path.append(_app_root)


try:
    import equity_master as eqm
except ImportError:
    fix_path()
    import equity_master as eqm

#
# Leverage the data configuration environment
# One can envision a process where these
# configuration files are detected dynamically.
#
from data_config import vendor_a
from data_config import vendor_b
from data_config import  my_firm

def detection_req(wfdir):
    """Helper function for creating file detection requests
    """
    fn = eqm.create_file_detection_request
    file_descs = (vendor_a.in_eq_def_file_desc,
                  vendor_b.in_eq_def_file_desc)
    reqs = [fn(eqm.WAIT,
                file_desc,
                file_desc,
                wfdir)
            for file_desc in file_descs]
    return reqs

def validation_req(wfdir):
    """
    Create a validation request
    """
    fn = eqm.create_file_validation_request
    in_desc  = (vendor_a.in_eq_def_file_desc,
                vendor_b.in_eq_def_file_desc)
    out_desc = (vendor_a.out_eq_def_file_desc,
                vendor_b.out_eq_def_file_desc)
    reqs = [fn(eqm.ARRIVED,
                in_d,
                out_d,
                wfdir)
            for in_d, out_d in zip(in_desc, out_desc)]
    return reqs

def sort_req(wfdir):
    """
    Create a file sort request
    """
    fn = eqm.create_file_sort_request
    in_desc  = (vendor_a.out_eq_def_file_desc,
                vendor_b.out_eq_def_file_desc)
    out_desc = (vendor_a.out_eq_def_file_desc,
                vendor_b.out_eq_def_file_desc)
    reqs = [fn(eqm.VALIDATED,
                in_d,
                out_d,
                wfdir)
            for in_d, out_d in zip(in_desc, out_desc)]
    return reqs



def merge_req(wfdir):
    """
    Create a file merge request
    """
    fn = eqm.create_file_merge_request
    input_file_descs = (vendor_a.out_eq_def_file_desc,
                        vendor_b.out_eq_def_file_desc)
    request = fn(eqm.SORTED,
                 input_file_descs, 
                my_firm.eq_def_file_desc,
                wfdir)
    return (request,)
                            

def dispatch(proc, reqs):
    """
    Send/receive request/response
    """
    resp = []
    for index in range(len(reqs)):
        proc.send(reqs[index]) 
        resp.append(proc.receive())
    return resp
        
        
   


def exec_workflow(
    parser,
    options,
    args,
    ):
    """
    Execute command line options related to file feed proces
    """
    print ('workflow  ->', ' '.join(sys.argv))
   
  
    wf = eqm.create_workflow(options.root_dir,
                                   options.wf_dir,
                                   options.log_dir,
                                   options.data_dir,
                                         data_files)
    print ('workflow  is using direcotry (%s)' % wf.dir)
    
    def detect_st():
        proc = eqm.create_file_detection_process()
        reqs = detection_req(wf.dir)
        return proc, reqs
    
    def validate_st():
        proc = eqm.create_file_validation_process()
        reqs = validation_req(wf.dir)
        return proc, reqs
    
    def sort_st():
        proc = eqm.create_file_sort_process()
        reqs = sort_req(wf.dir)
        return proc, reqs
    
    def merge_st():
        proc = eqm.create_file_merge_process()
        reqs = merge_req(wf.dir)
        return proc, reqs
        
    
    tmpl = 'process is now in state (%s) for  file (%s)'
    for state in (detect_st,validate_st, sort_st, merge_st):
        
        proc, reqs = state()
        proc.start()
        responses = dispatch (proc, reqs)
        assert (len(responses) == len(reqs))
        
        for result   in responses:
            assert(result.error is None)
            proc_st = eqm.process_state(result.response.file_state)
            print (tmpl % (proc_st.name,
                          result.response.file_name))
        proc.shutdown()
        proc.join()


    

def setup():
    """
    Setup workflow execution environment
    """
    
    parser = OptionParser(usage='%prog -q[query] -j[journey] ',
                          version='%prog 1.0')
    parser.add_option('-d', '--data_dir', action='store', dest='data_dir',
                      default=input_dir, help="data files directory")
    parser.add_option('-r', '--root_dir', action='store', dest='root_dir',
                      default=root_dir, help="demo root  directory")
    parser.add_option('-w', '--workflow_dir', action='store', dest='wf_dir',
                      default=wf_dir, help="workflow root directory")
    parser.add_option('-l', '--log_dir', action='store', dest='log_dir',
                      default=log_dir, help="log  directory")
  
    
   
    return parser


def main():

    parser= setup()
    (options, args) = parser.parse_args()
    exec_workflow(parser,  options, args)

if __name__ == '__main__':
    main()
