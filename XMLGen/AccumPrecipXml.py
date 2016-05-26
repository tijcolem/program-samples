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


def GetPrecipitation(
    Site,
    Path,
    PrecipIndex,
    BeginDate,
    EndDate,
    SampleRate,
    ):

    Records = []
    Precip = 0.
    YearIndex = 1
    JdayIndex = 2
    HrMinIndex = 3
    RecDateString = ''
    AbsMinAcceptanceSampleTime = 45
    Flag = 0

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

                    if len(Fields) > PrecipIndex:

                        if float(Fields[PrecipIndex]) >= 0.:
                            Precip += float(Fields[PrecipIndex])

                        if float(Fields[PrecipIndex]) < 0.:  #  QC check for any invalid precip amounts. If any, accumlated hour is marked invalid
                            print 'Invalid Found in Sample Set'
                            print InputFile
                            return (-8888, BeginDate)
                    else:
                        print 'Incomplete record on file ' + InputFile
                        return (-8888, BeginDate)
        else:

            print InputFile \
                + " doesn't exist, skipping accumlation for " + Site
            return (-8888, BeginDate)

        BeginDate = TimeOffset(BeginDate, 1)

    return (Precip / 25.4, RecDate)


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


print 'Running AccumPrecip_xml.py on ' + time.ctime() + '\n'

# All Varaibles used in main

AccumPrecipTimes = [
    1,
    3,
    6,
    12,
    24,
    48,
    ]

# ccumPrecipTimes   = [1, 3]

TotalPrecip = 0.
CurrentShefPrecipAll = {}
PrecipSites = {}
PrecipIndex = {}
PrecipFilePath = '/data/realtime/CsiDatalogger/SurfaceMet/'
RealTimePath = '/data/realtime/MapOverlays/AccumulatedPrecip/'
IconBasePath = \
    'http://www.somepath.com'

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
AND inst_type.CategoryID IN (12,15,16)
AND site.RealTimeDisplay = 'Y'
AND site_has_inst.Active = 'Y'
AND site_has_inst.InstRemovalDate is null;""")
r = db.store_result()

for row in r.fetch_row(0):
    PrecipSites[row[0]] = [
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[7],
        ]

# 0) Latitude
# 1) Longitude
# 2) Elevation
# 3) City
# 4) State
# 5) Instrument Type Name
# 6) Instrument Manf
# 7) Insturment Sample Rate

PrecipSites.keys().sort()

for site in PrecipSites.keys():

    PrecipQuery = \
        'Select site_has_inst.SiteID, site_has_inst_data.DataFormatFile, site_has_inst_data.SampleRatePerhour \
        From site_has_inst, site_has_inst_data, inst_type \
        Where site_has_inst.OperationalID = site_has_inst_data.OperationalID \
        AND inst_type.TypeID = site_has_inst.TypeID \
        AND inst_type.CategoryID = 2 \
	AND site_has_inst_data.DataTypeID = 14 \
        AND site_has_inst_data.EndDate is null \
        AND site_has_inst.SiteID = \'' \
        + site + '\';'

    db.query(PrecipQuery)

    result = db.store_result()

    for line in result.fetch_row(0):

        try:

            LineData = re.split(',', line[1])
        except:

            print 'No Data File Format for site ' + site
            continue

        for i in range(len(LineData)):
            if LineData[i].find('Precip') >= 0:
                PrecipIndex[site] = [i, line[2]]

# Get Current Time

EndTime = time.strftime('%Y,%j%H', time.gmtime())

EndTime = time.strptime(EndTime, '%Y,%j%H')

EndTime = TimeOffset(EndTime, 0)

StartHourTime = TimeOffset(EndTime, -1)  # since using Hour as start time.

for TimeIncr in AccumPrecipTimes:

    print 'Calculating ' + str(TimeIncr) + ' Precipitation'

    OutPutPath = '%s%04d/%03d/' % (RealTimePath, StartHourTime.tm_year,
                                   StartHourTime.tm_yday)

    OutPutFile = '%s%04d/%03d/%dHrPrecipitation_%02d%03d%02d.xml' % (
        RealTimePath,
        StartHourTime.tm_year,
        StartHourTime.tm_yday,
        TimeIncr,
        StartHourTime.tm_year % 100,
        StartHourTime.tm_yday,
        StartHourTime.tm_hour,
        )

    OutPutFileOld = '%s%dHrPrecipitation_%02d%03d%02d.xml' \
        % (RealTimePathOld, TimeIncr, StartHourTime.tm_year % 100,
           StartHourTime.tm_yday, StartHourTime.tm_hour)

    if not os.path.exists(OutPutPath):
        try:
            print 'Creating Dir ' + OutPutPath
            os.makedirs(OutPutPath)
        except:
            print 'Failed to create dir ' + OutPutPath

    try:
        FO = open(OutPutFile, 'wb')
    except:
        print "Error writing Accumlated Precip file."

        # SendEmailAlert("Error writing Accumlated Precip XML file.")

        sys.exit()

    FO.write('<markers>')
    FO.write('\n')

    for site in PrecipIndex.keys():

        print 'Processing site ' + site

        PrecipPath = PrecipFilePath + site

        BeginTime = TimeOffset(EndTime, -TimeIncr)

        (TotalPrecip, Time) = GetPrecipitation(
            site,
            PrecipPath,
            PrecipIndex[site][0],
            BeginTime,
            EndTime,
            PrecipIndex[site][1],
            )

        TotalPrecip = round(TotalPrecip, 3)

        if float(TotalPrecip) != -8888.00:

            EndTimeString = '%04d-%02d-%02d %02d:%02d' % (Time.tm_year,
                    Time.tm_mon, Time.tm_mday, Time.tm_hour,
                    Time.tm_min)
            BeginTimeString = '%04d-%02d-%02d %02d:%02d' \
                % (BeginTime.tm_year, BeginTime.tm_mon,
                   BeginTime.tm_mday, BeginTime.tm_hour,
                   BeginTime.tm_min)
        else:

            EndTimeString = ' '
            BeginTimeString = ' '

        TotalPrecip = '%.02f' % TotalPrecip

        IconPath = IconBasePath + TotalPrecip + '.png'
        InfoBox = 'Accumlated Precipitation = %s (in)' % TotalPrecip

        FO.write('<marker ')
        FO.write('siteID="')
        FO.write(site)
        FO.write('" name="')
        FO.write(PrecipSites[site][3])
        FO.write('" lat="')
        FO.write(PrecipSites[site][0])
        FO.write('" lng="')
        FO.write(PrecipSites[site][1])
        FO.write('" elev="')
        FO.write(PrecipSites[site][2])
        FO.write('" precip="')
        FO.write(TotalPrecip)
        FO.write('" begintime="')
        FO.write(BeginTimeString)
        FO.write('" endtime="')
        FO.write(EndTimeString)
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

print 'Finished Running AccumPrecip_xml.py on ' + time.ctime() + '\n'
