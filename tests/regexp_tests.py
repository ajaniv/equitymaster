#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# parser/test/tests.py - parsing unit test module
#
# standard copy right text
#

# Initial version: 2011-03-08
# Author: Amnon Janiv  

"""

.. module:: tests/regexp_tests
   :synopsis: regex_scripting test suite module

Test suite designed to test regex_scripting features

.. moduleauthor:: Amnon Janiv  

"""
import unittest
import re
 
from tests import  common
from  equity_master  import regexp
 





class TestParsing(common.BaseTest):
    """Test  regex_scripting package  functionality
    """
    
    def __init__(self, name=None):
        super(TestParsing, self).__init__(name)
        
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    @staticmethod
    def get_valid_tests_suite():
        suite = unittest.TestSuite()
        
        return suite
    
    @staticmethod
    def get_invalid_tests_suite():
        suite = unittest.TestSuite()
         
        return suite
    
         
    def displaymatch(self, match):
        if match is None:
            return None
        return '<Match: %r, groups=%r>' % (match.group(), match.groups())
    def test_alpha(self):
        min = 5
        max = 5
        sz = "{{{:d},{:d}}}".format(min,max)
        tmpl = r"^[a-zA-Z]" + sz + "$"
        print tmpl
        exp = re.compile(tmpl)
        #exp = re.compile(r"^[a-zA-Z]{3,5}$")
        
        self.assertTrue(exp)
        matched = exp.match("aAbBc")
        self.assertTrue(matched)
        print self.displaymatch(matched)
    def test_numeric(self):
        min = 5
        max = 5
        sz = "{{{:d},{:d}}}".format(min,max)
        tmpl = r"^[0-9]"+sz+"$"
        exp = re.compile(tmpl)
        self.assertTrue(exp)
        matched = exp.match("12345")
        self.assertTrue(matched)
        print self.displaymatch(matched)
        
        exp = regexp.NumericRegExp(min_width=5, max_width=5)
        
        self.assertTrue(exp.match('12345'))
        
    def test_alpha_numeric(self):
        min = 4
        max = 5
        sz = "{{{:d},{:d}}}".format(min,max)
        tmpl = r"^[a-zA-Z0-9]"+sz+"$"
        exp = re.compile(tmpl)
        self.assertTrue(exp)
        matched = exp.match("12AB")
        self.assertTrue(matched)
        print self.displaymatch(matched)
        
    def test_cusip(self):
        min = 8
        max = 8
        sz = "{{{:d},{:d}}}".format(min,max)
        tmpl = r"^[a-zA-Z0-9*#@]"+sz  #+"$"
        exp = re.compile(tmpl)
        self.assertTrue(exp)
        matched = exp.match("123#@*Abz")
        self.assertTrue(matched)
        print self.displaymatch(matched)
    
    def test_isin(self):
        exp = re.compile('$^')
        self.assertTrue(exp)
    
    def test_sedol(self):
        pass
    
    def test_common_number(self):
        pass
    
    def test_ticker(self):
        pass
    
    def test_counttry(self):
        pass
    
    def test_exchange_primary(self):
        pass

    
def suite():
    parsing_test_suite = unittest.TestSuite([
                                             TestParsing.get_valid_tests_suite(),
                                             TestParsing.get_invalid_tests_suite()])
    
    master_suite =  unittest.TestSuite( [ 
                                             parsing_test_suite,
                                              
                                             ])
         
    return master_suite



if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())


