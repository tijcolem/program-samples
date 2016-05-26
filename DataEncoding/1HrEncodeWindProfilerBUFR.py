#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import ftplib
import shutil
import datetime
import os
import sys
import re
import math

print 'Running 1HrWindProfilerSpeedDirXml.py on ' \
    + datetime.datetime.utcnow().isoformat() + ' utc'


def TimeOffset(Time, HrsOffset):

    Time = Time + datetime.timedelta(hours=HrsOffset)

    return Time


def FindSubString(
    Content,
    Beg,
    End,
    Pos,
    ):

    StringBeginIndex = Content.find(Beg, Pos)

    if StringBeginIndex != -1:

        StringBeginIndex = StringBeginIndex + len(Beg)

    StringEndIndex = Content.find(End, StringBeginIndex)

    Content = [StringBeginIndex, StringEndIndex]

    return Content


def FindSubStringRe(
    Content,
    Beg,
    End,
    Pos,
    ):

    Prog = re.compile('HT  .+\n')

    ReStartString = Prog.search(Content, Pos)

    if ReStartString:

        StringBeginIndex = ReStartString.end()

        Prog = re.compile(End)

        ReEndString = Prog.search(Content, StringBeginIndex)

        if ReEndString:

            StringEndIndex = ReEndString.start()

            Content = [StringBeginIndex, StringEndIndex]

            return Content
    else:

        return [0, 0]


UTCTime = datetime.datetime.utcnow()
StartTimeObj = TimeOffset(UTCTime, -1)
EndTimeObj = UTCTime
BaseInputPath = '/data/realtime'
BaseOutputPath = '/data/realtime'

ProgramName = \
    'EncodeWindProfilerBUFR.py'

WindSites = {}

try:
    db = MySQLdb.connection(host='host', user='user', passwd='passwd!', db='db')
except:
	print "Error connecting to MySQLdb"
	sys.exit()
						
db.query("""
Select site_has_inst.SiteID, data_type.RealtimeDirectoryPath, site_has_inst_data.DataTypeID
From site_has_inst, site, data_type, site_has_inst_data
Where site_has_inst_data.OperationalID = site_has_inst.OperationalID
AND site_has_inst_data.DataTypeID = data_type.DataTypeID
AND site_has_inst_data.EndDate is null
AND site_has_inst.Active = 'Y'
AND site_has_inst.SiteID = site.SiteID
AND site.RealTimeDisplay = 'Y'
AND site_has_inst.Active = 'Y'
AND site_has_inst.InstRemovalDate is null
AND site_has_inst.TypeID in (3,28) 
AND site_has_inst_data.DataTypeID in (57);
""")

OutputPaths = {'57': '/Radar449/BufrWwWind'}

# Remove this once and store in DB when we get offical WMO codes

WMOIDs = {
    'acv': '78998',
    'ast': '78996',
    'bby': '78999',
    'fks': '78997',
    'oth': '78995',
    }

r = db.store_result()

for row in r.fetch_row(0):
    WindSites[row[0]] = [row[1], row[2]]

DeleteSql = 'delete from tmp_wind_profiler;'

db.query(DeleteSql)

BeginTimeObj = StartTimeObj

while BeginTimeObj < EndTimeObj:

    WindDirDic = {}
    WindSpeedDic = {}

    for Site in WindSites.keys():

        DataTypeInputBasePath = WindSites[Site][0]
        DataTypeID = WindSites[Site][1]

        InputFile = '%s%s/%s/%04d/%03d/%s%02d%03d.%02dw' % (
            BaseInputPath,
            DataTypeInputBasePath,
            Site,
            BeginTimeObj.timetuple().tm_year,
            BeginTimeObj.timetuple().tm_yday,
            Site.lower(),
            BeginTimeObj.timetuple().tm_year % 100,
            BeginTimeObj.timetuple().tm_yday,
            BeginTimeObj.timetuple().tm_hour,
            )

        if not os.path.exists(InputFile):
            print 'File does not exist ' + InputFile
            continue

        if DataTypeID not in OutputPaths.keys():
            print 'DataTypeID ' + DataTypeOputBasePath \
                + ' not defined in OutputPaths.  Must define new ID and output path in HashMap'
            continue

        if Site not in WMOIDs.keys():
            print 'Site ' + Site \
                + ' does not have a WMO Code. Must define a new WMO ID in the HashMap'
            continue

        OutputPath = '%s%s/%s/%04d/%03d' % (BaseOutputPath,
                OutputPaths[DataTypeID], Site,
                BeginTimeObj.timetuple().tm_year,
                BeginTimeObj.timetuple().tm_yday)

        Command = ProgramName + ' ' + Site + ' ' + WMOIDs[Site] + ' ' \
            + InputFile + ' ' + OutputPath

        print Command

        os.system(Command)

    BeginTimeObj = TimeOffset(BeginTimeObj, 1)
