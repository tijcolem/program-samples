#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import urllib2
import sys

print 'Running IngestAfdFromNws.pl on ' + time.ctime()

states = ['ca', 'wa']  # define array containing states.

BaseOutPath = \
    '\\\\psdobs.psd.esrl.noaa.gov\\data\\realtime\\TextProductsNWS\\AreaForecastDiscussion'

URLBaseAddress = 'http://iwin.nws.noaa.gov/iwin'

utctime = time.gmtime()

for state in states:

    OutPath = BaseOutPath + '\\' + state + '\\' \
        + str(utctime.tm_year).zfill(4) + '\\' \
        + str(utctime.tm_yday).zfill(3)

    if not os.path.exists(OutPath):

        os.makedirs(OutPath)

    OutFile = '%s\\%s%02d%03d%02d.html' % (OutPath, state,
            utctime.tm_year % 100, utctime.tm_yday, utctime.tm_hour)

    URLFile = URLBaseAddress + '/' + state + '/discussion.html'

    try:
        fileobj = open(OutFile, 'wb')
    except IOError:
        print 'cannot open file ' + OutputFile

    # transfer image file

    print 'Transferring ' + URLFile + ' to ' + OutFile + ' ...'

    try:
        WebObj = urllib2.urlopen(URLFile)
    except:
        print '%s: %s' % sys.exc_info()[:2]
    else:
        fileobj.write(WebObj.read())

    WebObj.close()
    fileobj.close()
