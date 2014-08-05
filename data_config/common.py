#/usr/bin/env python
# -#- coding: utf-8 -#-

#
# data_config/common.py
#
# Standard copyright message
#
#  
#

# Initial version: 2012-04-12
# Author: Amnon Janiv  


"""
.. module:: data_config/common
   :synopsis:equity master data configuration common module

 


.. moduleauthor:: Amnon Janiv  
"""
__revision__ = '$Id: $'
__version__ = '0.0.1'

from equity_master import desc

name_sep = '_'
eq_def = 'eq'
eq_ts = 'eqts'
file_suffix= '.txt'



#Equity definition file layout
eq_def_field_desc = (
        desc.CusipFd(name='cusip'),
        desc.IsinFd(name='isin'),
        desc.SedolFd(name='sedol'),
        desc.CommonNumberFd(name='common_number'),
        desc.SymbolFd(name='symbol'),
        desc.CountryCodeFd(name='country'),
        desc.CategoryFd(name='category_primary'),
        desc.PrimaryExchangeFd(name='exchange_primary'),
        desc.IndustrySectorFd(name='industry_sector'),
        desc.IndustryGroupFd(name='industry_group'),
        desc.IndustrySubGroupFd(name='industry_subgroup')
        )

#Equity time series file layout - no work was done on it as of yet
# 
eq_ts_field_desc = (
        
        )