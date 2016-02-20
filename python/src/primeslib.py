#############################################################################
# pyapplib.py
#
# CHANGE LOG
# Date        Who  Description
# 2015/08/28  sgc  Initial version
#
###############################################################################
#
# Directory of routines:
#
# (egrep 'class|def' pyapplib.py > pyapplib.routines)
#
# def p_stderr( msg ):
# def p_stdout( msg ):
#
# class RunParameters(object):
#   def __init__(self):
#   def args(self):
#   def args(self, value):
#   def input_filename(self):
#   def input_filename(self, value):
#   def input_file(self):
#   def input_file(self, value):
#   def output_filename(self):
#   def output_filename(self, value):
#   def output_file(self):
#   def output_file(self, value):
#   def mode(self):
#   def mode(self, value):
#   def address(self):
#   def address(self, value):
#
# def createRunParameters( args ):
#
# class IntelHex80(object):
#   def __init__(self, runParams):
#   def run_params(self):
#   def run_params(self, value):
#   def hex80filename(self):
#   def hex80filename(self, value):
#   def hex80file(self):
#   def hex80file(self, value):
#   def hex80buf(self):
#   def hex80buf(self, value):
#   def datablock(self):
#   def datablock(self, value):
#   def readHex80File( self ):
#   def echoHex80Buf( self ):
#
# class OutputFile(object):
#   def __init__(self, runParams, inputFile):
#   def run_params(self):
#   def run_params(self, value):
#   def input_file(self):
#   def input_file(self, value):
#   def writeOutput(self):
#   def writeCSTOL(self):
#   def createLoadFswScript(self):
#
# def fletcher16checksum( datab, diag_print_list=[] ):
#
#------------------------------------------------------------------------------

#--- Python imports

import sys
import os
import argparse
import datetime
import math

#--- Project imports

from errmsgs import *

#--- Global functions

# p_stderr() writes to STDERR then flushes the STDERR buffer

def p_stderr( msg ):
  print( msg, file=sys.stderr )
  sys.stderr.flush()

# p_stdout() writes to STDOUT then flushes the STDOUT buffer

def p_stdout( msg ):
  print( msg, file=sys.stdout )
  sys.stdout.flush()

# p_err() and p_dbg() write/flush STDERR
# p_out() writes/flushes STDOUT

p_out = p_stdout
p_err = p_stderr
p_dbg = p_stderr

# Print function used to time things. Calls "p_dbg" to actually print
# things out.

t_0    = datetime.datetime.now()
t_last = t_0

def ptime(s):

  global p_dbg, t_0, t_last

  t_now         = datetime.datetime.now()
  t_since_start = t_now - t_0
  t_since_last  = t_now - t_last
  t_last        = t_now

  p_dbg(\
    str(t_since_start)+' # '+\
    str(t_since_last)+' # '+\
    s)

#--- Global variables

validRunModes      = ['DEFAULT', 'SPECIAL']
thisProgramVersion = ''


#------------------------------------------------------------------------------
# class RunParameters
#------------------------------------------------------------------------------

