###############################################################################
# errmsgs.py
#
# This file contains function and class definitions for error messages
# that include a call stack trace as well as error-specific message text.
#
###############################################################################
#
# Directory of routines:
# (egrep 'class|def' errmsgs.py > errmsgs.routines)
#
# def getCallStackStr(stk):
# def diagPrintHdr( stkList, srcFile, fcnName, optName=None, optNum=None):
# def ContentErrMsg(stkList, numErrors, ssRowNum, moduleName, errInfo):
# def ContentWarnMsg(stkList,numWarnings,ssRowNum,moduleName,dataMap,warnInfo):
#
# class ArgumentError(Exception):
#   def __init__( self, moduleName, errList ):
#   def __str__(self):
#

#--------
# Imports
#--------

# Python imports

import sys
import inspect

# Local imports

#----------------
# Gobal variables
#----------------

dataMap = None

#------------------------------------------------------------------------------
# getCallStackStr
#
# This function takes as input a list of lists as output by the
# inspect.stack() function (see "inspect.py") and returns a single
# string made up of the names of all routines on the call stack
# separated by ':'.
#------------------------------------------------------------------------------

def getCallStackStr(stk):
  '''Constructs call stack string from output of inspect.stack()'''

  call_depth = len(stk) - 1
  call_list = []

  for i in range(call_depth):
    call_list.append(stk[i][3])

  stk_str = ''
  for i in range(call_depth-1,0,-1):
    stk_str = stk_str + call_list[i]
    stk_str = stk_str + ':'

  return stk_str

#------------------------------------------------------------------------------
# diagPrintHdr
#
# This function creates a string that serves as a header for debug print
# messages. The header contains a full call stack trace as well as an
# optional numerical parameter and label which can be used to annotate
# the message header with a numerical value (such as a row number for
# instance).
#------------------------------------------------------------------------------

def diagPrintHdr( stkList, srcFile, fcnName, optName=None, optNum=None):
  callStackStr = getCallStackStr(stkList)
  hdr = '\n'+srcFile+':'+callStackStr+fcnName
  if optName:
    hdr += ': '+str(optName)+' = '
    if optNum:
      hdr += str(optNum)
    else:
      hdr += '0'
  return hdr

#------------------------------------------------------------------------------
# ContentErrMsg
#
# This function creates a content error message that includes a call stack
# trace, error count, module name, and a description of the error.
#------------------------------------------------------------------------------

def ContentErrMsg(stkList, numErrors, ssRowNum, moduleName, errInfo):

  callStackStr = getCallStackStr(stkList)
  errCountStr  = str(format(numErrors,"0=4d"))
  msg = '\n' + errCountStr + ':' + moduleName + ':' + callStackStr + '\n'
  msg = msg + '  ERROR in row ' + str(ssRowNum) + ': ' + errInfo

  return msg

#------------------------------------------------------------------------------
# ContentWarnMsg
#
# This function creates a content warning message that includes a call stack
# trace, warning count, row number, module name, variable name, data map,
# and a description of the warning.
#------------------------------------------------------------------------------

def ContentWarnMsg(stkList,numWarnings,ssRowNum,moduleName,dataMap,warnInfo):

  callStackStr = getCallStackStr(stkList)
  warnCountStr = str(format(numWarnings,'0=4d'))

  msg = \
    '\n' + moduleName + ':' + callStackStr + \
    '\n  WARNMSG ' + warnCountStr + ':\n'

  varName = warnInfo[0]
  warnMsg = warnInfo[1]

  msg = msg +\
    '    WARNING in row ' + str(ssRowNum) +\
    ', Column ' + str(dataMap[varName]) + ' : ' + varName + ' : ' + warnMsg

  return msg

#------------------------------------------------------------------------------
# ArgumentError
#
# This class is an exception class; it defines an "ArgumentError" exception.
#------------------------------------------------------------------------------

class ArgumentError(Exception):

  def __init__( self, moduleName, errList ):

    stkList      = inspect.stack()
    callStackStr = getCallStackStr(stkList)

    self.msg = \
      '\n' + moduleName + ':' + callStackStr + \
      '\n  EXCEPTION : Argument error(s) :\n'

    for i in range(len(errList)):
      varname    = errList[i][0]
      errmsg     = errList[i][1]
      errListStr = '  '+varname+' : '+errmsg
      self.msg   = self.msg + errListStr + '\n'

  def __str__(self):
    return self.msg
