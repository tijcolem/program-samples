<?php

include ("./src/SelectConnection.php");

function parseToXML($htmlStr)
{
$xmlStr=str_replace('<','&lt;',$htmlStr);
$xmlStr=str_replace('>','&gt;',$xmlStr);
$xmlStr=str_replace('"','&quot;',$xmlStr);
$xmlStr=str_replace("'",'&apos;',$xmlStr);
$xmlStr=str_replace("&",'&amp;',$xmlStr);
return $xmlStr;
}




if (isset($_GET['SiteID'])) {

        $SiteID = mysql_real_escape_string($_GET['SiteID']);
}
else {

$SiteID = "%";

}


$IconBasePath =  'http://www.esrl.noaa.gov/psd/data/obs/sitemap/psdmapdatatest/img/';


// Select all the rows in the markers table


$query = "select realtime_last_update.SiteID, realtime_last_update.DataTypeID, site.City, site.Latitude, site.Longitude, site.Elevation, realtime_last_update.DataTypeID, realtime_last_update.LastUpdate,
realtime_last_update.CurrentDate, realtime_last_update.TotalSeconds, realtime_last_update.ImageType,realtime_last_update.GroupImageType,
data_type.DataTypeName
from realtime_last_update, site, data_type
where site.SiteID = realtime_last_update.SiteID
and data_type.DataTypeID = realtime_last_update.DataTypeID
and site.SiteID like '" . $SiteID . "'" . " 
order by realtime_last_update.SiteID;";


if ($Status == "Red") { 

$query = "select realtime_last_update.SiteID, realtime_last_update.DataTypeID, site.City, site.Latitude, site.Longitude, site.Elevation, realtime_last_update.DataTypeID, realtime_last_update.LastUpdate,
realtime_last_update.CurrentDate, realtime_last_update.TotalSeconds, realtime_last_update.ImageType,realtime_last_update.GroupImageType,
data_type.DataTypeName
from realtime_last_update, site, data_type
where site.SiteID = realtime_last_update.SiteID
and data_type.DataTypeID = realtime_last_update.DataTypeID
and realtime_last_update.GroupImageType in ('Yellow', 'Red')
order by realtime_last_update.SiteID;";

}

echo $query;

$result = mysql_query($query);
if (!$result) {
   die('Invalid query: ' . mysql_error());
}



header("Content-type: text/xml");
// Start XML file, echo parent node
echo "<markers>";


// Iterate through the rows, echoing XML nodes for each


$SiteID = ""; 
$Counter = 0; 

while ($row = @mysql_fetch_assoc($result)){

   
  $SiteIcon = $IconBasePath .  $row['GroupImageType'] . "Dot.png";
  $DataIcon = $IconBasePath .  $row['ImageType'] . "Dot.png";


  if ($SiteID != $row['SiteID'])  { 

	$SiteID = $row['SiteID']; 

	if ($Counter != 0) { 

		echo ']]>';
       		echo '</description>';
       		echo '</marker>';
	 }

  // ADD TO XML DOCUMENT NODE
       echo '<marker ';
       echo 'siteID="' . parseToXML( $row['SiteID']) . '" ';
       echo ' name="' . parseToXML($row['City']) . '" ';
       echo ' lat="' . $row['Latitude'] . '" ';
       echo ' lng="' . $row['Longitude'] . '" ';
       echo ' elev="' . $row['Elevation'] . '" ';
       echo ' icon="' . $SiteIcon . '" ';
       echo '>';
       echo '<description>';
       echo '<![CDATA['; 
	
       $Format = '<b>%s</b><img src="%s" alt="some_text"/><br>';
       echo  sprintf($Format, $row['DataTypeName'], $DataIcon);
   }
    else { 

       $Format = '<b>%s</b><img src="%s" alt="some_text"/><br>';
       echo  sprintf($Format, $row['DataTypeName'], $DataIcon);


       $SiteID = $row['SiteID']; 
	
       }

$Counter += 1; 
	
}

// End XML file
echo ']]>';
echo '</description>';
echo '</marker>';
echo '</markers>';

?>

