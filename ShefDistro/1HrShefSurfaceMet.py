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


class SurfaceMetSite:

        # Constructs a new Site object.

    def __init__(
        self,
        SiteID,
        City,
        State,
        Latitude,
        Longitude,
        Elevation,
        NwsSiteID,
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

        self.Precipitation = {}
        self.WindSpeed = {}
        self.WindDirection = {}
        self.Temperature = {}
        self.RelativeHumidity = {}
        self.DewPoint = {}

        self.DataFormat = ''
        self.DataType = {}
        self.InstCat = []

    def setDataValue(
        self,
        DataVariable,
        Time,
        DataValue,
        ):

        DataTime = '%2d%02d%02d%02d' % (Time.tm_year % 100,
                Time.tm_mon, Time.tm_mday, Time.tm_hour)

        if DataVariable == 'Precipitation (mm)':
            self.Precipitation[DataTime] = DataValue
        if DataVariable == 'Scalar Wind Speed (m/s)':
            self.WindSpeed[DataTime] = DataValue
        if DataVariable == 'Wind Direction (degrees)':
            self.WindDirection[DataTime] = DataValue
        if DataVariable == 'Temperature (C)':
            self.Temperature[DataTime] = DataValue
        if DataVariable == 'Relative Humidity (%)':
            self.RelativeHumidity[DataTime] = DataValue
        if DataVariable == 'Dew Point':
            self.DewPoint[DataTime] = DataValue

    def getDataValue(self, DataVariable):

        if DataVariable == 'Precipitation (mm)':
            return self.Precipitation
        if DataVariable == 'Scalar Wind Speed (m/s)':
            return self.WindSpeed
        if DataVariable == 'Wind Direction (degrees)':
            return self.WindDirection
        if DataVariable == 'Temperature (C)':
            return self.Temperature
        if DataVariable == 'Relative Humidity (%)':
            return self.RelativeHumidity
        if DataVariable == 'Dew Point':
            return self.DewPoint

    def getDataPoint(self, DataVariable, Time):

        if DataVariable == 'Precipitation (mm)':
            return self.Precipitation[Time]
        if DataVariable == 'Scalar Wind Speed (m/s)':
            return self.WindSpeed[Time]
        if DataVariable == 'Wind Direction (degrees)':
            return self.WindDirection[Time]
        if DataVariable == 'Temperature (C)':
            return self.Temperature[Time]
        if DataVariable == 'Relative Humidity (%)':
            return self.RelativeHumidty[Time]
        if DataVariable == 'Dew Point':
            return self.DewPoint[Time]

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


def GetWindSpeed(
    Site,
    Path,
    WindSpeedIndex,
    BeginDate,
    EndDate,
    SampleRate,
    ):

    Records = []
    WindSpeed = 0.
    YearIndex = 1
    JdayIndex = 2
    HrMinIndex = 3
    RecDateString = ''
    AbsMinAcceptanceSampleTime = 5
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

                    if len(Fields) > WindSpeedIndex:

                        if float(Fields[WindSpeedIndex]) >= 0.:
                            WindSpeed = float(Fields[WindSpeedIndex])

                        if float(Fields[WindSpeedIndex]) < 0.:  #  QC check for any invalid precip amounts. If any, accumlated hour is marked invalid
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

    return (WindSpeed * 2.2369, RecDate)


def GetWindDirection(
    Site,
    Path,
    WindDirIndex,
    BeginDate,
    EndDate,
    SampleRate,
    ):

    Records = []
    WindDir = 0.
    YearIndex = 1
    JdayIndex = 2
    HrMinIndex = 3
    RecDateString = ''
    AbsMinAcceptanceSampleTime = 1
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

                    if len(Fields) > WindDirIndex:

                        if float(Fields[WindDirIndex]) >= 0.:
                            WindDir = float(Fields[WindDirIndex])

                        if float(Fields[WindDirIndex]) < 0.:  #  QC check for any invalid precip amounts. If any, accumlated hour is marked invalid
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

    return (WindDir, RecDate)


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
                return (-8888, BeginDate)

            FileContents = fileobj.readlines()

            if float(SampleRate) > 0:

                AbsSampleCompletion = float(len(FileContents)
                        / float(SampleRate)) * 60
            else:
                AbsSampleCompletion = 0

            if AbsSampleCompletion < AbsMinAcceptanceSampleTime:  # QC check. Must have correct amount of samples to be counted.
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

                    if len(Fields) > TempIndex:

                        if float(Fields[TempIndex]) >= -100.:
                            Temp = float(Fields[TempIndex])

                        if float(Fields[TempIndex]) < -100. \
                            or float(Fields[TempIndex]) > 100:  #  QC check for any invalids
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

    Temp = 1.8 * Temp + 32
    return (Temp, RecDate)


def GetRelativeHumdity(
    Site,
    Path,
    RHIndex,
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

            if float(SampleRate) > 0:

                AbsSampleCompletion = float(len(FileContents)
                        / float(SampleRate)) * 60
            else:
                AbsSampleCompletion = 0

            if AbsSampleCompletion < AbsMinAcceptanceSampleTime:  # QC check. Must have correct amount of samples to be counted.
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

                    if len(Fields) > RHIndex:

                        if float(Fields[RHIndex]) >= -100.:
                            RH = float(Fields[RHIndex])

                        if float(Fields[RHIndex]) < -100. \
                            or float(Fields[RHIndex]) > 100:  #  QC check for any invalids
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

    return (RH, RecDate)


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
    AbsMinAcceptanceSampleTime = 55

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
            return (-9999, BeginDate)

        for line in FileContents:
            Records.append(line)
        fileobj.close()

        Precip = 0.

        for i in range(len(Records)):

            try:

                Fields = re.split(',', Records[i])

                Hour = int(Fields[HrMinIndex]) / 100

                Minute = int(Fields[HrMinIndex]) - int(Hour * 100.)

                RecDateString = '%d%03d%02d%02d' \
                    % (int(Fields[YearIndex]), int(Fields[JdayIndex]),
                       Hour, Minute)

                RecDate = time.strptime(RecDateString, '%Y%j%H%M')

                RecDate = TimeOffset(RecDate, 0)  # For correct flag setting in time tuple tm_dst needs to = 0.

                if RecDate > EndDate:
                    break

                if RecDate >= BeginDate and RecDate < EndDate:

                    if float(Fields[PrecipIndex]) >= 0.:

                        Precip += float(Fields[PrecipIndex])

                    if float(Fields[PrecipIndex]) < 0.:  #  QC check for any invalid precip amounts. If any, accumlated hour is marked invalid
                        print 'Invalid Found in Sample Set'
                        print InputFile
                        return (-9999, BeginDate)
            except:

                print 'Parse error on file'
                print InputFile
                return (-9999, BeginDate)

        if Precip > 100:  # QC check for accumlated precip exceeding 4" per hour.
            print InputFile
            print 'Precip reported way over 4in per hour.  Check configuration or instrument'
            return (-9999, BeginDate)
        else:
            return (Precip / 25.4, BeginDate)
    else:

        return (-9999, BeginDate)


def GetDewPoint(Temperature, RelativeHumidity, Date):

    if Temperature < -100 or RelativeHumidity < 0:
        return (-8888, Date)

    VapPresSat = math.exp(55.2966 - 6810.5245 / (Temperature + 273.15)
                          - 5.0898 * math.log(Temperature + 273.15))

    VapPres = VapPresSat * RelativeHumidity / 100.

    if VapPres < 0.001:
        VapPres = 0.001

    DewPoint = (243.5 * math.log(VapPres) - 440.8) / (19.48
            - math.log(VapPres))

    DewPointDepression = Temperature - DewPoint

    if VapPres == 0.001 and DewPointDepression < 30.0:
        DewPointDepression = 30.0

    DewPoint = Temperature - DewPointDepression

    DewPoint = 1.8 * DewPoint + 32

    return (DewPoint, Date)


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

print 'Running 1HrShefSurfaceMet.py on ' + time.ctime() + '\n'

# All Varaibles used in main

RawDataTypes = {
    'Precipitation (mm)': ['12', '15', '16'],
    'Scalar Wind Speed (m/s)': ['21'],
    'Wind Direction (degrees)': ['21'],
    'Temperature (C)': ['24'],
    'Relative Humidity (%)': ['24'],
    }

DerivedDataTypes = {'Dew Point': ['24']}

Sites = {}
SurfaceMetData = '/data/realtime/CsiDatalogger/SurfaceMet/'
HistoryPath = '/home/dms7/process/data/ShefProducts/24HrHistory/'
RealTimePath = '/data/realtime/HydroProductsNWS/1HrShefSurfaceMet/'  #

try:
    db = MySQLdb.connection(host='host', user='user',
                            passwd='passwd!', db='db')
except:
    print "Error connecting to psdmeta MySQL DB"
    SendEmailAlert("Error connecting to psdmeta MySQL DB")
    sys.exit()

# Query the DB to find sites with SurfaceMet Instrumentation

db.query("""Select site_has_inst.SiteID, site.City, site.State, site.Latitude, site.Longitude, site.Elevation, site.NwsSiteID 
From site_has_inst, site, inst_manufacturer, inst_type
Where inst_type.TypeID = site_has_inst.TypeID
AND site_has_inst.SiteID = site.SiteID
AND inst_manufacturer.ManufacturerID = inst_type.ManufacturerID
AND inst_type.CategoryID IN (12,15,16,21,24)
AND site.RealTimeDisplay = 'Y'
AND site_has_inst.Active = 'Y'
AND site_has_inst.InstRemovalDate is null
group by site_has_inst.SiteID;""")

r = db.store_result()

# Create Site Objects

for row in r.fetch_row(0):

        # SurfMetSites[row[0]] = [ row[1], row[2], row[3], row[4], row[5], ]

    Sites[row[0]] = SurfaceMetSite(
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
	AND inst_type.CategoryID IN (12,15,16,21,24) \
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

# Calculate 24HRs of SurfaceMet Data

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

                        if LineData[i].find(DataType) >= 0 \
                            and LineData[i].find('Soil') < 0:

                            Index = i

                            if DataType == 'Precipitation (mm)':

                                DataTotal = GetPrecipitation(
                                    site,
                                    FilePath,
                                    Index,
                                    BeginTime,
                                    EndTime,
                                    Sites[site].getSampleRate(),
                                    )

                                Sites[site].setDataValue(DataType,
                                        BeginTime, DataTotal)

                            if DataType == 'Scalar Wind Speed (m/s)':

                                DataTotal = GetWindSpeed(
                                    site,
                                    FilePath,
                                    Index,
                                    BeginTime,
                                    EndTime,
                                    Sites[site].getSampleRate(),
                                    )

                                Sites[site].setDataValue(DataType,
                                        BeginTime, DataTotal)

                            if DataType == 'Wind Direction (degrees)':

                                DataTotal = GetWindDirection(
                                    site,
                                    FilePath,
                                    Index,
                                    BeginTime,
                                    EndTime,
                                    Sites[site].getSampleRate(),
                                    )

                                Sites[site].setDataValue(DataType,
                                        BeginTime, DataTotal)

                            if DataType == 'Temperature (C)':

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

                            if DataType == 'Relative Humidity (%)':

                                DataTotal = GetWindDirection(
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

# Calculate Dervied Data Vairables.

while BeginTime < CurrentTime:

    SiteTime = '%2d%02d%02d%02d' % (BeginTime.tm_year % 100,
                                    BeginTime.tm_mon,
                                    BeginTime.tm_mday,
                                    BeginTime.tm_hour)

    for site in Sites.keys():

        for DataType in DerivedDataTypes.keys():

            for InstCatID in DerivedDataTypes[DataType]:

                if InstCatID in Sites[site].getInstCat():

                    if DataType == 'Dew Point':

                        TemperatureDataValues = \
                            Sites[site].getDataValue('Temperature (C)')
                        RelativeHumidtyValues = \
                            Sites[site].getDataValue('Relative Humidity (%)'
                                )

                        if SiteTime in TemperatureDataValues.keys() \
                            and SiteTime \
                            in RelativeHumidtyValues.keys():

                            Temperature = .55555 \
                                * (float(TemperatureDataValues[SiteTime][0])
                                   - 32)

                            DataTotal = GetDewPoint(Temperature,
                                    RelativeHumidtyValues[SiteTime][0],
                                    BeginTime)

                            Sites[site].setDataValue(DataType,
                                    BeginTime, DataTotal)

    BeginTime = TimeOffset(BeginTime, 1)

HistoryStartTime = TimeOffset(CurrentTime, -1)  # Use Begin Hour for History File.

# Write 24Hr Historical File

OutPutPath = '%s%04d/%03d/' % (HistoryPath, HistoryStartTime.tm_year,
                               HistoryStartTime.tm_yday)

HistOutPutFile = '%s%04d/%03d/SHEFSurfaceMet%2d%03d%02d.txt' % (
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
    print "Can't write 24 HR Surface Met History file."

        # SendEmailAlert("Can't write 24 HR Surface Met History file.")

    sys.exit()

for site in Sites.keys():

    for DataType in RawDataTypes.keys():

        print DataType

        DataValues = Sites[site].getDataValue(DataType)

        for DataValue in DataValues.keys():

            DataTime = '%2d%02d%02d%02d%02d' \
                % (DataValues[DataValue][1].tm_year % 100,
                   DataValues[DataValue][1].tm_mon,
                   DataValues[DataValue][1].tm_mday,
                   DataValues[DataValue][1].tm_hour,
                   DataValues[DataValue][1].tm_min)

            HistoryFile.write(site)
            HistoryFile.write(',')
            HistoryFile.write(DataValue)
            HistoryFile.write(',')
            HistoryFile.write(DataType)
            HistoryFile.write(',')
            HistoryFile.write(str(DataValues[DataValue][0]))
            HistoryFile.write(',')
            HistoryFile.write(DataTime)
            HistoryFile.write('\n')

    for DataType in DerivedDataTypes.keys():

        DataValues = Sites[site].getDataValue(DataType)

        for DataValue in DataValues.keys():

            HistoryFile.write(site)
            HistoryFile.write(',')
            HistoryFile.write(DataValue)
            HistoryFile.write(',')
            HistoryFile.write(DataType)
            HistoryFile.write(',')
            HistoryFile.write(str(DataValues[DataValue][0]))
            HistoryFile.write(',')
            HistoryFile.write(DataTime)
            HistoryFile.write('\n')

# Write out Current Hour in SHEF

ShefHourlyPath = '%s%04d/%03d' % (RealTimePath, CurrentTime.tm_year,
                                  CurrentTime.tm_yday)

ShefHourlyFile = '%s%04d/%03d/1HrShefMet%02d%03d%02d.txt' % (
    RealTimePath,
    CurrentTime.tm_year,
    CurrentTime.tm_yday,
    CurrentTime.tm_year % 100,
    CurrentTime.tm_yday,
    CurrentTime.tm_hour,
    )

ShefHourlyFileOld = '%s1HrShefMet%02d%03d%02d.txt' % (RealTimePathOld,
        CurrentTime.tm_year % 100, CurrentTime.tm_yday,
        CurrentTime.tm_hour)

if not os.path.exists(ShefHourlyPath):
    try:
        print 'Creating Dir ' + ShefHourlyPath
        os.makedirs(ShefHourlyPath)
    except:
        print 'Failed to create dir ' + ShefHourlyPath

try:
    ShefMasterFH = open(ShefHourlyFile, 'wb')
except:
    print "Can't write SHEF met file"

        # SendEmailAlert("Can't open  24 HR Precip History file.")

    sys.exit()

ShefHeader = \
    '''.B DEN %02d%02d%02d DH%02d/DQZ/PPHRZZZ/XRIRZZZ/USIRZZZ/TAIRZZZ/UDIRZZZ/TDIRZZZ\r
: PSD SURFACE METEOROLOGY\r
:     PRECIP /     RH /WIND SPD/   TEMP /WIND DIR/ DEW PT\r
''' \
    % (CurrentTime.tm_year % 100, CurrentTime.tm_mon,
       CurrentTime.tm_mday, CurrentTime.tm_hour)

ShefMasterFH.write(ShefHeader)

BeginTime = TimeOffset(CurrentTime, -1)

while BeginTime < CurrentTime:

    for site in sorted(Sites.keys()):

        if Sites[site].getNwsSiteID() != None:

            ShefSiteEntry = '%s' % Sites[site].getNwsSiteID().upper()
        else:

            ShefSiteEntry = '%s%s' % (Sites[site].getSiteID().upper(),
                    Sites[site].getState())

        ShefMasterFH.write(ShefSiteEntry)

        State = Sites[site].getState().upper()
        Lat = float(Sites[site].getLat())
        Long = float(Sites[site].getLong())
        Elevation = float(Sites[site].getElevation()) * 3.2808399
        Name = Sites[site].getCity().upper()

        SiteMetaInfo = ': %s, %s (%.2f, %.2f, %.0f FT)' % (Name, State,
                Lat, Long, Elevation)

        NumOfDataTypes = len(RawDataTypes)

        Counter = 1

        for DataType in sorted(RawDataTypes.keys()):

            DataValues = Sites[site].getDataValue(DataType)

            CurrentHourData = '%2d%02d%02d%02d' % (BeginTime.tm_year
                    % 100, BeginTime.tm_mon, BeginTime.tm_mday,
                    BeginTime.tm_hour)

            try:

                if float(DataValues[CurrentHourData][0] > -8888):
                    ShefLineEntry = ' %6.2f /' \
                        % float(DataValues[CurrentHourData][0])
                    ShefMasterFH.write(ShefLineEntry)
                else:
                    ShefMasterFH.write('  -9999 /')
            except:
                ShefMasterFH.write('        /')

        Counter = 1

        for DataType in sorted(DerivedDataTypes.keys()):

            DataValues = Sites[site].getDataValue(DataType)

            CurrentHourData = '%2d%02d%02d%02d' % (BeginTime.tm_year
                    % 100, BeginTime.tm_mon, BeginTime.tm_mday,
                    BeginTime.tm_hour)

            try:
                if float(DataValues[CurrentHourData][0] > -8888):
                    ShefLineEntry = ' %6.2f  ' \
                        % float(DataValues[CurrentHourData][0])
                    ShefMasterFH.write(ShefLineEntry)
                else:
                    ShefMasterFH.write('  -9999  ')
            except:

                ShefMasterFH.write('         ')

            if Counter < len(DerivedDataTypes.keys()):
                ShefMasterFH.write('        /')

            Counter += 1

        ShefMasterFH.write(SiteMetaInfo + '\r\n')

    BeginTime = TimeOffset(BeginTime, 1)

ShefMasterFH.write('.END\r\n')

# Open Previous Historical File and find any differences with current data

PreviousHistTime = TimeOffset(CurrentTime, -2)  # Since using Begin Hour open previous hour is 2 hours past.

HistOutPutPath = '%s%04d/%03d/' % (HistoryPath,
                                   PreviousHistTime.tm_year,
                                   PreviousHistTime.tm_yday)

HistOutPutFile = '%s%04d/%03d/SHEFSurfaceMet%2d%03d%02d.txt' % (
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
    print 'Can not open 24 HR Surface Met History file.'

        # SendEmailAlert("Can't open  24 HR Surface Met History file.")

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

    NewRecord = round(float(NewRecord), 2)
    OldRecord = round(float(LineData[3]), 2)

    if NewRecord != OldRecord:
        print 'Changed Record'
        TimeStamp = LineData[1] + LineData[0]
        ChangeRecords[TimeStamp] = [OldRecord, NewRecord]
        print NewRecord, OldRecord
        print TimeStamp

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

                    ShefHeader = \
                        '.BR DEN %02d%02d%02d DH%02d/DQZ/PPHRZZZ/XRIRZZZ/USIRZZZ/TAIRZZZ/UDIRZZZ/TDIRZZZ\r\n' \
                        % (ShefChangeTime.tm_year % 100,
                           ShefChangeTime.tm_mon,
                           ShefChangeTime.tm_mday,
                           ShefChangeTime.tm_hour)
                    ShefMasterFH.write(ShefHeader)

                if Sites[site].getNwsSiteID() != None:

                    ShefSiteEntry = '%s' \
                        % Sites[site].getNwsSiteID().upper()
                else:

                    ShefSiteEntry = '%s%s' \
                        % (Sites[site].getSiteID().upper(),
                           Sites[site].getState())

                ShefSiteEntry = '%s%s' \
                    % (Sites[site].getSiteID().upper(),
                       Sites[site].getState())

                ShefMasterFH.write(ShefSiteEntry)

                State = Sites[site].getState().upper()
                Lat = float(Sites[site].getLat())
                Long = float(Sites[site].getLong())
                Elevation = float(Sites[site].getElevation()) \
                    * 3.2808399
                Name = Sites[site].getCity().upper()

                SiteMetaInfo = ': %s, %s (%.2f, %.2f, %.0f FT)' \
                    % (Name, State, Lat, Long, Elevation)

                NumOfDataTypes = len(RawDataTypes)

                HeaderCounter += 1

                for DataType in sorted(RawDataTypes.keys()):

                    DataValues = Sites[site].getDataValue(DataType)

                    CurrentHourData = '%2d%02d%02d%02d' \
                        % (BeginTime.tm_year % 100, BeginTime.tm_mon,
                           BeginTime.tm_mday, BeginTime.tm_hour)

                    try:

                        if float(DataValues[CurrentHourData][0]
                                 > -8888):
                            ShefLineEntry = ' %6.2f /' \
                                % float(DataValues[CurrentHourData][0])
                            ShefMasterFH.write(ShefLineEntry)
                        else:
                            ShefMasterFH.write('  -9999 /')
                    except:

                        ShefMasterFH.write('        /')

                Counter = 1

                for DataType in sorted(DerivedDataTypes.keys()):

                    DataValues = Sites[site].getDataValue(DataType)

                    CurrentHourData = '%2d%02d%02d%02d' \
                        % (BeginTime.tm_year % 100, BeginTime.tm_mon,
                           BeginTime.tm_mday, BeginTime.tm_hour)

                    try:

                        if float(DataValues[CurrentHourData][0]
                                 > -8888):
                            ShefLineEntry = ' %6.2f ' \
                                % float(DataValues[CurrentHourData][0])
                            ShefMasterFH.write(ShefLineEntry)
                        else:
                            ShefMasterFH.write('  -9999  ')
                    except:
                        ShefMasterFH.write('         ')

                if Counter < len(DerivedDataTypes.keys()):
                    ShefMasterFH.write('        /')

                Counter += 1

                ShefMasterFH.write('\r\n')

        BeginTime = TimeOffset(BeginTime, 1)

        if HeaderCounter > 0:

            ShefMasterFH.write('.END\r\n')

ShefMasterFH.close()

# Cleanup Old 24 Hour History Files.

FileScrubTime = TimeOffset(EndTime, -168)

ScrubExpression = 'SHEFSurfaceMet%02d%03d*' % (FileScrubTime.tm_year
        % 100, FileScrubTime.tm_yday)

ScrubRemovalCommand = 'rm ' + HistoryPath + ScrubExpression

os.system(ScrubRemovalCommand)

# Cleanup Old Shef Files

ScrubExpression = '1HrShefMet%02d%03d*' % (FileScrubTime.tm_year % 100,
        FileScrubTime.tm_yday)

ScrubRemovalCommand = 'rm ' + RealTimePath + ScrubExpression

os.system(ScrubRemovalCommand)
