
  require 'c:\Program Files\ESRL Applications\IngestScripts\Lib\TimeFunctions.pm';
  require 'c:\Program Files\ESRL Applications\IngestScripts\Lib\MadisFunctions.pm';

  use Net::FTP;
  use Time::Piece;
  use Time::Seconds;

  print "\nRunning IngestMapDataFromMadis.pl on ".gmtime()."\n\n";

  ##################  Begin User Configuration ######################

  # MODIFY THE FOLLOWING HASH LIST TO ADD OR REMOVE SITES
  # Define MADIS SiteID, PSD SiteID and RadarFrequency for each site 
  # MADIS SiteID list located at http://madis.noaa.gov/map_stations.html
  # SYNTAX:  'MadisSiteID' => [ 'PsdSiteID' , 'RadarFreqHz' ]

  %MadisMapSites = (  
                      'RTPNC' => [ 'rst', '915' ],
                      'IRVCA' => [ 'irv', '915' ],
                      'LAXCA' => [ 'usc', '915' ],
                      'MOVCA' => [ 'mrv', '915' ],
                      'ONTCA' => [ 'ont', '915' ],
                      'MMRCA' => [ 'mrm', '915' ],
                      'NPSCA' => [ 'nps', '915' ],
                      'SEAWA' => [ 'sea', '915' ], 
                      'TCYCA' => [ 'tcy', '915' ], 
                      'WHPCA' => [ 'wap', '915' ], 
                      'LBKTX' => [ 'lbk', '915' ],
                      'BPATX' => [ 'bpa', '915' ],
                      'HSNTX' => [ 'hsn', '915' ],
                      'LPTTX' => [ 'lpt', '915' ],
                      'CLETX' => [ 'cle', '915' ],
                     'LDBT2' => [ 'ldb', '915' ],
                      'MFATX' => [ 'mfa', '449' ],
                      'FHAAZ' => [ 'fha', '449' ]
			);
		

  ###################  End User Configuration #######################

  # input first command argument - the numer of hours of data to ingest
  $NumHoursToIngest = shift;
  if(!$NumHoursToIngest) { $NumHoursToIngest = 1; }

  # initialize variables 
  $FtpServer           = "madis-data.ncep.noaa.gov";
  $FtpUserName         = "anonymous"; 


  $FtpPassword 	       = "passwd"; 
  $FtpBaseDir          = "LDAD/profiler/netCDF";
 
  $WorkPath            = "C:\\Madis\\data";
  $TemplatePath        = "C:/Program Files/ESRL Applications/IngestScripts/Templates/";
  $NetCdfBasePath      = "LDAD/profiler/netCDF/";
  $OutputBasePath      = "\\\\psdobs.psd.esrl.noaa.gov\\data\\realtime";

  $InputParFile        = "$TemplatePath/MadisMapDump.par";
  $OutputParFile       = "mapdump.par";

  $MadisStaticPath     = "C:/Madis/static";
  $MadisDataPath       = $WorkPath;
  $MadisMapDumpCommand = "C:/Madis/bin/mapdump.exe";

  $NumFileTxSuccess    = 0;
  $NumScrubArchiveHour = 168;  # seven days

  # set MADIS enviromental variables
  $ENV{'MADIS_STATIC'} = $MadisStaticPath;
  $ENV{'MADIS_DATA'}   = $MadisDataPath;

  # change directory to working directory
  chdir($WorkPath);

  # create directory tree for downloaded NetCDF files
  MakeDirectoryTree($NetCdfBasePath);

  # create cutoff ingest date
  $IngestDate = gmtime() - ($NumHoursToIngest * ONE_HOUR);

  # get NetCDF files from the MADIS FTP server
  $ftp = Net::FTP->new($FtpServer, Passive => 1);
  
  $ftp->login($FtpUserName,$FtpPassword) or die "Cannot login ", $ftp->message;
  $ftp->binary();
  $ftp->cwd($FtpBaseDir);

  @GzipFileListing = $ftp->dir("*.gz");

  $NumFileTxSuccess = 0;

  for($GzipFileIndex = 0;$GzipFileIndex <= $#GzipFileListing;$GzipFileIndex++) {

    @FileFields = split(' ',$GzipFileListing[$GzipFileIndex],5);
    $GzipFileListing[$GzipFileIndex] = $FileFields[4];

    @FileFields = split(' ',$GzipFileListing[$GzipFileIndex]);
    $GzipFileName[$GzipFileIndex] = $FileFields[4];
    $FileName[$GzipFileIndex] = substr($FileFields[4],0,13);

    $FileDate = Time::Piece->strptime($FileName[$GzipFileIndex]," %Y%m%d_%H%M");

    if($FileDate >= $IngestDate) {

      # get the compressed NetCDF file using FTP
      $LocalFile = "$NetCdfBasePath/$GzipFileName[$GzipFileIndex]";
      print "Transferring $GzipFileName[$GzipFileIndex] from the MADIS server ...\n";
      $ftp->get($GzipFileName[$GzipFileIndex],$LocalFile);

      # decompress the local instance of the compressed NetCDF file
      if(-e $LocalFile) { `gzip -d -f $LocalFile`; }

      # add successfully transferred file info to the archive list
      if(-e "$NetCdfBasePath/$FileName[$GzipFileIndex]") {

        $NumFileTxSuccess++;
      } 
    }
  }

  $ftp->quit();

  print "Total number of MADIS NetCDF files transferred and decompressed: $NumFileTxSuccess\n";

  # generate list of NetCDF files that exist on disk
  @NetCdfFileList = <$NetCdfBasePath/*>;

  if($#NetCdfFileList >= 0) {

    # cycle through each NetCDF file
    for($NetCdfFileIndex = 0;$NetCdfFileIndex <= $#NetCdfFileList;$NetCdfFileIndex++) {

      if(($DateTimePos = rindex($NetCdfFileList[$NetCdfFileIndex],"/")) >= 0) { 

        $DateTimePos++;
      }
      else { $DateTimePos = 0; }

      $DateTime = substr($NetCdfFileList[$NetCdfFileIndex],$DateTimePos);
    
      print "Processing NetCDF file $NetCdfFileList[$NetCdfFileIndex]:\n";

      # parse data for each site
      while($MadisSiteID = each %MadisMapSites) {

        $SiteID    = $MadisMapSites{$MadisSiteID}[0];
        $RadarFreq = $MadisMapSites{$MadisSiteID}[1];

        print "  Parsing data for $MadisSiteID ...\n";

        # undefine $/ so we can slurp the entire par file into a string variable
        open(FILE,"< $InputParFile") || die "Cannot open input par file $InputParFile.";
        undef $/;
        $ParFileContents = <FILE>;
        close(FILE);
        $/ = "\n";

        # replace date/time and site strings
        $ParFileContents =~ s/yyyymmdd_hhmm/$DateTime/;
        $ParFileContents =~ s/sssss/$MadisSiteID/;

        # output new par file
        open(FILE,"> $OutputParFile") || die "Cannot open output par file $OutputParFile.";
        print FILE $ParFileContents;
        close(FILE);

        # dump the NetCDF data
        `$MadisMapDumpCommand`;    

        # set/create the output path
        $SiteID =~ tr/A-Z/a-z/;

        $OutputWindPath = $OutputBasePath."\\Radar".$RadarFreq."\\CnsWind\\".$SiteID;
        $OutputRassPath = $OutputBasePath."\\Radar".$RadarFreq."\\CnsTemp\\".$SiteID;

        if(!-e $OutputWindPath) { MakeDirectoryTree($OutputWindPath) };
        if(!-e $OutputRassPath) { MakeDirectoryTree($OutputRassPath) };

        # convert dump to CNS format
        OutputMapFormatToCnsFormat($SiteID,"mapdump.txt",$OutputWindPath,$OutputRassPath);

        # clean up dump and par files
        if(-e $WorkPath."\\mapdump.txt") { `del $WorkPath\\mapdump.txt`; }
        if(-e $WorkPath."\\mapdump.par") { `del $WorkPath\\mapdump.par`; }
      }
    }
   
    # clean up NetCDF files
    @filelist = glob("C:/Madis/data/LDAD/profiler/netCDF/*");   
    unlink @filelist;
  }

  print "\nIngestMapDataFromMadis.pl Finished on ".gmtime()."\n";

  exit;