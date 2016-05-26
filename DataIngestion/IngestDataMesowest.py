#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xml.dom.minidom
import urllib2
import datetime
import math
import shutil
import os
import time
import re


def ReadWebContent(UrlLink):

    try:

        ContentObj = urllib2.urlopen(UrlLink, timeout=120)

        WebContent = ContentObj.read()
    except:

        print 'Unable to open ' + UrlLink
        print sys.exec_info()
        WebContent = ''

    return WebContent


def TimeOffset(Time, HrsOffset):

    Time = Time + datetime.timedelta(hours=HrsOffset)

    return Time


def TimeDiff(TimeOne, TimeTwo):

    TimeDelta = TimeOne - TimeTwo

    SecondsDelta = TimeDelta.days * 24 * 60 * 60 + TimeDelta.seconds

    return SecondsDelta


# Define paths

WorkPath = \
    'C:/Program Files/ESRL Applications/IngestScripts/IngestFrostForecastData/Downloads/'
MesowestDataZiped = \
    'C:/Program Files/ESRL Applications/IngestScripts/IngestFrostForecastData/Downloads/mesowest.dat.gz'
MesowestMetaZiped = \
    'C:/Program Files/ESRL Applications/IngestScripts/IngestFrostForecastData/Downloads/mesowest_csv.tbl.gz'
MesowestData = \
    'C:/Program Files/ESRL Applications/IngestScripts/IngestFrostForecastData/Downloads/mesowest.dat'
MesowestMeta = \
    'C:/Program Files/ESRL Applications/IngestScripts/IngestFrostForecastData/Downloads/mesowest_csv.tbl'
MesowestDataUrl = 'http://mesowest.utah.edu/data/mesowest.dat.gz'
MesowestMetaUrl = 'http://mesowest.utah.edu/data/mesowest_csv.tbl.gz'
MesowestHistoryFile = \
    'C:/Program Files/ESRL Applications/IngestScripts/IngestFrostForecastData/History/MesowestHistory.dat'
ObsdumpOutputPath = '\\\\awipslx1.psd.esrl.noaa.gov\\data\\obsdump\\'
HistoryObsdumpOutputPath = \
    '\\Program Files\\ESRL Applications\\IngestScripts\\IngestFrostForecastData\\History\\data\\'

LineCount = 0
MesowestDataEnable = 0  # Set to 0 by default. If Mesowest meta file download then to 1

# Define Indexes in Mesowest Data

SiteIdIndex = 0
LatIndex = 1
LongIndex = 2
ElevIndex = 3
TimeIndex = 5
TempIndex = 6  # Temperature (F)
RHIndex = 7  # Relative Humidity
WindSpeedIndex = 8  # Wind Speed (kts)
WindGustIndex = 9  # Gust (kts)
WindDirIndex = 10  # Wind Direction
DewPointIndex = 12  # Dew Point (F)

DataDict = {}
HistoryDataDic = {}
MesowestMetaDict = {}
MesowestDataDic = {}

# Derived Variables

DD = ''

# Domain to extract data for

NorthLat = 40
SouthLat = 37
WestLong = -123
EastLong = -121



# Get UTC time

UTCTime = datetime.datetime.utcnow()

print 'Running IngestDataMesowest.py on ' + UTCTime.isoformat() + ' utc'

os.chdir(WorkPath)

# Get Mesowest Data

try:
    FO = open(MesowestDataZiped, 'wb')
    FO.write(ReadWebContent(MesowestDataUrl))
    FO.close()
except:
    print 'Unable to download Mesowest Data from ' + MesowestDataUrl
    print 'Exiting program'
    sys.exit()

# Get Mesowest Meta Data

try:
    FO = open(MesowestMetaZiped, 'wb')
    FO.write(ReadWebContent(MesowestMetaUrl))
    FO.close()
except:
    print 'Unable to download Mesowest Meta from ' + MesowestDataUrl
    print 'Will not output specfic meta details for site. Continuing program'
    sys.exit()

# Command to unzip data

UnzipMesowestDataCommand = 'gzip -df ' \
    + '"C:/Program Files/ESRL Applications/IngestScripts/IngestFrostForecastData/Downloads/mesowest.dat.gz"'
UnzipMesowestMetaCommand = 'gzip -df ' \
    + '"C:/Program Files/ESRL Applications/IngestScripts/IngestFrostForecastData/Downloads/mesowest_csv.tbl.gz"'

