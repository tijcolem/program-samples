#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib
import shutil
import time
import os
import sys
import glob

print '\nRunning IngestGpsIpwDataFromGsd.py on ' + time.ctime() + '\n'

if len(sys.argv) != 2:
    print '\nUSAGE:  IngestGpsIpwDataFromGsd.py Number of Days To Download',
    exit()

  # #################  Begin User Configuration ######################

  # MODIFY THE FOLLOWING HASH LIST TO ADD OR REMOVE SITES
  # Define FSL SiteID and PSD SiteID
  # SYNTAX:  'GsdSiteID' => 'PsdSiteID'

GpsIpwSites = {  # GPS sites
    'ANW1': 'anw',
    'BBY7': 'bby',
    'BBD2': 'bbd',
    'BKF1': 'bkf',
    'CCL1': 'ccl',
    'CCO3': 'cco',
    'CCR2': 'ccr',
    'CFC6': 'cfc',
    'FBG2': 'fbg',
    'OFT1': 'oft',
    'GLB1': 'glb',
    'KNV1': 'knv',
    'GMN1': 'gmn',
    'LDS1': 'lds',
    'LHS1': 'lhs',
    'LVW1': 'lvw',
    'EWN1': 'EWN',
    'MBG1': 'mbg',
    'MPI2': 'mpi',
    'OVL1': 'ovl',
    'OHT1': 'oht',
    'PFD1': 'pfd',
    'PPBA': 'ppb',
    'PTS1': 'pts',
    'RVD2': 'rvd',
    'SEAI': 'sea',
    'SHS6': 'shs',
    'SNS1': 'sns',
    'STD2': 'std',
    'SWY1': 'swy',
    'TRK1': 'trk',
    'UCLP': 'usc',
    'WPT2': 'wpt',
    'WFC1': 'wfc',
    'P140': 'smt',
    'P188': 'brg',
    'P196': 'mhl',
    'P618': 'bkr',
    'P315': 'lgt',
    'P729': 'sms',
    'P491': 'lqt',
    'P316': 'klm',
    'P344': 'crn',
    'CNPP': 'cna',
    'P217': 'lcd',
    'P224': 'svc',
    'P305': 'pld',
    'P306': 'wcc',
    'P534': 'cpk',
    'P059': 'pan',
    'P176': 'mck',
    'P268': 'ffm',
    'P630': 'omm',
    'P056': 'prv',
    'P174': 'log',
    'P298': 'ccy',
    'P304': 'mta',
    'P725': 'ser',
    'P523': 'lso',
    'BURN': 'brn',
    'GMPK': 'gmp',
    'P011': 'spr',
    'P015': 'duc',
    'P020': 'dyl',
    'P021': 'rdh',
    'P022': 'lgr',
    'P023': 'mca',
    'P025': 'bna',
    'P029': 'mnt',
    'P058': 'hmb',
    'P066': 'jcb',
    'P107': 'gts',
    'P392': 'wrp',
    'P349': 'wdl',
    'P365': 'csb',
    'P380': 'otc',
    'P387': 'ssh',
    'P395': 'rsl',
    'P398': 'sfr',
    'P422': 'fth',
    'P436': 'dgs',
    'P445': 'wca',
    'P499': 'dsc',
    'P623': 'vdj',
    'P090': 'drn',
    'P171': 'stl',
    'P177': 'cdt',
    'P183': 'bdh',
    'P206': 'cyc',
    'P212': 'lnv',
    'P270': 'hns',
    'P272': 'srl',
    'P277': 'pnp',
    'P309': 'cva',
    'P513': 'pns',
    'P565': 'doa',
    'P625': 'cos',
    'TALH': 'tlh',
    'SNY1': 'sny',
    'PQL1': 'pql',
    'JZI1': 'jzi',
    'TALH': 'tlh',
    'BCWR': 'bcw',
    'VNDP': 'vnd',
    'BKR2': 'bkd',
    'BLSA': 'bls',
    'BSRY': 'bsr',
    'CAT2': 'ctd',
    'CHO5': 'cho',
    'CME5': 'cme',
    'CMOD': 'cmo',
    'COTD': 'cot',
    'CRRS': 'crr',
    'CSN1': 'csn',
    'DHLG': 'dhl',
    'FVPK': 'fvp',
    'GVRS': 'gvr',
    'HBCO': 'hbc',
    'HIVI': 'hvi',
    'JPLM': 'jpl',
    'LJRN': 'ljr',
    'LNC1': 'lnc',
    'OEOC': 'oeo',
    'P474': 'flk',
    'P475': 'ptl',
    'P486': 'bos',
    'P496': 'elo',
    'P505': 'nld',
    'P510': 'cla',
    'POTR': 'pto',
    'PPBF': 'prs',
    'RAAP': 'raa',
    'SBCC': 'mnv',
    'SCIP': 'sci',
    'SIO5': 'sio',
    'SLMS': 'slm',
    'TABV': 'tab',
    'TORP': 'tor',
    'UCSB': 'ucs',
    'USGC': 'usg',
    'VAN5': 'van',
    'WHYT': 'why',
    'WIDC': 'wid',
    'ZLA1': 'zla',
    'ZOA1': 'zoa',
    'FKS1': 'fks',
    'AST3': 'ast',
    'TDE1': 'tde',
    'ACV1': 'acv',
    }

  # ##################  End User Configuration #######################

  # initialize variables

