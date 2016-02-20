#!/usr/bin/env python3
###############################################################################
# primes.py
#
# Template Python 3 application.
#
# CHANGE LOG
# Date        Who  Description
# 2015/08/28  sgc  Initial version
#
# TODO:
# - add config file reader
#
###############################################################################
#
#--- Directory of routines:
#
# (egrep 'class|def' primes.py > primes.routines)
#
#------------------------------------------------------------------------------

#--- Python Imports

import sys
import os
import argparse
import subprocess

#--- Project imports

import primeslib

from errmsgs import *

# Wrap argparse.ArgumentParser() in a class that throws
# an exception we can catch.

class ArgumentParserError(Exception): pass

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

# Get path to directory where PRIMES is installed

thisScriptDir = sys.path[0]

#--- Global functions

# "primes.py" uses print functions defined in "primeslib.py" These
# print functions write to either STDERR or STDOUT and then flush the
# output buffer.

p_err = primeslib.p_err
p_dbg = primeslib.p_dbg
p_out = primeslib.p_out

#--- Global variables

thisProgramName, thisProgramExt = os.path.splitext(__file__)

thisScriptDir  = sys.path[0]

#------------------------------------------------------------------------------
#- Main Script
#------------------------------------------------------------------------------

def main(argv=None):
  '''Main program - PRIMES'''

  global \
    p_out, p_err, p_dbg, \
    primesMissionID

  diagPrint = 0

  #--- Must have a "version.txt" file to run!

  primeslib.thisProgramVersion = getVersionNumberFromFile()

  if not primeslib.thisProgramVersion:
    hdr = diagPrintHdr(inspect.stack(),'primes.py:','main()')
    p_err(hdr)
    p_err('  ERROR: cannot find "version.txt" file!')
    return 1

  #--- Get arguments from the command line

  if argv is None:
    argv = sys.argv

  #--- Parse the command line & create run parameters

  runParams = None

  try:
    runParams = parseCmdLine( argv )
  except ArgumentError as e:
    p_err(e)
    return 2

  #--- print out prime numbers

  try:
    primeGen = primeslib.PrimesGenerator( runParams )
    primeGen.printPrimes()
  except ArgumentError as e:
    p_err(e)
    return 5

  # end main()

#------------------------------------------------------------------------------
# FUNCTIONS
#------------------------------------------------------------------------------

#------------------------------------
# function getVersionNumberFromFile()
#------------------------------------

def getVersionNumberFromFile():

  global p_err

  # Locate "version.txt" file
  #
  # Look for "../version.txt" (command-line utility)
  # If not found at all, error exit

  errMsg = ''
  versionFileFound = False
  hdr = diagPrintHdr(inspect.stack(),'primes.py','getVersionNumberFromFile:')

  try:
    versionFile = \
      open(os.path.join(thisScriptDir, '..', 'version.txt'), 'r')
    versionFileFound = True
  except IOError as e1:
    errMsg1 = '  ERROR: "../version.txt" not found:'+'\n  '+str(e1)
    try:
      versionFile = \
        open(os.path.join(thisScriptDir, '.', 'version.txt'), 'r')
      versionFileFound = True
    except IOError as e2:
      errMsg2 = '  ERROR: "./version.txt" not found:'+'\n  '+str(e2)
      p_err(hdr)
      p_err(errMsg1)
      p_err(errMsg2)

  thisProgramVersion = ''
  if versionFileFound:
    thisProgramVersion = versionFile.readline().rstrip(os.linesep)

  return thisProgramVersion

  # end function getVersionNumberFromFile() ///////////////////////////////////

#------------------------
# function parseCmdLine()
#------------------------

