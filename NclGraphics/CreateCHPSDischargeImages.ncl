;*******************************************
; lcnative_1.ncl
;*******************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"  
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"  
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

begin

; define carriage return, line feed, and double quote characters
  CR = inttochar(13)
  LF = inttochar(10)
  DQ = str_get_dq()

; check for command line interface arguments
  if((.not. isvar("InputFile")) .or. \
     (.not. isvar("OutputBasePath"))) then

    system("echo")
    system("echo 'PROGRAM USAGE:'")
    system("echo")
    system("echo 'ncl CreateCHPSDischargeImages.ncl InputFile=<string>'")
    system("echo")
    system("echo '   where,  InputFile = path and filename of the input CHPS NetCDF file'")
    system("echo")
    system("echo '           OutputBasePath = path to where the output image files are written (YYY/JJJ path appended)'")
    system("echo")
    system("echo 'Example:'")
    system("echo")

    system("echo     ncl CreateCHPSDischargeImages.ncl " + \
           "\'InputFile=\" + DQ + "./Discharge201412101200.nc\" + DQ + "\' " + \ 
           "\'OutputPath=\" + DQ + "./data\" + DQ + "\'")

    system("echo")
    system("echo Inputs CHPS NetCDF discharge data from file ./Discharge201412101200.nc")
    system("echo and writes transparent overlay images for Google Maps/Earth to ./data/2014/344")
    system("echo")

    exit

  end if

  ; open file and read in data
  f = addfile (InputFile, "r")

  ; read in data from file
  time            = f->time
  discharge       = f->discharge
  discharge@lat2d = f->lat
  discharge@lon2d = f->lon

  ; convert discharge from cms to kcfs
  discharge = (discharge * 35.3146667) / 1000.

  ; convert epoch from minutes to seconds
  time        = time * 60
  time@units = "seconds since 1970-1-1"

  InitTimeIndex = 24

  ; create dynamic output path
  OutputPath = cd_string(time(InitTimeIndex),OutputBasePath + "/%Y/%J")
  system("mkdir -p " + OutputPath)

  ; set plotting resources
  res_ce = True
  res_ce@cnFillOn              = True 
  res_ce@cnFillMode            = "CellFill"
  res_ce@trGridType            = "TriangularMesh"
  res_ce@cnLinesOn             = False 
  res_ce@cnLineLabelsOn        = False
  res_ce@gsnSpreadColors       = True
  res_ce@gsnSpreadColorStart   = 4
  res_ce@gsnSpreadColorEnd     = -1
  res_ce@cnInfoLabelOn         = False
  res_ce@tfDoNDCOverlay        = False
  res_ce@gsnAddCyclic          = False
  res_ce@mpFillOn              = False 
  res_ce@mpOutlineBoundarySets = False
  res_ce@gsnSpreadColorStart   = 2
  res_ce@gsnSpreadColorEnd     = 55
  res_ce@lbLabelStride         = 4
  res_ce@mpMinLatF             = 38.
  res_ce@mpMaxLatF             = 39.5
  res_ce@mpMinLonF             = -123.5
  res_ce@mpMaxLonF             = -122.

  ; define explicit logarithmic scale from 0.5 - 50 kcfs
  maxVal = 50
  x      = fspan(19.905,maxVal,54) 
  levels = x^4.*log(exp(x))/(maxVal^4)

  res_ce@cnLevelSelectionMode  = "ExplicitLevels"
  res_ce@cnLevels              = levels

  ; create plots
  dims = dimsizes(discharge)

  do i = 0, dims(0) - 1

    InitOffsetHr = i - InitTimeIndex

    ValidTime  = cd_string(time(i),"%Y-%N-%D %H:00")
    FilePrefix = cd_string(time(InitTimeIndex),"%Y%N%D%H_discharge") + sprinti("%02d", i + 1)

    OutputFilePrefix = OutputPath + "/" + FilePrefix 
 
    wks_ce = gsn_open_wks("png" ,OutputFilePrefix)

    gsn_define_colormap(wks_ce,"Chps")

    plot_ce = gsn_csm_contour_map_ce(wks_ce,discharge(i,:,:),res_ce)

    SrcImgFile = OutputFilePrefix + ".png"
    DstImgFile = OutputFilePrefix + ".gif"

    ; use exclamation mark to set the virtual canvas page size to the cropped image size
    system("convert -transparent \#ffffff -crop !530x530+247+247 " + SrcImgFile + " " + DstImgFile)
    system("rm " + SrcImgFile)

    ; output KML file
    OutText = "<?xml version=" + DQ + "1.0" + DQ + " encoding=" + DQ + "UTF-8" + DQ + "?>"+CR+LF + \
              "<kml xmlns=" + DQ + "http://earth.google.com/kml/2.0" + DQ + ">" + DQ + CR+LF     + \
              "<GroundOverlay>" + CR+LF                                                          + \
              "<name>" + "Stream discharge valid " + ValidTime + "</name>" + CR+LF               + \
              "<InitOffsetHr>" +  InitOffsetHr + "</InitOffsetHr>" + CR+LF                       + \
              "<ValidTimeEpochSec>" + time(i) + "</ValidTimeEpochSec>" + CR+LF                   + \
              "<Icon>" + CR+LF                                                                   + \
              "<href>" + "./" + FilePrefix + ".gif" + "</href>" + CR+LF                          + \
              "</Icon><LatLonBox>" + CR + LF                                                     + \
              "<north>" + sprintf("%.1f",res_ce@mpMaxLatF) + "</north>" + CR+LF                  + \
              "<south>" + sprintf("%.1f",res_ce@mpMinLatF) + "</south>" + CR+LF                  + \
              "<east>" + sprintf("%.1f",res_ce@mpMaxLonF) + "</east>" + CR+LF                    + \
              "<west>" + sprintf("%.1f",res_ce@mpMinLonF) + "</west>" + CR+LF                    + \
              "</LatLonBox>" + CR + LF                                                           + \
              "</GroundOverlay>" + CR + LF                                                       + \
              "</kml>"

    asciiwrite(OutputPath + "/" + FilePrefix + ".kml",OutText)

  end do

end
