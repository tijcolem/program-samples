#!/usr/bin/python
# -*- coding: utf-8 -*-

# the mercurial revisioning system hosted at google code.
#
# Written by: J. de Kloe, KNMI, Initial version 25-Feb-2010
#
# Copyright J. de Kloe
# This software is licensed under the terms of the LGPLv3 Licence
# which can be obtained from https://www.gnu.org/licenses/lgpl.html

#  #[ imported modules

#
#Modified 4/15/2016 Tim Coleman
#Used for encoding Wind Profiler data as BUFR.  This is needed to properly ingest into AWIPS2. 
#

from __future__ import print_function
import os  # operating system functions
import sys
import re
import math
import datetime
import numpy as np  # import numerical capabilities
import random

# import BUFR wrapper module
# import pybufr_ecmwf

from pybufr_ecmwf.raw_bufr_file import RawBUFRFile
from pybufr_ecmwf.bufr_interface_ecmwf import BUFRInterfaceECMWF
from pybufr_ecmwf.bufr_template import BufrTemplate


#  #]
#  #[ define constants for the descriptors we need

class RadarProfilerData:

    def __init__(self, SiteID):

        self.SiteID = SiteID
        self.Lat = ''
        self.Long = ''
        self.Elev = ''
        self.CnsAvg = ''
        self.NumBeams = ''
        self.NumGates = ''
        self.PulseWidth = []
        self.GateSpace = []
        self.WD = {}
        self.WindComp = {}
        self.TotNum = {}
        self.SnrDB = {}
        self.DateTimes = []

    def getSiteID(self):
        return self.SiteID

    def setLatitude(self, Lat):
        self.Lat = Lat

    def setLongitude(self, Long):
        self.Long = Long

    def setElev(self, Elev):
        self.Elev = Elev

    def setCnsAvg(self, CnsAvg):
        self.CnsAvg = CnsAvg

    def setNumBeams(self, NumBeams):
        self.NumBeams = NumBeams

    def setNumGates(self, NumGates):
        self.NumGates = NumGates

    def setPulseWidth(self, PulseWidth):
        self.PulseWidth.append(int(PulseWidth))

    def setGateSpace(self, GateSpace):
        self.GateSpace.append(int(GateSpace))

    def setDateTime(self, DateTime):
        self.DateTimes.append(DateTime)

    def setWindDirection(
        self,
        Time,
        PulseWidth,
        WD,
        ):
        self.WD.setdefault(Time, {}).setdefault(int(PulseWidth),
                []).append(WD)

    def setWindComponents(
        self,
        Time,
        PulseWidth,
        WS,
        WD,
        TotNum,
        SnrDB,
        ):
        self.WindComp.setdefault(Time, {}).setdefault(int(PulseWidth),
                []).append([WS, WD, TotNum, SnrDB])

    def setTotalNumber(
        self,
        Time,
        PulseWidth,
        TotNum,
        ):
        self.SnrTotalNumber.setdefault(Time,
                {}).setdefault(int(PulseWidth), []).append(TotNum)

    def setSnrDB(
        self,
        Time,
        PulseWidth,
        SnrDB,
        ):
        self.SnrDB.setdefault(Time, {}).setdefault(int(PulseWidth),
                []).append(SnrDB)

    def getLatitude(self):
        return self.Lat

    def getLongitude(self):
        return self.Long

    def getElev(self):
        return self.Elev

    def getCnsAvg(self):
        return self.CnsAvg

    def getNumBeams(self):
        return self.NumBeams

    def getNumGates(self):
        return self.NumGates

    def getPulseWidth(self):
        return self.PulseWidth

    def getGateSpace(self):
        return self.GateSpace

    def getWindComponents(self):
        return self.WindComp

    def getWindDirections(self):
        return self.WD

    def getSnrDBs(self):
        return self.SnrDB

    def getTotalNums(self):
        return self.TotNum


# Define Base Paths for input/output

