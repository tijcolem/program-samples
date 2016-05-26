<?php

include ("./src/SelectConnection.php");

date_default_timezone_set('UTC');


function parseToXML($htmlStr)
{

$xmlStr=str_replace('<','&lt;',$htmlStr);
$xmlStr=str_replace('>','&gt;',$xmlStr);
$xmlStr=str_replace('"','&quot;',$xmlStr);
$xmlStr=str_replace("'",'&apos;',$xmlStr);
$xmlStr=str_replace("&",'&amp;',$xmlStr);

return $xmlStr;

}

$query = array(); 


if (isset($_GET['SiteID'])) {

    $SiteID = mysql_real_escape_string($_GET['SiteID']);
}
else {

    $SiteID = "%";
}


if (isset($_GET['DataTypeID'])) {

    $DataTypeID = mysql_real_escape_string($_GET['DataTypeID']);
}
else {

    $DataTypeID = "%";
}





if (isset($_GET['ActiveID'])) {

    $ActiveID = mysql_real_escape_string($_GET['ActiveID']);

    if ($ActiveID == "Y") { 

        $ActiveSqlString = " and site_has_inst_data.EndDate is null "; 
    }
 
      else if ($ActiveID == "All")  {

	$ActiveID = '%';
        $ActiveSqlString = "";
    }


       else if ($ActiveID == "N")  {

        $ActiveID = 'N';
        $ActiveSqlString = " and site_has_inst_data.EndDate is not null  ";
    }



}
else {

    $ActiveID = "Y";
    $ActiveSqlString = " and site_has_inst_data.EndDate is null  "; 
}



    #Find Data Types based on instrument cateogry

    $query['DataTypeID'] = "select data_type.DataTypeID, data_type.DataTypeName, DATE_FORMAT(MIN(site_has_inst_data.StartDate), '%Y-%m-%d'), 
    DATE_FORMAT(MAX(IFNull(site_has_inst_data.EndDate, UTC_DATE())),'%Y-%m-%d') 
    from site_has_inst_data, site_has_inst, data_type, inst_type, site
    where site_has_inst.OperationalID = site_has_inst_data.OperationalID
    and site_has_inst_data.DataTypeID = data_type.DataTypeID
    and site_has_inst.TypeID = inst_type.TypeID
    and site_has_inst.SiteID = site.SiteID
    and site_has_inst.SiteID like  '" . $SiteID . "'" . " 
    and site_has_inst_data.DataTypeID like  '" . $DataTypeID . "'" . " 
    and data_type.Realtime = 'Y'
    and data_type.DataStateID in (2,4)   " . $ActiveSqlString . "
    group by site_has_inst_data.DataTypeID
    order by data_type.DataTypeName;"; 



    $query['SiteID'] = " select site.SiteID, CONCAT(site.City, \" (\", site.SiteID,  \")\"  ), DATE_FORMAT(site.StartDate, '%Y-%m-%d'), DATE_FORMAT(site.EndDate,'%Y-%m-%d')
    from site_has_inst_data, site_has_inst, data_type, inst_type, site
    where site_has_inst.OperationalID = site_has_inst_data.OperationalID
    and site_has_inst_data.DataTypeID = data_type.DataTypeID
    and site_has_inst.TypeID = inst_type.TypeID
    and site_has_inst.SiteID = site.SiteID
    and site_has_inst.SiteID like '" . $SiteID . "'" . " 
    and site_has_inst_data.DataTypeID like  '" . $DataTypeID . "'" . " 
    and data_type.Realtime = 'Y'
    and data_type.DataStateID in (2,4) " . $ActiveSqlString . "
    group by site.SiteID
    order by site.City;"; 
// Select all the rows in the markers table


echo "<Options>";

header("Content-type: text/xml");
// Start XML file, echo parent node

foreach ($query as $key => $value  ) {

//echo $value; 
//echo "/n/n/n/n/n";


    echo "<" . $key .  ">";

    $result = mysql_query($value);
    if (!$result) {
       die('Invalid query: ' . mysql_error());
    }

    // Iterate through the rows, echoing XML nodes for each

    echo '<option ID="%" name="All"></option>';

    while($row=mysql_fetch_row($result)) { 

      if ($row[3] == "") { 
 
          $EDate = date('Y'). "-" . date('m') . "-"  . date('d');
       
       } 
       else { 

          $EDate =  $row[3];

       }  
        
        echo '<option ID="'  . parseToXml($row[0])   . '" name="' . parseToXml($row[1]) . '"' .  ' sdate="' . parseToXml($row[2]) . '"' .  ' edate="' . parseToXml($EDate) . '"  ></option>'; 
    }

    echo "</" . $key .  ">";

    // End XML file


    }

    echo "</Options>";

?>



