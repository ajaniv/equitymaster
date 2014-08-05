#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/common.py - equity master  common classes
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  

"""

.. module:: equity_master/common
   :synopsis: miscellaneous abstract classes and other core constructs



.. moduleauthor:: Amnon Janiv  

"""
__revision__ = '$Id: $'
__version__ = '0.0.1'





import sys
import logging



from equity_master import util




class UnicodeMixin(object):

    """Unicode mixin class to help in 
        python 2 to python 3 migration
    """

    if sys.version_info[0] >= 3:  # Python 3

        def __str__(self):
            return self.__unicode__()

    else:
        # Python 2

        def __str__(self):
            return self.__unicode__().encode('utf8')





class ExecutionError(UnicodeMixin, Exception):
    """Execution error class
    """
    def __init__(
        self,
        traceback=None,
        wrapped_ex=None,
        args=None,
        kwargs=None
        ):
        super(ExecutionError, self).__init__(args, kwargs)
        self.traceback = traceback
        self.wrapped_ex = wrapped_ex

    def __unicode__(self):
        return util.pretty_args(*self.args)


class EquityMasterError(ExecutionError):
    """EquityMaster package  error class
    """
    pass


class ClassMixin(object):
    """Class mixin abstraction
    """
    def class_name(self):
        return util.class_name(self)
    

class ErrorMixin(object):
    """Error mixin class 
    """
    
    
    def error(
        self,
        exc_class,
        logger,
        tmpl,
        *args,
        **kwargs
        ):
        """Log and raise an error"""
        util.log_raise(exc_class, logger, logging.ERROR, tmpl, *args, **kwargs)
    
    def fatal(
        self,
        exc_class,
        logger,
        tmpl,
        *args,
        **kwargs):
        """Log and exit"""
        pass
        
class LoggingMixin(object):
    """Log utilities abstraction
    """
    def log(
        self,
        logger,
        severity,
        tmpl,
        *args,
        **kwargs
        ):
        util.log(logger, severity, tmpl, *args, **kwargs)
    
    def debug(
        self,
        logger,
        tmpl,
        *args,
        **kwargs
        ):
        """Log a debug message"""
         
        util.log(logger, logging.DEBUG, tmpl, *args, **kwargs)
        
    def info(self, 
        logger,
        tmpl,
        *args,
        **kwargs):
        util.log(logger, logging.INFO, tmpl, *args, **kwargs)
        
    def warn(self, 
        logger,
        tmpl,
        *args,
        **kwargs):
        util.log(logger, logging.WARNING, tmpl, *args, **kwargs)
        
    def log_error(self,
        logger,
        tmpl,
        *args,
        **kwargs):
        util.log(logger, logging.ERROR, tmpl, *args, **kwargs)

class BusinessObject(UnicodeMixin, ClassMixin, ErrorMixin,
    LoggingMixin, object):
    """Base class business object
    Facilitates creation of complex object graphs with
    reduced development and maintenance costs, flexible,
    yet with rich functionality
    """

    def is_valid(self):
        """Check if object instance is valid
        Demonstrates abstract method construct
        """
        raise NotImplementedError