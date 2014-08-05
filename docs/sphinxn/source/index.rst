.. Router documentation master file

.. Sphinx standard indentations
   # with overline, for parts
   * with overline, for chapters
   =, for sections
   -, for subsections
   ^, for subsubsections
   ", for paragraphs

.. role:: namespace(literal)

##################################
Equity Master  Feed Processing
##################################

Objectives 
----------

- Implement the required functionality 
- Make it easy to review the design and implementation.
- Facilitate the distribution and documentation by using standard 
  Python utilities
- Assemble a skeleton of component whose collaboration can help
  support data feed file validation and transformation
- Show appreciation for the complexity inherant in feed file processing


Clarifications
--------------

- A set of cooperating processes using the underlying threading
  model move files between various stages of the workflow.
- As a file moves from state to state, different directories
 are used to store the file contents.  One of the primary
 objectives was to make it easier to see the file progressing
 through the pipeline

Design considerations

- No single point of failure.  Multiple processes will be
  waiting for file arrival and other workflow stages.
- Capturing of statistics, including messages processed
  in error, capturing invalid records and writing them
  to error files.
- Ability to resart a process at any state
- No assuming that the entire file can be held in memory
  and leveraging heap related sorting and merging 
  techniques
- Not limiting the merging to two files, but extending
  it to N files.
- A facility of describing a file, its fields, using regular
  expression, set of allowed values, min/max width, validation
  against a reference source (i.e. database table), ability to
  leverage yesterday's data if new data has not arrived.

+ 




Known issues
------------

- Unit testing development is not complete.
- Did not get a chance to develop the file
  descriptors and regular expressions for the
  time series files.
- Did not complete the implementation of all
  the regular expressions.
- Did not implement field mapping capability 

Environment used
----------------

- IDE: Eclipse 3.6 (Helios) with PyDev Python support
- Python 2.7.2
- Microsoft Visio

OO Design
---------

- Field Descriptor. Key concept for describing file contents
  and layout.  In order to desctibe a file, one uses a set
  of generic and specialized field descriptors

- File Descriptor.  A collection of field descriptors.

- Process.  An abstraction used to manage the movement
  of files through the work flow.  Each process has
  an input and an output queue.  There are specialized
  processes for sorting, merging, etc


Contents
--------

.. toctree::
    :maxdepth: 5

    reference



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

