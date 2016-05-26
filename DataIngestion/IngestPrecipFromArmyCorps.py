#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import sys
import urllib2
import re

print 'Running IngestPrecipFromArmyCorps.py on ' + time.ctime()

  # #################  Begin User Configuration ######################

  # MODIFY THE FOLLOWING HASH LIST TO ADD OR REMOVE SITES
  # Define SiteID, URL link to data,  The precip column in the collected array, total # of elements in array.

PrecipSites = \
    {'hhd': ['http://www.nwd-wc.usace.army.mil/nws/hh/basins/text/hah.prn'
     , 11, 13],
     'ltr': ['http://www.nwd-wc.usace.army.mil/nws/hh/basins/text/ltcw.prn'
     , 6, 8]}

  # ##################  End User Configuration #######################

  # initialize variables and define functions.

OutPutPath = \
    '/data'


def ReadWebContent(UrlLink):

    ContentObj = urllib2.urlopen(UrlLink)

    WebContent = ContentObj.read()

    return WebContent


def FindSubString(Content, Beg, End):

    StringBeginIndex = WebContent.find(Beg)

    StringBeginIndex = StringBeginIndex + len(Beg)

    if not StringBeginIndex:
        return False

    StringEndIndex = WebContent.find(End, StringBeginIndex)

    return Content[StringBeginIndex:StringEndIndex]


def UTCTimeOffset(timeobj, hrsoffset):

    offset = hrsoffset * 3600

    timeobj = time.mktime(timeobj)

    timeobj += offset

    timeobj = time.localtime(timeobj)

    return timeobj


# Begin Main script.

for site in PrecipSites:  # loop through each site in hash table.

    print 'Parsing ' + site + ' precip data at ' + PrecipSites[site][0]

    WebContent = ReadWebContent(PrecipSites[site][0])

    WebContent = re.sub(' +', ',', WebContent)

    WebContentLines = WebContent.split('\n')

    Counter = 0

    for WebLine in WebContentLines:

        if Counter > 0:  # Skip header row
            WebElement = WebLine.split(',')

            if len(WebElement) >= 2:

                Month = (WebElement[2])[2:6]
                Day = (WebElement[2])[0:2]
                Year = WebElement[3]
                Time = (WebElement[4])[0:2]

                Time = str(int(Time) - 1)  # adjust for their hour off. Using base 1, not 0. Fix to base 0.

                TimeString = Year + ',' + Month + ',' + Day + ',' + Time  # make a time string.

                TimeStruct = time.strptime(TimeString, '%Y,%b,%d,%H')  # convert time string into a time tuple

                UTCTime = UTCTimeOffset(TimeStruct, 7)  # Change from CA time to UTC time.

                OutPutPathName = OutPutPath + '\\' + site + '\\' \
                    + str(UTCTime.tm_year).zfill(4) + '\\' \
                    + str(UTCTime.tm_yday).zfill(3)

                if not os.path.exists(OutPutPathName):

                    os.makedirs(OutPutPathName)

                OutPutFile = '%s\\%s%02d%03d.%02dm' % (OutPutPathName,
                        site, UTCTime.tm_year % 100, UTCTime.tm_yday,
                        UTCTime.tm_hour)

                print 'Output: ', OutPutFile

                try:
                    fileobj = open(OutPutFile, 'wb')
                except IOError:
                    print 'cannot open file ' + OutPutFile
                    exit(1)

                if len(WebElement) == PrecipSites[site][2]:
                    try:
                        float(WebElement[PrecipSites[site][1]])
                    except ValueError:
                        WebElement[PrecipSites[site][1]] = -9999.999

                    if WebElement[PrecipSites[site][1]] >= 0:

                        fileobj.write('112,%d,%d,%d,%.3f\r\n'
                                % (UTCTime.tm_year, UTCTime.tm_yday,
                                UTCTime.tm_hour * 100 + 59,
                                float(WebElement[PrecipSites[site][1]])
                                * (2.54 * 10)))
                    else:

                        fileobj.write('112,%d,%d,%d,-9999.999\r\n'
                                % (UTCTime.tm_year, UTCTime.tm_yday
                                + 1, UTCTime.tm_hour * 100 + 59))
                else:

                    fileobj.write('112,%d,%d,%d,-9999.999\r\n'
                                  % (UTCTime.tm_year, UTCTime.tm_yday
                                  + 1, UTCTime.tm_hour * 100 + 59))

        Counter += 1
