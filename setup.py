#!/usr/bin/env python

from distutils.core import setup

setup(name='Equity Master',
      version='1.0',
      description='Equity master data consolidation',
      license="Not for distribution",
      author='Amnon Janiv',
      author_email='amnon.janiv@ondalear.com',
      url='http://www.ondalear.com',
      package_dir = { 'equity_master': 'equity_master' },
      packages=['equity_master'],
     )