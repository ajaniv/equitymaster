#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# router/tests/common.py - router tests common module
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv

"""

.. module:: equity_master/tests/common
   :synopsis: eqity_master unit test common constructs

Common utilities and classes for unit testing the  equity_master module.

.. moduleauthor:: Amnon Janiv  

"""
import os
import sys
import unittest


def fix_path():
    """
    Configure python path
    Required in order to support non Eclipse test execution
    without setting PYTHONPATH
    """
    _cwd = os.path.dirname(__file__)
    _app_root = os.path.abspath(os.path.join(_cwd, '..'))
    if not _app_root in sys.path:
        sys.path.append(_app_root)


try:
    import equity_master
except ImportError:
    fix_path()

from equity_master import config
from equity_master import builder



class EquityMasterTestData(object):
    """
    Implement data factory pattern
    Designed to simply test data reuse
    and reduce unit testing data errors
    """
     
    def __init__(self):
        pass

    def data_files(self):
        return (config.data_input_dir + '/' + 'vendor_a_eq.txt', )

    
    def detector_name(self):
        return config.FILE_DETECTION
    
    def validator_name(self):
        return config.FILE_VALIDATION
    
    def sorter_name(self):
        return config.FILE_SORT
    
    def create_file_detection_process(self):
        return builder.create_file_detection_process()
    
    def create_file_validation_process(self):
        return builder.create_file_validation_process()
    
    def create_file_sort_process(self):
        return builder.create_file_sort_process()
    
    def create_file_merge_process(self):
        return builder.create_file_merge_process()
    
    def create_input_queue(self):
        return builder.create_queue()
    
    def create_output_queue(self):
        return builder.create_queue()
    
    def create_input_desc(self):
        return builder.create_file_desc()
    
    def create_file_detection_request(self, 
                                      input_desc,
                                      output_desc,
                                      ):
        
        return builder.create_file_detection_request(config.WAIT,
                                                     input_desc,
                                                     output_desc,
                                                     self.wf_dir())
        
    def create_file_validation_request(self, 
                                       input_desc, 
                                       output_desc,
                                       ):
        return builder.create_file_validation_request(
                                                     config.ARRIVED,
                                                     input_desc,
                                                     output_desc,
                                                     self.wf_dir())
        
    def create_file_sort_request(self, 
                                 input_desc, 
                                 output_desc, 
                                 ):
        return builder.create_file_sort_request(
                                                    config.VALIDATED,
                                                    input_desc,
                                                    output_desc,
                                                    self.wf_dir())
    def create_file_merge_request(self, 
                                  input_descs, 
                                  output_desc):
        return builder.create_file_merge_request(
                                                    config.SORTED,
                                                    input_descs,
                                                    output_desc,
                                                    self.wf_dir())
        
    def create_work_flow(self, file_list):
        return builder.create_workflow(config.data_dir, file_list)
        
    
    
    def wf_dir(self):
        return config.data_dir + 'wf/'

class BaseTest(unittest.TestCase):
    """Base unit test class
    Designed to facilitate common unit test patterns
    """
    def __init__(self, name=None):
        super(BaseTest, self).__init__(name)
        self._factory = None

    @property
    def factory(self):
        """Get the factory instance.
        Designed to facilitate data consitency
        with hooks for overriding"""

        if not self._factory:
            self._factory = self.create_factory()
        return self._factory

    def create_factory(self):
        """Hook for derived class to override
        """
        return EquityMasterTestData()


