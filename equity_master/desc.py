#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# equity_master/desc.py - describes file layout
#
# standard copy right text
#

# Initial version: 2012-04-02
# Author: Amnon Janiv  

"""

.. module:: equity_master/desc
   :synopsis: file composition, format description 



.. moduleauthor:: Amnon Janiv  

"""
__revision__ = '$Id: $'
__version__ = '0.0.1'




from equity_master  import config
from equity_master import common

from equity_master import regexp
class FieldDescriptor(common.BusinessObject): 
    """
    Base class for field description
    This is an area that would require extenstion
    """
    
    def __init__(self, 
                 name,
                 min_length, 
                 max_length,
                 regex=None, 
                 cmp=None, 
                 val=None,
                 mapper=None):
        self.name = name
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex
        self.comparator = cmp
        self.validator = val 
        self.mapper = mapper

         
class FileDescriptor(common.BusinessObject):
    """
    Describes file laoyt
    """
    def __init__(self, firm, file_name, 
                 fields, 
                 field_sep, 
                 alt_names=None,
                 header_lines=0):
        self.firm = firm
        self.file_name = file_name
        self.fields = fields
        self.field_sep = field_sep
        self.trimmer = config.FIELD_TRIM
        self.alt_names = alt_names
        self.header_lines = header_lines
        
        
class CusipFd(FieldDescriptor):
    """ CUSIP is a 9 character identifier used in North America
    It consists of 8 characters plus a checksum digit (http://en.wikipedia.org/wiki/Cusip) 
    """
    min_length = 8
    max_length = 9
    def __init__(self, name):
        super(CusipFd, 
              self).__init__(name, 
                             CusipFd.min_length, 
                             CusipFd.max_length,
                             regex = regexp.CusipRegExp())
        
class IsinFd(FieldDescriptor):
    """ISIN is a 12 character identifier used throughout the world.  
    It consists of 11 characters plus an additional checksum digit
    (http://en.wikipedia.org/wiki/International_Securities_Identifying_Number)
    """
    min_length = 12
    max_length = 12
    def __init__(self, name):
        super(IsinFd, 
              self).__init__(name, 
                             IsinFd.min_length, 
                             IsinFd.max_length,
                             regex = regexp.IsinRegExp())

class SedolFd(FieldDescriptor):
    """SEDOL is a 7 character identifier issued by the London Stock exchange
    It is seven characters in length - the last character is a checksum
    """
    #(http://en.wikipedia.org/wiki/SEDOL)
    min_length = 7
    max_length = 7
    def __init__(self, name):
        super(SedolFd, 
              self).__init__(name, 
                             SedolFd.min_length, 
                             SedolFd.max_length,
                             regex = regexp.SedolRegExp())

class TickerFd(FieldDescriptor):
    """ 
    Stock symbol
    """
    min_length = 2
    max_length = 4
    def __init__(self, name):
        super(TickerFd, 
              self).__init__(name, TickerFd.min_length, TickerFd.max_length )
        
SymbolFd = TickerFd

class CommonNumberFd(FieldDescriptor):
    """Common number is a 9-digit identifier
    """
    min_length = 9
    max_length = 9
    def __init__(self, name):
        super(CommonNumberFd, 
              self).__init__(name, CommonNumberFd.min_length, CommonNumberFd.max_length )
        
class PrimaryExchangeFd(FieldDescriptor):
    """Primary listing exchanges generally follow an ISO standard 
    
    """
    #(http://wikifr.wordpress.com/2007/11/10/iso-10383-codes-for-exchanges-and-market-identification-mic/
    min_length = 3
    max_length = 4
    def __init__(self, name):
        super(PrimaryExchangeFd, 
              self).__init__(name, PrimaryExchangeFd.min_length, PrimaryExchangeFd.max_length )
        
ExchangeFd = PrimaryExchangeFd

  

class CategoryFd(FieldDescriptor):
    """
    Security categorization
    """
    min_length = config.FIELD_CAT_MIN
    max_length = config.FIELD_CAT_MAX  

    def __init__(self, name):
        super(CategoryFd, 
              self).__init__(name, CategoryFd.min_length, CategoryFd.max_length )

SecurityCategoryFd = CategoryFd

class IndustrySectorFd(FieldDescriptor):
    """
    Industry sector classification
    """
    min_length = config.FIELD_CAT_MIN
    max_length = config.FIELD_CAT_MAX  
    def __init__(self, name):
        super(IndustrySectorFd, 
              self).__init__(name, IndustrySectorFd.min_length, IndustrySectorFd.max_length )
SectorFd = IndustrySectorFd
        
class IndustryGroupFd(FieldDescriptor):
    """
    """
    min_length = config.FIELD_CAT_MIN
    max_length = config.FIELD_CAT_MAX   
    def __init__(self, name):
        super(IndustryGroupFd, 
              self).__init__(name, IndustryGroupFd.min_length, IndustryGroupFd.max_length )
GroupFd = IndustryGroupFd

class IndustrySubGroupFd(FieldDescriptor):
    """
    """
    min_length = config.FIELD_CAT_MIN
    max_length = config.FIELD_CAT_MAX  
    def __init__(self, name):
        super(IndustrySubGroupFd, 
              self).__init__(name, IndustrySubGroupFd.min_length, IndustrySubGroupFd.max_length )
SubGroupFd = IndustrySubGroupFd

class CountryCodeFd(FieldDescriptor): 
    """Country codes generally follow an ISO standard (http://en.wikipedia.org/wiki/ISO_3166-1)
    """
    min_length = 2
    max_length = 2
    def __init__(self, name):
        super(CountryCodeFd, 
              self).__init__(name,
                            CountryCodeFd.min_length,
                            CountryCodeFd.max_length )
    

        
        