class RunParameters(object):
  '''Calculates run parameters from command line arguments'''

  def __init__(self):

    #==================================
    # Class Properties:
    #   - include setter, getter
    #   - may be checked at assign time
    #==================================

    self.__argv            = None
    self.__args            = None

    self.__conf_path       = None
    self.__conf_file       = None
    self.__input_filename  = None
    self.__input_file      = None
    self.__output_filename = None
    self.__output_file     = None
    self.__run_mode        = None
    self.__diag_print      = None

    #==========================
    # Class variables
    #   - direct access
    #   - no checking performed
    #==========================

    # errList is a list of lists:
    #
    # for error number n:
    # errList[n] = ["var_name", "error message"]
    # where
    #   "var_name"      = name of variable with error
    #   "error message" = descriptive error message
    # thus
    #   errList[n][0] = name of variable with error
    #   errList[n][1] = error message

    self.errList = []
    self.errors  = 0

    # end RunParameters::__init__() ///////////////////////////////////////////


  #--- start_search (integer)

  @property
  def start_search(self):
    return self.__start_search

  @start_search.setter
  def start_search(self, value):
    self.__start_search = int(value)
    # end RunParameters::start_search.setter //////////////////////////////////

  #--- end_search (integer)

  @property
  def end_search(self):
    return self.__end_search

  @end_search.setter
  def end_search(self, value):
    self.__end_search = int(value)
    # end RunParameters::end_search.setter //////////////////////////////////

  #--- args (object)

  @property
  def args(self):
    return self.__args

  @args.setter
  def args(self, value):
    self.__args = value
    # end RunParameters::args.setter //////////////////////////////////////////

  #--- conf_path (string)
  #--- conf_file (file handle)

  @property
  def conf_path(self):
    return self.__conf_path

  @conf_path.setter
  def conf_path(self, value):

    # "value" must be a string

    if not isinstance(value,str):
      self.errors += 1
      errMsg = 'Invalid value "'+str(value)+'" : must be of type "str"'
      errInfo = ['conf_path.setter', errMsg]
      self.errList.append(errInfo)
      self.__conf_path = value
      self.__conf_file = None
      return

    # Try to open the file identified by "value"

    try:
      self.__conf_path = value
      self.__conf_file = open(value,'r')
    except IOError as e:
      self.errors += 1
      errMsg = \
        'Error opening config file "'+str(value)+'"\n'+\
        '  IOError message = "'+str(e)+'"'
      errInfo = ['conf_path.setter', errMsg]
      self.errList.append(errInfo)
      self.__conf_path = value
      self.__conf_file = None
      raise ArgumentError('pyapplib.py - ', self.errList)

    # end RunParameters::@conf_path.setter() //////////////////////////////////


  #--- conf_file (file handle)

  @property
  def conf_file(self):
    return self.__conf_file

  @conf_file.setter
  def conf_file(self, value):
    self.__conf_file = value
    # end RunParameters::@conf_file.setter() //////////////////////////////////


  #--- input_filename (string)

  @property
  def input_filename(self):
    return self.__input_filename

  @input_filename.setter
  def input_filename(self, value):

    # "-i|--input_filename" must be a string

    if not isinstance(value,str):
      self.errors += 1
      errMsg = 'Invalid input file name "'+str(value)+\
               '" : must be of type "str"'
      errInfo = ['input_filename.setter', errMsg]
      self.errList.append(errInfo)
      self.__input_filename = value
      self.__input_file     = None
      raise ArgumentError('pyapplib.py - ', self.errList)

    # Try to open the input file

    try:
      self.__input_filename = value
      self.input_file = open(value,'r')
    except IOError as e:
      self.errors += 1
      errMsg = \
        'Error opening input file "'+str(value)+'"\n'+\
        '  IOError message = "'+str(e)+'"'
      errInfo = ['input_filename.setter', errMsg]
      self.errList.append(errInfo)
      self.__conf_path = value
      self.__conf_file = None
      raise ArgumentError('pyapplib.py - ', self.errList)

    # end RunParameters::input_filename.setter ////////////////////////////////

  #--- input_file (file handle)

  @property
  def input_file(self):
    return self.__input_file

  @input_file.setter
  def input_file(self, value):
    self.__input_file = value
    # end RunParameters::input_file.setter ////////////////////////////////////

  #--- output_filename (string)

  @property
  def output_filename(self):
    return self.__output_filename

  @output_filename.setter
  def output_filename(self, value):

    # "-o|--output_filename" must be a string

    if not isinstance(value,str):
      self.errors += 1
      errMsg = 'Invalid output file name "'+str(value)+\
               '" : must be of type "str"'
      errInfo = ['input_filename.setter', errMsg]
      self.errList.append(errInfo)
      self.__input_filename = value
      self.__input_file     = None
      raise ArgumentError('pyapplib.py - ', self.errList)

    # Try to open the output file

    try:
      self.__output_filename = value
      self.output_file = open(value,'w')
    except IOError as e:
      self.errors += 1
      errMsg = \
        'Error opening output file "'+str(value)+'"\n'+\
        '  IOError message = "'+str(e)+'"'
      errInfo = ['output_filename.setter', errMsg]
      self.errList.append(errInfo)
      self.__conf_path = value
      self.__conf_file = None
      raise ArgumentError('pyapplib.py - ', self.errList)

    # end RunParameters::output_filename //////////////////////////////////////

  #--- output_file (file handle)

  @property
  def output_file(self):
    return self.__output_file

  @output_file.setter
  def output_file(self, value):
    self.__output_file = value
    # end RunParameters::output_file.setter ///////////////////////////////////

  #--- run_mode (string)

  @property
  def run_mode(self):
    return self.__run_mode

  @run_mode.setter
  def run_mode(self, value):

    global validRunModes

    if value == None:
      self.__run_mode = None
    else:

      # "-m|--run_mode" must be a string
      if not isinstance(value,str):
        self.errors += 1
        errMsg = 'Invalid mode value "'+str(value)+'" : must be of type "str"'
        errInfo = ['run_mode.setter', errMsg]
        self.errList.append(errInfo)
        self.__run_mode = None
        raise ArgumentError('pyapplib.py - ',self.errList)

      # "-m|--run_mode" must be one of the valid run modes
      if not value in validRunModes:
        self.errors += 1
        errMsg = \
          'Unknown run mode "'+str(value)+'" : valid modes are :'+\
          str(validRunModes)
        errInfo = ['run_mode.setter', errMsg]
        self.errList.append(errInfo)
        self.__run_mode = None
        raise ArgumentError('pyapplib.py - ',self.errList)

      self.__run_mode = value

      # end if value == None

    # end RunParameters::run_mode.setter //////////////////////////////////////


  #--- diag_print (list of strings)

  @property
  def diag_print(self):
    return self.__diag_print

  @diag_print.setter
  def diag_print(self, value):
    if value == None:
      self.__diag_print = []
    else:
      self.__diag_print = value
    # end RunParameters::@diag_print.setter() /////////////////////////////////


  # end class RunParameters ///////////////////////////////////////////////////


