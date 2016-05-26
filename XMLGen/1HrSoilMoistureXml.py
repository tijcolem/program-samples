#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import os
import sys
import glob
import re
import math
import smtplib
import base64

from collections import defaultdict


def GetSoilMoisture(
    Site,
    Path,
    SoilMoistureIndex,
    BeginDate,
    EndDate,
    SampleRate,
    ):

    Records = []
    Temp = 0.
    YearIndex = 1
    JdayIndex = 2
    HrMinIndex = 3
    RecDateString = ''
    AbsMinAcceptanceSampleTime = 5
    Flag = 0
    Counter = 0

    while BeginDate < EndDate:

        InputFile = '%s/%04d/%03d/%s%02d%03d.%02dm' % (
            Path,
            BeginDate.tm_year,
            BeginDate.tm_yday,
            Site,
            BeginDate.tm_year % 100,
            BeginDate.tm_yday,
            BeginDate.tm_hour,
            )

        if os.path.exists(InputFile):

            try:
                fileobj = open(InputFile, 'rb')
            except:
                print 'cannot open file ' + OutputFile
                return (-9999, BeginDate)

            FileContents = fileobj.readlines()

            if float(SampleRate) > 0:

                AbsSampleCompletion = float(len(FileContents)
                        / float(SampleRate)) * 60
            else:
                AbsSampleCompletion = 0

            if AbsSampleCompletion < AbsMinAcceptanceSampleTime:  # QC check. Must have correct amount of samples to be counted.
                print InputFile
                print ' Did not meet sample rate '
                print ' Number of samples: '
                print len(FileContents)
                return (-9999, BeginDate)

            for line in FileContents:
                Records.append(line)
            fileobj.close()

            for i in range(len(Records)):

                try:

                    Fields = re.split(',', Records[i])

                    Hour = int(Fields[HrMinIndex]) / 100

                    Minute = int(Fields[HrMinIndex]) - int(Hour * 100.)

                    RecDateString = '%d%03d%02d%02d' \
                        % (int(Fields[YearIndex]),
                           int(Fields[JdayIndex]), Hour, Minute)

                    RecDate = time.strptime(RecDateString, '%Y%j%H%M')

                    RecDate = TimeOffset(RecDate, 0)  # For correct flag setting in time tuple tm_dst needs to = 0.
                except:

                    print 'Parse error on file'
                    print InputFile
                    return (-9999, BeginDate)

                if RecDate > EndDate:
                    break

                if RecDate >= BeginDate and RecDate < EndDate:

                    if len(Fields) >= SoilMoistureIndex:

                        try:
                            SoilMoisture = \
                                float(Fields[SoilMoistureIndex])
                        except:
                            print 'Unable to float data element in column ' \
                                + SoilMoisture + ' in file ' + InputFile

                        if SoilMoisture < -100. or float(SoilMoisture) \
                            > 100:  #  QC check for any invalids
                            print 'Invalid Found in Sample Set'
                            print InputFile
                            return (-9999, RecDate)
                    else:
                        print 'Incomplete record on file ' + InputFile
                        return (-9999, BeginDate)
        else:

            print InputFile + " doesn't exist, skipping " + Site
            return (-9999, BeginDate)

        BeginDate = TimeOffset(BeginDate, 1)

    return (SoilMoisture, RecDate)


def TimeOffset(timeobj, hrsoffset):

    offset = hrsoffset * 3600

    timeobj = time.mktime(timeobj)

    timeobj += offset

    timeobj = time.localtime(timeobj)

    return timeobj

	
def SendEmailAlert(Message):

    EmailServer = 'test.server.com'  # email server
    EmailUser = 'test.user@server.com'  # email user for server authentication
    EmailSender = 'test.user@server.com'  # email sender
    EmailData = 'JEBwcGgxcmUkNHUh'

    EmailRecipients = ['user1@someserver.com',
                       'user1@someserver.com']

    EmailMessage = \
        '''From: User <test.user@server.com>
Subject: Some Subject

''' \
        + Message

    data = base64.b64decode(EmailData)

    server = smtplib.SMTP(EmailServer)

    server.helo(EmailServer)

    for EmailRecip in EmailRecipients:

        print ('Sending email data alert to: ', EmailRecip)

        server.sendmail(EmailSender, EmailRecip, EmailMessage)

    server.quit()


