; NCL script: PlotScanRadarRef.ncl
; Author:     Dan Gottas NOAA/ESRL/PSD
; Created:    10/16/2012
;
; Inputs NIDS NEXRAD and NetCDF V3 scanning radar reflectivity data and produces a reflectivity
; plot transformed onto a constant latitude/longitude grid with a transparent background for 
; overlaying in mapping applications such as Google Maps/Earth. KML output is also supported.
;
; Uses ScanningRadar.rgb PSD custom color table located in /usr/local/etltools/ncl/colormaps
; The path to this color table is specified as an envoironmental variable that NCL reads during
; initialization before running the requested script. To specify this custom path in addition to
; the standard path for other NCL color tables, define the following in the .cshrc file:
;
; "setenv NCARG_ROOT /usr/local"
; "setenv NCARG_COLORMAPS /usr/local/etltools/ncl/colormaps:$NCARG_ROOT/lib/ncarg/colormaps"
;
;
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"

begin

; path to Java NetCDF tool to convert NIDS to NetCDF
  Nids2NetcdfProg = "/usr/local/etltools/lib/NetCDFJava/toolsUI-4.2.jar"

; define carriage return, line feed, and double quote characters
  CR = inttochar(13)
  LF = inttochar(10)
  DQ = str_get_dq()
  
