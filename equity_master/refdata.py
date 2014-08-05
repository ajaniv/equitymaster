#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/file_sort - merge and sort
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  

"""

.. module:: equity_master/refdata
   :synopsis: basic reference data abstractions



.. moduleauthor:: Amnon Janiv  

"""
__revision__ = '$Id: $'
__version__ = '0.0.1'



from equity_master import common

class Refdata(common.BusinessObject):
    pass


class Address(Refdata):
    def __init__(self):
        self.primary = False

class EmailAddress(Address):
    pass

class BusinessAddress(Address):
    pass

class Contact(Refdata):
    def __init__(self):
        self.emails=[]
        self.phones = []

class Firm(Refdata):
    def __init__(self, name):
        self.name = name
        self.contacts = []
        self.bus_address = []
        
class Vendor(Firm):
    pass
        
class RefDataCache(common.BusinessObject):
    def __init__(self):
        self.name = None
        self.values = {}
    