print 'Running Temperature_xml.py on ' + time.ctime() + '\n'

# All Varaibles used in main

Temp = 0.
SoilMoistureSites = {}
SoilMoistureIndex = defaultdict(list)
SoilMoistureFilePath = '/data/realtime/CsiDatalogger/SurfaceMet/'
RealTimePath = '/data/realtime/MapOverlays/SoilMoisture/'
IconBasePath = \
    'http://www.somepath.com'

SoilMoistureSaturation = {
    'czc': 25.165,
    'hbg': 36.527,
    'hld': 24.179,
    'lsn': 34.047,
    'ptv': 37.257,
    'rod': 45.893,
    'wls': 31.538,
    }

SoilMoistureLevels = [
    5,
    10,
    15,
    20,
    30,
    50,
    100,
    ]

try:
    db = MySQLdb.connection(host='host', user='user',
                            passwd='passwd!', db='db')
except:
    print "Error connecting to psdmeta MySQL DB"
    SendEmailAlert("Error connecting to psdmeta MySQL DB")

    sys.exit()

db.query("""
Select site_has_inst.SiteID, site.Latitude, site.Longitude, site.Elevation, site.City, site.State, COUNT(site_has_inst.TypeID) as InstCount
From site_has_inst, site, inst_manufacturer, inst_type
Where inst_type.TypeID = site_has_inst.TypeID
AND site_has_inst.SiteID = site.SiteID
AND inst_manufacturer.ManufacturerID = inst_type.ManufacturerID
AND inst_type.CategoryID IN (26)
AND site.RealTimeDisplay = 'Y'
AND site_has_inst.Active = 'Y'
AND site_has_inst.InstRemovalDate is null
AND site_has_inst.SiteID in ('czc', 'hbg', 'hld', 'lsn', 'ptv', 'rod', 'wls') 
group by site_has_inst.SiteID;
""")

r = db.store_result()

for row in r.fetch_row(0):
    SoilMoistureSites[row[0]] = [
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        ]

# 0) Latitude
# 1) Longitude
# 2) Elevation
# 3) City
# 4) State
# 5) Instrument Type Name
# 6) Instrument Manf
# 7) Insturment Sample Rate

for site in SoilMoistureSites.keys():

    SoilQuery = \
        'Select site_has_inst.SiteID, site_has_inst_data.DataFormatFile, site_has_inst_data.SampleRatePerhour \
	From site_has_inst, site_has_inst_data, inst_type \
	Where site_has_inst.OperationalID = site_has_inst_data.OperationalID \
	AND inst_type.TypeID = site_has_inst.TypeID \
	AND site_has_inst_data.DataTypeID = 14 \
	AND inst_type.CategoryID = 2 \
	AND site_has_inst_data.EndDate is null \
	AND site_has_inst.SiteID = \'' \
        + site + '\';'

    db.query(SoilQuery)

    result = db.store_result()

    for line in result.fetch_row(0):

        try:
            LineData = re.split(',', line[1])
        except:
            print 'No data file format found for site ' + site
            continue

        for i in range(len(LineData)):
            DataElement = LineData[i].lstrip().rstrip()
            if DataElement.find('Volumetric Water Content') >= 0 \
                or DataElement.find('Wetness Fraction') >= 0:
                Level = -9999
                if DataElement.find('5cm') >= 0:
                    Level = 5
                if DataElement.find('10cm') >= 0:
                    Level = 10
                if DataElement.find('15cm') >= 0:
                    Level = 15
                if DataElement.find('20cm') >= 0:
                    Level = 20
                if DataElement.find('20cm') >= 0:
                    Level = 30
                if DataElement.find('50cm') >= 0:
                    Level = 50
                if DataElement.find('100cm') >= 0:
                    Level = 100

                # i = Column Number in format, DataElement = Name of Column, Numeric Level of Soil, Sample Rate

                SoilMoistureIndex[site].append([i, DataElement, Level,
                        line[2]])