def parseCmdLine( argv ):
  '''Parse the command line & create run parameters'''

  global \
    p_out, p_dbg, p_err

  diagPrint = 0

  if diagPrint:
    hdr = diagPrintHdr(inspect.stack(),'primes.py:','parseCmdLine()')
    p_dbg(hdr)
    p_dbg('  argv      = '+str(argv))
    p_dbg('  len(argv) = '+str(len(argv)))

  # Detect "help", "version", and "examples" arguments;
  # print appropriate message and exit.

  if '-h' in argv or '--help' in argv:
    usage()
    exit(2)

  if '-v' in argv or '--version' in argv:
    p_out('')
    p_out(thisProgramName+' '+primeslib.thisProgramVersion)
    exit(2)

  if '-x' in argv or '--examples' in argv:
    examples()
    exit(2)

  #-------------------------------------------------------------------
  # Create argument parser
  #
  # argParser.parse_args() will return (see below) an object with data
  # members having the same names as each of the argument "long names"
  #
  # e.g.:
  #    argument             data field
  #    |--------------------|--------------------------
  #    "--input_filename"   --> "args.input_filename"
  #
  # and so on.
  #-------------------------------------------------------------------

  argParser = \
  ThrowingArgumentParser( \
    prog=thisProgramName, \
    description= \
    thisProgramName+' v'+\
    primeslib.thisProgramVersion+' : Template Python 3 Application' \
    )

  #------------------------------------------
  # add REQUIRED arguments to argument parser
  #------------------------------------------


  #------------------------------------------
  # add OPTIONAL arguments to argument parser
  #------------------------------------------

  argParser.add_argument( \
    '-s', '--start_search', \
    help='start of interval to be searched for primes', \
    default = 1 \
    )

  argParser.add_argument( \
    '-e', '--end_search', \
    help='end of interval to be searched for primes' \
    )

  argParser.add_argument( \
    '-c', '--config', \
    help='config file name' \
    )

  # UNADVERTISED
  argParser.add_argument( \
    '-D', '--diag_print', \
    help='Name of routine for which debug print is desired', \
    default=[], \
    action='append' \
    )

  argParser.add_argument( \
    '-m', '--run_mode', \
    help='REQUIRED: processing mode', \
     default=None \
    )

  argParser.add_argument( \
    '-o', '--output_filename', \
    help='REQUIRED: name of output file', \
    default=None \
    )

  argParser.add_argument( \
    '-v', '--version', \
    help='OPTIONAL: print version number then exit', \
    default=None \
    )

  argParser.add_argument( \
    '-x', '--examples', \
    help='OPTIONAL: print "examples()" message then exit', \
    default='' \
    )

  #----------------------------------------------------------------
  # parse the arguments:
  #
  # create object "args" containing data members that have the same
  # names as all the "--<long_name>" command-line options
  #----------------------------------------------------------------

  try:
    args = argParser.parse_args()
  except ArgumentParserError as e:
    p_err('ERROR parsing arguments:'+str(e))
    exit(1)

  # Create run parameters from command line arguments

  runParams = primeslib.createRunParameters( args )

  return runParams

  # end function parseCmdLine() ///////////////////////////////////////////////


#-----------------
# function usage()
#-----------------

def usage():
  '''Prints the command line script usage'''

  global p_out

  p_out(\
    '\n'+\
    thisProgramName+' version '+primeslib.thisProgramVersion)

  p_out(
    '\n'+\
    'PRIMES for mission "'+str(primesMissionID)+'"\n'+\
    '  Template Python 3 application'+\
    '\n'+\
    '\n'+\
    'primes \ \n'+\
    '  -i/--input_file  <input_file> \ \n'+\
    '  -o/--output_file <output_file> \ \n'+\
    '  -m/--mode        <run_mode> \ \n'+\
    '  [ -h/--help ] \ \n'+\
    '  [ -v/--version ] \ \n'+\
    '  [ -x/--examples ] \ \n'+\
    '\n'+\
    'REQUIRED ARGUMENTS:\n'+\
    '\n'+\
    '-i|--input:\n'+\
    '  Name of input file\n'+\
    '\n'+\
    'OPTIONAL ARGUMENTS []:\n'+\
    '\n'+\
    '[-o|--output] :\n'+\
    '  Name of output file\n'+\
    '\n'+\
    '[-m|--mode] :\n'+\
    '  Name of run mode. Valid run mode names are:\n'+\
    '  '+str(primeslib.validRunModes)+'\n'\
    '\n'+\
    '[-h|--help] :\n'+\
    '  Print "usage()" message then exit.\n'+\
    '\n'+\
    '[-v|--version] :\n'+\
    '  Print version number then exit.\n'+\
    '\n'+\
    '[-x|--examples] :\n'+\
    '  Print "examples()" message then exit.\n')

  # end function usage() //////////////////////////////////////////////////////


#--------------------
# function examples()
#--------------------

def examples():
  '''Prints examples of PRIMES usage'''

  global p_out

  p_out(
    'PRIMES for mission "'+str(primesMissionID)+'"; examples:\n'+\
    '\n'+\
    'primes \\\n'+\
    '  -i input_file \\\n'+\
    '  -o output_file \\\n'+\
    '  -m PRIMES_MODE\n')

  # end function examples() ///////////////////////////////////////////////////


#--------------------------------------------------------
# Prevent interactive use from exiting Python interpreter
#--------------------------------------------------------

if __name__ == '__main__':
  sys.exit(main())
