<?php session_start(); ?>


<link rel="stylesheet" href="/psd/data/obs/src/development-bundle/themes/ui-lightness/jquery.ui.all.css">
<script type="text/javascript"> 


//$(function() {

//  $("#DataImage").resizable();

//});
</script>

<style type="text/css"> 

html {width:100%}
body {
margin:0;
width:100%;
}

.btn {
  display: inline-block;
  padding: 6px 12px;
  margin-bottom: 0;
  font-size: 14px;
  font-weight: normal;
  line-height: 1.42857143;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  -ms-touch-action: manipulation;
      touch-action: manipulation;
  cursor: pointer;
  -webkit-user-select: none;
     -moz-user-select: none;
      -ms-user-select: none;
          user-select: none;
  background-image: none;
  border: 1px solid transparent;
  border-radius: 4px;
}


</style>




<?php
include ("./src/SelectConnection.php");

date_default_timezone_set('UTC');

$CurrentTime =  mktime(0,0,0,date('m'), date('d'), date('Y'));

if (isset($_GET['SiteID'])) {

        $SiteID = mysql_real_escape_string($_GET['SiteID']);
}
else {

$SiteID = "";

}


if (isset($_GET['DataTypeID'])) {

        $DataTypeID = mysql_real_escape_string($_GET['DataTypeID']);
}
else {

$DataTypeID = "";

}



if (isset($_GET['Img'])) {

        $Img = mysql_real_escape_string($_GET['Img']);
}
else {

$Img = "";

}



if (isset($_GET['ImgExt'])) {

        $ImgExt = mysql_real_escape_string($_GET['ImgExt']);

        $_SESSION["ImgExt"] = $ImgExt;


}
else {

$ImgExt = "";

}





if ( isset ($_GET["Date"])) {

   $Date = mysql_real_escape_string($_GET["Date"]);

   list($Year, $Month, $Date) =  explode("-", $Date );
 
   $DateObj = mktime(0,0,0,$Month,$Date,$Year);

   $MySQLDataString = date("Y-m-d", $DateObj);

   $JDay =  date("z", $DateObj);
   $JDay += 1 ;

#    $Time = date(mktime(0, 0, 0, 7, 1, ));
   $YearDay = $Year . $JDay;
   $LongYear = $Year;
   $ShortYear = ($Year % 100);
   $YearDay = $ShortYear . $JDay;

}



else  {

    $JDay = date("z",$CurrentTime  );

   $MySQLDataString = date( "Y-m-d", $CurrentTime);
 
   $JDay += 1 ;

    $Year   = date("Y", $CurrentTime );
    $Month  = date("m", $CurrentTime );
    $Date    = date("j", $CurrentTime );

    $LongYear = date("Y", $CurrentTime );
    $ShortYear = date("y", $CurrentTime );

    $YearDay = $ShortYear . $JDay;

    $DateString = date("Y-m-d", $CurrentTime );


}
$BasePath  =  "/data/realtime";
$HtmlBasePath = "http://example.com/somepath";
$MissingDataLink = "http://example.com/somepath/missinglink.png";
$Contents = ""; 


// Select all the rows in the markers table

      
$query = "select data_type.RealtimeDirectoryPath, data_type.FileNameConvention, data_type.DataStateID, data_type.SiteLevel
from data_type
where data_type.DataTypeID = '" . $DataTypeID . "';";



$result = mysql_query($query);
if (!$result) {
   die('Invalid query: ' . mysql_error());
}


$row = mysql_fetch_row($result);


$FileParts = explode("_", $row[1]);

if (count($FileParts) == 2) {

  $FileExt = $FileParts[1];

}
else {
  $FileExt = "";
}


 # Check to see if it's site level type product
if ($row[3]  == 'Y') {

  $format = '%s/%s/%s';
  $BasePath = sprintf($format, $BasePath, $row[0], $SiteID);
  $HtmlBasePath = sprintf($format, $HtmlBasePath, $row[0], $SiteID);



}
else {

  $format = '%s/%s';
  $BasePath = sprintf($format, $BasePath, $row[0]);
  $HtmlBasePath = sprintf($format, $HtmlBasePath, $row[0]);
}


