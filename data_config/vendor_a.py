#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# data_config/my_firmt.py
#
# Standard copyright message
#
#  
#

# Initial version: 2012-04-12
# Author: Amnon Janiv  


"""
.. module:: data_config/vendor_a
   :synopsis:equity file layout definition for vendor_a

 


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
firm = refdata.Firm('vendor_a')

#
#Equity definition input file  configuration section
#

in_eq_def_field_desc = (
        desc.CusipFd('cusip'),
        desc.IsinFd('isin'),
        desc.SedolFd('sedol'),
        desc.TickerFd('ticker'),
        desc.CategoryFd('category'),
        desc.PrimaryExchangeFd('primary_exchange'),
        desc.IndustrySectorFd('industry_sector'),
        desc.IndustryGroupFd('industry_group'),
        desc.IndustrySubGroupFd('industry_subgroup')
        )

in_eq_def_file_desc = desc.FileDescriptor(
                        firm = firm,
                        file_name = 'vendor_a_eq.txt',
                        fields = in_eq_def_field_desc,
                        field_sep = ',',
                        alt_names = {'ticker' : 'symbol',
                                     'category' : 'category_primary',
                                     'primary_exchange' : 'exchange_primary',
                                     
                                     },
                        header_lines = 1)
                                     
out_eq_def_file_desc = desc.FileDescriptor(
                        firm = firm,
                        file_name = 'vendor_a_eq.txt',
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
                        file_name = 'vendor_a_ts.txt',
                        fields = eq_ts_field_desc,
                        field_sep = config.FIELD_SEP,
                        header_lines = 1)