FtpServer = 'gpsftp.fsl.noaa.gov'
FtpUserName = 'anonymous'
FtpPassword = 'anonymous'
FtpBaseDir = './'

WorkPath = \
    '\\Program Files\\ESRL Applications\\IngestScripts\\Workspace\\GPS'
OutputBasePath = \
    '\\\\psdobs.psd.esrl.noaa.gov\\data\\realtime\\GpsTrimble\\WaterVapor'

NumArchiveDays = int(sys.argv[1])
SiteIndex = 0
DateIndex = 2  # column in GPS file where the data is.
NumRecord = 0
GpsDownloadKeyFound = False
GpsStoredKeyFound = False
TransferSuccess = True
MissingDataCounter = 0
RecoveredDataCounter = 0
gpsfiles = {}
GpsStoredData = {}
os.chdir(WorkPath)


def RemoveFiles(DirPath):

    for localfile in os.listdir(DirPath):

        if os.path.isfile(DirPath + '\\' + localfile):

            os.remove(localfile)


def Minus2Hour(Hour):
    if Hour == 1:
        return 23
    elif Hour == 0:
        return 22
    else:
        return Hour - 2


def WriteDownloadedData(site, file, linenum):

    OutputFile = '%s\\%s%02d%03d.txt' % (WorkPath, site,
            file[linenum][DateIndex].tm_year % 100,
            file[linenum][DateIndex].tm_yday)

    try:
        fileobj = open(OutputFile, 'ab')
    except:
        print 'cannot open file ' + OutputFile
        return False

    fileobj.write('%02d%03d,%02d:%02d' % (file[linenum][2].tm_year
                  % 100, file[linenum][DateIndex].tm_yday,
                  file[linenum][2].tm_hour,
                  file[linenum][DateIndex].tm_min))
    for l in range(3, len(file[linenum])):

        fileobj.write(', ' + file[linenum][l])


def WriteStoredData(site, file, linenum):

    OutputFile = '%s\\%s%s.txt' % (WorkPath, site, file[linenum][0])

    try:
        fileobj = open(OutputFile, 'ab')
    except:
        print 'cannot open file ' + OutputFile
        return False

    fileobj.write(file[linenum][0] + ',' + file[linenum][1])

    for l in range(2, len(file[linenum])):
        fileobj.write(',' + file[linenum][l])


### Main ###

RemoveFiles(WorkPath)  # cleanup any files in working directory.

