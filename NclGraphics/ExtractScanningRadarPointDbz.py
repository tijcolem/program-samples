#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
import datetime
import optparse
from datetime import datetime
from datetime import timedelta
from time import strftime
from time import mktime

# check command-line arguments

usage = \
    '''
\t%prog InputFileExp NexradSite3ID

\twhere,

\tInputFileExp  = path and file expression resolving the input NIDS-NetCDF files to be processed
\tNexradSite3ID = the 3-letter site identifier of the NEXRAD site where the InputFileExp data was acquired'''
parser = optparse.OptionParser(usage=usage)
(options, args) = parser.parse_args()

if len(args) != 2:
    parser.error('Missing argument.')
    sys.exit()
else:
    InputFileExp = sys.argv[1]
    NexradSite3ID = sys.argv[2]

# set NCL environmental variables so the interpreter can execute
# and custom color maps can be accessed

# NCL 6.2

os.environ['NCARG_ROOT'] = '/usr/local/ncl62'
os.environ['NCARG_BIN'] = '/usr/local/ncl62/bin'

os.environ['NCARG_COLORMAPS'] = '/usr/local/etltools/ncl/colormaps:' \
    + os.environ.get('NCARG_ROOT') + '/lib/ncarg/colormaps'

# set shared object path for NCL/FORTRAN wrappers

os.environ['LD_LIBRARY_PATH'] = '/usr/local/etltools/ncl/lib'

# define NCL interpreter and graphics production script

Ncl = os.environ.get('NCARG_BIN') + '/ncl'
NclProg = \
    '/home/dms7/workspace/Dan/NclWrapit/ExtractScanningRadarPointDbz.ncl'

os.system(Ncl + ' ' + NclProg + ' \'InputFileExp="' + InputFileExp
          + '"\' \'NexradSite3ID="' + NexradSite3ID + '"\'')
