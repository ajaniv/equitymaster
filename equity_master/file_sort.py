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

.. module:: equity_master/file_sort
   :synopsis: file sorting and merging using heapqu.  The file
   does not need to be in memory



.. moduleauthor:: Amnon Janiv  

"""
__revision__ = '$Id: $'
__version__ = '0.0.1'



# based on Recipe 466302: Sorting big files the Python 2.4 way
# by Nicolas Lehuen

import os
from tempfile import gettempdir
from itertools import islice, cycle
from collections import namedtuple
import heapq
from equity_master import config

Keyed = namedtuple("Keyed", ["key", "obj"])


def merge(key, skip, *iterables):
    """
    Merge n number of iterables that are sorted, using the key
    if defined, and skipping header records if and when required
    """
    # based on code posted by Scott David Daniels in c.l.p.
    # http://groups.google.com/group/comp.lang.python/msg/484f01f1ea3c832d

    skipped = [iterable.next() for i in xrange(skip) #@UnusedVariable
               for iterable in iterables] 
    if key is None:
        keyed_iterables = iterables
    else:
        keyed_iterables = [(Keyed(key(obj), obj) for obj in iterable)
                            for iterable in iterables]
   
    for element in heapq.merge(*keyed_iterables):
        if key:
            yield element.obj
        else:
            yield element
            
            
def keyed_merge(key=None, *iterables):
    """
    This function prepends a unique object id to a record
    """
    # based on code posted by Scott David Daniels in c.l.p.
    # http://groups.google.com/group/comp.lang.python/msg/484f01f1ea3c832d


    if key is None:
        keyed_iterables = iterables
    else:
        keyed_iterables = [(Keyed(key(obj), obj) for obj in iterable)
                            for iterable in iterables]
    tmpl = '{:d}' + config.FIELD_SEP + '{:s}'
    for index, element in enumerate (heapq.merge(*keyed_iterables)):
        if key:
            yield tmpl.format(index, element.obj)
        else:
            yield tmpl.format(index,element)


def sort(  input_file_name, 
           output_file_name, 
           key=None, 
           buffer_size=32000, 
           tempdirs=None,
           skip=0):
    """
    Sort a file in chunks
    """
    if tempdirs is None:
        tempdirs = []
    if not tempdirs:
        tempdirs.append(gettempdir())

    
    chunks = []
    try:
        with open(input_file_name,'rb',64*1024) as input_file:
            input_iterator = iter(input_file)
            #Capture lines that are skipped 
            skipped = [input_iterator.next() for i in xrange(skip)] #@UnusedVariable
         

            
            for tempdir in cycle(tempdirs):
                current_chunk = list(islice(input_iterator,buffer_size))
                if not current_chunk:
                    break
                current_chunk.sort(key=key)
                output_chunk = open(os.path.join(tempdir,'%06i'%len(chunks)),'w+b',64*1024)
                chunks.append(output_chunk)
                output_chunk.writelines(current_chunk)
                output_chunk.flush()
                output_chunk.seek(0)
        with open(output_file_name,'wb',64*1024) as output_file:
            if skipped:
                output_file.writelines(skipped)
            output_file.writelines(merge(key, 0, *chunks))
    finally:
        for chunk in chunks:
            try:
                chunk.close()
                os.remove(chunk.name)
            except Exception:
                pass

