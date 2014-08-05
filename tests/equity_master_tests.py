#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# router/tests/calc_tests.py - router journey calculator tests
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv

"""

.. module:: tests/equity_master_tests
   :synopsis: process level related tests



.. moduleauthor:: Amnon Janiv  

"""

import unittest

import common as tests_common

from equity_master import config

from equity_master import model
#from equity_master import builder


from equity_master import file_sort

from data_config import  vendor_a
from data_config import  vendor_b
from data_config import  my_firm



class ProcessTest(tests_common.BaseTest):

    """Process test cases
    """

    def __init__(self, name=None):
        super(ProcessTest, self).__init__(name)

    @staticmethod
    def get_valid_tests_suite():
        """Define  valid test cases
           
        """

        suite = unittest.TestSuite()
        #suite.addTest(ProcessTest('test_workflow_creation'))
        suite.addTest(ProcessTest('test_file_arrival'))
        suite.addTest(ProcessTest('test_file_validation'))
        suite.addTest(ProcessTest('test_file_sort'))
        suite.addTest(ProcessTest('test_merge_algo'))
        suite.addTest(ProcessTest('test_file_merge'))
        return suite

    @staticmethod
    def get_invalid_tests_suite():
        """Define  invalid test cases
           
        """

        # @TODO: outstanding work

        suite = unittest.TestSuite()
        return suite

    def test_workflow_creation(self):
        """test process environment creation
        """
        file_list = config.data_files()
        work_flow = self.factory.create_work_flow(file_list)
        self.assertTrue(work_flow)
        
    def test_file_arrival(self):
        """test file detection process
        """
        fac = self.factory
        detector = fac.create_file_detection_process()
        self.assertTrue(detector, 'create_detector is None')
        detector.start()
        
        file_descs = (vendor_a.in_eq_def_file_desc,
                       vendor_b.in_eq_def_file_desc)
        for file_desc in (file_descs) :
            request = fac.create_file_detection_request(file_desc, file_desc)
            self.assertTrue(request)
            detector.send(request)
            
        detector.shutdown()
       
            
        detector.join()
        
        self.assertTrue(len(file_descs) == detector.output_queue.qsize())
        
        for index in xrange(len(file_descs)): #@UnusedVariable
            results = detector.receive()
            self.assertFalse(results.error)
            self.assertTrue(results.priority == model.Request.Priority.DEFAULT)
            #@TODO: compare vs. original request
            self.assertTrue(results.request)
            self.assertTrue(results.response)
            self.assertTrue(config.ARRIVED == results.response.file_state)
    

    def test_file_validation(self):
        """test file validation process 
        """
        fac = self.factory
        input_file_descs = (vendor_a.in_eq_def_file_desc,
                            vendor_b.in_eq_def_file_desc)
        output_file_descs = (vendor_a.out_eq_def_file_desc,
                             vendor_b.out_eq_def_file_desc)
        validator = fac.create_file_validation_process()

        self.assertTrue(validator, 'create_validation is None')
        validator.start()
        
        for input_desc, output_desc  in zip(input_file_descs, output_file_descs):
            request = fac.create_file_validation_request(input_desc, output_desc)
            self.assertTrue(request)
            validator.send(request)


        
        
        validator.shutdown()
            
        validator.join()
        
        
        self.assertTrue(len(input_file_descs) == validator.output_queue.qsize())
        
        for index in xrange(len(input_file_descs)): #@UnusedVariable
            results = validator.receive()
            self.assertFalse(results.error)
            self.assertTrue(results.priority == model.Request.Priority.DEFAULT)
            #@TODO: compare vs. original request
            self.assertTrue(results.request)
            self.assertTrue(results.response)
            self.assertTrue(config.VALIDATED == results.response.file_state)
    
    def test_file_sort(self):
        """test file sort process 
        """  
        
        fac = self.factory
        input_file_descs = (vendor_a.out_eq_def_file_desc,
                            vendor_b.out_eq_def_file_desc,)
        output_file_descs = (my_firm.eq_def_file_desc,
                             my_firm.eq_def_file_desc)
        
        sorter = fac.create_file_sort_process()

        self.assertTrue(sorter, 'create file sorter  is None')
        
        sorter.start()
        
        for input_desc, output_desc  in zip(input_file_descs, 
                                                             output_file_descs
                                                             ):
            request = fac.create_file_sort_request(input_desc, 
                                                   output_desc, 
            
                                                   )
            self.assertTrue(request)
            sorter.send(request)
            

        
        sorter.shutdown()
            
        sorter.join()

    def test_file_merge(self):
        """test file merge process 
        """
        fac = self.factory
        input_file_descs = (vendor_a.out_eq_def_file_desc,
                            vendor_b.out_eq_def_file_desc)
        
                             
        merger = fac.create_file_merge_process()

        self.assertTrue(merger, 'create merger is None')
        merger.start()
        
        
        request = fac.create_file_merge_request(input_file_descs, 
                                                     my_firm.eq_def_file_desc)
        self.assertTrue(request)
        merger.send(request)


        
        
        merger.shutdown()
            
        merger.join()
        
        
        self.assertTrue(1 == merger.output_queue.qsize())
        
        for index in xrange(len(input_file_descs)): #@UnusedVariable
            results = merger.receive()
            self.assertFalse(results.error)
            self.assertTrue(results.priority == model.Request.Priority.DEFAULT)
            #@TODO: compare vs. original request
            self.assertTrue(results.request)
            self.assertTrue(results.response)
            self.assertTrue(config.MERGED == results.response.file_state)
            
    def test_merge_algo(self):
        #simple case: keys are equal, need to do merge of fields
        s_1_r_1 = [1, 'a']
        s_1_r_2 = [1, 'f']
       
        s_2_r_1 = [1, 'b']
        s_2_r_2 = [2, 'e']
        
        s_3_r_1 = [1, 'a']
        s_3_r_2 = [2, 'b']
        s_3_r_3 = [3, 'b'] #dup in file
         
        
        file_1 = [s_1_r_1, s_1_r_2]
        file_2 = [s_2_r_1, s_2_r_2]
        file_3 = [s_3_r_1, s_3_r_2, s_3_r_3]
        
        file_1.sort()
        file_2.sort()

        key = lambda x : x[1] 
        merged = do_write(key, file_sort.merge(key, 0, file_1, file_2, file_3))
        self.assertTrue(4 == len(merged))
        self.assertTrue(merged[1][0] == 'b')
        self.assertTrue(merged[3][0] == 'f')
        
        
      
