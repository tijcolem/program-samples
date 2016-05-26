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

$query = array(); 


if (isset($_GET['DataStateID'])) {

    $DataStateID = mysql_real_escape_string($_GET['DataStateID']);
}
else {

    $DataStateID = "%";
}



if (isset($_GET['AgencyID'])) {

    $AgencyID = mysql_real_escape_string($_GET['AgencyID']);
}
else {

    $AgencyID = "%";
}



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



if (isset($_GET['CategoryID'])) {

    $CategoryID = mysql_real_escape_string($_GET['CategoryID']);
} 
else {

    $CategoryID = "%";
} 




    #Find Data Types based on instrument cateogry

    $query['DataTypeID'] = "select data_type.DataTypeID, data_type.DataTypeName
    from site_has_inst_data, site_has_inst, data_type, inst_type, site
    where site_has_inst.OperationalID = site_has_inst_data.OperationalID
    and site_has_inst_data.DataTypeID = data_type.DataTypeID
    and site_has_inst.TypeID = inst_type.TypeID
    and site_has_inst.SiteID = site.SiteID
    and data_type.DataStateID like  '" . $DataStateID . "'" . " 
    and site_has_inst.SiteID like  '" . $SiteID . "'" . " 
    and site_has_inst.AgencyID like  '" . $AgencyID . "'" . " 
    and site_has_inst_data.DataTypeID like  '" . $DataTypeID . "'" . " 
    and inst_type.CategoryID like  '" . $CategoryID . "'" . "
    and data_type.Realtime = 'Y'
    and site.RealTimeDisplay = 'Y'
    and site_has_inst.Active = 'Y'
    group by data_type.DataTypeID 
    order by data_type.DataTypeName;"; 



    $query['SiteID'] = " select site.SiteID, CONCAT(site.City, \" (\", site.SiteID,  \")\"  )
    from site_has_inst_data, site_has_inst, data_type, inst_type, site
    where site_has_inst.OperationalID = site_has_inst_data.OperationalID
    and site_has_inst_data.DataTypeID = data_type.DataTypeID
    and site_has_inst.TypeID = inst_type.TypeID
    and site_has_inst.SiteID = site.SiteID
    and data_type.DataStateID like   '" . $DataStateID . "'" . "
    and site_has_inst.SiteID like '" . $SiteID . "'" . " 
    and site_has_inst.AgencyID like  '" . $AgencyID . "'" . "
    and site_has_inst_data.DataTypeID like  '" . $DataTypeID . "'" . " 
    and inst_type.CategoryID like  '" . $CategoryID . "'" . "
    and data_type.Realtime = 'Y'
    and site.RealTimeDisplay = 'Y'
    and site_has_inst.Active = 'Y'
    group by site.SiteID
    order by site.City;"; 



    $query['AgencyID'] = "select agency.AgencyID, agency.AgencyName
    from site_has_inst_data, site_has_inst, data_type, inst_type, agency, site
    where site_has_inst.OperationalID = site_has_inst_data.OperationalID
    and site_has_inst_data.DataTypeID = data_type.DataTypeID
    and site_has_inst.TypeID = inst_type.TypeID
    and site_has_inst.AgencyID = agency.AgencyID
    and site_has_inst.SiteID = site.SiteID
    and data_type.DataStateID like   '" . $DataStateID . "'" . "
    and site_has_inst.SiteID like '" . $SiteID . "'" . " 
    and site_has_inst.AgencyID like '" . $AgencyID . "'" . " 
    and site_has_inst_data.DataTypeID like '" . $DataTypeID . "'" . " 
    and inst_type.CategoryID like  '" . $CategoryID . "'" . " 
    and data_type.Realtime = 'Y'
    and site.RealTimeDisplay = 'Y'
    and site_has_inst.Active = 'Y'
    group by agency.AgencyID 
    order by agency.AgencyName;"; 
    



    $query['DataStateID'] = "  select data_state.DataStateID, data_state.Name
    from site_has_inst_data, site_has_inst, data_type, inst_type, data_state, site
    where site_has_inst.OperationalID = site_has_inst_data.OperationalID
    and site_has_inst_data.DataTypeID = data_type.DataTypeID
    and data_type.DataStateID = data_state.DataStateID
    and site_has_inst.TypeID = inst_type.TypeID
    and site_has_inst.SiteID = site.SiteID
    and data_type.DataStateID like   '" . $DataStateID . "'" . "
    and site_has_inst.SiteID like  '" . $SiteID . "'" . "
    and site_has_inst.AgencyID like  '" . $AgencyID . "'" . "
    and site_has_inst_data.DataTypeID like  '" . $DataTypeID . "'" . "
    and inst_type.CategoryID like  '" . $CategoryID . "'" . "
    and data_type.Realtime = 'Y'
    and site.RealTimeDisplay = 'Y'
    and site_has_inst.Active = 'Y'
    group by data_state.DataStateID
    order by data_state.Name;";


    $query['CategoryID'] =  " select inst_category.CategoryID, inst_category.Name
    from site_has_inst_data, site_has_inst, data_type, inst_type, inst_category,site
    where site_has_inst.OperationalID = site_has_inst_data.OperationalID
    and site_has_inst_data.DataTypeID = data_type.DataTypeID
    and site_has_inst.TypeID = inst_type.TypeID
    and inst_type.CategoryID = inst_category.CategoryID
    and site_has_inst.SiteID = site.SiteID
    and data_type.DataStateID like   '" . $DataStateID . "'" . "
    and site_has_inst.SiteID like  '" . $SiteID . "'" . "
    and site_has_inst.AgencyID like  '" . $AgencyID . "'" . "
    and site_has_inst_data.DataTypeID like  '" . $DataTypeID . "'" . "
    and inst_type.CategoryID like  '" . $CategoryID . "'" . "
    and data_type.Realtime = 'Y'
    and site.RealTimeDisplay = 'Y'
    and site_has_inst.Active = 'Y'
    group by inst_category.CategoryID
    order by inst_category.Name;";

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

        echo '<option ID="'  . parseToXml($row[0])   . '" name="' . parseToXml($row[1]) . '"></option>'; 
    }

    echo "</" . $key .  ">";

    // End XML file


    }

    echo "</Options>";

?>



