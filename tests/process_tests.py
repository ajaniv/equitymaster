#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# equity_master/tests/process_tests.py - equity master tests
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv

"""

.. module:: router/tests/process_tests
   :synopsis: process life cycle related tests

Utilities and classes for unit testing the process module.

.. moduleauthor:: Amnon Janiv  

"""

import unittest

import common



from equity_master import process
from equity_master import builder




class FileDetectionTest(common.BaseTest):

    """file detection  process cass   test cases
    """

    def __init__(self, name=None):
        super(FileDetectionTest, self).__init__(name)

    @staticmethod
    def get_valid_tests_suite():
        """Define  valid test cases
           
        """

        suite = unittest.TestSuite()
        suite.addTest(FileDetectionTest('test_creation'))
        return suite

    @staticmethod
    def get_invalid_tests_suite():
        """Define  invalid test cases
           
        """

        # @TODO: outstanding work

        suite = unittest.TestSuite()
        return suite

    def test_creation(self):
        """test file detection process  creation
        """
        fac = self.factory
        proc_name = fac.detector_name()
        det_proc1 = process.FileDetection(
                                             fac.create_input_queue(),
                                             fac.create_output_queue(),
                                             name=proc_name)
        
        self.assertTrue(det_proc1, 'FileDetection() is None')
        self.assertTrue(proc_name == det_proc1.getName() )
        self.assertTrue(0 == det_proc1.input_queue.qsize())
        self.assertTrue(0 == det_proc1.output_queue.qsize())
    
        det_proc2 = builder.create_file_detection_process()
        self.assertTrue(proc_name == det_proc2.getName() )
        self.assertTrue(0 == det_proc2.input_queue.qsize())
        self.assertTrue(0 == det_proc2.output_queue.qsize())
        
        
class FileValidationTest(common.BaseTest):

    """FileDetector thread  test cases
    """

    def __init__(self, name=None):
        super(FileValidationTest, self).__init__(name)

    @staticmethod
    def get_valid_tests_suite():
        """Define  valid test cases
           
        """

        suite = unittest.TestSuite()
        suite.addTest(FileValidationTest('test_creation'))
        return suite

    @staticmethod
    def get_invalid_tests_suite():
        """Define  invalid test cases
           
        """

        # @TODO: outstanding work

        suite = unittest.TestSuite()
        return suite

    def test_creation(self):
        """test file validation  process  creation
        """
        fac = self.factory
        proc_name = fac.validator_name()
        val_proc_1 = process.FileValidation(
                                             input_queue = fac.create_input_queue(),
                                             output_queue = fac.create_output_queue(),
                                             name=proc_name)
        
        self.assertTrue(val_proc_1, 'FileValidation() is None')
        self.assertTrue(proc_name == val_proc_1.getName() )
        self.assertTrue(0 == val_proc_1.input_queue.qsize())
        self.assertTrue(0 == val_proc_1.output_queue.qsize())
        
    
        val_proc_2 = builder.create_file_validation_process()
        self.assertTrue(proc_name == val_proc_2.getName() )
        self.assertTrue(0 == val_proc_2.input_queue.qsize())
        self.assertTrue(0 == val_proc_2.output_queue.qsize())


class FileSortTest(common.BaseTest):

    """FileDetector thread  test cases
    """

    def __init__(self, name=None):
        super(FileSortTest, self).__init__(name)

    @staticmethod
    def get_valid_tests_suite():
        """Define  valid test cases
           
        """

        suite = unittest.TestSuite()
        suite.addTest(FileSortTest('test_creation'))
        return suite

    @staticmethod
    def get_invalid_tests_suite():
        """Define  invalid test cases
           
        """

        # @TODO: outstanding work

        suite = unittest.TestSuite()
        return suite

    def test_creation(self):
        """test file validation  process  creation
        """
        fac = self.factory
        proc_name = fac.sorter_name()
        sort_proc_1 = process.FileSort(
                                    input_queue = fac.create_input_queue(),
                                    output_queue = fac.create_output_queue(),
                                    name=proc_name)
        
        self.assertTrue(sort_proc_1, 'FileSort() is None')
        self.assertTrue(proc_name == sort_proc_1.getName() )
        self.assertTrue(0 == sort_proc_1.input_queue.qsize())
        self.assertTrue(0 == sort_proc_1.output_queue.qsize())
        
    
        sort_proc_2 = builder.create_file_sort_process()
        self.assertTrue(proc_name == sort_proc_2.getName() )
        self.assertTrue(0 == sort_proc_2.input_queue.qsize())
        self.assertTrue(0 == sort_proc_2.output_queue.qsize())



def suite():
    """
    Create test suite of thread test cases
    """
    file_detection_test_suite = \
        unittest.TestSuite([FileDetectionTest.get_valid_tests_suite(),
                           FileDetectionTest.get_invalid_tests_suite()])
        
    file_validation_test_suite = \
        unittest.TestSuite([FileValidationTest.get_valid_tests_suite(),
                           FileValidationTest.get_invalid_tests_suite()])
        
    file_sort_test_suite = \
        unittest.TestSuite([FileSortTest.get_valid_tests_suite(),
                           FileSortTest.get_invalid_tests_suite()])
    master_suite = unittest.TestSuite([file_detection_test_suite,
                                       file_validation_test_suite,
                                       file_sort_test_suite
                                       ])

    return master_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
