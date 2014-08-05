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
.. module:: data_config/my_firm
   :synopsis:equity file layout definition for 'us'

 


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

firm = refdata.Firm('my_firm')

#
#Equity definition configuration section
#

eq_def_file_name = 'my_firm_eq.txt'

eq_def_file_desc = desc.FileDescriptor(
                        firm = firm,
                        file_name = eq_def_file_name,
                        fields = common.eq_def_field_desc,
                        field_sep = config.FIELD_SEP,
                        header_lines = 1
                        )
    
#
#Equity time series configuration section
#
eq_ts_file_name = 'my_firm_ts.txt'


eq_ts_file_desc = desc.FileDescriptor(
                        firm = firm,
                        file_name = eq_ts_file_name,
                        fields = common.eq_ts_field_desc,
                        field_sep = config.FIELD_SEP,
                        header_lines = 1)

    
firm_desc = dict(
                     eq_file_desc = eq_def_file_desc,
                     eq_ts_field_desc = eq_ts_file_desc
                     )