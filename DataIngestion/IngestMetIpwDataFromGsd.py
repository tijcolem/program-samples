#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib
import shutil
import time
import os
import sys
import glob
import re

print '\nRunning IngestMetIpwDataFromGsd.py on ' + time.ctime() + '\n'

  # #################  Begin User Configuration ######################

  # MODIFY THE FOLLOWING HASH LIST TO ADD OR REMOVE SITES
  # Define FSL SiteID and PSD SiteID
  # SYNTAX:  'GsdSiteID' => 'PsdSiteID'

GSDMetSites = {  # GPS sites
    'p140': 'smt',
    'p188': 'brg',
    'p618': 'bkr',
    'p315': 'lgt',
    'p729': 'sms',
    'p491': 'lqt',
    'p316': 'klm',
    'p344': 'crn',
    'cnpp': 'cna',
    'p196': 'mhl',
    'p217': 'lcd',
    'p224': 'svc',
    'p305': 'pld',
    'p306': 'wcc',
    'p534': 'cpk',
    'p059': 'pan',
    'p176': 'mck',
    'p268': 'ffm',
    'p630': 'omm',
    'p090': 'drn',
    'p056': 'prv',
    'p174': 'log',
    'p298': 'ccy',
    'p304': 'mta',
    'p725': 'ser',
    'p523': 'lso',
    'burn': 'brn',
    'gmpk': 'gmp',
    'p011': 'spr',
    'p015': 'duc',
    'p020': 'dyl',
    'p021': 'rdh',
    'p022': 'lgr',
    'p023': 'mca',
    'p025': 'bna',
    'p029': 'mnt',
    'p058': 'hmb',
    'p066': 'jcb',
    'p107': 'gts',
    'p392': 'wrp',
    'p349': 'wdl',
    'p365': 'csb',
    'p380': 'otc',
    'p387': 'ssh',
    'p395': 'rsl',
    'p398': 'sfr',
    'p422': 'fth',
    'p436': 'dgs',
    'p445': 'wca',
    'p499': 'dsc',
    'p623': 'vdj',
    'p171': 'stl',
    'p177': 'cdt',
    'p183': 'bdh',
    'p206': 'cyc',
    'p212': 'lnv',
    'p270': 'hns',
    'p272': 'srl',
    'p277': 'pnp',
    'p309': 'cva',
    'p513': 'pns',
    'p565': 'doa',
    'p625': 'cos',
    'talh': 'tlh',
    'vndp': 'vnd',
    }

  # ##################  End User Configuration #######################

  # initialize variables

FtpServer = 'gpsdmz.fsl.noaa.gov'
FtpUserName = 'anonymous'
FtpPassword = 'passwd'
FtpBaseDir = '/outgoing/gpsdist/met/'

WorkPath = \
    '\\Program Files\\ESRL Applications\\IngestScripts\\Workspace1'
OutPutBasePath = \
    '\\\\psdobs.psd.esrl.noaa.gov\\data\\realtime\CsiDatalogger\\SurfaceMet'

DataSynchString = 'END OF HEADER\n'
NumDataColumns = 13


def RemoveFiles(DirPath):

    for localfile in os.listdir(DirPath):

        if os.path.isfile(DirPath + '\\' + localfile):

            os.remove(DirPath + '\\' + localfile)


### Main ###

RemoveFiles(WorkPath)  # cleanup any files in working directory.

os.chdir(WorkPath)

utctime = time.gmtime()
yday = '%.3d' % utctime.tm_yday
year = '%.2d' % (utctime.tm_year % 100)
hour = utctime.tm_hour

try:
    f = ftplib.FTP(FtpServer, FtpUserName, FtpPassword)
except:
    print 'Error ',
    print sys.exc_info()[1]
    sys.exit()

for site in GSDMetSites:

    FtpPutDir = FtpBaseDir + year + str(yday) + '/' + site
    print FtpPutDir

    try:
        f.cwd(FtpPutDir)
        f.set_pasv(0)
    except:
        print 'Error trying to change directory ' + site
        continue

    files = f.nlst()

    for file in files:

        try:
            f.retrbinary('RETR ' + file, open(file, 'wb').write)
        except:
            print 'error transferring ' + file + ' from ' + FtpServer
            print sys.exc_info()[1]

f.close()

for localfile in os.listdir(WorkPath):  # for all files just received via ftp.

    if os.path.isfile(WorkPath + '\\' + localfile):

        SiteID = localfile[:4]

        if SiteID in GSDMetSites:

            SiteID = GSDMetSites[localfile[:4]]

            try:

                fh = open(WorkPath + '\\' + localfile, 'rb')
            except:
                print 'Unable to open file'
                continue

            data = fh.read()

            fh.close()

            StringBeginIndex = data.find(DataSynchString)

            if StringBeginIndex < 0:
                continue

            StringBeginIndex = StringBeginIndex + len(DataSynchString)

            StringEndIndex = len(data)

            Content = data[StringBeginIndex:StringEndIndex]

            RowContent = Content.split('\n')

            RowContent[0] = RowContent[0].strip()

            TimeStringLine = re.split(' +', RowContent[0])

            if len(TimeStringLine) != 13:

                print 'Parse error on ' + localfile \
                    + ' does not have 13 fields, skipping file.'

                continue

            try:
                TimeString = '%s %s %s %s' % (TimeStringLine[0],
                        TimeStringLine[1], TimeStringLine[2],
                        TimeStringLine[3])

                ObsTime = time.strptime(TimeString, '%y %m %d %H')
            except:

                print 'Unable to convert time into string'
                continue

            OutPutPath = '%s\\%s\\%04d\\%03d' % (OutPutBasePath,
                    SiteID, ObsTime.tm_year, ObsTime.tm_yday)

            if not os.path.exists(OutPutPath):

                os.makedirs(OutPutPath)

            OutputFile = '%s\\%s%02d%03d.%02dm' % (OutPutPath, SiteID,
                    ObsTime.tm_year % 100, ObsTime.tm_yday,
                    ObsTime.tm_hour)

            try:
                fileobj = open(OutputFile, 'wb')
            except:
                print 'cannot open file ' + OutputFile
                continue

            # print "Parsing " + localfile + " and tranfering to " + OutputFile

            for line in RowContent:

                line = line.strip()

                elements = re.split(' +', line)

                if len(elements) == NumDataColumns:

                    fileobj.write('110,%d,%d,%d' % (ObsTime.tm_year,
                                  ObsTime.tm_yday, ObsTime.tm_hour
                                  * 100 + int(elements[4])))

                    for i in range(6, len(elements)):
                        fileobj.write(',')
                        fileobj.write(elements[i])

                    fileobj.write('\n')

            fileobj.close()

print '\nIngestMetIpwDataFromGsd.py finshed on ' + time.ctime() + '\n'
