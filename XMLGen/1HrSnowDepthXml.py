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


def GetSnowDepth(
    Site,
    Path,
    SnowDepthIndex,
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
                return (-8888, BeginDate)

            FileContents = fileobj.readlines()

            if SampleRate > 0:

                AbsSampleCompletion = float(len(FileContents)
                        / float(SampleRate)) * 60
            else:
                AbsSampleCompletion = 0

            if AbsSampleCompletion < AbsMinAcceptanceSampleTime:  # QC check. Must have correct amount of samples to be counted.
                print InputFile
                print ' Did not meet sample rate '
                print ' Number of samples: '
                print len(FileContents)
                return (-8888, BeginDate)

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
                    return (-8888, BeginDate)

                if RecDate > EndDate:
                    break

                if RecDate >= BeginDate and RecDate < EndDate:

                    if len(Fields) >= SnowDepthIndex:

                        if float(Fields[SnowDepthIndex]) >= -100.:
                            SnowDepth = float(Fields[SnowDepthIndex])

                        if float(Fields[SnowDepthIndex]) < 0. \
                            or float(Fields[SnowDepthIndex]) > 30:  #  QC check for any invalids
                            print 'Invalid Found in Sample Set'
                            print InputFile
                            return (-8888, RecDate)
                    else:
                        print 'Incomplete record on file ' + InputFile
                        return (-8888, BeginDate)
        else:

            print InputFile + " doesn't exist, skipping " + Site
            return (-8888, BeginDate)

        BeginDate = TimeOffset(BeginDate, 1)

    return (SnowDepth * 39.37, RecDate)  # Meters to inches


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


print 'Running SnowDepth_xml.py on ' + time.ctime() + '\n'

# All Varaibles used in main

SnowDepth = 0.
SnowDepthSites = {}
SnowDepthIndex = {}
SnowDepthFilePath = '/data/realtime/CsiDatalogger/SurfaceMet/'
RealTimePath = '/data/realtime/MapOverlays/SnowDepth/'
IconBasePath = \
    'http://somepath.com'

try:
    db = MySQLdb.connection(host='host', user='user',
                            passwd='passwd!', db='db')
except:
    print "Error connecting to psdmeta MySQL DB"
    SendEmailAlert("Error connecting to psdmeta MySQL DB")

    sys.exit()

db.query("""Select site_has_inst.SiteID, site.Latitude, site.Longitude, site.Elevation, site.City, site.State, inst_type.Name, inst_manufacturer.Name 
From site_has_inst, site, inst_manufacturer, inst_type
Where inst_type.TypeID = site_has_inst.TypeID
AND site_has_inst.SiteID = site.SiteID
AND inst_manufacturer.ManufacturerID = inst_type.ManufacturerID
AND inst_type.CategoryID IN (27)
AND site.RealTimeDisplay = 'Y'
AND site_has_inst.Active = 'Y'
AND site_has_inst.InstRemovalDate is null;""")
r = db.store_result()

for row in r.fetch_row(0):
    SnowDepthSites[row[0]] = [
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[7],
        ]
    print row[0]

# 0) Latitude
# 1) Longitude
# 2) Elevation
# 3) City
# 4) State
# 5) Instrument Type Name
# 6) Instrument Manf
# 7) Insturment Sample Rate

for site in SnowDepthSites.keys():
    TempQuery = \
        'Select site_has_inst.SiteID, site_has_inst_data.DataFormatFile, site_has_inst_data.SampleRatePerhour \
	From site_has_inst, site_has_inst_data, inst_type \
	Where site_has_inst.OperationalID = site_has_inst_data.OperationalID \
	AND inst_type.TypeID = site_has_inst.TypeID \
	AND inst_type.CategoryID = 2 \
	AND site_has_inst_data.DataTypeID = 14 \
	AND site_has_inst_data.EndDate is null \
	AND site_has_inst.SiteID = \'' \
        + site + '\';'

    db.query(TempQuery)

    result = db.store_result()

    for line in result.fetch_row(0):

        try:
            LineData = re.split(',', line[1])
        except:
            print 'No data file found for site ' + site
            continue

        for i in range(len(LineData)):
            if LineData[i].find('Snow Depth') >= 0:
                SnowDepthIndex[site] = [i, line[2]]

# Get Current Time

EndTime = time.strftime('%Y,%j%H', time.gmtime())

EndTime = time.strptime(EndTime, '%Y,%j%H')

EndTime = TimeOffset(EndTime, 0)

StartHourTime = TimeOffset(EndTime, -1)  # since using Hour as start time.

OutPutPath = '%s%04d/%03d/' % (RealTimePath, StartHourTime.tm_year,
                               StartHourTime.tm_yday)

OutPutFile = '%s%04d/%03d/SnowDepth_%02d%03d%02d.xml' % (
    RealTimePath,
    StartHourTime.tm_year,
    StartHourTime.tm_yday,
    StartHourTime.tm_year % 100,
    StartHourTime.tm_yday,
    StartHourTime.tm_hour,
    )

OutPutFileOld = '%sSnowDepth_%02d%03d%02d.xml' % (RealTimePathOld,
        StartHourTime.tm_year % 100, StartHourTime.tm_yday,
        StartHourTime.tm_hour)

if not os.path.exists(OutPutPath):
    try:
        print 'Creating Dir ' + OutPutPath
        os.makedirs(OutPutPath)
    except:
        print 'Failed to create dir ' + OutPutPath

try:
    FO = open(OutPutFile, 'wb')
except:
    print "Error writing Snow Depth xml file."

# ....SendEmailAlert("Error writing Temperature xml file.")

    sys.exit()

FO.write('<markers>')
FO.write('\n')

for site in SnowDepthIndex.keys():

    SnowDepthPath = SnowDepthFilePath + site

    BeginTime = TimeOffset(EndTime, -1)

    (SnowDepth, Time) = GetSnowDepth(
        site,
        SnowDepthPath,
        SnowDepthIndex[site][0],
        BeginTime,
        EndTime,
        SnowDepthIndex[site][1],
        )

    SnowDepth = round(SnowDepth, 0)

    if float(SnowDepth) != -8888.00:

        TimeString = '%04d-%02d-%02d %02d:%02d' % (Time.tm_year,
                Time.tm_mon, Time.tm_mday, Time.tm_hour, Time.tm_min)
    else:

        TimeString = ' '

    SnowDepth = '%.2f' % SnowDepth

    IconPath = IconBasePath + SnowDepth + '.png'
    InfoBox = 'Snow Depth = %s (in)' % SnowDepth

    FO.write('<marker ')
    FO.write('siteID="')
    FO.write(site)
    FO.write('" name="')
    FO.write(SnowDepthSites[site][3])
    FO.write('" lat="')
    FO.write(SnowDepthSites[site][0])
    FO.write('" lng="')
    FO.write(SnowDepthSites[site][1])
    FO.write('" elev="')
    FO.write(SnowDepthSites[site][2])
    FO.write('" snowdepth="')
    FO.write(SnowDepth)
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

print 'Finished Running SnowDepth_xml.py on ' + time.ctime() + '\n'
