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


def getSoilLevel(DataVariable):

    if DataVariable.find(' 5cm') >= 0:
        return 5
    if DataVariable.find(' 10cm') >= 0:
        return 10
    if DataVariable.find(' 15cm') >= 0:
        return 15
    if DataVariable.find(' 20cm') >= 0:
        return 20
    if DataVariable.find(' 50cm') >= 0:
        return 50
    if DataVariable.find(' 100cm') >= 0:
        return 100


class SoilMetSite:

        # Constructs a new Site object.

    def __init__(
        self,
        SiteID,
        NwsSiteID,
        City,
        State,
        Latitude,
        Longitude,
        Elevation,
        ):

                # Make a dictionary to hold all the information of the site

        self.Info = {}
        self.Info['SiteID'] = SiteID
        self.Info['NwsSiteID'] = NwsSiteID
        self.Info['City'] = City
        self.Info['State'] = State
        self.Info['Latitude'] = Latitude
        self.Info['Longitude'] = Longitude
        self.Info['Elevation'] = Elevation
        self.Info['SampleRate'] = 0

        self.SoilSaturation5 = {}
        self.SoilSaturation10 = {}
        self.SoilSaturation15 = {}
        self.SoilSaturation20 = {}
        self.SoilSaturation50 = {}
        self.SoilSaturation100 = {}

        self.SoilTemperature5 = {}
        self.SoilTemperature10 = {}
        self.SoilTemperature15 = {}
        self.SoilTemperature20 = {}
        self.SoilTemperature50 = {}
        self.SoilTemperature100 = {}

        self.DataFormat = ''
        self.DataType = {}
        self.InstCat = []

    def getShefValue(self, DataVariable, DataValue):

                # See 7.4.6 Encoding Paired Value (Vector) Physical Elements in SHEF manual

        SoilDepthInInches = float('%.0f' % (getSoilLevel(DataVariable)
                                  * 1. / 2.54))
        ShefDataValue = SoilDepthInInches + abs(DataValue / 1000.)

        if DataValue < 0.:
            ShefDataValue *= -1.

        return ShefDataValue

    def setDataValue(
        self,
        DataVariable,
        Time,
        DataValue,
        ):

        DataTime = '%2d%02d%02d%02d' % (Time.tm_year % 100,
                Time.tm_mon, Time.tm_mday, Time.tm_hour)

        if DataValue[0] != -8888:
            DataValue[0] = self.getShefValue(DataVariable, DataValue[0])

        if DataVariable.find('Volumetric Water Content') >= 0 \
            or DataVariable.find('Soil Wetness Fraction') >= 0 \
            or DataVariable.find('Soil Saturation') >= 0:

            if DataVariable.find(' 5cm') >= 0:
                self.SoilSaturation5[DataTime] = DataValue
                return
            if DataVariable.find(' 10cm') >= 0:
                self.SoilSaturation10[DataTime] = DataValue
                return
            if DataVariable.find(' 15cm') >= 0:
                self.SoilSaturation15[DataTime] = DataValue
                return
            if DataVariable.find(' 20cm') >= 0:
                self.SoilSaturation20[DataTime] = DataValue
                return
            if DataVariable.find(' 50cm') >= 0:
                self.SoilSaturation50[DataTime] = DataValue
                return
            if DataVariable.find(' 100cm') >= 0:
                self.SoilSaturation100[DataTime] = DataValue
                return

        if DataVariable.find('Soil Temperature') >= 0:

            if DataVariable.find(' 5cm') >= 0:
                self.SoilTemperature5[DataTime] = DataValue
                return
            if DataVariable.find(' 10cm') >= 0:
                self.SoilTemperature10[DataTime] = DataValue
                return
            if DataVariable.find(' 15cm') >= 0:
                self.SoilTemperature15[DataTime] = DataValue
                return
            if DataVariable.find(' 20cm') >= 0:
                self.SoilTemperature20[DataTime] = DataValue
                return
            if DataVariable.find(' 50cm') >= 0:
                self.SoilTemperature50[DataTime] = DataValue
                return
            if DataVariable.find(' 100cm') >= 0:
                self.SoilTemperature100[DataTime] = DataValue
                return

    def getDataValue(self, DataVariable):

        if DataVariable.find('Volumetric Water Content') >= 0 \
            or DataVariable.find('Soil Wetness Fraction') >= 0 \
            or DataVariable.find('Soil Saturation') >= 0:

            if DataVariable.find(' 5cm') >= 0:
                return self.SoilSaturation5
            if DataVariable.find(' 10cm') >= 0:
                return self.SoilSaturation10
            if DataVariable.find(' 15cm') >= 0:
                return self.SoilSaturation15
            if DataVariable.find(' 20cm') >= 0:
                return self.SoilSaturation20
            if DataVariable.find(' 50cm') >= 0:
                return self.SoilSaturation50
            if DataVariable.find(' 100cm') >= 0:
                return self.SoilSaturation100

        if DataVariable.find('Soil Temperature') >= 0:

            if DataVariable.find(' 5cm') >= 0:
                return self.SoilTemperature5
            if DataVariable.find(' 10cm') >= 0:
                return self.SoilTemperature10
            if DataVariable.find(' 15cm') >= 0:
                return self.SoilTemperature15
            if DataVariable.find(' 20cm') >= 0:
                return self.SoilTemperature20
            if DataVariable.find(' 50cm') >= 0:
                return self.SoilTemperature50
            if DataVariable.find(' 100cm') >= 0:
                return self.SoilTemperature100

    def getDataPoint(self, DataVariable, Time):

        if DataVariable.find('Volumetric Water Content') >= 0 \
            or DataVariable.find('Soil Wetness Fraction') >= 0 \
            or DataVariable.find('Soil Saturation') >= 0:

            if DataVariable.find(' 5cm') >= 0:
                return self.SoilSaturation5[Time]
            if DataVariable.find(' 10cm') >= 0:
                return self.SoilSaturation10[Time]
            if DataVariable.find(' 15cm') >= 0:
                return self.SoilSaturation15[Time]
            if DataVariable.find(' 20cm') >= 0:
                return self.SoilSaturation20[Time]
            if DataVariable.find(' 50cm') >= 0:
                return self.SoilSaturation50[Time]
            if DataVariable.find(' 100cm') >= 0:
                return self.SoilSaturation100[Time]

        if DataVariable.find('Soil Temperature') >= 0:

            if DataVariable.find(' 5cm') >= 0:
                return self.SoilTemperature5[Time]
            if DataVariable.find(' 10cm') >= 0:
                return self.SoilTemperature10[Time]
            if DataVariable.find(' 15cm') >= 0:
                return self.SoilTemperature15[Time]
            if DataVariable.find(' 20cm') >= 0:
                return self.SoilTemperature20[Time]
            if DataVariable.find(' 50cm') >= 0:
                return self.SoilTemperature50[Time]
            if DataVariable.find(' 100cm') >= 0:
                return self.SoilTemperature100[Time]

    def getSiteID(self):
        return self.Info['SiteID']

    def getNwsSiteID(self):
        return self.Info['NwsSiteID']

    def getCity(self):
        return self.Info['City']

    def getState(self):
        return self.Info['State']

    def getLat(self):
        return self.Info['Latitude']

    def getLong(self):
        return self.Info['Longitude']

    def getElevation(self):
        return self.Info['Elevation']

        # Returns the Data Dict of the site

    def getDataType(self):
        return self.DataType

    def setDataType(self, Type):
        self.DataType[Type] = 0

    def setDataTypeIndex(self, Type, Index):
        self.DataType[Type] = Index

    def setDataFormat(self, Format):
        self.DataFormat = Format

    def setSampleRate(self, SampleRate):
        self.Info['SampleRate'] = SampleRate

    def getSampleRate(self):
        return self.Info['SampleRate']

    def getDataFormat(self):
        return self.DataFormat

    def appendInstCat(self, CatID):
        self.InstCat.append(CatID)

    def getInstCat(self):
        return self.InstCat


