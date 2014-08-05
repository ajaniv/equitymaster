#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity masger/regexp.py - regular expressions
#
# standard copy right text
#

# Initial version: 2011-03-08
# Author: Amnon Janiv  

"""

.. module:: equity_master/regex
   :synopsis: regex related constructs

Miscellaneous regular expression utilities

.. moduleauthor:: Amnon Janiv  

"""
import re
import sys
import logging
from equity_master import common
from equity_master import util


_m_logger = logging.getLogger(__name__)

def formatted_match(self, match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())

class RegExp(common.ErrorMixin, object):
    """
    Base class construct designed to integrate with the meta
    data/description of files
    """
    def __init__(self,
                binary=None, 
                min_width=None,
                max_width=None):
        self.binary = binary
        self.min_width = None
        self.max_width = None
    def compile(self):
        """
        Compile a regular expression
        """
        if not self.binary:
            code = self.source()
            if self.source:
                try:
                    self.binary = re.compile(code)
                except Exception as ex: #@UnusedVariable
                    self.error(common.EquityMasterError, 
                   _m_logger,
                   'invalid regular expression {:s}', code)
            else:
                self.error(common.EquityMasterError, 
                   _m_logger,
                   'empty regular expression',
                   )
        return self.binary
    
    def match(self, input_str):
        """
        Perform the matching
        """
        reg_exp = self.compile()
        return reg_exp.match(input_str)
    
    def source(self):
        """
        Abstraction for derived classes to override
        and return the formatted string
        """
        self.error(NotImplementedError,
                   _m_logger,
                   'Exception details ({:s})',
                   util.where(sys._getframe())
                   )
        
    def format(self, value):
        me = self.match(value)
        if me:
            return me.group()
        return None
       

class NumericRegExp(RegExp):
    """
    Numeric reg exp
    """
    def __init__(self, min_width=None, max_width=None):
        super(NumericRegExp, 
              self).__init__(
                min_width=min_width,
                max_width=max_width)
              
    def source(self):
        code = r"^[0-9]"
        if self.min_width and self.max_width:
            sz = "{{{:d},{:d}}}".format(self.min_width,
                                    self.max_width)
            code = code + sz + "$"
        return code

class AlphaRegExp(RegExp):
    """
    Alpha regexp
    """
    template = r"^[a-zAZ]"
    def __init__(self, min_width=None, max_width=None):
        super(AlphaRegExp, 
              self).__init__(
                min_width=min_width,
                max_width=max_width)
              
    def source(self):
        code = r"^[0-9]"
        if self.min_width and self.max_width:
            sz = "{{{:d},{:d}}}".format(self.min_width,
                                    self.max_width)
            code = code + sz + "$"
        return code

class AlphaNumericRegExp(RegExp):
    """
    Alphanumerc
    """
    template = r"^[]"
    def __init__(self, min_width=None, max_width=None):
        super(AlphaNumericRegExp, 
              self).__init__(tmpl=AlphaRegExp.template, 
                min_width=min_width,
                max_width=max_width)
              
    def source(self):
        code = r"^[a-zAZ0-9]"
        if self.min_width and self.max_width:
            sz = "{{{:d},{:d}}}".format(self.min_width,
                                    self.max_width)
            code = code + sz + "$"
        return code


class CusipRegExp(RegExp):
    """
    Cusip reg exp, ignores the check digint
    """
    def __init__(self):
        super(CusipRegExp, 
              self).__init__()
    def source(self):
        return r"^[a-zA-Z0-9*#@]{8}"
    
class IsinRegExp(RegExp):
    """
    Isign reg exp
    """
    def __init__(self):
        super(IsinRegExp, 
              self).__init__()
    def source(self):
        return r"^[A-Z]{2}[a-zA-Z0-9]{9}"
              
class SedolRegExp(RegExp):
    """
    Sedol regexp
    """
    def __init__(self):
        super(SedolRegExp, 
              self).__init__()
    def source(self):
        return  r"^[a-zA-Z0-9]{6}"