time.sleep(3)  #

try:
    print 'Unzipping ' + MesowestDataZiped
    print UnzipMesowestDataCommand
    os.system(UnzipMesowestDataCommand)
    print 'Unziped'
except:
    print 'Unable extract Mesowest data file ' + MesowestData
    print 'Exiting program'
    sys.exit()

try:
    print 'Unzipping ' + MesowestMetaZiped
    print UnzipMesowestMetaCommand
    os.system(UnzipMesowestMetaCommand)
    print 'Unziped'
except:
    print 'Unable to extract Mesowest meta file'
    print 'Will not output specfic meta details for site. Continuing program'
    sys.exit()

# Open and read in site contents

try:
    print 'Opening Mesowest meta file ' + MesowestMeta
    FI = open(MesowestMeta, 'rb')
    MesowestMetaContents = FI.readlines()
    FI.close()
    MesowestDataEnable = 1
except:
    print 'Unable to open Mesowest Meta data file ' + MesowestMeta
    print 'Will not write out specfic meta entries to files'

try:
    print 'Opening Mesowest meta file ' + MesowestData
    FI = open(MesowestData, 'rb')
    MesowestDataContents = FI.readlines()
    FI.close()
except:
    print 'Unable to open Mesowest data file ' + MesowestMeta
    print 'Exiting program'
    sys.exit()

# Populate Meta data into dictionary

LineCount = 0
if MesowestDataEnable == 1:
    for Line in MesowestMetaContents:
        if LineCount != 0:  # Skip Header
            Elements = Line.split(',')
            if len(Elements) > 2:
                MesowestMetaDict[Elements[0]] = Elements[2]
            else:
                continue
        LineCount += 1

LineCount = 0

PrevSiteID = ''

print 'Parsing Mesowest data contents'
for Line in MesowestDataContents:

    if LineCount < 3:  # Skip header

        LineCount += 1

        continue

    Elements = Line.split(',')

    if len(Elements) > 50:

        try:
            SiteID = Elements[SiteIdIndex]
            Lat = float(Elements[LatIndex])
            Long = float(Elements[LongIndex])
            Elev = Elements[ElevIndex]
            Time = Elements[TimeIndex]
            T = Elements[TempIndex]
            RH = Elements[RHIndex]
            WGust = Elements[WindGustIndex]
            Td = Elements[DewPointIndex]
            WS = Elements[WindSpeedIndex]
            WD = Elements[WindDirIndex]
        except:

            print sys.exc_info()
            print 'Unable to parse line number ' + str(LineCount)
            print 'continuing'
            continue

        if MesowestDataEnable == 1:

            try:

                SiteName = MesowestMetaDict[SiteID]
            except:
                sys.exc_info()
                SiteName = ''
        else:

            SiteName = ''

        try:

            TimeObj = datetime.datetime.strptime(Time, '%Y%m%d/%H%M')
        except:

            print Time
            print 'Unable to convert time string to datetime object time for SiteID ' \
                + SiteID
            TimeObj = UTCTime

        if T != '':
            try:
                T = float(T)
                T = round(T)
                if T < 150 and T > -50:
                    T = '%.0f' % T
                else:
                    T = ''
            except:
                T = ''

        if Td != '':
            try:
                Td = float(Td)
                Td = round(Td)
                if Td < 150 and Td > -50:
                    Td = '%.0f' % Td
                else:
                    Td = ''
            except:
                TD = ''

        if T != '' and Td != '':
            DD = round(float(T) - float(Td))
            DD = '%.0f' % DD

        if WS != '':
            try:
                WS = round(float(WS))
                if WS > 0 or WS < 150:
                    WS = '%.0f' % WS
                else:
                    WS = ''
            except:
                WS = ''

        if WGust != '':
            try:
                WGust = round(float(WGust))
                if WGust > 0 and WGust < 150:
                    WGust = '%.0f' % WGust
                else:
                    WGust = ''
            except:
                WGust = ''

        if WD != '':
            try:
                WD = round(float(WD))
                if WD >= 0 and WD <= 360:
                    WD = '%.0f' % WD
                else:
                    WD = ''
            except:
                WD = ''

        if Lat <= NorthLat and Lat >= SouthLat and Long >= WestLong \
            and Long <= EastLong:

            if TimeDiff(UTCTime, TimeObj) < 43200:  # Check for data in previous 12 hours

                OfficalRecordTime = '%04d%02d%02d%02d%02d' \
                    % (TimeObj.timetuple().tm_year,
                       TimeObj.timetuple().tm_mon,
                       TimeObj.timetuple().tm_mday,
                       TimeObj.timetuple().tm_hour,
                       TimeObj.timetuple().tm_min)

                SampleHourTime = '%04d%02d%02d%02d' \
                    % (TimeObj.timetuple().tm_year,
                       TimeObj.timetuple().tm_mon,
                       TimeObj.timetuple().tm_mday,
                       TimeObj.timetuple().tm_hour)

                HourTimeObj = \
                    datetime.datetime.strptime(SampleHourTime,
                        '%Y%m%d%H')

                TimeDifference = TimeDiff(TimeObj, HourTimeObj)

                if TimeDifference >= 2700:  # 45-60 min past the hour will be rounded to next hour.

                    TimeObj = TimeOffset(TimeObj, 1)

                LineOut = '%s,%s CA US,%2.4f,%3.4f,%s,%s,%s,%s,%s,%s\n' \
                    % (
                    '{0: >5}'.format(SiteID),
                    '{0: <33}'.format(SiteName[:33]),
                    Lat,
                    Long,
                    Elev,
                    T,
                    Td,
                    WD,
                    WS,
                    WGust,
                    )
                ID = '%04d%02d%02d%02d00%s' \
                    % (TimeObj.timetuple().tm_year,
                       TimeObj.timetuple().tm_mon,
                       TimeObj.timetuple().tm_mday,
                       TimeObj.timetuple().tm_hour, SiteID)
                ObsDumpTime = '%04d%02d%02d%02d00' \
                    % (TimeObj.timetuple().tm_year,
                       TimeObj.timetuple().tm_mon,
                       TimeObj.timetuple().tm_mday,
                       TimeObj.timetuple().tm_hour)
                MesowestDataDic[ID] = [ID, ObsDumpTime,
                        OfficalRecordTime, LineOut]  # Store Data in Dictionary

        LineCount += 1

        SiteID = Lat = Long = Elev = Time = T = RH = WGust = Td = WS = \
            WD = DD = ''  # Reset Variables
    else:

        print 'Skiping line ' + Line
        LineCount += 1
        continue

