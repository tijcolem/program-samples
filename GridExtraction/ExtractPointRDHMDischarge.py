#!/usr/bin/python
# -*- coding: utf-8 -*-

from scipy.io import netcdf
import os
import sys
import datetime
import math
import time


def EpochTime(ObsTime):

    EpochStartTime = datetime.datetime(1970, 1, 1, 0)

    DeltaTime = ObsTime - EpochStartTime

    TotalSeconds = DeltaTime.days * 24 * 60 * 60 + DeltaTime.seconds

    return TotalSeconds


def recalculate_coordinate(val, _as=None):
    """
    Accepts a coordinate as a tuple (degree, minutes, seconds)
    You can give only one of them (e.g. only minutes as a floating point number)
    and it will be duly recalculated into degrees, minutes and seconds.
    Return value can be specified as 'deg', 'min' or 'sec'; default return value is
    a proper coordinate tuple.
  """

    (deg, min, sec) = val

  # pass outstanding values from right to left

    min = (min or 0) + int(sec) / 60
    sec = sec % 60
    deg = (deg or 0) + int(min) / 60
    min = min % 60

  # pass decimal part from left to right

    (dfrac, dint) = math.modf(deg)
    min = min + dfrac * 60
    deg = dint
    (mfrac, mint) = math.modf(min)
    sec = sec + mfrac * 60
    min = mint
    if _as:
        sec = sec + min * 60 + deg * 3600
        if _as == 'sec':
            return sec
        if _as == 'min':
            return sec / 60
        if _as == 'deg':
            return sec / 3600
    return (deg, min, sec)


def points2distance(start, end):
    """
    Calculate distance (in kilometers) between two points given as (long, latt) pairs
    based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
    Implementation inspired by JavaScript implementation from
    http://www.movable-type.co.uk/scripts/latlong.html
    Accepts coordinates as tuples (deg, min, sec), but coordinates can be given
    in any form - e.g. can specify only minutes:
    (0, 3133.9333, 0)
    is interpreted as
    (52.0, 13.0, 55.998000000008687)
    which, not accidentally, is the lattitude of Warsaw, Poland.
  """

    start_long = math.radians(recalculate_coordinate(start[0], 'deg'))
    start_latt = math.radians(recalculate_coordinate(start[1], 'deg'))
    end_long = math.radians(recalculate_coordinate(end[0], 'deg'))
    end_latt = math.radians(recalculate_coordinate(end[1], 'deg'))
    d_latt = end_latt - start_latt
    d_long = end_long - start_long
    a = math.sin(d_latt / 2) ** 2 + math.cos(start_latt) \
        * math.cos(end_latt) * math.sin(d_long / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371 * c


if len(sys.argv) != 5:
    print 'Usage:  1) Input path plus file name  2) Latitude(dec)  3) Longitude(dec)  4) Output path plus file name'
    print '        SiteID'
    exit()

UTCTime = datetime.datetime.utcnow()
print 'Running ParseMRRData.py at ' + UTCTime.isoformat()

InputFile = sys.argv[1]
Latitude = float(sys.argv[2])
Longitude = float(sys.argv[3])
OutputFile = sys.argv[4]

SiteLat = ((Longitude, 0, 0), (Latitude, 0, 0))
BaseOutputPath = '/home/dms7/workspace/Tim/'

try:
    print 'Opening file ' + InputFile
    FI_NetCDF = netcdf.netcdf_file(InputFile, 'r')
except:
    print 'Unable to open file ' + InputFile
    sys.exit()

try:

    Dis = FI_NetCDF.variables['discharge']
    Time = FI_NetCDF.variables['time']
    Lat = FI_NetCDF.variables['lat']
    Long = FI_NetCDF.variables['lon']
except:

    print 'Unable to access netcdf variables in ' + InputFile
    sys.exit()

try:
    FO = open(OutputFile, 'wb')
except:
    print 'Unable to write file ' + OutputFile
    sys.exit()

# Intitally set the distance to a high number

CurrentDiff = 500

for i in range(0, len(Long[0])):

    for t in range(0, len(Lat[0])):

        GridLatLong = ((Long[i][t], 0, 0), (Lat[i][t], 0, 0))

        Diff = points2distance(SiteLat, GridLatLong)

        if Diff < CurrentDiff:

            CurrentDiff = Diff
            SiteGridPoints = [i, t]

print 'Closest grid point is ' + str(CurrentDiff) \
    + ' km away from target. Writing discharge for closest grid point'

FO.write('DateTime (UTC), Discharge (cms)\n')

for i in range(0, len(Time[:])):
    EpochTime = Time[i] * 60
    t1 = time.gmtime(EpochTime)
    TimeString = '%02d-%02d-%4d %02d:%02d:%02d' % (
        t1.tm_mon,
        t1.tm_mday,
        t1.tm_year,
        t1.tm_hour,
        t1.tm_min,
        t1.tm_sec,
        )
    OutputString = TimeString + ',' \
        + str(Dis[i][SiteGridPoints[0]][SiteGridPoints[1]])
    FO.write(OutputString)
    FO.write('\n')

FO.close()