def GetSoilSaturation(
    Site,
    Path,
    SoilMoistureIndex,
    BeginDate,
    EndDate,
    SampleRate,
    SoilSaturationFactor,
    ):

    Records = []
    SoilMoisture = 0.
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
                return [-8888, BeginDate]

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
                return [-8888, BeginDate]

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
                    return [-8888, BeginDate]

                if RecDate > EndDate:
                    break

                if RecDate >= BeginDate and RecDate < EndDate:

                    if len(Fields) > SoilMoistureIndex:

                        if float(Fields[SoilMoistureIndex]) >= -100.:
                            SoilMoisture = \
                                float(Fields[SoilMoistureIndex])

                        if float(Fields[SoilMoistureIndex]) < -100. \
                            or float(Fields[SoilMoistureIndex]) > 100:  #  QC check for any invalids
                            print 'Invalid flag found in raw data. value=', \
                                Fields[SoilMoistureIndex], 'year:', \
                                RecDate.tm_year, 'doy:', \
                                RecDate.tm_yday, 'hour:', \
                                RecDate.tm_hour, 'minute:', \
                                RecDate.tm_min, \
                                '... ignoring data and pressing on...'
                            return [-8888, RecDate]
                    else:
                        print 'Incomplete record on file ' + InputFile
                        return [-8888, BeginDate]
        else:

            print InputFile + " doesn't exist, skipping " + Site
            return [-8888, BeginDate]

        BeginDate = TimeOffset(BeginDate, 1)

    SoilMoisture = SoilMoisture / float(SoilSaturationFactor) * 100.

    return [SoilMoisture, RecDate]


