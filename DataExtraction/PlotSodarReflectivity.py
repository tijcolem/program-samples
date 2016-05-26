#!/usr/bin/python

import os
import sys
import getopt
import datetime
from datetime import datetime
from datetime import timedelta
from time import strftime
from time import mktime
from optparse import OptionParser

####### check command-line arguments #######
usage           = "Usage: %prog [options] SiteID\n\twhere, SiteID = 3-letter site identifier"
parser          = OptionParser(usage=usage)
(options, args) = parser.parse_args()

if(len(args) != 1):

  parser.error("Missing argument.")
else:
  SiteID = args[0]

####### define begin and end date/times in YYJJJHHMM format #######
BeginPlotTimeString = "130981130"
EndPlotTimeString   = "130981130"

PlotTime    = datetime.strptime(BeginPlotTimeString,"%y%j%H%M") 
EndPlotTime = datetime.strptime(EndPlotTimeString,  "%y%j%H%M") 

####### fill path variables for NCL argument list ######
InputFilePath  = "/data/realtime/SodarEt7/Reflectivity" + "/" + SiteID
OutputFilePath = "/data/realtime/SodarEt7/Images" + "/" + SiteID
#OutputFilePath = "./"
ConfigFilePath = "/usr/local/etltools/specfiles"

####### end user defined variables ######
# set NCL environmental variables so the interpreter can execute
# and custom color maps can be accessed
#os.environ["NCARG_ROOT"]      = "/usr"
#os.environ["NCARG_BIN"]       = "/usr/bin"
os.environ["NCARG_ROOT"]      = "/usr/local/ncl62"
os.environ["NCARG_BIN"]       = "/usr/local/ncl62/bin"

os.environ["NCARG_COLORMAPS"] = "/usr/local/etltools/ncl/colormaps:" + \
                                os.environ.get('NCARG_ROOT') + \
                                "/lib/ncarg/colormaps"
#os.environ["NCARG_COLORMAPS"] = "colormaps:" + \
#                                os.environ.get('NCARG_ROOT') + \
#                                "/lib/ncarg/colormaps"

# set shared object path for FORTRAN wrappers
os.environ["LD_LIBRARY_PATH"] = "/home/dms7/workspace/Dan/NclWrapit"

# define NCL interpreter and graphics production script
Ncl          = os.environ.get('NCARG_BIN') + "/ncl"
PlotSodarRef = "/home/dms7/process/web/SodarReflectivity/PlotSodarReflectivity.ncl"

while(PlotTime <= EndPlotTime):
  
  YYJJJHHMM = PlotTime.strftime("%y%j%H%M")

  print("\nCreating plot for " + YYJJJHHMM + "...\n\n")

  # shell out NCL PlotSodarReflectivity.ncl command: 
  #
  # ncl PlotSodarReflectivity.ncl 'EndYYJJJHHMM="<string>"'
  #                               'InputFilePath="<string>"' 
  #                               'OutputFilePath="<string>"' 
  #                               'ConfigFilePath="<optional string>"'
  #                               'ConfigSiteID="<optional string>"'

  os.system(Ncl + ' ' + PlotSodarRef +
            ' \'EndYYJJJHHMM="'      +
            YYJJJHHMM                +
            '"\' \'InputFilePath="'  +
            InputFilePath            +
            '"\' \'OutputFilePath="' +
            OutputFilePath           +
            '"\' \'ConfigFilePath="' +
            ConfigFilePath           +
            '"\' \'ConfigSiteID="'   +
            SiteID                   +
            '"\'')

  PlotTime += timedelta(minutes=30)