LineCount = 0

# Read in History File and check for differences.

try:
    print 'Opening history file ' + MesowestHistoryFile
    FI = open(MesowestHistoryFile, 'rb')
    HistoryContents = FI.readlines()
    FI.close()
except:
    print 'No History file. All records are considered new.'
    HistoryContents = ''

# Load in History contents used to check for new records. # Store in Unqiue id. Time + SiteID

for Line in HistoryContents:

    Elements = Line.split('\t')

    if len(Elements) > 2:
        HistoryDataDic[Elements[0]] = [Elements[1], Elements[2]]
    else:
        continue

# Write out current data to obs dump

LineCount = 0

for ID in sorted(MesowestDataDic.keys()):

    if not ID in HistoryDataDic.keys():
        LineCount += 1

        HistoryFileName = HistoryObsdumpOutputPath \
            + MesowestDataDic[ID][1] + '.dat'

        try:
            print 'Writing out data for ID ' + ID + ' to file ' \
                + HistoryFileName
            FOH = open(HistoryFileName, 'ab')
            FOH.write(MesowestDataDic[ID][3])
            FOH.close()
        except:
            print 'Unable to append file ' + HistoryFileName
            print sys.exc_info()
            print 'Continuing'

        # Add to history dict

        HistoryDataDic[ID] = [MesowestDataDic[ID][2],
                              MesowestDataDic[ID][3]]

print str(LineCount) + ' New Entries'

# Write out new 24hr history file

UTCTimeMinusDay = TimeOffset(UTCTime, -24)

try:
    FO = open(MesowestHistoryFile, 'wb')
except:
    print 'Unable to write to history file ' + MesowestHistoryFile
    print 'Exiting'
    sys.exit()

for ID in sorted(HistoryDataDic.keys()):

    HistoryTime = datetime.datetime.strptime(ID[:10], '%Y%m%d%H')

    if HistoryTime > UTCTimeMinusDay:  # Only keep 24 hour history file

        FO.write(ID)
        FO.write('\t')
        FO.write(HistoryDataDic[ID][0])
        FO.write('\t')
        FO.write(HistoryDataDic[ID][1])

FO.close()

print 'Finished running IngestMesowestData'

sys.exit()