# For ASCII Data Displays
  if ($row[2] == 2) {

      $format = '%s/%04d/%03d/';

      $ScanPath = sprintf($format, $BasePath, $LongYear, $JDay);

      $YearDirectories = scandir( $ScanPath );

      foreach ( $YearDirectories as &$value ) {

          if (($value != ".") and ($value != "..")  and ($value != "latest") ) {

             if ($FileExt != "" ) {

                 if (preg_match("/.$FileExt/i", $value)) {

                     $FilePath = $ScanPath . "/" . $value;
                     $Contents = $Contents . file_get_contents($FilePath);
                 }

             }
             else {

                     $FilePath = $ScanPath . "/" . $value;
                     $Contents = $Contents . file_get_contents($FilePath);

             }


           }

      }


        if ($Contents != "") {


	    # For site specfic formats
            if (($DataTypeID == 14) or ($DataTypeID == 13)) { 

                   $mysql1 = "    select site_has_inst_data.DataFormatFile
 				  from site_has_inst_data, site_has_inst, inst_type
  				  where site_has_inst_data.OperationalID = site_has_inst.OperationalID
			          and site_has_inst_data.DataTypeID = '" . $DataTypeID ."'
			          and site_has_inst.SiteID = '" . $SiteID ."'
			          and site_has_inst_data.StartDate <= '" . $MySQLDataString ."'
			          and (site_has_inst_data.EndDate >= '" . $MySQLDataString ."' or site_has_inst_data.EndDate is null)
			          group by site_has_inst_data.DataFormatFile;";
 
 

                      $res=mysql_query($mysql1);

                  if($res) {

                         $row = mysql_fetch_row($res);

                         $SiteSpecficDataFormatFile = $row[0];
                  }
                  else { 
                         $SiteSpecficDataFormatFile = "";

                  } 
                

                $Rows = explode("\n", $Contents); 
        
                ?><table border="1">
                        
                         <?php 
                             if ( $SiteSpecficDataFormatFile != "") { 
                                  $Columns = explode(",", $SiteSpecficDataFormatFile);   
                      
                                 echo "<tr>"; 
                                     foreach ($Columns as $Column) {
                                         echo "<td>";
                                         echo $Column;
                                         echo "</td>";
                                      }

                                  echo "</tr>";     
                                
                              }               
                         
                         foreach ($Rows as &$Row) { 
                            echo "<tr>";   
                             $Columns = explode(",", $Row); 
                             
                                 foreach ($Columns as $Column) { 
                                  echo "<td>";  
                                  echo $Column; 
                                  echo "</td>";
                                 } 
                              echo "</tr>";

                        } ?> 
                 </table> <?php    
            }
            else { 
                 echo "<pre>";
                echo $Contents;
                echo "</pre>";
            } 
      
        } 
        else { 

           echo  "Data not available for selected dates"; 

        } 

  }
 



# For all Image type products

if ($row[2] == 4  ) { 

   $format = 'ls %s/%04d/%03d/*%s* | tail -1';
   $SysCommand = sprintf($format, $BasePath, $LongYear, $JDay, $FileExt );

#  $format = 'ls %s%s/%s/%04d/%03d/*%s* | tail -1';

#  $SysCommand = sprintf($format, $BasePath, $row[0], $SiteID, $LongYear, $JDay, $FileExt );
  

  exec($SysCommand, &$output);

  $pathparts = pathinfo( $output[0]);

  $FileName = $pathparts['basename'];


# Look previous day's dir for image type files

  if ($FileName == "") {

        $PreviousDay = $DateObj - 86400; 

        $JDay =  date("z", $PreviousDay);
   	$JDay += 1 ;

        $Year   = date("Y", $PreviousDay );
    	$Month  = date("m", $PreviousDay );
    	$Date    = date("j",$PreviousDay );

    	$LongYear = date("Y", $PreviousDay );
    	$ShortYear = date("y", $PreviousDay );

   	$ShortYear = ($Year % 100);
    	$YearDay = $ShortYear . $JDay;
     
        $format = 'ls %s/%04d/%03d/*%s* | tail -1';
        $SysCommand = sprintf($format, $BasePath, $LongYear, $JDay, $FileExt );
       

        #$format = 'ls %s/*%s* | tail -1';

        #$format = 'ls %s%s/%s/%04d/%03d/*%s* | tail -1';
 
        exec($SysCommand, &$output);

        $pathparts = pathinfo( $output[0]);

        $FileName = $pathparts['basename'];

   }



  if ($FileName != "") {

        $format = '%s/%04d/%03d/%s';

        $DataOutputLink = sprintf($format, $HtmlBasePath,  $LongYear, $JDay, $FileName );
  
     

        echo "<img id=\"DataImage\" src=$DataOutputLink >";
        
   }
  else {

        echo  "Data not available for selected dates"; 

  }
}