# define descriptor/codes that are used in the BUFR file.

YEAR = int('004001', 10)
MONTH = int('004002', 10)
MDAY = int('004003', 10)
HOUR = int('004004', 10)
MIN = int('004005', 10)
WMO_BLOCK_NUM = int('001001', 10)
WMO_STATION_NUM = int('001002', 10)
DD_LATITUDE_COARSE_ACCURACY = int('005002', 10)
DD_LONGITUDE_COARSE_ACCURACY = int('006002', 10)
STATION_HEIGHT = int('007001', 10)
TIME_SIGNIFICANCE = int('008021', 10)
TIME_PERIOD = int('004025', 10)
DD_WIND_SPEED = int('0010101011111010', 2)
DD_WIND_DIR = int('011001', 10)
DD_PRESSURE = int('010051', 10)  # pressure [pa]
DD_TEMPERATURE = int('012001', 10)  # [dry-bulb] temperature [K]
RAINFALL_SWE = int('013014', 10)  # [dry-bulb] temperature [K]
DD_RELATIVE_HUMD = int('013003', 10)  # [dry-bulb] temperature [K]
HEIGHT_INCREMENT = int('007005', 10)
WIND_PROFILER_SUB_MODE_INFO = int('25033', 10)  # [dry-bulb] temperature [K]
WIND_PROFILER_MODE_INFO = int('025032', 10)
WIND_PROFILER_QC_RESULTS = int('025034', 10)
RADAR_BACK_SCATTER = int('021192', 10)  # [dry-bulb] temperature [K]
WIND_W_COMPONENT = int('011006', 10)  # [dry-bulb] temperature [K]
TOTAL_NUMBER = int('008022', 10)
WIND_U_COMPONENT = int('011003', 10)
WIND_V_COMPONENT = int('011004', 10)
STD_DEV_HORIZONTAL_WIND_SPEED = int('011050', 10)
STD_DEV_VERTICAL_SPEED = int('011051', 10)


