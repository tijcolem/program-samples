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

    python CAL_LID_L2_VFM-ValStage1-V3-02.2011-12-31T23-18-11ZD.hdf.v.py

The netCDF file must either be in your current working directory
or in a directory specified by the environment variable HDFEOS_ZOO_DIR.
"""
import os
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
import sys

USE_NETCDF4 = False

def run(FILE_NAME,OUT_PATH):
    # Identify the data field.
    DATAFIELD_NAME = 'Feature_Classification_Flags'

    if USE_NETCDF4:
        from netCDF4 import Dataset
        nc = Dataset(FILE_NAME)

    
        # Subset the data to match the size of the swath geolocation fields.
        # Turn off autoscaling, we'll handle that ourselves due to presence of
        # a valid range.
        var = nc.variables[DATAFIELD_NAME]
        data = var[:,:]
        print data.shape

        # Read geolocation datasets.
        lat = nc.variables['Latitude'][:]
        long = nc.variables['Longitude'][:]

        lat  = np.squeeze(lat)
        long = np.squeeze(long)
        print lat.shape
    else:
        from pyhdf.SD import SD, SDC
        hdf = SD(FILE_NAME, SDC.READ)
        
        # Read dataset.
        data2D = hdf.select(DATAFIELD_NAME)
        data = data2D[:,:]
        print data.shape
        
        
    
     

        # Read geolocation datasets.
        latitude = hdf.select('Latitude')
        lat = latitude[:]
        
        longitude = hdf.select('Longitude')
        long = longitude[:]
        
    
 

    # Extract Feature Type only (1-3 bits) through bitmask.
    data_feature_type = data & 7
    
 #   if datanew[datanew = 3 == 3 
    
    
   # datashifted = data >> 9
    
    #data_sub_feature_type = datashifted & 7
    
    
    #data_feature_type[data_feature_type > 3] = 0;
    #data_feature_type[data_feature_type < 3] = 0;
    #data_feature_type[data_feature_type == 3] = 1;
    
    #data_sub_feature_type[data_feature_type != 1] = 0 

    
  #  data = data.equal(5,5,-9)
    
  #  data.
    
    print data_feature_type.shape
    

    

    
#    for t in range[0]
    
    #print bin(datashiftednew[0][i])
        


   

#    for i in range(0,len(data[:])):
#        
#      for t in range(0,len(data[i][:])):
#    
#        print 'record'
#        print i 
#    #    print datanew[0][i]
#        print data[i][t]
#        print format(data[i][t], '#017b')
#        print data_feature_type[i][t]
#        print format(data_feature_type[i][t], '#017b')
#   #     print format(datashifted[i][t], '#017b')
#        print data_sub_feature_type[i][t]
#        print format(data_sub_feature_type[i][t], '#017b')
#        
#      break


      
        

    # Subset latitude values for the region of interest (40N to 62N).
    # See the output of CAL_LID_L2_VFM-ValStage1-V3-02.2011-12-31T23-18-11ZD.hdf.py example.
    lat = lat[:]
    long = long[:]
    size = lat.shape[0]
    
    print lat.shape[0]
    
    # You can visualize other blocks by changing subset parameters.
    #  data2d = data[3500:3999, 0:164]    # 20.2km to 30.1km
    #  data2d = data[3500:3999, 165:1164] #  8.2km to 20.2km

    # data2d = data[3500:4000, 1165:]  # -0.5km to  8.2km
   
    
    low_data2d = data_feature_type[:, 1165:1455 ] #8.2 to -.5km  # -0.5km to  8.2km
    med_data2d2 = data_feature_type[:, 165:365  ] # 20.2km to 8.2km 8.2km to  20.2km
   # high_data2d2 = data_feature_type[:, 0:55  ] # 30.2 to 20.km 8.2km to  20.2km
    
    #data2d = high_data2d2
    #print med_data2d2.shape
    #print high_data2d2.shape
    

  #  data2d = np.concatenate((high_data2d2, med_data2d2), axis=1)
    data2d = np.concatenate((med_data2d2, low_data2d), axis=1)
  #  data2d = np.concatenate((data2d, low_data2d), axis=1)

    
    print data2d.shape

    

    


    #data3d = np.reshape(data2d, (size, 15, 290))

    #data_sub_feature_type = data3d[:,0,:]
    


    # Focus on cloud (=2) data only.
    # data[data > 2] = 0;
    #data[data < 2] = 0;
    #data[data == 2] = 1;
    
  #  Focus on aersol (=3) data only.
  
   
  
   
    

    # Generate altitude data according to file specification [1].
   # alt = np.zeros(55)
    #alt = np.zeros(200)
    
   # alt = np.zeros(290)
    #alt = np.zeros(545)
    alt = np.zeros(490)
    

    # You can visualize other blocks by changing subset parameters.
    #  20.2km to 30.1km
    # for i in range (0, 54):
    #       alt[i] = 20.2 + i*0.18;



    # -0.5km to 8.2km
  
    for i in range (0, 290):
        
          print i 
          alt[i] = -0.5 + i*0.03
          
    print "breaK"  
    for i in range (290, 490):
        
          print i
          alt[i] = 8.2 + (i-289)*0.06
          
 #   for i in range (490, 545):
 #       
 #         print i
 #         alt[i] = 20.2 + (i-490)*0.180


 

      
    # Contour the data on a grid of longitude vs. pressure
    latitude, altitude = np.meshgrid(lat, alt)


    # Make a color map of fixed colors.
    
    
    cmap = colors.ListedColormap(['gray', 'blue', 'yellow', 'red', 'green', 'brown', 'black', 'white' ])
   # cmap = colors.ListedColormap(['white', 'red', 'orange','magenta','green','blue','gray', ])



  
    # Define the bins and normalize.
    
   

    

    bounds = np.linspace(0,8,num=9)
    #print bounds
    levels = [0,.99,1.99,2.99,3.99,4.99,5.99,6.99,7.99]
    
    print levels
    
    print cmap.colors
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

  
    
  #  print norm.boundaries
    print levels

    long_name = 'Feature Type (Bits 1-3) at Altitude 0 - 20.2km'
    basename = os.path.basename(FILE_NAME)
    plt.contourf(latitude, altitude, np.rot90(data2d,1),cmap=cmap,levels=levels)
    
    plt.title('{0}\n{1}\n\n\n\n'.format(basename, long_name),  fontsize=10)
    plt.xlabel('Latitude (degrees)',fontsize=8)
    plt.ylabel('Altitude (km)',fontsize=8)
    
    xticks = plt.xticks(fontsize="10")
    plt.yticks(fontsize="10")
    
    xticks.set_xticks([0,1,2,3,4,5,6,7])
    
    
    #plt.subplots_adjust(right=0.87)
    
  
    axtwo = plt.twiny()
    
    axtwo.set_xlabel("Longitude (degrees)",fontsize=8)
    
    #axtwo.xaxis.set_label_coords(.5, 1.01)
    
    intlong= long.astype(int).flatten()
    
    longspace = int(math.floor((len(long[:]) / 7 )))
    
    print "long space"
    print longspace
    print len(long[:])
    intlong_reversed_arr = intlong[::-1]
    
   
    axtwo.set_xticks([0,1,2,3,4,5,6,7])
    axtwo.set_xticklabels(intlong_reversed_arr[::longspace], fontsize=10 )

    print intlong_reversed_arr[::longspace]
    print intlong_reversed_arr[0]
    print intlong_reversed_arr[3743]
    
    print lat[::longspace]
    print lat[0]
    print lat[3743]
   
   
    print lat[2000]
    print long[2000]

    fig = plt.gcf()
    
    
    
    
    fig.set_figheight(4)
    fig.set_figwidth(6)
    
    plt.subplots_adjust(right=0.65)

    
   
    fig.tight_layout() 
 
    
    # Create a second axes for the discrete colorbar.
    ax2 = fig.add_axes([0.88, 0.1, 0.01, 0.6])

   
    cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, boundaries=bounds)
    cb.ax.set_yticklabels(['invalid','clear air', 'cloud', 'aerosol', 'stratospheric\nfeature', 'surface', 'subsurface', 'no signal' ], fontsize=6)

    # plt.show()
    pngfile = OUT_PATH + '/' + "{0}.v.py_feature_type_0-20.2km.png".format(basename)
    fig.savefig(pngfile)
    fig.clf()
    
    
print __name__ 
if __name__ == "__main__":

    BasePath = "C:/EtlData/Calipso/WestUS/10z"
    

    for File in os.listdir(BasePath):
        
        
        OutPutPath = "C:/EtlData/Calipso/Images/Profile_Test"
        
        FullPathFile =  BasePath + "/" + File
        
        OutPutPath = OutPutPath + "/" + File + "/"
        
        if not os.path.exists(OutPutPath):
          os.mkdir(OutPutPath)

    

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
        #ncfile = 'C:/EtlData/hdf4/CAL_LID_L2_VFM-ValStage1-V3-30.2015-08-15T09-13-47ZN.hdf'
   
        run(FullPathFile, OutPutPath)

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
   # ncfile = 'C:/EtlData/hdf4/CAL_LID_L2_VFM-ValStage1-V3-30.2015-08-15T09-13-47ZN.hdf'
 