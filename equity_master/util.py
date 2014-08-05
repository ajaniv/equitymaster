#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/util.py - equity masger utilities module
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  

"""

.. module:: equity_nasger/util
   :synopsis: router utilities

Miscellaneous constructs facilitate equity masger implementation.

.. moduleauthor:: Amnon Janiv  

"""
from __future__ import with_statement

import sys
import collections
import logging
import string
import time

from contextlib import contextmanager

from equity_master import config

_m_logger = logging.getLogger(__name__)




def whoami():
    """Return called function name"""
    return sys._getframe(1).f_code.co_name

CALLING_FUNC = whoami()



def caller_name():
    """Return calling function name"""
    return sys._getframe(2).f_code.co_name
CALLER_FUNC= caller_name()


def function_name(frame):
    """Return current frames function name"""
    return frame.f_code.co_name

def file_name(frame):
    """Return current frames file name"""
    return frame.f_code.co_filename


def line_no(frame):
    """Return current frames line number"""
    return frame.f_lineno


def where(frame):
    """Return code location information for current frame"""
    return (frame.f_code.co_filename, frame.f_code.co_name,
            frame.f_lineno)


def is_callable(obj):
    """Check if object instance is callable"""
    isinstance(obj, collections.Callable)

def class_name(obj):
    """class name wrapper function"""
    return obj.__class__.__name__


@contextmanager
def file_open(file_name, mode="r"):
    try:
        f = open(file_name, mode)
    except IOError, err:
        _m_logger.error('File open error: %s mode: %s', file_name, mode, exc_info=True)
        yield None, err
    else:
        try:
            _m_logger.debug('Opened file: %s mode: %s', file_name, mode)
            yield f, None
        finally:
            f.close()
            
@contextmanager
def file_readline(file):
    try:
        line = file.readline()
    except IOError, err:
        _m_logger.error('file read error: %s mode: %s', file_name, exc_info=True)
        yield None, err
    else:
        try:
            _m_logger.debug('read line: %s', line)
            yield line, None
        finally:
            file.close()

def pretty_args(*args, **kwargs):
    """prepare a format string"""
    tmpl = string.Template('{$fld_pos:$fld_type}, ')
    fld_fmt = 's'
    fmt_str = ''.join([tmpl.substitute(fld_pos=index, fld_type=fld_fmt)
                      for index in xrange(0, len(args))])

    # trimming extra formating from format string i.e (: ")

    pretty = fmt_str[0:len(fmt_str) - 2].format(*args)

    return pretty

def log_raise(
    ex_class,
    logger,
    severity,
    tmpl,
    *args,
    **kwargs 
    ):
    """Log and raise an exception
    """
    
    (wrapped_exc_cl, wraped_exc, traceback) = sys.exc_info()  # @UnusedVariable
    fmt_msg = tmpl.format(*args, **kwargs)
    logger.log(severity, fmt_msg, exc_info=True)
    
    raise ex_class(traceback, wraped_exc, fmt_msg)

def log(
    logger,
    severity,
    tmpl,
    *args,
    **kwargs 
    ):
    """Log a message
    """
    fmt_msg = tmpl.format(*args, **kwargs)
    logger.log(severity, fmt_msg)
    


def file_time_suffix():
    return time.strftime(config.file_time_format)