try:
    f = ftplib.FTP(FtpServer, FtpUserName, FtpPassword)
    f.cwd(FtpBaseDir)
except:
    print 'Error ',
    print sys.exc_info()[1]
    exit()

utctime = time.gmtime()
yday = utctime.tm_yday

for DayIndex in range(NumArchiveDays):  # loop through by number of days.

    FileExp = 'GPSIPW_CSV_gpsmet.%02d%03d*' % (utctime.tm_year % 100,
            yday)

    for file in f.nlst(FileExp):  # retrive all files from ftp server.

        try:
            print 'Downloading file ' + file
            f.retrbinary('RETR ' + file, open(file, 'wb').write)
        except:
            print 'error transferring ' + file + ' from ' + FtpServer
            print sys.exc_info()[1]

    yday = yday - 1

f.close()

for localfile in os.listdir(WorkPath):  # for all files just received via ftp.

    if os.path.isfile(WorkPath + '\\' + localfile):

        fh = open(localfile, 'rb')

        data = fh.readlines()

        Header = data[0].split(', ')

        if len(Header) == 3 and Header[0] \
            == 'Ground Based GPS Integrated Precipitable Water Vapor':  # QC check for each file to ensure correct formating

            gpsfiles[localfile] = data  # loading all data into memory

            fh.close()

for key in gpsfiles:  # changing the date index to a time struct.

    linenum = 0

    print 'Processing Data File ' + key

    for line in gpsfiles[key]:

        gpsfiles[key][linenum] = line.split(', ')

        if linenum > 0:

            try:
                gpsfiles[key][linenum][DateIndex] = \
                    time.strptime(gpsfiles[key][linenum][DateIndex],
                                  '%y/%m/%d %H:%M:%S')
            except:
                print 'line ' + str(linenum) + ' in gps file ' + key \
                    + ' could not be converted to time object'

            linenum += 1
        else:

            linenum += 1

yday = utctime.tm_yday  # load all stored gps files into memory

for DayIndex in range(NumArchiveDays):

    for directory in os.listdir(OutputBasePath):  # for stored files

        OutputPath = OutputBasePath + '\\' + directory + '\\' \
            + str(utctime.tm_year).zfill(4) + '\\' + str(yday).zfill(3)

        if os.path.isdir(OutputPath):

            FileExp = '*%02d%03d*' % (utctime.tm_year % 100, yday)

            for file in glob.glob(OutputPath + '\\' + FileExp):

                fh = open(file, 'rb')

                data = fh.readlines()

                GpsStoredData[os.path.basename(file)] = data

    yday -= 1

for key in GpsStoredData:  # changing the date index to a time struct.

    linenum = 0
    for line in GpsStoredData[key]:

        GpsStoredData[key][linenum] = line.split(',')

        linenum = linenum + 1

yday = utctime.tm_yday

