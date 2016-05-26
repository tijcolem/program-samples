"""
Copyright (C) 2014 The HDF Group
Copyright (C) 2014 John Evans

This example code illustrates how to access and visualize a LaRC CALIPSO file
 in file in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Modfied Nov 2015 by Tim Coleman 
for use for Jessie Creamen publication


Usage:  save this script and run

    python CAL_LID_L2_VFM-ValStage1-V3-02.2011-12-31T23-18-11ZD.hdf.py

The netCDF file must either be in your current working directory
or in a directory specified by the environment variable HDFEOS_ZOO_DIR.
"""

import os, sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib import colors

USE_NETCDF4 = False

def run(FILE_NAME, OUT_PATH):

    # Identify the data field.
    DATAFIELD_NAME = 'Feature_Classification_Flags'

    if USE_NETCDF4:
        from netCDF4 import Dataset
        nc = Dataset(FILE_NAME)
    
        # Subset the data to match the size of the swath geolocation fields.
        # Turn off autoscaling, we'll handle that ourselves due to presence of
        # a valid range.
        var = nc.variables[DATAFIELD_NAME]
        data = var[:,1256]

        # Read geolocation datasets.
        lat = nc.variables['Latitude'][:]
        lon = nc.variables['Longitude'][:]
    else:
        from pyhdf.SD import SD, SDC
        hdf = SD(FILE_NAME, SDC.READ)
        
        # Read dataset.
        data2D = hdf.select(DATAFIELD_NAME)
        data = data2D[:,:]

        # Read geolocation datasets.
        latitude = hdf.select('Latitude')
        lat = latitude[:]
        longitude = hdf.select('Longitude')
        lon = longitude[:]


    # Subset data. Otherwise, all points look black.
    lat = lat[::40]
    lon = lon[::40]
    data = data[::40]

    # Extract Feature Type only through bitmask.
    data_feature_type = data & 7
    
    
    # Shift array to analyze bit 10-12
    datashifted = data >> 9
    
    # Mask bits 10-12
    data_sub_feature_type = datashifted & 7
    
    # check data_feature_type where = 3 (aerosol) and set to 1
    data_feature_type[data_feature_type > 3] = 0;
    data_feature_type[data_feature_type < 3] = 0;
    data_feature_type[data_feature_type == 3] = 1;
    
    # check data_feature_type where != 1 and set data_sub_feature_type = 0. Only want aersol subtypes. 
    data_sub_feature_type[data_feature_type != 1] = 0 

    # Only look at smoke.  This is bits 10-12 set to 6. 
    data_sub_feature_type[data_sub_feature_type != 6] = 0;
    
  
    for i in range(0,len(data_sub_feature_type)):
    
        if (np.any(data_sub_feature_type[i]==6)):
            data_sub_feature_type[i] = 1
   #     np.put(data_sub_feature_type[::],1256-1259,[1,1,1])
    
    
   # if data_sub_feature_type[data_sub_feature_type[:,1256:1259] == 5]:
        
     #   np.put(data_sub_feature_type, [1256-1259], 1)
    
    
    data_sub_feature_type = data_sub_feature_type[:,1256]
    
    #print data_sub_feature_type.shape
    
  #  for i in data_sub_feature_type:
   #     print i,


    np.seterr(divide='ignore', invalid='ignore')

    # Make a color map of fixed colors.
    cmap = colors.ListedColormap(['white', 'black'])
    #cmap = colors.ListedColormap(['gray', 'blue', 'yellow', 'red', 'green', 'brown', 'black', 'white' ])
  
    # The data is global, so render in a global projection.
    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90.,90,45),labelstyle="+/-", labels=[True,False,False,True])
    m.drawmeridians(np.arange(-180.,180,45), labelstyle="+/-", labels=[True,False,False,True])
    x,y = m(lon, lat)
    i = 0
    for feature in data_sub_feature_type:
        m.plot(x[i], y[i], 'ro', color=cmap(feature),  markersize=3, fillstyle='full')
        i = i+1


    long_name = 'Smoke Sub Feature Type at Altitude 0 - 20.2km'
    basename = os.path.basename(FILE_NAME)
    plt.title('{0}\n{1}'.format(basename, long_name))

    fig = plt.gcf()
    
        
 

    # define the bins and normalize
    bounds = np.linspace(0,2,3)
    
    bounds = [0,1,2]
    
    print bounds
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # create a second axes for the colorbar
    ax2 = fig.add_axes([0.93, 0.2, 0.01, 0.6])
    cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')

   # cb.ax.set_yticklabels(['invalid', 'clear', 'cloud', 'aerosol', 'strato', 'surface', 'subsurf', 'no signal'], fontsize=5)
    cb.ax.set_yticklabels(['Other','Smoke'], fontsize=5)

    pngfile = OUT_PATH + '/' + "{0}_swath_sub_feature_smoke.png".format(basename)
    fig.savefig(pngfile)
    plt.clf()
    
if __name__ == "__main__":

    BasePath = "F:/VFM files/WestUS"
   


    for File in os.listdir(BasePath):
        
        OutPutPath = "C:/EtlData/Calipso/Images/Profile"
        
        FullPathFile =  BasePath + "/" + File
        
        OutPutPath = OutPutPath + "/" + File + "/"
        
        if not os.path.exists(OutPutPath):
          os.mkdir(OutPutPath)

        
        FullPathFile =  BasePath + "/" + File
    

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
        #ncfile = 'C:/EtlData/hdf4/CAL_LID_L2_VFM-ValStage1-V3-30.2015-08-15T09-13-47ZN.hdf'
   
        run(FullPathFile, OutPutPath)

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
   # ncfile = 'C:/EtlData/hdf4/CAL_LID_L2_VFM-ValStage1-V3-30.2015-08-15T09-13-47ZN.hdf'
   
    #run(ncfile)
