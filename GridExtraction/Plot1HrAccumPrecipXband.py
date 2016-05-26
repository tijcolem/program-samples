#!/usr/bin/python
# -*- coding: utf-8 -*-

from scipy.io import netcdf
import os
import sys
import datetime


def EpochTime(ObsTime):

    EpochStartTime = datetime.datetime(1970, 1, 1, 0)

    DeltaTime = ObsTime - EpochStartTime

    TotalSeconds = DeltaTime.days * 24 * 60 * 60 + DeltaTime.seconds

    return TotalSeconds


BeginYYJJJHHMM = ''
RefInputPath = ''
RefFormat = ''
ImageDirTimePath = ''
KmlHrefPath = ''

print len(sys.argv)

if len(sys.argv) != 7:

    print '\nUSAGE: Plot1HrAccumPrecipXband.py BeginYYJJJHHMM RefInputPath RefFormat ImageDirTimePath KmlHrefPath',
    print """
 
         n"""
    sys.exit()
else:

    BeginYYJJJHHMM = sys.argv[1]
    RefInputPath = sys.argv[2]
    RefFormat = sys.argv[3]
    ImageDirTimePath = sys.argv[4]
    KmlHrefPath = sys.argv[5]

####### end user defined variables ######
# set NCL environmental variables so the interpreter can execute
# and custom color maps can be accessed

# NCL 6.0

os.environ['NCARG_ROOT'] = '/usr'
os.environ['NCARG_BIN'] = '/usr/bin'

# NCL 6.2

os.environ['NCARG_ROOT'] = '/usr/local/ncl62'
os.environ['NCARG_BIN'] = '/usr/local/ncl62/bin'

os.environ['NCARG_COLORMAPS'] = '/usr/local/etltools/ncl/colormaps:' \
    + os.environ.get('NCARG_ROOT') + '/lib/ncarg/colormaps'

# os.environ["NCARG_COLORMAPS"] = "colormaps:" + \
#                                os.environ.get('NCARG_ROOT') + \
#                                "/lib/ncarg/colormaps"
# set shared object path for FORTRAN wrappers

os.environ['LD_LIBRARY_PATH'] = '/home/dms7/workspace/Dan/NclWrapit'

# define NCL interpreter and graphics production script

Ncl = os.environ.get('NCARG_BIN') + '/ncl'

# PlotScanRadarRef = "/home/dms7/process/web/ScanningRadar/PlotScanRadarRef.ncl"

PlotScanRadarRef = '/usr/local/etltools/ncl/PlotScanRadarRef.ncl'
PlotScanRainfallRate = \
    '/usr/local/etltools/ncl/PlotScanRadarRainRate.ncl'
PlotScan1HrRainAcc = \
    '/usr/local/etltools/ncl/PlotScanRadarRainAccumlate.ncl'

Command = Ncl + ' ' + PlotScan1HrRainAcc + ' \'BeginYYJJJHHMM="' \
    + BeginYYJJJHHMM + '"\' \'RefInputPath="' + RefInputPath \
    + '"\' \'RefFormat="' + RefFormat + '"\' \'ImageOutputPath="' \
    + ImageDirTimePath + '"\' \'KmlOutputPath="' + ImageDirTimePath \
    + '"\' \'KmlHrefPath="' + KmlHrefPath + '"\''

print Command

os.system(Command)