; check for command line interface arguments 
  if((.not. isvar("RefInputFile")) .or. \
     (.not. isvar("RefFormat"))) then

    system("echo")
    system("echo 'PROGRAM USAGE:'")
    system("echo")
    system("echo 'ncl PlotScanRadarRef.ncl RefInputFile=<string> " + \
           "RefFormat=<string> ImageOutputPath =<string> KmlOutputPath =<string> " + \
           "KmlHrefPath =<string>'")
    system("echo")
    system("echo '   where,  RefInputFile = file containing input reflecivity data'")
    system("echo")
    system("echo '           RefFormat = NIDS for NIDS in native NWS NEXRAD format'")
    system("echo '           RefFormat = NIDSNC for NIDS in NetCDF V3 format'")
    system("echo '                     = KPIX for NSSL NetCDF V3 format for KPIX data'")
    system("echo '                     = XBAND for X-band NetCDF V3 format for Santa Clara data'")
    system("echo")
    system("echo '           ImageOutputPath = path to reflectivity image output file.'")
    system("echo '                             If ImageOutputPath is undefined or is'")
    system("echo '                             defined as an empty string, the image'")
    system("echo '                             file is output to the current directory'")
    system("echo")
    system("echo '           KmlOutputPath = path to output KML file.'")
    system("echo '                           Output occurs only if KmlOutputPath is defined.'")
    system("echo '                           If KmlOutputPath is defined as an empty string,'")
    system("echo '                           a KML file is written to the current directory.'")
    system("echo")
    system("echo '           KmlHrefPath = KML <href> path to reflectivity image.'")
    system("echo '                         Output occurs only if KmlOutputPath is defined.'")
    system("echo '                         If KmlOutputPath is defined and KmlHrefPath is'")
    system("echo '                         either undefined or an empty string, the'")
    system("echo '                         current directory path is specified.'")
    system("echo 'Example:'")
    system("echo")

    system("echo     ncl PlotScanRadarRef.ncl " + \
           "\'ReflectivityInputFile=\" + DQ + "./data/sn.last\" + DQ + "\' " + \
           "\'RefFormat=\" + DQ + "NIDS\" + DQ + "\' " + \
           "\'ImageOutputPath=\" + DQ + "./img/\" + DQ + "\' " + \
           "\'KmlOutputPath=\" + DQ + "./kml\" + DQ + "\' " + \
           "\'KmlHrefPath=\" + DQ + "http://www.esrl.noaa.gov/psd/data/obs/\" + DQ + "\'")

    system("echo")
    system("echo Inputs NIDS format refelctivity data from the file ./data/sn.last, produces a")
    system("echo reflectivity graphic in the ./img/sn.gif file, and outputs the ./kml/sn.kml")
    system("echo file with http://www.esrl.noaa.gov/psd/data/obs/sn.gif in the \<href\>")
    system("echo tag and the plot perimeter latitude/longitude in the \<LatLonBox\> tag.")
    system("echo")

    exit

  end if

; set ImageOutputPath to current dir, if undefined or is an empty string 
  if(.not. isvar("ImageOutputPath") .or. (strlen(ImageOutputPath) .eq. 0)) then

    ImageOutputPath = "./"

  end if

; disable KML output if KmlOutputPath is undefined
  if(.not. isvar("KmlOutputPath")) then

    EnableKmlOutput = 0;

  else

    EnableKmlOutput = 1;

    ; if empty output path, set KML output to current path
    if(strlen("KmlOutputPath") .eq. 0)

      KmlOutputPath = "./" 

    end if

    ; if undefined or empty href path, set to current path
    if((.not. isvar("KmlHrefPath")) .or. \
       (strlen(KmlHrefPath) .eq. 0)) then

      KmlHrefPath = "./"

    end if

  end if

; initialize arrays and constants
  PI             = new((1),double)
  Deg2Rad        = new((1),double)
  SiteLat        = new((1),double)
  SiteLon        = new((1),double)
  PlotLat        = new((1),double)
  PlotLon        = new((1),double)
  MeridianLength = new((1),double)
  ParallelLength = new((1),double)
  Rn             = new((1),double)
  ElevationAngle = new((1),double)

  PI      = 4. * atan(1.)
  Deg2Rad = PI / 180.

  MeridianDegreeLength = (/ 110575.6,110576.3,110577.6,110579.7,110582.4, \
                            110585.8,110589.8,110594.5,110599.9,110605.9, \
                            110612.5,110619.8,110627.8,110636.3,110645.4, \
                            110655.2,110665.5,110676.4,110687.9,110699.9, \
                            110712.4,110725.4,110739.0,110753.0,110767.5, \
                            110782.5,110797.9,110813.7,110829.9,110846.4, \
                            110863.3,110880.6,110898.2,110916.0,110934.2, \
                            110952.6,110971.2,110990.0,111009.0,111028.2, \
                            111047.5,111066.9,111086.4,111105.9,111125.5, \
                            111145.2,111164.8,111184.4,111203.9,111223.4, \
                            111242.7,111261.9,111281.0,111299.9,111318.6, \
                            111337.1,111355.4,111373.4,111391.1,111408.5, \
                            111425.5,111442.3,111458.6,111474.6,111490.1, \
                            111505.2,111519.9,111534.1,111547.8,111561.0, \
                            111573.7,111585.9,111597.5,111608.5,111619.0, \
                            111628.9,111638.2,111646.8,111654.9,111662.3, \
                            111669.1,111675.2,111680.6,111685.4,111689.5, \
                            111693.0,111695.7,111697.8,111699.2,111699.9 /)

  ParallelDegreeLength = (/ 111324.,111307.,111257.,111172.,110055., \
                            110903.,110718.,110500.,110248.,109962., \
                            109644.,109292.,108907.,108489.,108038., \
                            107555.,107039.,106490.,105909.,105296., \
                            104651.,103975.,103266.,102527.,101756., \
                            100954.,100122., 99259., 98366., 97443., \
                             96490., 95508., 94497., 93457., 92389., \
                             91292., 90168., 89016., 87836., 86630., \
                             85398., 84139., 82855., 81545., 80210., \
                             78850., 77467., 76060., 74629., 73175., \
                             71699., 70201., 68681., 67140., 65579., \
                             63997., 62396., 60775., 59136., 57478., \
                             55803., 54110., 52401., 50675., 48934., \
                             47178., 45407., 43622., 41824., 40012., \
                             38189., 36353., 34506., 32648., 30781., \
                             28904., 27017., 25123., 23220., 21311., \
                             19395., 17472., 15545., 13612., 11675., \
                              9735.,  7792.,  5846.,  3898.,  1949. /)

; create output image file name by replacing or adding raster suffix to the input file prefix
  nfield          = str_fields_count(RefInputFile,"/")
  ImageFilePrefix = str_get_field(RefInputFile,nfield,"/")
  ImageFilePrefix = str_get_field(ImageFilePrefix,1,".")

; if NIDS format, convert to NetCDF 3
  NidsToNetCDFFile = ""
  if(RefFormat .eq. "NIDS") then

    NidsToNetCDFFile = RefInputFile + ".nc"

    system("java -classpath " + Nids2NetcdfProg + " ucar.nc2.FileWriter -in " + \
           RefInputFile + " -out " + NidsToNetCDFFile)

    RefInputFile = NidsToNetCDFFile

    RefFormat = "NIDSNC" 

  end if

  InFile = addfile(RefInputFile,"r")

; load data from NetCDF 3 files 
  if(RefFormat .eq. "NIDSNC") then

    ; lat and lon from global attributes
    SiteLat = InFile@RadarLatitude
    SiteLon = InFile@RadarLongitude

    ; radar elevation angle from global attributes
    ElevationAngle = InFile@RadarElevationNumber / 10.

    ; load reflectivity array
    RefDz = InFile->BaseReflectivity

    ; replace NaN in reflectivity data array with missing values of -999.
    if(any(isnan_ieee(RefDz))) then
      value = -999.
      replace_ieeenan(RefDz, value, 0)
      RefDz@_FillValue = value
    end if

    ; load azimuth array
    Azimuth = InFile->azimuth

    ; load radial distance to the start of each gate array
    Range = InFile->gate

  else if(RefFormat .eq. "KPIX") then

    ; lat and lon from global attributes
    SiteLat = InFile@Latitude
    SiteLon = InFile@Longitude

    ; radar elevation angle from global attributes
    ElevationAngle = InFile@Elevation

    ; load azimuth array
    Azimuth = InFile->Azimuth

    ; sparse grid exists if global attribute DataType=SparseRadialSet
    if(InFile@DataType .eq. "SparseRadialSet") then

      ; get the dimension names and sizes
      DimNames = getvardims(InFile)
      DimValue = getfiledimsizes(InFile) 

      ; get the number of azimuths from the dimension name 'Azimuth'
      DimIndex = str_match_ind(DimNames,"Azimuth")
      NumAz    = DimValue(DimIndex)

      ; get the number of gates from the dimension name 'Gate'
      DimIndex = str_match_ind(DimNames,"Gate")
      NumGate  = DimValue(DimIndex)

      SparseRefDz = InFile->Reflectivity
      SparsePixX  = InFile->pixel_x
      SparsePixY  = InFile->pixel_y

      RefDz = new((/ NumAz,NumGate /),double,-99900.0)

      do i = 0,dimsizes(SparseRefDz) - 1

        RefDz(SparsePixX(i),SparsePixY(i)) = SparseRefDz(i)

      end do

    else

      ; load reflectivity array
      RefDz = InFile->Reflectivity

    end if

    ; set missing data value
    RefDz@_FillValue = -99900.0

    ; load radial distance to the start of each gate array
    GateSpace = InFile->GateWidth
    RefDzSize = dimsizes(RefDz)
    Range     = GateSpace(0) * ispan(0,RefDzSize(1)-1,1)

  else if(RefFormat .eq. "XBAND") then

    ; lat and lon from global attributes
    SiteLat = InFile@Latitude
    SiteLon = InFile@Longitude

    ; radar elevation angle from global attributes
    ElevationA = InFile->Elevation
    ElevationAngle = ElevationA(0)

    ; load azimuth array
    Azimuth = InFile->Azimuth

    ; load reflectivity array
    RefDz = InFile->Reflectivity

    ; set missing data value
    RefDz@_FillValue = -99900.0

    ; load radial distance to the start of each gate array
    GateSpace = InFile->GateWidth
    GateSpace = GateSpace / 1000
    RefDzSize = dimsizes(RefDz)
    Range     = GateSpace(0) * ispan(0,RefDzSize(1)-1,1)


  else
  end if
  end if
  end if

  VectorFileName     = ImageFilePrefix + ".ps"
  RasterFileNameBase = ImageFilePrefix +  "_reflectivity_" +  sprintf("%.1f",ElevationAngle) + ".gif"
  RasterFileName     = ImageOutputPath + RasterFileNameBase
  KmlFileName        = KmlOutputPath    + ImageFilePrefix +  "_reflectivity_" +  sprintf("%.1f",ElevationAngle) + ".kml"

  ; redfine azimuths for plotting, assuming azimuth array values are at the center of beam
  AzimuthTmp = Azimuth

  do i = 0,dimsizes(Azimuth) - 1

    ; neighboring azimuth in counter-clockwise (CCW) direction
    if(i .eq. 0) then

      AzCCwise = Azimuth(dimsizes(Azimuth) - 1)

    else

      AzCCwise = Azimuth(i - 1)

    end if

    ; define new azimuth one half of a beam width CCW from current
    if(AzCCwise .gt. Azimuth(i)) then

      ; special case where CCW azimuth is CCW of north and azimuth is CW of north
      AzimuthTmp(i) = AzCCwise + ((Azimuth(i) + 360.) - AzCCwise) / 2.

    else

      AzimuthTmp(i) = Azimuth(i) - (Azimuth(i) - AzCCwise) / 2.

   end if

    ; check for north crossing
    if( AzimuthTmp(i) .gt. 360.) then

      AzimuthTmp(i) = AzimuthTmp(i) - 360.
    end if

  end do


  ; Add in hack for XBAND.  The Azimuth orders change since only scanning 130 - 309 range.  The data files can be ascending or desecnding depending. Needs to revise code above. 
  if(RefFormat .ne. "XBAND") then
    Azimuth = AzimuthTmp
  end if

; get dimensions of reflectivity array
  RefDzSize = dimsizes(RefDz)

; convert 1D arrays of azimuth and range to 2D arrays conforming to the size of RefDz
  Azimuth2D = conform(RefDz,Azimuth,0)
  Range2D   = conform(RefDz,Range,1)

  Azimuth2D = where(Azimuth2D .eq. 0.,360.,Azimuth2D)

; calculate x,y coordinates in cartesion space for each range/azimuth pair
  XCoord =  Range2D * sin(Deg2Rad * Azimuth2D)
  YCoord =  Range2D * cos(Deg2Rad * Azimuth2D)

; transform from cartesion grid to latitude/longitude WGS84 grid
  DeltaAlpha = new((/ RefDzSize(0),RefDzSize(1) /),double)
  DeltaPhi   = new((/ RefDzSize(0),RefDzSize(1) /),double)
  DeltaTheta = new((/ RefDzSize(0),RefDzSize(1) /),double)
  Latitude   = new((/ RefDzSize(0),RefDzSize(1) /),double)
  Longitude  = new((/ RefDzSize(0),RefDzSize(1) /),double)

  MeridianLength = MeridianDegreeLength(doubletoint(SiteLat))

  ParallelLength = ParallelDegreeLength(doubletoint(SiteLat)) - \
                   ((SiteLat - doubletoint(SiteLat)) *          \
                    (ParallelDegreeLength(doubletoint(SiteLat)) \
                     - ParallelDegreeLength(doubletoint(SiteLat) + 1)))

  Rn = 360. * ParallelLength / (2. * PI * sin(Deg2Rad * SiteLat))

  DeltaAlpha = atan( XCoord / (Rn - YCoord)) / Deg2Rad

  DeltaAlpha = where(DeltaAlpha .ne. 0,DeltaAlpha,9999.)  ; replace zero condition

  DeltaPhi = where(DeltaAlpha .ne. 9999., \
                   (Rn - (XCoord / sin(DeltaAlpha * Deg2Rad))) / MeridianLength,0.)

  DeltaAlpha = where(DeltaAlpha .ne. 9999.,DeltaAlpha,0.) ; restore zero condition

  DeltaTheta = DeltaAlpha / sin( SiteLat * Deg2Rad)

  Latitude  = SiteLat + DeltaPhi
  Longitude = SiteLon + DeltaTheta

; overlap the lat and lon arrays by one delta azimuth so that color fill will be continuous
  LatitudeOvrlap  = new((/ RefDzSize(0) + 1,RefDzSize(1) /),double)
  LongitudeOvrlap = new((/ RefDzSize(0) + 1,RefDzSize(1) /),double)

  do i = 0,RefDzSize(0) - 1
    do j = 0,RefDzSize(1) - 1
      LatitudeOvrlap(i,j)  = Latitude(i,j)
      LongitudeOvrlap(i,j) = Longitude(i,j)
    end do
  end do

  do j = 0,RefDzSize(1) - 1
    LatitudeOvrlap(RefDzSize(0),j)  = Latitude(0,j)
    LongitudeOvrlap(RefDzSize(0),j) = Longitude(0,j)
  end do

; configure plotting workstation to postscript output
  wks_type = "ps"
  wks_type@wkOrientation = "portrait"
  wks = gsn_open_wks(wks_type,ImageFilePrefix)

; load custom color map for Scanning radars
  gsn_define_colormap(wks,"ScanningRadar")

; configure contouring resources
  res                   = True
  res@sfXArray          = LongitudeOvrlap
  res@sfYArray          = LatitudeOvrlap
  res@cnFillOn          = True
  res@cnLinesOn         = False
  res@cnFillMode        = "CellFill"
  res@trGridType        = "TriangularMesh"
  res@lbLabelAutoStride = True
  res@lbLabelBarOn      = False

; set contour value range and interval
  res@cnLevelSelectionMode = "ManualLevels"  ; set manual contour levels
  res@cnMinLevelValF       =  -25.           ; set min contour level
  res@cnMaxLevelValF       =   75            ; set max contour level
  res@cnLevelSpacingF      =    5            ; set contour spacing

; disable contour labeling and information label string (e.g., "CONTOUR FROM ...")
  res@cnLineLabelsOn = False
  res@cnInfoLabelOn  = False

; disable border drawing
  res@tmXBBorderOn = False  ; bottom
  res@tmXTBorderOn = False  ; top
  res@tmYLBorderOn = False  ; left
  res@tmYRBorderOn = False  ; right
 
; disable tick mark drawing
  res@tmXBOn = False  ; bottom
  res@tmXTOn = False  ; top
  res@tmYLOn = False  ; left
  res@tmYROn = False  ; right

; disable plot and axis titles
  res@tiMainOn       = False  ; main plot title
  res@gsnLeftString  = ""     ; upper-left plot title (data array long-name)
  res@gsnRightString = ""     ; upper-right plot title (data array units)
  res@tiXAxisOn      = False  ; x-axis title
  res@tiYAxisOn      = False  ; y-axis title

; force postscript output to portrait
  res@gsnMaximize         = True
  res@gsnPaperOrientation = "portrait"
  res@gsnPaperMargin      = 0.0

; draw the color-fill contour plot
  contour = gsn_csm_contour(wks,RefDz,res)

; convert postscript to gif
; use exclamation mark to set the virtual canvas page size to the cropped image size 
  system("convert -transparent \#ffffff -crop !610x612+1+91 " + \
         VectorFileName + " " + RasterFileName)

; cleanup intermediate postscript file
  system("rm " + VectorFileName)

; cleanup intermediate data files
  if(strlen(NidsToNetCDFFile) .gt. 0) then

    system("rm " + NidsToNetCDFFile)

  end if

; output KML file, if a KML path was specified
  if(EnableKmlOutput .gt. 0) then

    OutText = "<?xml version=" + DQ + "1.0" + DQ + " encoding=" + DQ + "UTF-8" + DQ + "?>"+CR+LF + \
              "<kml xmlns=" + DQ + "http://earth.google.com/kml/2.0" + DQ + ">" + DQ + CR+LF     + \
              "<GroundOverlay>" + CR+LF                                                          + \
              "<name>" + ImageFilePrefix + "</name>" + CR+LF                                     + \
              "<ElevationAngle>" + sprintf("%.1f",ElevationAngle) + "</ElevationAngle>" + CR+LF  + \
              "<Icon>" + CR+LF                                                                   + \
              "<href>" + KmlHrefPath + RasterFileNameBase + "</href>" + CR+LF                    + \
              "</Icon><LatLonBox>" + CR + LF                                                     + \
              "<north>" + sprintf("%.14f",max(Latitude)) + "</north>" + CR+LF                    + \
              "<south>" + sprintf("%.14f",min(Latitude)) + "</south>" + CR+LF                    + \
              "<east>" + sprintf("%.14f",max(Longitude)) + "</east>" + CR+LF                     + \
              "<west>" + sprintf("%.14f",min(Longitude)) + "</west>" + CR+LF                     + \
              "</LatLonBox>" + CR + LF                                                           + \
              "</GroundOverlay>" + CR + LF                                                       + \
              "</kml>"

    asciiwrite(KmlFileName,OutText)

  end if

end