def GetTemperature(
    Site,
    Path,
    TempIndex,
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
                return [-8888, BeginDate]

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
                return [-8888, BeginDate]

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
                    return [-8888, BeginDate]

                if RecDate > EndDate:
                    break

                if RecDate >= BeginDate and RecDate < EndDate:

                    if len(Fields) > TempIndex:

                        if float(Fields[TempIndex]) >= -100.:
                            Temp = float(Fields[TempIndex])

                        if float(Fields[TempIndex]) < -100. \
                            or float(Fields[TempIndex]) > 100:  #  QC check for any invalids
                            print 'Invalid flag found in raw data. value=', \
                                Fields[TempIndex], 'year:', \
                                RecDate.tm_year, 'doy:', \
                                RecDate.tm_yday, 'hour:', \
                                RecDate.tm_hour, 'minute:', \
                                RecDate.tm_min, \
                                '... ignoring data and pressing on...'
                            return [-8888, RecDate]
                    else:
                        print 'Incomplete record on file ' + InputFile
                        return [-8888, BeginDate]
        else:

            print InputFile + " doesn't exist, skipping " + Site
            return [-8888, BeginDate]

        BeginDate = TimeOffset(BeginDate, 1)

    Temp = 1.8 * Temp + 32
    return [Temp, RecDate]


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


print 'Running 1HrShefSoilTemperature.py on ' + time.ctime() + '\n'

# All Varaibles used in main

RawDataTypes = {
    'Soil Temperature (C) 5cm': ['26'],
    'Soil Temperature (C) 10cm': ['26'],
    'Soil Temperature (C) 15cm': ['26'],
    'Soil Temperature (C) 20cm': ['26'],
    'Soil Temperature (C) 50cm': ['26'],
    'Soil Temperature (C) 100cm': ['26'],
    }

ShefDataTypes = [
    'Soil Temperature (C) 5cm',
    'Soil Temperature (C) 10cm',
    'Soil Temperature (C) 15cm',
    'Soil Temperature (C) 20cm',
    'Soil Temperature (C) 50cm',
    'Soil Temperature (C) 100cm',
    ]

ShefDataCode = [
    'TVIRZZZ',
    'TVIRZZZ',
    'TVIRZZZ',
    'TVIRZZZ',
    'TVIRZZZ',
    'TVIRZZZ',
    ]

Sites = {}
SurfaceMetData = '/data/realtime/CsiDatalogger/SurfaceMet/'
HistoryPath = '/home/dms7/process/data/ShefProducts/24HrHistory/'
RealTimePath = '/data/realtime/HydroProductsNWS/1HrShefSoilTemperature/'

try:
    db = MySQLdb.connection(host='host', user='user',
                            passwd='passwd!', db='db')
except:
    print "Error connecting to psdmeta MySQL DB"
    SendEmailAlert("Error connect to psdmeta MySQL DB")
    sys.exit()

# Query the DB to find sites with Soil Temperature Instrumentation

db.query("""Select site_has_inst.SiteID, site.NwsSiteID,  site.City, site.State, site.Latitude, site.Longitude, site.Elevation
From site_has_inst, site, inst_manufacturer, inst_type
Where inst_type.TypeID = site_has_inst.TypeID
AND site_has_inst.SiteID = site.SiteID
AND inst_manufacturer.ManufacturerID = inst_type.ManufacturerID
AND inst_type.CategoryID IN (26)
AND site.RealTimeDisplay = 'Y'
AND site_has_inst.Active = 'Y'
AND site_has_inst.InstRemovalDate is null
group by site_has_inst.SiteID;""")

r = db.store_result()

# Create Site Objects

for row in r.fetch_row(0):
    Sites[row[0]] = SoilMetSite(
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        )

# Query DB to find DataTypes and InstCategories

for site in Sites.keys():

    FormatDesc = \
        'Select site_has_inst.SiteID, inst_type.Name, inst_manufacturer.Name, inst_type.CategoryID \
	From site_has_inst, inst_manufacturer, inst_type \
	Where inst_type.TypeID = site_has_inst.TypeID \
	AND inst_manufacturer.ManufacturerID = inst_type.ManufacturerID \
	AND inst_type.CategoryID IN (26) \
	AND site_has_inst.SiteID = \'' \
        + site + '\';'

    db.query(FormatDesc)

    r = db.store_result()

    for row in r.fetch_row(0):
        Sites[site].setDataType(row[1])
        Sites[site].appendInstCat(row[3])

# Get Data Format

for site in Sites.keys():

    FindFormatQuery = \
        'Select site_has_inst.SiteID, site_has_inst_data.DataFormatFile, site_has_inst_data.SampleRatePerhour \
        From site_has_inst, site_has_inst_data, inst_type \
        Where site_has_inst.OperationalID = site_has_inst_data.OperationalID \
        AND inst_type.TypeID = site_has_inst.TypeID \
        AND site_has_inst_data.DataTypeID = 14 \
	AND inst_type.CategoryID = 2 \
        AND site_has_inst_data.EndDate is null \
        AND site_has_inst.SiteID = \'' \
        + site + '\';'

    db.query(FindFormatQuery)

    result = db.store_result()

    for row in result.fetch_row(0):

        try:
            LineData = re.split(',', row[1])
        except:
            print 'No data file format found for site ' + site
            continue

        Sites[site].setDataFormat(row[1])
        Sites[site].setSampleRate(row[2])

# Calculate 24HRs of Soil Temperature Data

CurrentTime = time.strftime('%Y,%j%H', time.gmtime())

CurrentTime = time.strptime(CurrentTime, '%Y,%j%H')

BeginTime = TimeOffset(CurrentTime, -24)

while BeginTime < CurrentTime:

    EndTime = TimeOffset(BeginTime, 1)

    SiteTime = '%2d%02d%02d%02d%s' % (BeginTime.tm_year % 100,
            BeginTime.tm_mon, BeginTime.tm_mday, BeginTime.tm_hour,
            site)

    for site in Sites.keys():

        FilePath = SurfaceMetData + site

        for DataType in RawDataTypes.keys():

            for InstCatID in RawDataTypes[DataType]:

                if InstCatID in Sites[site].getInstCat():

                    try:
                        LineData = re.split(',',
                                Sites[site].getDataFormat())
                    except:
                        print 'No data file format found for site ' \
                            + site
                        continue

                    for i in range(len(LineData)):

                        if LineData[i].find(DataType) >= 0:

                            Index = i

                            if DataType.find('Soil Wetness Fraction') \
                                >= 0 \
                                or DataType.find('Volumetric Water Content'
                                    ) >= 0:

                                if site in SoilSaturationFactor:

                                    DataTotal = GetSoilSaturation(
                                        site,
                                        FilePath,
                                        Index,
                                        BeginTime,
                                        EndTime,
                                        Sites[site].getSampleRate(),
                                        SoilSaturationFactor[site],
                                        )

                                    Sites[site].setDataValue(DataType,
        BeginTime, DataTotal)

                            if DataType.find('Soil Temperature') >= 0:

                                DataTotal = GetTemperature(
                                    site,
                                    FilePath,
                                    Index,
                                    BeginTime,
                                    EndTime,
                                    Sites[site].getSampleRate(),
                                    )

                                Sites[site].setDataValue(DataType,
                                        BeginTime, DataTotal)
    BeginTime = TimeOffset(BeginTime, 1)
BeginTime = TimeOffset(CurrentTime, -24)

HistoryStartTime = TimeOffset(CurrentTime, -1)  # Use Begin Hour for History File.

# Write 24Hr Historical File

OutPutPath = '%s%04d/%03d/' % (HistoryPath, HistoryStartTime.tm_year,
                               HistoryStartTime.tm_yday)
HistOutPutFile = '%s%04d/%03d/SHEFSoilTemperature%2d%03d%02d.txt' % (
    HistoryPath,
    HistoryStartTime.tm_year,
    HistoryStartTime.tm_yday,
    HistoryStartTime.tm_year % 100,
    HistoryStartTime.tm_yday,
    HistoryStartTime.tm_hour,
    )

if not os.path.exists(OutPutPath):
    try:
        print 'Creating Dir ' + OutPutPath
        os.makedirs(OutPutPath)
    except:
        print 'Failed to create dir ' + OutPutPath

try:
    HistoryFile = open(HistOutPutFile, 'wb')
except:
    print "Can't write 24 HR Soil Temperature History file."

        # SendEmailAlert("Can't write 24 HR Soil Temperature History file.")

    sys.exit()

for site in sorted(Sites.keys()):

    for DataType in ShefDataTypes:

        DataValues = Sites[site].getDataValue(DataType)

        for DataValue in DataValues.keys():

#      print site,DataValue,DataType,DataValues[DataValue][0]
#      print DataValue
#      print DataValues[DataValue][1]....

            DataTime = '%2d%02d%02d%02d%02d' \
                % (DataValues[DataValue][1].tm_year % 100,
                   DataValues[DataValue][1].tm_mon,
                   DataValues[DataValue][1].tm_mday,
                   DataValues[DataValue][1].tm_hour,
                   DataValues[DataValue][1].tm_min)

            if DataValues[DataValue][0] is not None:

                HistoryFile.write(site)
                HistoryFile.write(',')
                HistoryFile.write(DataValue)
                HistoryFile.write(',')
                HistoryFile.write(DataType)
                HistoryFile.write(',')
                HistoryFile.write('%7.4f'
                                  % round(float(DataValues[DataValue][0]),
                                  4))
                HistoryFile.write(',')
                HistoryFile.write(DataTime)
                HistoryFile.write('\n')

# Write out Current Hour in SHEF

ShefHourlyPath = '%s%04d/%03d' % (RealTimePath, CurrentTime.tm_year,
                                  CurrentTime.tm_yday)
ShefHourlyFile = '%s%04d/%03d/1HrShefSoilTemperature%02d%03d%02d.txt' \
    % (
    RealTimePath,
    CurrentTime.tm_year,
    CurrentTime.tm_yday,
    CurrentTime.tm_year % 100,
    CurrentTime.tm_yday,
    CurrentTime.tm_hour,
    )

print ShefHourlyFile

if not os.path.exists(ShefHourlyPath):
    try:
        print 'Creating Dir ' + ShefHourlyPath
        os.makedirs(ShefHourlyPath)
    except:
        print 'Failed to create dir ' + ShefHourlyPath

try:
    ShefMasterFH = open(ShefHourlyFile, 'wb')
except:
    print "Can't write SHEF SoilTemperature file"

        # SendEmailAlert("Can't open  24 HR Precip History file.")

    sys.exit()

ShefHeader = '.B DEN %02d%02d%02d DH%02d/DQZ' % (CurrentTime.tm_year
        % 100, CurrentTime.tm_mon, CurrentTime.tm_mday,
        CurrentTime.tm_hour)

for DataCode in ShefDataCode:
    ShefHeader += '/%s' % DataCode

ShefHeader += \
    '''\r
: PSD SOIL TEMPERATURE AT DEPTH (DEGREE F)\r
:   '''
for DataType in ShefDataTypes:
    ShefHeader += '%4.0f-INCH ' % (getSoilLevel(DataType) * 1. / 2.54)
ShefHeader += '\r\n'

ShefMasterFH.write(ShefHeader)

BeginTime = TimeOffset(CurrentTime, -1)

while BeginTime < CurrentTime:

    for site in sorted(Sites.keys()):

        State = Sites[site].getState().upper()
        Lat = float(Sites[site].getLat())
        Long = float(Sites[site].getLong())
        Elevation = float(Sites[site].getElevation()) * 3.2808399
        Name = Sites[site].getCity().upper()
        NwsSiteID = Sites[site].getNwsSiteID()
        SiteID = ''

        if NwsSiteID is None:
            SiteID = site + State
        else:
            SiteID = NwsSiteID

        ShefLineEntry = '%s' % SiteID.upper()

#   SiteMetaInfo  = (": %s, %s (%.2f, %.2f, %.0fFT)\n" % (Name, State, Lat, Long, Elevation ))....

        NumOfDataTypes = len(ShefDataTypes)

        NumValue = 0
        ValidValues = 0

        for DataType in ShefDataTypes:

            DataValues = Sites[site].getDataValue(DataType)

            CurrentHourData = '%2d%02d%02d%02d' % (BeginTime.tm_year
                    % 100, BeginTime.tm_mon, BeginTime.tm_mday,
                    BeginTime.tm_hour)

            if NumValue > 0:
                ShefLineEntry += '/'

            try:

                if float(DataValues[CurrentHourData][0] > -8888):
                    ShefLineEntry += ' %7.4f ' \
                        % float(DataValues[CurrentHourData][0])
                    ValidValues += 1
                else:

                    ShefLineEntry += '   -9999 '
                    ValidValues += 1
            except:

                ShefLineEntry += '         '

            NumValue += 1

        if ValidValues:
            SiteInfo = ': %s, %s (%.2f, %.2f, %.0f FT)' % (Name, State,
                    Lat, Long, Elevation)
            ShefMasterFH.write(ShefLineEntry + SiteInfo + '\r\n')

    BeginTime = TimeOffset(BeginTime, 1)

ShefMasterFH.write('.END\r\n')

# Open Previous Historical File and find any differences with current data

PreviousHistTime = TimeOffset(CurrentTime, -2)  # Since using Begin Hour open previous hour is 2 hours past.

HistOutPutPath = '%s%04d/%03d/' % (HistoryPath,
                                   PreviousHistTime.tm_year,
                                   PreviousHistTime.tm_yday)

HistOutPutFile = '%s%04d/%03d/SHEFSoilTemperature%2d%03d%02d.txt' % (
    HistoryPath,
    PreviousHistTime.tm_year,
    PreviousHistTime.tm_yday,
    PreviousHistTime.tm_year % 100,
    PreviousHistTime.tm_yday,
    PreviousHistTime.tm_hour,
    )

if not os.path.exists(HistOutPutPath):
    try:
        print 'Creating Dir ' + HistOutPutPath
        os.makedirs(OutPutPath)
    except:
        print 'Failed to create dir ' + HistOutPutPath

try:
    FI = open(HistOutPutFile, 'rb')
except:
    print 'Can not open 24 HR Soil Temperature History file.'

        # SendEmailAlert("Can't open  24 HR Soil Temperature History file.")

    sys.exit()

FileContents = FI.readlines()

ChangeRecords = {}

# Loop through Historical File and compare with current values.  Indentify any changes.

for line in FileContents:

    LineData = re.split(',', line)

    try:
        NewRecord = Sites[LineData[0]].getDataPoint(LineData[2],
                LineData[1])[0]
    except:
        continue

    NewRecord = round(float(NewRecord), 4)
    OldRecord = round(float(LineData[3]), 4)

    if NewRecord != OldRecord:
        print 'Changed Record for', LineData[0], 'at', LineData[1], \
            'from', OldRecord, 'to', NewRecord
        TimeStamp = LineData[1] + LineData[0]

        if TimeStamp not in ChangeRecords:
            ChangeRecords[TimeStamp] = []

        ChangeRecords[TimeStamp].append([OldRecord, NewRecord])

# Write out any changes to SHEF .BR Format

if len(ChangeRecords) > 0:

    BeginTime = TimeOffset(CurrentTime, -23)

    while BeginTime < CurrentTime:

        HeaderCounter = 0

        for site in sorted(Sites.keys()):

            MatchedHourData = '%2d%02d%02d%02d%s' % (BeginTime.tm_year
                    % 100, BeginTime.tm_mon, BeginTime.tm_mday,
                    BeginTime.tm_hour, Sites[site].getSiteID())

            if MatchedHourData in ChangeRecords.keys():

                if HeaderCounter == 0:

                    ShefChangeTime = TimeOffset(BeginTime, 1)  #  Change to adjust for SHEF End Hour vs Begin hour stored in History File

                    ShefHeader = '.BR DEN %02d%02d%02d DH%02d/DQZ' \
                        % (ShefChangeTime.tm_year % 100,
                           ShefChangeTime.tm_mon,
                           ShefChangeTime.tm_mday,
                           ShefChangeTime.tm_hour)

                    for DataCode in ShefDataCode:
                        ShefHeader += '/%s' % DataCode

                    ShefHeader += '\r\n'

                    ShefMasterFH.write(ShefHeader)

                State = Sites[site].getState().upper()
                Lat = float(Sites[site].getLat())
                Long = float(Sites[site].getLong())
                Elevation = float(Sites[site].getElevation()) \
                    * 3.2808399
                Name = Sites[site].getCity().upper()
                NwsSiteID = Sites[site].getNwsSiteID()
                SiteID = ''

                if NwsSiteID is None:
                    SiteID = site + State
                else:
                    SiteID = NwsSiteID

                ShefLineEntry = '%s' % SiteID.upper()

                SiteMetaInfo = ': %s, %s (%.2f, %.2f, %.0fFT)\n' \
                    % (Name, State, Lat, Long, Elevation)

                NumOfDataTypes = len(ShefDataTypes)

                HeaderCounter += 1

                NumValue = 0
                ValidValues = 0

                for DataType in ShefDataTypes:

                    DataValues = Sites[site].getDataValue(DataType)

                    CurrentHourData = '%2d%02d%02d%02d' \
                        % (BeginTime.tm_year % 100, BeginTime.tm_mon,
                           BeginTime.tm_mday, BeginTime.tm_hour)
                    if NumValue > 0:
                        ShefLineEntry += '/'

                    try:
                        if float(DataValues[CurrentHourData][0]
                                 > -8888):
                            ShefLineEntry += ' %7.4f ' \
                                % round(float(DataValues[CurrentHourData][0]),
                                    4)
                        else:
                            ShefLineEntry += '   -9999 '

                        ValidValues += 1
                    except:

                        ShefLineEntry += '         '

                    NumValue += 1

                ShefMasterFH.write(ShefLineEntry + '\r\n')

        BeginTime = TimeOffset(BeginTime, 1)

        if HeaderCounter > 0:

            ShefMasterFH.write('.END\r\n')

ShefMasterFH.close()

# Cleanup Old 24 Hour History Files.

FileScrubTime = TimeOffset(EndTime, -168)

ScrubExpression = 'SHEFSoilTemperature%02d%03d*' \
    % (FileScrubTime.tm_year % 100, FileScrubTime.tm_yday)

ScrubRemovalCommand = 'rm ' + HistoryPath + ScrubExpression

os.system(ScrubRemovalCommand)

# Cleanup Old Shef Files

# ScrubExpression = ("1HrShefSoilTemperature%02d%03d*" % (   (FileScrubTime.tm_year % 100), FileScrubTime.tm_yday))

# ScrubRemovalCommand = "rm " + RealTimePath + ScrubExpression

# os.system(ScrubRemovalCommand)
