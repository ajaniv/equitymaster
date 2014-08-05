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

.. module:: equity_master/process
   :synopsis: process functionality including scheduling, queuing of messages



.. moduleauthor:: Amnon Janiv  

"""
__revision__ = '$Id: $'
__version__ = '0.0.1'






import sys
import shutil
import threading
import logging



from equity_master import config
from equity_master import common
from equity_master import util
from equity_master import model
from equity_master import  file_sort


_m_logger = logging.getLogger(__name__)

class ProcessResults(object):
    """
    Class to capture process execution results
    """
    def __init__(self, 
                  priority=None, 
                  request=None, 
                  response=None, 
                  error=None):
        self.priority = priority
        self.request = request
        self.response = response
        self.error = error

class FileMixin(object):
    """
    Process related file operations
    
    """
    def files_open(self, mode, *names):
        """
        Open a set of files for read, write, or append
        """
        files = [self.file_open(name, mode) for name in names]
        return tuple(files)
    
    def file_open(self, name, mode):
        """
        Open a single file.  Intention is to provde detailed
        file state information, loggined
        """
        return open(name, mode)
    
    def files_close(self, *files):
        """
        Cloase a set of files
        """
        rv = [file.close() for file in files]
        return tuple(rv)
    
                
    def file_read_n_split(self, file, record_sep, trim_tmpl):
        """Read a record, trim it, and split, return also record read
        """
        #validation: check existence of header record
      
        record = file.readline()
        if record:
            return self.split_n_trim(record, 
                                     record_sep, 
                                     trim_tmpl)
        return (None, None)
           
    
    def split_n_trim(self, record, record_sep, trim_tmpl):
        """
        Split and trim a record
        """
        #validation: strip white space from beginning and end
        data_fields = record.split(record_sep)
        data_fields = [field_value.strip(trim_tmpl)
                            for field_value in data_fields]
        return data_fields, record
    
    def validate_state(self, file_name, state, expected_state):
        """
        Validate a process state related to a file vs what is
        expected
        """
        if state != expected_state:
            util.log_raise(common.EquityMasterError, 
                       _m_logger,
                       logging.ERROR,
                       'Invalid file {:s} process state: {:d} expected {:d}', 
                       file_name, 
                       state, 
                       expected_state)
            
    def validate_header(self, file, file_desc):
        """
        Validate a header record
        """
        msg = None
        #validation: existence  of header record
        header, record  = self.file_read_n_split(file, #@UnusedVariable
                                  file_desc.field_sep, 
                                  file_desc.trimmer)
        #
        # Note: the validation below is more detailed
        # than absolutely required, list comparison would work up-front
        # Hooks are in place for detailed error reporting
        #
        if header:
            header_len = len(header)
            desc_len = len(file_desc.fields)
            #validation: compare size of header record
            if header_len == desc_len:
                #validation: compare naming of each field and field order
                field_desc_names = [fd.name for fd  in file_desc.fields]
                if field_desc_names == header:
                    self.info (_m_logger, 'header validation for ({:s}) passed', file.name)
                    return header
                else:
                    tmpl = 'header record mismatch expected({:s}) received({:s})'
                    msg = tmpl.format(','.join(field_desc_names), ','.join(header))
                 
            else:
                tmpl = 'field mismatch, expected ({:d})  received ({:d)}'
                msg = tmpl.format(desc_len, header_len, )
        else:
            msg = 'cannot read header record'
        
        util.log_raise(common.EquityMasterError,
                            _m_logger,
                            logging.ERROR,
                            'invalid file header: {:s} {:s}',
                            file.name, 
                            msg)
    
    def write_raw(self, file, record):
        """
        Encapsulate law level file operation - my be required
        for detailed logging, exception handling
        """
        file.write(record)
        
    def read_raw(self, file):
        
        return file.readline()
    
    def write_error(self, file_name, record):
        """
        Write an error record
        """
        try:
            with open( file_name, 'a' ) as err_file :
                self.write_raw(err_file, record)
        except IOError: 
            self.error(common.EquityMasterError,
                            _m_logger,
                            'invalid record write to error file {:s} failed',
                            file_name
                            )
    
    def write_header(self, file, file_desc):
        """
        Write a header record
        """
        field_names = [fd.name for fd in file_desc.fields]
        self.write_record(file, file_desc, field_names)
        
    def write_mapped_record(self,
                            file, 
                            output_file_desc, 
                            data_fields,
                            input_file_desc):
        """
        Map input record format with target record format
        """
        #step 1: extract input file headers
        header_1 = [fd.name for fd in input_file_desc.fields]
        
        #step 2: map input file headers to target file headers
        header_2 = [ input_file_desc.alt_names.get(name,name) for name in header_1]
        
        #step 3: create dictionary of  output data with output file headers
        out_1 = dict(zip(header_2, data_fields))
        
        #step 4: create output record with filler 
        out_2 = [out_1.get(fd.name, config.FIELD_FILLER) for fd in output_file_desc.fields]
         
        #step 5: write formatted output
        self.write_record(file, output_file_desc, out_2)
        
       
    def write_record(self, file, file_desc, fields):
        """Write formatted output"""
        record = file_desc.field_sep.join(fields) + '\n'
        self.write_raw(file, record)
      
   

            
class BaseProcess(FileMixin, 
                  common.ErrorMixin, 
                  common.LoggingMixin, 
                  threading.Thread):
    def __init__(self, 
                 input_queue=None, 
                 output_queue=None,
                 group=None, 
                 name=None, 
                 state_id=None,
                 args=(), kwargs=None, verbose=None ):
        """
        Base class abstraction for file related processes
        """
        super(BaseProcess,self).__init__(group=group,  name=name,
                  args=args, kwargs=kwargs, verbose=verbose)
        
        
        if not input_queue and kwargs:
            self.input_queue = kwargs.get('input_queue')
        else:
            self.input_queue = input_queue
            
        
        if not output_queue and kwargs:
            self.output_queue = kwargs.get('output_queue')
        else:
            self.output_queue = output_queue    
            
        
        if not state_id and kwargs:
            self.state_id = kwargs.get('state_id')
        else:
            self.state_id = state_id
        self.should_exit = False
    
    def send(self, request, priority=model.FileRequest.default_priority):
        """
        Send a request to a process for file processing, shutdown, etc
        
        """
        prioritized_req = (priority,request)
        self.input_queue.put(prioritized_req)
        
    def receive(self):
        """
        Receive a message from process
        """
        res = ProcessResults()
        res.priority, res.request, res.response,  res.error = \
            self.output_queue.get()
        return res
       
    def begin_work(self):
        """
        Utilitiy for process management
        """
        self.info(_m_logger, 'Process begin')
        
    def end_work(self):
        """
        Utilitiy for process management
        """
        self.info(_m_logger, 'Process end')
    
    def log_begin(self, request):
        """
        Utilitiy for process management
        """
        self.debug(
                   _m_logger, 
                  'Request details input({:s}) output({:s}) error({:s}) state({:s})',
                  request.input_file_names[0],
                  request.output_file_names[0],
                  request.error_file_names[0],
                  model.process_state(request.input_file_state).name
                  )
        
    def log_end(self, response):
        pass
    
    def report_stats(self, in_file_name, out_file_name, valid, invalid):
        """
        Report exection statistics
        """
        tmpl = 'file validation for in ({:s}) out ({:s}) valid({:d}) invalid({:d}) '
        if not valid:
            severity = logging.ERROR
            tmpl += ' failed'
        elif invalid:
            severity = logging.WARNING
            tmpl += ' completed with errors'
        else:
            severity = logging.INFO
            tmpl += ' completed'
            
        self.log(_m_logger,
                 severity,
                 tmpl,
                 in_file_name,
                 out_file_name,
                 valid,
                 invalid)
    
    def shutdown(self):
        """
        Stop the process
        """
        self.send(
                  model.SystemRequest(model.SystemRequest.RequestType.SHUTDOWN ),
                  model.Request.Priority.LOW)
    def run(self):
        """
        Main driver for process execution
        Handles exceptions, their logging, dispatching of requests
        """
        self.begin_work()
        while not self.should_exit:
            results = ()
            request = None
            try:
                priority, request = self.input_queue.get() #@UnusedVariable
                if request.is_system():
                    break
                self.validate_request(request)
                self.log_begin(request)
                response = self.handle(request)
                self.log_end(response)
                results = (model.Request.Priority.DEFAULT, request, response, None)
            except common.EquityMasterError as error_app:
                results = (model.Request.Priority.HIGH, 
                           request, 
                           None, 
                           error_app)
                self.log_error(_m_logger, 
                               'application error {:s} ', 
                               error_app)
            except Exception as  error_system:
                self.log_error(_m_logger, 
                               'system error {:s} ', 
                               error_system)
                results = (model.Request.Priority.HIGH,
                            request,
                            None,
                            error_system)
            self.output_queue.put(results)
        self.end_work()
        
    def handle(self, req):
        """
        Process specific entry point
        """
        self.error(NotImplementedError,
                   _m_logger,
                   'Exception details ({:s})',
                   util.where(sys._getframe())
                   )
        
    def required_state(self):
        """
        Process expected state
        """
        return self.state_id

    
    def validate_state(self, request):
        """
        Verify that the process is in the right state
        """
        in_state = request.input_file_state
        required_state = self.required_state()
        if  required_state != in_state:
            self.error(common.EquityMasterError, 
                       _m_logger,
                       'Invalid file {:s} process state: {:s} expected {:s}', 
                       request.input_file_names[0], 
                       model.process_state(in_state).name, 
                       model.process_state(required_state).name, 
                       )
            
    def validate_request(self, request):
        """
        High level validaiton function
        """
        self.validate_state(request)
             
class FileDetection(BaseProcess):
    """Class that detects availability of feed files.
    """
    
    
    def handle(self, request):
        """ Detect required files, initialize per-file process
        Typical process would include:
            
            - Verify that file exists and can be opened
             
        """
        
        return self.detect(
                             request.input_file_names[0],
                             request.input_file_desc,
                             request.input_file_state,
                             request.output_file_names[0],
                             request.output_file_desc,
                             request.error_file_names[0])
        
    def detect(self, 
               input_file_name, 
               input_file_desc,
               input_file_state, 
               output_file_name,
               output_file_desc,
               error_file_name
               ):
        """
        Main function for detecting file arrival
        """
        try:
            in_file = self.file_open(input_file_name, 'r' ) 
            out_file = self.file_open(output_file_name, 'w')
            shutil.copyfileobj(in_file, out_file)
            self.info (_m_logger, 'file detection for ({:s}) passed', input_file_name)
            return model.FileResponse(output_file_name, 
                                  config.ARRIVED)
        except IOError:
            self.error(common.EquityMasterError,
                            _m_logger,
                            'file processing error: {:s} {:s}',
                            input_file_name, 
                            output_file_name,
                            error_file_name)
        finally:
            self.files_close(in_file, out_file)
           
        

class FileValidation(BaseProcess):
    """Class that validates feed files.
    """
    
    
    
    def handle(self, request):
        """ Validate file
        Typical process would include:
        
            - Abort if:
                * The file is not empty
                * The file does not  conform to the formatting rules
                  defined in the file descriptor and which are defined
                  in the first line of the file.
            
            - For each line in the file:
                   * validate each field per the formatting rules
                   * validate each field contents using reference data repository
                   * upon detection of an error, log error, skip the line
            - Generate statistics
           
        """
        return self.validate(
                             request.input_file_names[0],
                             request.input_file_desc,
                             request.input_file_state,
                             request.output_file_names[0],
                             request.output_file_desc,
                             request.error_file_names[0])
            
            
 
    def validate(self, 
                      input_file_name, 
                      input_file_desc,
                      input_file_state, 
                      output_file_name,
                      output_file_desc,
                      error_file_name):
        """file validation main driver 
        """
        
        
        
        try:
            #open required files files
            in_file = self.file_open(input_file_name, 'r') 
            out_file = self.file_open(output_file_name, 'w')
            
            #validate header line vs file descriptor
            header = self.validate_header(in_file, 
                                          input_file_desc)
            #validate each line 
            valid, invalid = self.validate_records(in_file, 
                                  input_file_desc,
                                  header, 
                                  out_file,
                                  output_file_desc,
                                  error_file_name)
            #generate statistics
            self.report_stats(in_file.name, out_file.name, valid, invalid)
            
            return model.FileResponse(output_file_name, 
                                  config.VALIDATED)
        except IOError:
            self.error(common.EquityMasterError,
                            _m_logger,
                            'file processing error: {:s} {:s}',
                            input_file_name, 
                            output_file_name
                            )
        finally:
            self.files_close(in_file, out_file)

    
    def validate_records(self, 
                         in_file, 
                         input_file_desc,
                         header, 
                         out_file,
                         output_file_desc,
                         error_file_name):
        """
        Record level validation driver
        """
        valid = 0
        invalid = 0    
         
        self.write_header(out_file, output_file_desc)  
        
        
             
        while True:
            data_fields, record = self.file_read_n_split(in_file,
                                        input_file_desc.field_sep,
                                        input_file_desc.trimmer) 
            #@TODO: change implementation 
            if not data_fields:
                break
            if self.validate_record(data_fields,
                                 input_file_desc.fields) == 0:
                self.write_mapped_record(out_file,
                                  output_file_desc,
                                  data_fields,
                                  input_file_desc)
                valid += 1
            else:
                self.write_error(error_file_name, record)
                invalid += 1
        
        return valid, invalid
                
            
    def validate_record(self, data_fields, field_descs):
        """"Hook is in place for record  level validaiton
        across multiple feeds"""
        errors = 0
        for index, field_value, field_desc in zip(
                                                  xrange(len(data_fields)),
                                                  data_fields, 
                                                  field_descs):
            new_value = self.validate_field(field_value, field_desc)
            if new_value:
                data_fields[index] = new_value
            else:
                errors += 1
        return errors
            
        
 
    
    def validate_field(self, field_value, field_desc):
        """
        Validate a single field given a value and its
        descriptor
        """
        #validation: validate field length
        field_len = len(field_value)
        if (field_len >=  field_desc.min_length 
            and  field_len <= field_desc.max_length):
            #validation: validate field format - reg exp
            if field_desc.regex:
                new_value = field_desc.regex.format(field_value)
                if new_value:
                    return new_value
            else:
                new_value = field_value
                return new_value
           
            #validation: validate field contents - cross check against ref data
        tmpl = 'invalid field ({:s}) value ({:s}) '
        tmpl += 'expected min/max length ({:d}/{:d}) actual length ({:d})'
        self.log_error(
                 _m_logger,
                 tmpl,
                 field_desc.name,
                 field_value,
                 field_desc.min_length,
                 field_desc.max_length,
                 field_len
                    )
        return None

  

class FileSort(BaseProcess):
    """Class that sorts validated files.
    """
    def handle(self, request):
        """ sort the file
        Typical process would include:
            - Sort
            - Generate statistics
           
        """
        
      
        return self.sort(
                             request.input_file_names[0],
                             request.input_file_desc,
                             request.output_file_names[0]
                             )
            
            
 
    def sort(self, 
                      input_file_name, 
                      input_file_desc,
                      output_file_name,
                      ):
        """file sort "
        """
        
         
         
        try:
             
            
             
            #sort the file
             
            file_sort.sort(input_file_name, 
                           output_file_name, 
                           skip=input_file_desc.header_lines)
            #generate statistics
            #self.report_stats(in_file.name)
            
            return model.FileResponse(output_file_name, 
                                  config.SORTED)
        except IOError:
            self.error(common.EquityMasterError,
                            _m_logger,
                            'file processing error: {:s} {:s} ',
                            input_file_name, 
                            output_file_name,
                            )
    

    def report_stats(self, file_name, count_records):
        tmpl = 'file sorting for ({:s}) records({:d}) completed '
        self.info(_m_logger,
                 tmpl,
                 file_name,
                 count_records,
                 )
        
        
class FileMerge(BaseProcess):
    """Class that can merge N number of sorted files
    """
    def handle(self, request):
        """ merge n number of sorted files
        first field in the file is an integer id
         
           
        """
        
        return self.merge(request.input_file_names,
                          request.input_file_desc,
                          request.input_file_state,
                          request.output_file_names[0],
                          request.output_file_desc,
                          request.error_file_names[0])
            
            
 
     
       
    
    def merge(self, 
              input_file_names, 
              input_file_desc,
              input_file_state, 
              output_file_name,
              output_file_desc,
              error_file_name):
        """ N file merge  
        """
        infd = input_file_desc
        ofd = output_file_desc
        try:
            #open required files files
            in_files = self.files_open(
                                       'r', 
                                       *input_file_names) 
            out_file = self.file_open(
                                      output_file_name, 
                                      'w')
            self.write_header(out_file,
                               output_file_desc)  
            
            key = lambda x : x[0] 
            valid, invalid = self.merge_files(
                                      out_file,
                                      ofd,
                                      error_file_name,
                                      key, 
                                      file_sort.merge(key, 
                                                      infd.header_lines,
                                                      *in_files))
            #generate statistics
            self.report_stats(','.join(input_file_names), 
                              out_file.name, 
                              valid, 
                              invalid)
            
            return model.FileResponse(output_file_name, 
                                  config.MERGED)
            
        except IOError:
            self.error(common.EquityMasterError,
                            _m_logger,
                            'file processing error: {:s} {:s} ',
                            ','.join(input_file_names), 
                            output_file_name,
                            )
        finally:
            self.files_close(out_file, *in_files)
    
      
    def merge_files(self,
                out_file,
                output_file_desc,
                error_file_name,
                key,
                file_records):
        """
        Methods that drives the merging
        """
        valid = 0 
        invalid = 0
        last = []
        ofd = output_file_desc
        efn = error_file_name
        for record in file_records:
            
            data_fields, orig_rec  = self.split_n_trim(record,
                                            ofd.field_sep,
                                            ofd.trimmer)
            if last:
                current_key = key(data_fields)
                if current_key != key(last[0]):
                    if self.merge_n_write(last,
                                          ofd, 
                                          efn,
                                          out_file):
                        valid += 1
                    else:
                        invalid += 1
                    last = []
                    
            last.append(data_fields)
        if last:
            if self.merge_n_write(last, ofd, efn, out_file):
                valid +=1
            else:
                invalid +=1
           
            
        return valid, invalid
    
    def merge_n_write(self, 
                      records,
                      output_file_desc, 
                      error_function_name,
                      output_file):
        
        new_rec = self.merge_fields(records,
                                    output_file_desc,
                                    error_function_name)
        if new_rec:
            self.write_record(
                            output_file, 
                            output_file_desc, 
                            new_rec)
            return True
        
        return False
    def merge_fields(self, 
                     records, 
                     output_file_desc,
                     error_file_name ):
        """
        Field level merge
        """
        ofd = output_file_desc
        flds = ofd.fields
        efn = error_file_name
        new_rec =[]
        stub=config.FIELD_FILLER

        for field_id, field_desc in zip(xrange(len(flds)),
                                        flds):
            new_value = stub
            for record in records:
                #get current value
                value = record[field_id]
                if value == stub:
                    continue
                elif new_value == stub:
                    new_value = value    
                elif new_value == value:
                    continue
                else:
                    #there is a diff in field values
                    #log an error, write all records to error file
                    self.log_error(
                            _m_logger,
                            'file merge error: file {:s} field {:s} offset {:d} ',
                            ofd.file_name,
                            field_desc.name,
                            field_id 
                            )
                    for rec in records:
                        self.write_error(efn, ofd.field_sep.join(rec)+'\n') 
                    return None
            if new_value == stub:
                #log a warning
                tmpl = 'stub value in file {:s} field {:s} offset {:d}'
                self.warn(_m_logger,
                            tmpl,
                            ofd.file_name,
                            field_desc.name,
                            field_id 
                            )
            new_rec.append(new_value)
            
        return new_rec