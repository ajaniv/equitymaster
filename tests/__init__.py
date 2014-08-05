#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/tests/__init__.py - equity masger  unit test package
#
# Standard copyright message
#
#  
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  


"""
.. module:: equity_master/tests
   :synopsis: equity_master module   unit test package

This package is designed to demonstrate TDD best practices:
- Structured approach to test data creation
- Per module unit test (not achievable due to time constraints)
- Per public and critical private class method, instance method,  and function test cases
- Valid and invalid test suites and test cases
- Object life cycle including creation, configuration, validation
- Structured for expansion as more functionality is to be tested
- Implement unit test first, flushing out interfaces and underlying
   functionality iteratively
- Each module is structured to be easily customized on specific 
  functionality being developed.
- Include functional, performance, and memory utilization test cases

While using the underlying python unit test module, the implementation
would be relatively simple to port to other unit test frameworks.

Each test module is name x_test, where x is the corresponding
module under test.

In order to run all the tests, execute 'python run_tests

The tests can be executed stand alone as well as when using
an IDE such as Eclipse


It is comprised of the following modules:

- common.py - common classes used
- equity_master_tests - higher level process tests
- process tests - process creation
- regexp_tests - regular expression related tests

 

.. moduleauthor:: Amnon Janiv  
"""

__revision__ = '$Id: $'
__version__ = '0.0.1'