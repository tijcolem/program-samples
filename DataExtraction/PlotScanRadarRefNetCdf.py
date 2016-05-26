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


if len(sys.argv) != 4:

    print '\nUSAGE: PlotScanRadarRefMod.py RadarSiteID RadarDataType RadarFile',
    print """
 
         RadarSiteID    = e.g., "dax", "pix", "mux"
         RadarDataType  = "NIDS" for native NWS NIDS format or "KPIX" for NSSL NetCDF V3.0
         RadarFile      = Full path and file name of radar input file
"""
    sys.exit()

if sys.argv[2] == 'KPIX' or sys.argv[2] == 'NIDS' or sys.argv[2] \
    == 'KGO':

    SiteID = sys.argv[1]
    RefFormat = sys.argv[2]
    RefInputFile = sys.argv[3]
else:

    print '\n Please used a valid DataType. "NIDS", "KPIX", "KGO"'
    sys.exit(1)

####### begin user defined variables ######

# define base path for input and output files

BaseOutputPath = '/data/realtime/ScanningRadar/Reflectivity0.50/'

# NCL command-line argument: reflectivity input file
# RefInputFile = BaseOutputPath + "nids/KSTO_SDUS56_N0RDAX_201203141601"
# RefInputFile = BaseOutputPath + "nids/KMTR_SDUS56_N0RMUX_201203161857"

# NCL command-line argument: file format NIDS or KPIX
# RefFormat = "NIDS"
# RefFormat = "KPIX"

# NCL command-line argument: path to write output image file;
# empty string outputs to current directory

ImageOutputPath = '/data/realtime/ScanningRadar/Images/'

# NCL command-line argument: path to write output KML file;
# empty string disables KML output

KmlOutputPath = ImageOutputPath

# NCL command-line argument: path to image file in <href> tag
# in KML output if KML output is enabled

KmlHrefPath = ''

# Nids2NetcdfProg = "/home/dms7/process/web/ScanningRadar/NetCDFJava/toolsUI-4.2.jar"

Nids2NetcdfProg = '/usr/local/etltools/lib/NetCDFJava/toolsUI-4.2.jar'

####### end user defined variables ######

# set NCL environmental variables so the interpreter can execute
# and custom color maps can be accessed
# os.environ["NCARG_ROOT"]      = "/usr"
# os.environ["NCARG_BIN"]       = "/usr/bin"

os.environ['NCARG_ROOT'] = '/usr/local/ncl62'
os.environ['NCARG_BIN'] = '/usr/local/ncl62/bin'

# os.environ["NCARG_COLORMAPS"] = "/usr/local/etltools/ncl/colormaps:" + \
#                                os.environ.get('NCARG_ROOT') + \
#                                "/lib/ncarg/colormaps"

os.environ['NCARG_COLORMAPS'] = '/usr/local/etltools/ncl/colormaps:' \
    + os.environ.get('NCARG_ROOT') + '/lib/ncarg/colormaps'

# define NCL interpreter and graphics production script

Ncl = os.environ.get('NCARG_BIN') + '/ncl'

# PlotScanRadarRef = "/home/dms7/process/web/ScanningRadar/PlotScanRadarRef.ncl"

PlotScanRadarRef = \
    '/home/dms7/process/web/ScanningRadar/PlotScanRadarRef.ncl'

# shell out NCL PlotScanRadarRef.ncl command:
#
# ncl PlotScanRadarRef.ncl 'RefInputFile="<string>"'
#                          'RefFormat="<string>"'
#                          'ImageOutputPath="<string>"'
#                          'KmlOutputPath="<string>"'
#                          'KmlHrefPath="<string>"'

RadarDirPath = BaseOutputPath + RefFormat.lower() + '/'

NetCdfAtrrTime = ''

if RefFormat == 'NIDS':

    NidsToNetCDFFile = RefInputFile + '.nc'

    NidsToNetCDFCommand = 'java -classpath ' + Nids2NetcdfProg \
        + ' ucar.nc2.FileWriter -in ' + RefInputFile + ' -out ' \
        + NidsToNetCDFFile

    os.system(NidsToNetCDFCommand)

    RemoveNidsFileCommand = 'rm ' + RefInputFile

    os.system(RemoveNidsFileCommand)

    RefInputFile = NidsToNetCDFFile

    f = netcdf.netcdf_file(RefInputFile, 'r')

    NetCdfAtrrTime = getattr(f, 'time_coverage_start')

    f.close()

    print NetCdfAtrrTime

    TimeObj = datetime.datetime.strptime(NetCdfAtrrTime,
            '%Y-%m-%dT%H:%M:%SZ')

    RefFormat = 'NIDSNC'
elif RefFormat == 'KPIX' or RefFormat == 'KGO':

    RefFormat = 'KPIX'

    f = netcdf.netcdf_file(RefInputFile, 'r')

    NetCdfAtrrTime = getattr(f, 'Time')

    TimeObj = datetime.datetime.utcfromtimestamp(NetCdfAtrrTime)

    f.close()

NetCdfDirTimePath = '%s%s/%04d/%03d/' % (BaseOutputPath, SiteID,
        TimeObj.timetuple().tm_year, TimeObj.timetuple().tm_yday)

if not os.path.exists(NetCdfDirTimePath):

    os.makedirs(NetCdfDirTimePath)

ImageDirTimePath = '%s%s/%04d/%03d/' % (ImageOutputPath, SiteID,
        TimeObj.timetuple().tm_year, TimeObj.timetuple().tm_yday)

print ImageDirTimePath

if not os.path.exists(ImageDirTimePath):

    os.makedirs(ImageDirTimePath)

NewFileName = '%s%s%02d%03d%02d%02d.nc' % (
    NetCdfDirTimePath,
    SiteID,
    TimeObj.timetuple().tm_year % 100,
    TimeObj.timetuple().tm_yday,
    TimeObj.timetuple().tm_hour,
    TimeObj.timetuple().tm_min,
    )

FullNewFileName = NewFileName

ChangeFileNameCommand = 'mv ' + RefInputFile + ' ' + FullNewFileName

print ChangeFileNameCommand

os.system(ChangeFileNameCommand)

RefInputFile = FullNewFileName

os.system(Ncl + ' ' + PlotScanRadarRef + ' \'RefInputFile="'
          + RefInputFile + '"\' \'RefFormat="' + RefFormat
          + '"\' \'ImageOutputPath="' + ImageDirTimePath
          + '"\' \'KmlOutputPath="' + ImageDirTimePath
          + '"\' \'KmlHrefPath="' + KmlHrefPath + '"\'')

if RefFormat == 'NIDSNC':

    PointDataCommand = \
        'python /home/dms7/process/web/ScanningRadar/ExtractScanningRadarPointDbz.py ' \
        + RefInputFile + ' ' + SiteID
    print PointDataCommand
    os.system(PointDataCommand)