for key in sorted(GpsIpwSites.keys(), reverse=True):  # finding rows of data in gps files that match site listing and writing output.

    for gpsfile in sorted(gpsfiles.keys()):  # for each gps file recently downloaded

        GpsDownloadKeyFound = False

        for i in range(len(gpsfiles[gpsfile])):  # for number of lines in gps file

            if i != 0:  # skip header line

                if gpsfiles[gpsfile][i][0] == key:  # find a match in each downloaded file

                    GpsDownloadKeyFound = True
                    GpsStoredKeyFound = False

                    YearDate = '%02d%03d' \
                        % (gpsfiles[gpsfile][i][2].tm_year % 100,
                           gpsfiles[gpsfile][i][DateIndex].tm_yday)
                    HourMin = '%02d:%02d' \
                        % (gpsfiles[gpsfile][i][DateIndex].tm_hour,
                           gpsfiles[gpsfile][i][DateIndex].tm_min)
                    FileExp = '%s%02d%03d%s' % (GpsIpwSites[key],
                            gpsfiles[gpsfile][i][DateIndex].tm_year
                            % 100,
                            gpsfiles[gpsfile][i][DateIndex].tm_yday,
                            '.txt')

                    if FileExp in GpsStoredData.keys():

                        for l in range(len(GpsStoredData[FileExp])):

                            if YearDate == GpsStoredData[FileExp][l][0] \
                                and HourMin \
                                == GpsStoredData[FileExp][l][1]:

                                GpsStoredKeyFound = True

                                if gpsfiles[gpsfile][i][3] == '-9.99':

                                    WriteStoredData(GpsIpwSites[key],
        GpsStoredData[FileExp], l)
                                elif gpsfiles[gpsfile][i][3] \
                                    != GpsStoredData[FileExp][l][2]:

                                    WriteDownloadedData(GpsIpwSites[key],
        gpsfiles[gpsfile], i)
                                else:

                                    WriteStoredData(GpsIpwSites[key],
        gpsfiles[gpsfile], i)

                    if not GpsStoredKeyFound:  # found a site in the downloaded files but not in the stored data.

                        WriteDownloadedData(GpsIpwSites[key],
                                gpsfiles[gpsfile], i)

        if not GpsDownloadKeyFound:

            if len(gpsfiles[gpsfile]) > 1:  # testing to make sure the file has more than one record.

                MissingDataCounter += 1

                try:
                    YearDate = '%02d%03d' \
                        % (gpsfiles[gpsfile][1][2].tm_year % 100,
                           gpsfiles[gpsfile][1][DateIndex].tm_yday)

                    HourMin = '%02d:%02d' \
                        % (gpsfiles[gpsfile][1][DateIndex].tm_hour,
                           gpsfiles[gpsfile][1][DateIndex].tm_min)

                    FileExp = '%s%02d%03d%s' % (GpsIpwSites[key],
                            gpsfiles[gpsfile][1][DateIndex].tm_year
                            % 100,
                            gpsfiles[gpsfile][1][DateIndex].tm_yday,
                            '.txt')
                except:
                    print sys.exc_info()[1],
                    print ' failed to convert time struct in line 2 to a year date'
                    FileExp = 'None'

                if FileExp in GpsStoredData.keys():

                    for l in range(len(GpsStoredData[FileExp])):

                        if YearDate == GpsStoredData[FileExp][l][0] \
                            and HourMin == GpsStoredData[FileExp][l][1]:

                            RecoveredDataCounter += 1

                            WriteStoredData(GpsIpwSites[key],
                                    GpsStoredData[FileExp], l)

for localfile in os.listdir(WorkPath):  # moving files to output directory.

    if os.path.isfile(WorkPath + '\\' + localfile):

        if localfile[:3] in GpsIpwSites.values():

            Year = str(int(localfile[3:5]) + 2000)
            Yday = localfile[5:8]

            OutputPath = OutputBasePath + '\\' + localfile[:3] + '\\' \
                + str(Year).zfill(4) + '\\' + str(Yday).zfill(3)

            if not os.path.exists(OutputPath):

                os.makedirs(OutputPath)

            try:
                OutputFile = OutputPath + '\\' + localfile
                Command = 'rm ' + OutputFile
                os.system(Command)
                print 'Transferring ' + os.path.abspath(localfile) \
                    + ' to ' + OutputPath + '\n',
                shutil.move(os.path.abspath(localfile), OutputPath
                            + '\\' + localfile)
            except:
                print 'failed to transfer' + localfile,
                print sys.exc_info()[1],
                TransferSuccess = False

if TransferSuccess:
    print 'Total number of records not found in Gps Downloaded data: ' \
        + str(MissingDataCounter)
    print 'Total number of records recovered in stored data: ' \
        + str(RecoveredDataCounter)
    print 'All GPS files parsed and transfered successfully from ' \
        + FtpServer + ' to ' + OutputBasePath,
else:
    print 'Error in one or more file transfers, check log for the exact file',

RemoveFiles(WorkPath)
