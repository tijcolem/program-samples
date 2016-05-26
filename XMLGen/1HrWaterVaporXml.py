#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import os
import sys
import glob
import re
import math


def GetWaterVaporNew(
    Site,
    Path,
    IwvIndex,
    BeginDate,
    EndDate,
    ):

    Records = []
    Temp = 0.0
    YearIndex = 0
    JdayIndex = 0
    HrMinIndex = 1
    RecDateString = ''
    Flag = 0
    Counter = 0

    for i in range(3):

        InputFile = '%s/%04d/%03d/%s%02d%03d.txt' % (
            Path,
            BeginDate.tm_year,
            BeginDate.tm_yday,
            Site,
            BeginDate.tm_year % 100,
            BeginDate.tm_yday,
            )

        if os.path.exists(InputFile):

            try:
                fileobj = open(InputFile, 'rb')
            except:
                print 'cannot open file ' + OutputFile
                return (-8888, BeginDate)

            FileContents = fileobj.readlines()

            for line in FileContents:
                Records.append(line)
            fileobj.close()

            for line in reversed(Records):

                try:

                    Fields = re.split(',', line)

                    Year = int((Fields[YearIndex])[0:2])
                    Jday = int((Fields[JdayIndex])[2:5])
                    Hour = int((Fields[HrMinIndex])[0:2])
                    Min = int((Fields[HrMinIndex])[3:5])
                    RecDateString = '%d%03d%02d%02d' % (Year, Jday,
                            Hour, Min)

                    RecDate = time.strptime(RecDateString, '%y%j%H%M')

                    RecDate = TimeOffset(RecDate, 0)  # For correct flag setting in time tuple tm_dst needs to = 0.
                except:

                    print 'Parse error on file'
                    print InputFile
                    return (-8888, BeginDate)

                if RecDate.tm_hour == BeginDate.tm_hour:
                    if len(Fields) > IwvIndex:

                        if float(Fields[IwvIndex]) >= 0.0:
                            return (float(Fields[IwvIndex]), RecDate)
                    else:

                        print 'Incomplete record on file ' + InputFile
                        return (-8888, BeginDate)
        else:

            print InputFile + " doesn't exist, skipping " + Site
            return (-8888, BeginDate)

        BeginDate = TimeOffset(BeginDate, -1)
        Records = []

    return (-9999, RecDate)


def TimeOffset(timeobj, hrsoffset):

    offset = hrsoffset * 3600

    timeobj = time.mktime(timeobj)

    timeobj += offset

    timeobj = time.localtime(timeobj)

    return timeobj


# All Varaibles used in main

print 'Running 1HrWaterVaporXml.py on ' + time.ctime() + '\n'

WaterVapor = 0.0
IwvIndex = 2
WaterVaporSites = {}
XmlOutPutPath = '/home/httpd/html/obs/sitemap/psdmapdata/'
RealTimePath = '/data/realtime/MapOverlays/WaterVapor/'
IconBasePath = \
    'http://www.somepath.com'

db = MySQLdb.connection(host='host', user='user',
                        passwd='passwd!', db='db')

db.query("""Select site_has_inst.SiteID, site.Latitude, site.Longitude, site.Elevation, site.City, site.State, inst_category.Name, inst_type.RealtimeBaseDirName
From site_has_inst, site, inst_category, inst_type
Where inst_type.TypeID = site_has_inst.TypeID
AND site_has_inst.SiteID = site.SiteID
AND inst_type.CategoryID = inst_category.CategoryID
AND inst_type.CategoryID IN (5)
AND site.RealTimeDisplay = 'Y'
AND site_has_inst.Active = 'Y'
AND site_has_inst.InstRemovalDate is null; """)
r = db.store_result()

for row in r.fetch_row(0):
    WaterVaporSites[row[0]] = [
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[7],
        ]

WaterVaporSites.keys().sort()

EndTime = time.strftime('%Y,%j%H', time.gmtime())

EndTime = time.strptime(EndTime, '%Y,%j%H')

EndTime = TimeOffset(EndTime, 0)

StartHourTime = TimeOffset(EndTime, -1)  # since using Hour as start time.

OutPutPath = '%s%04d/%03d/' % (RealTimePath, StartHourTime.tm_year,
                               StartHourTime.tm_yday)

OutPutFile = '%s%04d/%03d/WaterVapor_%02d%03d%02d.xml' % (
    RealTimePath,
    StartHourTime.tm_year,
    StartHourTime.tm_yday,
    StartHourTime.tm_year % 100,
    StartHourTime.tm_yday,
    StartHourTime.tm_hour,
    )

OutPutFileOld = '%sWaterVapor_%02d%03d%02d.xml' % (RealTimePathOld,
        StartHourTime.tm_year % 100, StartHourTime.tm_yday,
        StartHourTime.tm_hour)

if not os.path.exists(OutPutPath):
    try:
        print 'Creating Dir ' + OutPutPath
        os.makedirs(OutPutPath)
    except:
        print 'Failed to create dir ' + OutPutPath

FO = open(OutPutFile, 'wb')

FO.write('<markers>')
FO.write('\n')

for site in WaterVaporSites.keys():

    WaterVaporPath = '/data/realtime/GpsTrimble/WaterVapor/' + site

    (WaterVapor, Time) = GetWaterVaporNew(site, WaterVaporPath,
            IwvIndex, StartHourTime, EndTime)

    WaterVapor = round(WaterVapor, 2)

    if float(WaterVapor) != -8888.00:

        TimeString = '%04d-%02d-%02d %02d:%02d' % (Time.tm_year,
                Time.tm_mon, Time.tm_mday, Time.tm_hour, Time.tm_min)
    else:

        TimeString = ' '

    WaterVapor = '%.02f' % WaterVapor

    IconPath = IconBasePath + WaterVapor + '.png'
    InfoBox = 'IWV = %s (cm)' % WaterVapor

    FO.write('<marker ')
    FO.write('siteID="')
    FO.write(site)
    FO.write('" name="')
    FO.write(WaterVaporSites[site][3])
    FO.write('" lat="')
    FO.write(WaterVaporSites[site][0])
    FO.write('" lng="')
    FO.write(WaterVaporSites[site][1])
    FO.write('" elev="')
    FO.write(WaterVaporSites[site][2])
    FO.write('" watervapor="')
    FO.write(WaterVapor)
    FO.write('" begintime="')
    FO.write(TimeString)
    FO.write('" endtime="')
    FO.write(TimeString)
    FO.write('" icon="')
    FO.write(IconPath)
    FO.write('" infobox="')
    FO.write(InfoBox)
    FO.write('" />')
    FO.write('\n')

FO.write('</markers>')

FO.close()

Command1 = 'cp ' + OutPutFile + ' ' + OutPutFileOld
print Command1

os.system(Command1)

print 'Finshed Running 1HrWaterVaporXml.py on ' + time.ctime() \
    + '\n'
