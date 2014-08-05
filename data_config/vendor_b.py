#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# data_config/vendor_b.py
#
# Standard copyright message
#
#  
#

# Initial version: 2012-04-12
# Author: Amnon Janiv  


"""
.. module:: data_config/vendor_b
   :synopsis:equity file layout definition for vendor_b

 


.. moduleauthor:: Amnon Janiv  
"""
__revision__ = '$Id: $'
__version__ = '0.0.1'



from equity_master import desc
from equity_master import refdata
from equity_master import config

from data_config import common

#
#Basic configuration section
#

firm = refdata.Firm('vendor_b')

#
#Equity definition configuration section
#

in_eq_def_field_desc = (
        desc.CusipFd('cusip'),
        desc.IsinFd('isin'),
        desc.CommonNumberFd('common_number'),
        desc.SymbolFd('symbol'),
        desc.CountryCodeFd('country'),
        desc.CategoryFd('security_category'),
        desc.PrimaryExchangeFd('exchange'),
        desc.IndustrySectorFd('sector'),
        desc.IndustryGroupFd('group'),
        desc.IndustrySubGroupFd('subgroup')
        )
in_eq_def_file_desc = desc.FileDescriptor(
                        firm = firm,
                        file_name = 'vendor_b_eq.txt',
                        fields = in_eq_def_field_desc,
                        field_sep = '|',
                        alt_names = {
                                     'security_category' : 'category_primary',
                                     'exchange' : 'exchange_primary',
                                     'sector' : 'industry_sector',
                                     'group' : 'industry_group',
                                     'subgroup' : 'industry_subgroup'
                                     },
                        header_lines = 1)

out_eq_def_file_desc = desc.FileDescriptor(
                        firm = firm,
                        file_name = 'vendor_b_eq.txt',
                        fields = common.eq_def_field_desc,
                        field_sep = config.FIELD_SEP,
                        header_lines = 1)                   
    


#
#Equity time series configuration section
#

eq_ts_field_desc = (
         
        )

eq_ts_file_desc = desc.FileDescriptor(
                        firm = firm,
                        file_name = 'vendor_b_ts.txt',
                        fields = eq_ts_field_desc,
                        field_sep =  '|',
                        header_lines = 1)

    
