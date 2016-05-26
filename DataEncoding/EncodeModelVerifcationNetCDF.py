#!/usr/bin/python
# -*- coding: utf-8 -*-

from Scientific.IO import NetCDF
from Numeric import *
import numpy as np
import os
import sys
import math
import time
import datetime


def TimeOffset(Time, MinsOffset):

    Time = Time + datetime.timedelta(minutes=MinsOffset)

    return Time


UTCTime = datetime.datetime.utcnow()
StartDate = datetime.datetime(2015, 2, 15, 00)
EndDate = datetime.datetime(2015, 2, 16, 00)

TimeStamp = '%04d%02d%02d%02d' % (UTCTime.timetuple().tm_year,
                                  UTCTime.timetuple().tm_mon,
                                  UTCTime.timetuple().tm_mday,
                                  UTCTime.timetuple().tm_hour)

NetCdfMetaFile = '/data/verify/Grids/MinT/MOSGuideBC_MinT_index.nc'
NetCdfDataFile = '/data/verify/Grids/MinT/MOSGuideBC_MinT_data.nc'
NetCdfOutputFile = \
    '/awips/adapt/ifps/workspace/FrostForcast/MOSGuideBC_Summary_MinT_data.nc'
NetCdfLatLongIinfo = \
    '/awips/adapt/ifps/workspace/FrostForcast/MTR_GRID__ISC_00000000_0000_Winery_1515118.cdf'

try:
    Index_nc = NetCDF.NetCDFFile(NetCdfMetaFile, 'r')
except:

    print 'Unable to open netcdf file ' + NetCdfMetaFile
    print sys.exc_info()
    print 'Exiting program'
    sys.exit()

try:

    Data_nc = NetCDF.NetCDFFile(NetCdfDataFile, 'r')
except:

    print 'Unable to open netcdf file ' + NetCdfDataFile
    print sys.exc_info()
    print 'Exiting program'
    sys.exit()

try:

    LatLong_nc = NetCDF.NetCDFFile(NetCdfLatLongIinfo, 'r')
except:

    print 'Unable to open netcdf file ' + NetCdfLatLongIinfo
    print sys.exc_info()
    print 'Exiting program'
    sys.exit()

try:

    Output_nc = NetCDF.NetCDFFile(NetCdfOutputFile, 'w')
except:

    print 'Unable to open netcdf file ' + NetCdfOutputFile
    print sys.exc_info()
    print 'Exiting program'
    sys.exit()

# Get handlers to each of the data fields in the _index.nc file

btime = Index_nc.variables['btime']
stime = Index_nc.variables['stime']
etime = Index_nc.variables['etime']
vtime = Index_nc.variables['vtime']
scale = Index_nc.variables['scale']
addit = Index_nc.variables['addit']

# Get handlers to each of the data fields in the _data.nc file

value = Data_nc.variables['value']

# Get handlers to each of the data fields in the _data.nc file

lat = LatLong_nc.variables['latitude']
long = LatLong_nc.variables['longitude']
topo = LatLong_nc.variables['Topo']

print value.shape

# Create dims

Output_nc.createDimension('stime', None)
Output_nc.createDimension('latitude', 476)
Output_nc.createDimension('longitude', 224)

# create varirable dims in netcdf

tempDims = ('stime', 'latitude', 'longitude')
latlongDims = ('latitude', 'longitude')
recordDims = ('stime', )

# Create variables

OutputValue = Output_nc.createVariable('surface_temperature', 'f',
        tempDims)
OutputLat = Output_nc.createVariable('latitude', 'f', latlongDims)
OutputLong = Output_nc.createVariable('longitude', 'f', latlongDims)
OutputBtime = Output_nc.createVariable('forecast_init_time', 'i',
        recordDims)
OutputStime = Output_nc.createVariable('stime', 'i', recordDims)
OutputEtime = Output_nc.createVariable('forcast_end_time', 'i',
        recordDims)

# Assign values to new netcdf file

OutputLat[:] = lat[:]
OutputLong[:] = long[:]

# Assing attribute values

attName = 'newAtt'
attValue = 'newAttValue'

# Lattiude description

setattr(OutputLat, 'descriptiveName', 'latitude')
setattr(OutputLat, 'units', 'degrees')
setattr(OutputLat, 'projectionType', 'LAMBERT_CONFORMAL')

# Longitude description

setattr(OutputLong, 'descriptiveName', 'longitude')
setattr(OutputLong, 'units', 'degrees')
setattr(OutputLong, 'projectionType', 'LAMBERT_CONFORMAL')

# Data value description

setattr(OutputValue, 'descriptiveName', 'Min Temperature between 3-17z')
setattr(OutputValue, 'units', 'F')
setattr(OutputValue, 'projectionType', 'LAMBERT_CONFORMAL')

# Btime description

setattr(OutputBtime, 'descriptiveName',
        'Model Initialization Time (UTC)')
setattr(OutputBtime, 'units', 'Epoch (seconds)')

# STime description

setattr(OutputStime, 'descriptiveName',
        'Model Forecast Start Time (UTC)')
setattr(OutputStime, 'units', 'Epoch (seconds)')

# ETime description

setattr(OutputEtime, 'descriptiveName', 'Model Forecast End Time (UTC)')
setattr(OutputEtime, 'units', 'Epoch (seconds)')

# NewTimes =  np.empty_like(value)
# NewTimes = np.empty([None, 476, 224], dtype=float)

NewTimes = []

BTimes = []
STimes = []
ETimes = []

# print NewTimes.shape

for i in range(00, len(btime[:])):

    BTimeObj = datetime.datetime.utcfromtimestamp(btime[i])
    STimeObj = datetime.datetime.utcfromtimestamp(stime[i])
    ETimeObj = datetime.datetime.utcfromtimestamp(etime[i])
    VTimeObj = datetime.datetime.utcfromtimestamp(vtime[i])

    if BTimeObj >= StartDate and BTimeObj <= EndDate:
        print 'btime ' + BTimeObj.isoformat()
        print 'stime ' + STimeObj.isoformat()
        print 'etime ' + ETimeObj.isoformat()
        print 'vtime ' + VTimeObj.isoformat()
        print 'Scale ' + str(scale[i])
        print 'Addit ' + str(addit[i])

        DataValue = value[i] * scale[i] + addit[i]

        BTimes.append(btime[i])
        STimes.append(stime[i])
        ETimes.append(etime[i])

        NewTimes.append(DataValue)

# Assing values

OutputValue[:] = np.array(NewTimes).astype('float32')

OutputBtime[:] = BTimes[:]
OutputStime[:] = STimes[:]
OutputEtime[:] = ETimes[:]

Output_nc.sync()

Output_nc.close()
