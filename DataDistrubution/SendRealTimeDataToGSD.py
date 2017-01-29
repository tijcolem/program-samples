#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import ftplib
import time
import sys
import re

if len(sys.argv) != 3:
    print 'Usage: requires two arguments. 1.) file containing site listing,  2.) # of hours to backfill (max 24)'
    exit()

if int(sys.argv[2]) > 24:
    print 'Max of 24hr backfill exceeded'
    exit()

SiteList = sys.argv[1]  # Define FTP get directory

HoursFill = int(sys.argv[2])  # Define hours to backfill


def calhr(i, hr):  # function to calc hours
    if hr - i < 0:
        return 24 + hr - i
    else:
        return hr - i


def calday(i, hr, day):  # function to calc days
    if day == 0:
        return day
    if hr - i < 0:
        return day - 1
    else:
        return day


PutPath = '/pub/psd'  # FTP put directory
BasePath = '/data'  # define source base path. Some thing to test

FTPServer = 'gpsdmz.fsl.noaa.gov'
User = '***'
Pass = '***'
Success = 1

# define source file paths

SourcePaths = {
    '915Wind': [BasePath + '\\Radar915\\CnsWind', '%s%02d%03d.%02d%s',
                'w'],
    '915WwWind': [BasePath + '\\Radar915\\WwWind', '%s%02d%03d.%02d%s',
                  'w'],
    '915Temp': [BasePath + '\\Radar915\\CnsTemp', '%s%02d%03d.%02d%s',
                't'],
    '915Snow': [BasePath + '\\Radar915\\BrightBand',
                '%s%02d%03d%02d.snw%s', ''],
    '449Wind': [BasePath + '\\Radar449\\CnsWind', '%s%02d%03d.%02d%s',
                'w'],
    '449WwWind': [BasePath + '\\Radar449\\WwWind', '%s%02d%03d.%02d%s',
                  'w'],
    '449Temp': [BasePath + '\\Radar449\\CnsTemp', '%s%02d%03d.%02d%s',
                't'],
    '449Snow': [BasePath + '\\Radar449\\BrightBand',
                '%s%02d%03d%02d.snw%s', ''],
    '3000Mom': [BasePath + '\\Radar3000\\PopMoments',
                '%s%02d%03d%02d.raw%s', ''],
    '3000Snow': [BasePath + '\\Radar3000\\BrightBand',
                 '%s%02d%03d%02d.snw%s', ''],
    'SurfMet': [BasePath + '\\CsiDatalogger\\SurfaceMet',
                '%s%02d%03d.%02d%s', 'm'],
    }

utctime = time.gmtime()  # get current time

try:
    fileobj = open(SiteList, 'rb')
except:
    print 'Error, cannot open site list file',
    print sys.exc_info()[1]
    exit()

try:
    f = ftplib.FTP(FTPServer, User, Pass)
    f.cwd(PutPath)
except:
    print 'FTP Error ',
    print sys.exc_info()[1]
    exit()

SourcePathKeys = SourcePaths.keys()
SourcePathKeys.sort()

SiteContents = fileobj.readlines()

for line in SiteContents:

    element = re.split('|', line)

    site = (element[0])[0:3].lower()

    for key in SourcePathKeys:

        for i in range(HoursFill):  # specify the range in hours up to 24

            File = SourcePaths[key][1] % (site, utctime[0] % 100,
                    calday(i, utctime[3], utctime[7]), calhr(i,
                    utctime[3]), SourcePaths[key][2])  # placeholder in array for year
                                                       # call calendar year function
                                                       # call hour function

            InputFile = SourcePaths[key][0] + '\\' + site + '\\' \
                + str(utctime[0]).zfill(4) + '\\' + str(calday(i,
                    utctime[3], utctime[7])).zfill(3) + '\\' + File

            if os.path.isfile(InputFile):

                try:
                    f.storbinary('STOR ' + os.path.basename(InputFile),
                                 open(InputFile, 'rb'))  # Send the file
                except:
                    print 'Error, trying to transfer ' + InputFile
                    print sys.exc_info()[1]
                    Success = 0

if Success:
    print 'All files transfered successfully from ' + BasePath + ' to ' \
        + FTPServer + PutPath,
else:
    print 'Error transferring one or more files from ' + BasePath \
        + ' to ' + FTPServer + PutPath + ' check error log for file'

# Close FTP connection & fileobj

f.close()
fileobj.close()