def populateRadarData(InputFile, SiteID):

    HeaderBeginIndexes = []
    HeaderLocationIndex = 2
    HeaderTimeIndex = 3
    HeaderConsusAvgIndex = 4
    HeaderNumBeamsIndex = 4
    HeaderNumGatesIndex = 4
    HeaderNumofRecordsIndex = 5
    HeaderPulseWidthIndex = 6
    HeaderGateSpace = 7
    DataStart = 10

    HeaderBeginIndexes = []

    try:
        FI = open(InputFile, 'rb')
        Contents = FI.readlines()
    except:
        print('Error opening file ' + InputFile)

    RadarData = RadarProfilerData(SiteID)  # Create New Radar Data Instance

    for i in range(0, len(Contents)):

    # Find all headers in the file.

        if Contents[i].find(SiteID.upper()) >= 0:

            HeaderBeginIndexes.append(i)

  # Loop through each header block

    for BeginIndex in HeaderBeginIndexes:

      # Parse contentes

        LatLong = re.split(' +', Contents[BeginIndex
                           + HeaderLocationIndex].lstrip(' ').rstrip(' '
                           ))
        Time = re.split(' +', Contents[BeginIndex
                        + HeaderTimeIndex].lstrip(' ').rstrip(' '))
        ConsensusAvgBeamsGates = re.split(' +', Contents[BeginIndex
                + HeaderConsusAvgIndex].lstrip(' ').rstrip(' '))
        NumOfRecords = re.split(' +', Contents[BeginIndex
                                + HeaderNumofRecordsIndex].lstrip(' '
                                ).rstrip(' '))
        PulseWidth = re.split(' +', Contents[BeginIndex
                              + HeaderPulseWidthIndex].lstrip(' '
                              ).rstrip(' '))
        GateSpace = re.split(' +', Contents[BeginIndex
                             + HeaderGateSpace].lstrip(' ').rstrip(' '))

        if len(LatLong) != 3:
            print('Error parsing Lat, Long and Elev in Header')
            print(sys.exc_info())
            sys.exit(1)
        else:
            RadarData.setLatitude(float(LatLong[0]))
            RadarData.setLongitude(float(LatLong[1]))
            RadarData.setElev(float(LatLong[2]))

        try:
            TimeObj = datetime.datetime(int('20' + Time[0]),
                    int(Time[1]), int(Time[2]), int(Time[3]),
                    int(Time[4]))
        except:
            print('Error parsing Time String')
            print(sys.exc_info())
            sys.exit(1)

        RadarData.setDateTime(TimeObj)

        if len(ConsensusAvgBeamsGates) != 3:
            print('Error parsing consensus averaging time (minutes); number of beams; number of range gates in Header'
                  )
            print(sys.exc_info())
            sys.exit(1)
        else:
            RadarData.setCnsAvg(int(ConsensusAvgBeamsGates[0]))
            RadarData.setNumBeams(int(ConsensusAvgBeamsGates[1]))
            RadarData.setNumGates(int(ConsensusAvgBeamsGates[2]))

        if len(PulseWidth) != 8:
            print('Error parsing pulse width in header')
            sys.exit(1)
        elif int(PulseWidth[5]) < 200 or int(PulseWidth[5]) > 5000:
            print('Error. Pulse width is outside range of 200ns to 5000ns '
                   + PulseWidth[5])
        else:

            PulseWidth = PulseWidth[5]
            GateSpace = GateSpace[7]

            RadarData.setPulseWidth(int(PulseWidth))
            RadarData.setGateSpace(int(GateSpace))

      # Begin Data read

        i = BeginIndex + DataStart
        while Contents[i].find('$') < 0:

            Elements = re.split(' +', Contents[i].lstrip(' ').rstrip(' '
                                ))

            if len(Elements) >= 3:
                WS = float(Elements[1])
                WD = float(Elements[2])
                TotNum = float(Elements[7])
                SnrDB = float(Elements[10])

                RadarData.setWindComponents(
                    TimeObj,
                    GateSpace,
                    WS,
                    WD,
                    TotNum,
                    SnrDB,
                    )

            i += 1

    return RadarData