def do_write(key, a_list):
    cleaned=[] 
    last = []
    for record in a_list:
        if last:
            current_key = key(record)
            if current_key != key(last[0]):
                #do the record merge
                new_rec = merge_fields(last)
                last = []
                cleaned.append(new_rec)
        
        last.append(record)
    if last:
        new_rec = merge_fields(last)
        cleaned.append(new_rec)
    return cleaned

def merge_fields(a_list):
    new_rec =[]
    stub=9
    for field_id, field_desc in zip((1,),(2,)):
        new_value = stub
        for record in a_list:
            #get current value
            value = record[field_id]
            if value == stub:
                continue
            elif new_value == stub:
                new_value = value    
            elif new_value == value:
                continue
            else:
                #there is a diff in field values
                #log an error, write all records to error file
                pass
        if new_value == stub:
            #log a warning
            pass
        new_rec.append(new_value)
        
    return new_rec
        
#        iter_n = [iter(file) for file in (file_1, file_2)]
#        keys_n = []
#        while True:
#            iter_n, keys_n = do_next(iter_n, keys_n)
#            if keys_n:
#                pass
#            else:
#                break

#def do_next(iter, recs):
#    keys = []
#    for iter, rec in zip(iter, recs):
#        if key:
#            my_list.append(key)
#        else:
#            my_list.append(iter.next)
#            
#def merge_next(recs):
#    keys = [rec[0] for rec in recs]
#    keys.sort()
#    for index, key in enumerate(keys):
#        if keys[index] == keys[index+1]:
#            new_rec = merge_recs(recs[index], recs[index+1])
#            return merge_next([new_rec].extend(recs[index+2:]))
#        break
#    return merged_rec
def merge_recs(rec1,rec2):
    pass
def suite():
    """
    Create test suite of thread test cases
    """
    trip_calc_test_suite = \
        unittest.TestSuite([ProcessTest.get_valid_tests_suite(),
                           ProcessTest.get_invalid_tests_suite()])
    master_suite = unittest.TestSuite([trip_calc_test_suite])

    return master_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
