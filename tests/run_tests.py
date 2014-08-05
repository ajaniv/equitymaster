#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# router/tests/run_tests.py - router package unit test engine
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv

"""

.. module:: tests/run_tests
   :synopsis: equity masger package unit test suite execution module 



.. moduleauthor:: Amnon Janiv  

"""
import unittest

import regexp_tests
import process_tests
import equity_master_tests


def suite():
    """
    Create test suite for the package 
    """
    master_suite = unittest.TestSuite([regexp_tests.suite(),
                                       process_tests.suite(),
                                       equity_master_tests.suite()])
    return master_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