def encode(output_bufr_file, RadarData, WMOID):

    # Get the data for the wind profilers

    WindComponentData = RadarData.getWindComponents()

    GateSpaceWidths = RadarData.getGateSpace()

    if len(GateSpaceWidths) > 1:

        MaxWidth = 0
        for Width in GateSpaceWidths:

            if Width > MaxWidth:
                MaxWidth = Width
    else:

        MaxWidth = GateSpaces[0]

    print('Using Pulse Mode ' + str(MaxWidth))

    for DateTime in WindComponentData:

        print('Processing ' + str(DateTime))

        print(MaxWidth)
        print(WindComponentData[DateTime].keys())

        if MaxWidth in WindComponentData[DateTime].keys():
            print('Processing high mode only. Pulse ' + str(MaxWidth)
                  + 'ns')

            WindComponents = WindComponentData[DateTime][MaxWidth]

            # Create tge buffer for the hour block of data.

            bufr = BUFRInterfaceECMWF(verbose=True)

            # fill sections 0, 1, 2 and 3 in the BUFR table

            num_subsets = 1
            bufr.fill_sections_0123(  # ECMWF
                                      # wind profiler . Also know as Message Type (Table A)
                                      # Message sub-type
                                      # L2B processing facility
                bufr_code_centre=59,
                bufr_obstype=2,
                bufr_subtype=7,
                bufr_table_local_version=1,
                bufr_table_master=0,
                bufr_table_master_version=3,
                bufr_code_subcentre=0,
                num_subsets=num_subsets,
                bufr_compression_flag=0,
                )

            bufr.setup_tables()

        # define a descriptor list

            template = BufrTemplate()

            print('adding {0} descriptors'.format(10))

            template.add_descriptors(
                WMO_BLOCK_NUM,
                WMO_STATION_NUM,
                DD_LATITUDE_COARSE_ACCURACY,
                DD_LONGITUDE_COARSE_ACCURACY,
                STATION_HEIGHT,
                YEAR,
                MONTH,
                MDAY,
                HOUR,
                MIN,
                TIME_SIGNIFICANCE,
                TIME_PERIOD,
                DD_WIND_SPEED,
                DD_WIND_DIR,
                DD_PRESSURE,
                DD_TEMPERATURE,
                RAINFALL_SWE,
                DD_RELATIVE_HUMD,
                HEIGHT_INCREMENT,
                WIND_PROFILER_SUB_MODE_INFO,
                HEIGHT_INCREMENT,
                HEIGHT_INCREMENT,
                HEIGHT_INCREMENT,
                )

        # delay replication for the next 10 descriptors

            template.add_replicated_descriptors(
                len(WindComponents),
                WIND_PROFILER_MODE_INFO,
                WIND_PROFILER_QC_RESULTS,
                TOTAL_NUMBER,
                WIND_U_COMPONENT,
                WIND_V_COMPONENT,
                STD_DEV_HORIZONTAL_WIND_SPEED,
                TOTAL_NUMBER,
                RADAR_BACK_SCATTER,
                WIND_W_COMPONENT,
                STD_DEV_VERTICAL_SPEED,
                )

            bufr.register_and_expand_descriptors(template)

        # activate this one if the encoding crashes without clear cause:
        # bufr.estimated_num_bytes_for_encoding = 25000

        # retrieve the length of the expanded descriptor list

            exp_descr_list_length = bufr.ktdexl

        # fill the values array with some dummy varying data

            num_values = exp_descr_list_length

            values = np.zeros(num_values, dtype=np.float64)  # this is the default

        # note: these two must be identical for now, otherwise the
        # python to fortran interface breaks down. This also ofcourse is the
        # cause of the huge memory use of cvals in case num_values is large.

            num_cvalues = num_values
            cvals = np.zeros((num_cvalues, 80), dtype=np.character)

        # note that python starts counting with 0, unlike fortran,
            # so there is no need to take (subset-1)
        #     i = subset*exp_descr_list_length

            values[0] = WMOID[0:2]  # WMO Block Number
            values[1] = WMOID[2:5]  # WMO Station #

            values[2] = RadarData.getLatitude()  # Latitude
            values[3] = RadarData.getLongitude()
            values[4] = RadarData.getElev()  # Elevation of Station (meters)
            values[5] = DateTime.timetuple().tm_year  # year
            values[6] = DateTime.timetuple().tm_mon  # month
            values[7] = DateTime.timetuple().tm_mday  # day
            values[8] = DateTime.timetuple().tm_hour  # hour
            values[9] = 0  # minute
            values[10] = 2  # Time Significance
            values[11] = -60  # Time Period
            values[12] = 1  # Wind Speed
            values[13] = 1  # Wind Dir
            values[14] = 1  # Pressure
            values[15] = 1  # Temperature
            values[16] = .2  # Rainfall
            values[17] = 1  # Realative Humidty
            GateSpace = int(MaxWidth) * 1.e-9 * 3.e+8 / 2.
            values[18] = GateSpace  # Height Increment
            values[19] = 0  # Wind Profiler Sub Mode
            values[20] = GateSpace  # Height Increment
            values[21] = GateSpace  # Height Increment
            values[22] = GateSpace  # Height Increment

            print('Number of gates ' + str(len(WindComponents)))

            for i in range(0, len(WindComponents)):

                for t in range(0, 10):

                    # Calulcate the correct index in the BUFR

                    rec = i * 10 + 23 + t

                    if WindComponents[i][0] <= 1000 \
                        and WindComponents[i][1] <= 1000:
                        WindRadians = math.radians(WindComponents[i][1])
                        VelocityU = -WindComponents[i][0] \
                            * math.sin(WindRadians)
                        VelocityV = -WindComponents[i][0] \
                            * math.cos(WindRadians)
                        TotalNumber = WindComponents[i][2]
                        SnrDB = WindComponents[i][3]
                    else:

                        VelocityU = VelocityV = TotalNumbe = SnrDB = -99
                        values[rec] = float('NaN')  # level mode
                        continue

                    if rec % 10 == 3:
                        values[rec] = 1  # level mode

                    if rec % 10 == 4:
                        values[rec] = 0  # Quality Control test

                    if rec % 10 == 5:
                        values[rec] = TotalNumber  # Total Number (with respect to accumlation or average)

                    if rec % 10 == 6:
                        values[rec] = VelocityU  # U-Component

                    if rec % 10 == 7:
                        values[rec] = VelocityV  # V-Component

                    if rec % 10 == 8:
                        values[rec] = 0.000  # Std Deviation of horizontal wind speed

                    if rec % 10 == 9:
                        values[rec] = TotalNumber  # Total Number  (with respect to accumlation or average)

                    if rec % 10 == 0:
                        values[rec] = SnrDB / 100  # Radar Back Scatter (Peak Power)  x100

                    if rec % 10 == 1:
                        values[rec] = 0.000  # W-Component  x100

                    if rec % 10 == 2:
                        values[rec] = 0.000  # Std Deviation of vertical wind

            # do the encoding to binary format

            bufr.encode_data(values, cvals)

            HeaderString = '''

287

IUAK01 PANC %02d%02d00

''' \
                % (DateTime.timetuple().tm_mday,
                   DateTime.timetuple().tm_hour)

            if not os.path.exists(OutputPath):
                os.makedirs(OutputPath)

            OutputFile = \
                '%s/IUPTO2_%s_%02d%02d00_216234297.bufr.%04d%02d%02d%02d' \
                % (
                OutputPath,
                RadarData.getSiteID().upper(),
                DateTime.timetuple().tm_mon,
                DateTime.timetuple().tm_mday,
                DateTime.timetuple().tm_year,
                DateTime.timetuple().tm_mon,
                DateTime.timetuple().tm_mday,
                DateTime.timetuple().tm_hour,
                )

             # Remove file if exsists

            if os.path.exists(OutputFile):
                os.remove(OutputFile)

            bf1 = open(OutputFile, 'ab')
            bf1.write(HeaderString)
            bf1.close()

            # get an instance of the RawBUFRFile class

            bf1 = RawBUFRFile()

            # open the file for writing

            bf1.open(OutputFile, 'ab')

            # write the encoded BUFR message

            bf1.write_raw_bufr_msg(bufr.encoded_message)

            # close the file

            bf1.close()

            #  #]

            print('succesfully written BUFR encoded data to file: ',
                  OutputFile)


# Main Program

if len(sys.argv) != 5:
    print('USAGE:   siteDIR WMOID FullPathFileName OutputPath)\
           ./wind_profiler_bufrinterface_ecmwf_for_encoding.py ast 78999 /data/realtime/Radar449/WwWind/ast/2016/106/ast16106.17w ./out'
          )
    sys.exit(1)

SiteID = sys.argv[1]
WMOID = sys.argv[2]
InputFile = sys.argv[3]
OutputPath = sys.argv[4]

# OutputFile = "%s/IUPTO2_KBOU_%02d%02d00_216234297.bufr.%04d%02d%02d%02d"  % ( OutputPath,  DateObj.timetuple().tm_mon, DateObj.timetuple().tm_mday, DateObj.timetuple().tm_year , DateObj.timetuple().tm_mon, DateObj.timetuple().tm_mday, DateObj.timetuple().tm_hour)

if os.path.exists(InputFile):
    print('Processing ' + InputFile)
    RadarData = populateRadarData(InputFile, SiteID)
else:
    print('File does not exist ' + InputFile)
    sys.exit(1)

encode(OutputPath, RadarData, WMOID)