#------------------------------------------------------------------------------
# createRunParameters()
#------------------------------------------------------------------------------

def createRunParameters( args ):
  '''Generate run parameters from command line arguments'''

  global \
    p_err, p_dbg, \
    validRunModes

  if 'createRunParameters' in args.diag_print:
    debugPrint = 1
  else:
    debugPrint = 0

  # The "run parameters" are the quantities that actually control
  # execution. A single command line argument may simply be used as is
  # (such as a string containing a file name) or it may be used to
  # derive one or more run parameters, e.g. --diag_print, which is
  # used to create a list of routine names in which debug print
  # statements will be turned on.

  rp = RunParameters()

  # These assignment statements invoke 'setter' methods
  # in the RunParameters object (rp) which perform all checks
  # on command line argument validity as well as calculating
  # all "run parameters" that are derived from them.

  # NOTE!: these assignment statements may be order-dependent!
  # Some of them may depend on others having been completed first.

  rp.args = args

  rp.start_search = args.start_search
  rp.end_search   = args.end_search
  rp.run_mode     = args.run_mode
  rp.diag_print   = args.diag_print

  return rp

  # end createRunParameters


#------------------------------------------------------------------------------
# class PrimesGenerator
#------------------------------------------------------------------------------

class PrimesGenerator(object):
  '''Generates prime numbers between args.start_search and args.end_search'''

  def __init__(self, runParams):

    #==================================
    # Class Properties:
    #   - include setter, getter
    #   - may be checked at assign time
    #==================================

    self.__run_params   = None

    #==========================
    # Class variables
    #   - direct access
    #   - no checking performed
    #==========================

    # errList is a list of lists:
    #
    # for error number n:
    # errList[n] = ["var_name", "error message"]
    # where
    #   "var_name"      = name of variable with error
    #   "error message" = descriptive error message
    # thus
    #   errList[n][0] = name of variable with error
    #   errList[n][1] = error message

    self.errList = []
    self.errors  = 0

    # Buffer to hold output script

    self.buf = []

    # Perform initializations

    self.run_params = runParams

  #--- run_params (object)

  @property
  def run_params(self):
    return self.__run_params

  @run_params.setter
  def run_params(self, value):
    self.__run_params = value

  #--- Print out prime numbers

  def printPrimes(self):
    '''Prints out prime numbers'''

    i_start = self.run_params.start_search
    i_end   = self.run_params.end_search

    if i_end != None:
      if i_end <= i_start:
        self.errors += 1
        errMsg   = 'end_search = '+str(end_search)+' <= '
        errMsg  += 'start_search = '+str(start_search)
        errInfo  = ['printPrimes', errMsg]
        self.errList.append(errInfo)
        raise ArgumentError('pyapplib.py - ',self.errList)

    # i_start must be an odd number
    if i_start % 2 == 0:
      i_start += 1

    x = i_start

    print('DEBUG: i_start = '+str(i_start))
    print('DEBUG: i_end   = '+str(i_end))

    i_div = 0
    i_div_tot = 0

    if i_end != None:

      while(x <= i_end):
        max_divisor = int(math.sqrt(x))
        if max_divisor % 2 == 0:
          max_divisor += 1
        d = 3
        remainder = -1
        while (d <= max_divisor) and (remainder != 0):
          remainder = x % d
          d += 2
          i_div += 1
        if remainder != 0:
          print(str(x)+' ['+str(i_div)+']')
          i_div_tot += i_div
          i_div = 0
        x += 2
        # end while(x <= i_end)

    else:

      while(1):
        max_divisor = int(math.sqrt(x))
        if max_divisor % 2 == 0:
          max_divisor += 1
        d = 3
        remainder = -1
        while (d <= max_divisor) and (remainder != 0):
          remainder = x % d
          d += 2
          i_div += 1
        if remainder != 0:
          print(str(x)+' ['+str(i_div)+']')
          i_div_tot += i_div
          i_div = 0
        x += 2
        # end while(1)

    t_now           = datetime.datetime.now()
    t_since_start   = t_now - t_0
    divs_per_second = i_div_tot / t_since_start.total_seconds()

    print('total divisors tested = '+str(i_div_tot))
    print('total run time        = '+str(t_since_start))
    print('divisors per second   = '+str(divs_per_second))

    # end printPrimes() ///////////////////////////////////////////////////////

  # end class PrimesGenerator /////////////////////////////////////////////////