# Get Current Time

EndTime = time.strftime('%Y,%j%H', time.gmtime())

EndTime = time.strptime(EndTime, '%Y,%j%H')

# EndTime = "2014,04001"

EndTime = TimeOffset(EndTime, 0)

StartHourTime = TimeOffset(EndTime, -1)  # since using Hour as start time.

OutPutPath = '%s%04d/%03d/' % (RealTimePath, StartHourTime.tm_year,
                               StartHourTime.tm_yday)

if not os.path.exists(OutPutPath):
    try:
        print 'Creating Dir ' + OutPutPath
        os.makedirs(OutPutPath)
    except:
        print 'Failed to create dir ' + OutPutPath
        print 'Exiting'
        sys.exit()

for Level in SoilMoistureLevels:

    OutPutFile = '%s%04d/%03d/%02dSoilMoisture_%02d%03d%02d.xml' % (
        RealTimePath,
        StartHourTime.tm_year,
        StartHourTime.tm_yday,
        Level,
        StartHourTime.tm_year % 100,
        StartHourTime.tm_yday,
        StartHourTime.tm_hour,
        )

    try:
        FO = open(OutPutFile, 'wb')
    except:
        print "Error writing file: " + OutPutFile

        sys.exit()

    FO.write('<markers>')
    FO.write('\n')


    for Site in SoilMoistureIndex.keys():

        print "Processing " + Site
        SoilMoisturePath = SoilMoistureFilePath + Site

        for Index in SoilMoistureIndex[Site]:

            SoilLevel = Index[2]

            if SoilLevel == Level:

                IndexNumber = Index[0]
                ColumnLablel = Index[0]
                SoilLevel = Index[2]
                SampleRate = Index[3]

                SoilMoisturePath = SoilMoistureFilePath + Site

                BeginTime = TimeOffset(EndTime, -1)

                (SoilMoisture, Time) = GetSoilMoisture(
                    Site,
                    SoilMoisturePath,
                    IndexNumber,
                    BeginTime,
                    EndTime,
                    SampleRate,
                    )

                SoilMoisture = SoilMoisture \
                    / SoilMoistureSaturation[Site] * 100

                SoilMoisture = round(SoilMoisture, 0)

                if SoilMoisture != -9999:

                    TimeString = '%04d-%02d-%02d %02d:%02d' \
                        % (Time.tm_year, Time.tm_mon, Time.tm_mday,
                           Time.tm_hour, Time.tm_min)
                else:
                    TimeString = ' '

                if SoilMoisture < 25 and SoilMoisture > 0:
                    IconPath = IconBasePath + 'bucket00.png'
                elif SoilMoisture >= 25 and SoilMoisture < 50:
                    IconPath = IconBasePath + 'bucket25.png'
                elif SoilMoisture >= 50 and SoilMoisture < 75:
                    IconPath = IconBasePath + 'bucket50.png'
                elif SoilMoisture >= 75 and SoilMoisture < 100:
                    IconPath = IconBasePath + 'bucket75.png'
                elif SoilMoisture >= 100:
                    IconPath = IconBasePath + 'bucket100.png'
                else:

                    IconPath = IconBasePath + '-9999.00.png'

                SoilMoisture = '%.0f' % SoilMoisture
                InfoBox = 'Soil Moisture Saturation = %s (%%)' \
                    % SoilMoisture

                FO.write('<marker ')
                FO.write('siteID="')
                FO.write(Site)
                FO.write('" name="')
                FO.write(SoilMoistureSites[Site][3])
                FO.write('" lat="')
                FO.write(SoilMoistureSites[Site][0])
                FO.write('" lng="')
                FO.write(SoilMoistureSites[Site][1])
                FO.write('" elev="')
                FO.write(SoilMoistureSites[Site][2])
                FO.write('" soilmoisture="')
                FO.write(SoilMoisture)
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

# print 'Finshed Running Temperature_xml.py on ' + time.ctime() + '\n'

