<?php
$a = session_id();
if(empty($a)) session_start();

echo "<script>";
echo "var SID = \"" . session_id() .  "\" ;"; 
echo "</script>";

?>




<!-- site-wide style sheets -->
<link rel="stylesheet" type="text/css" href="/css/font-awesome/css/font-awesome.css" />
<!-- A style sheet with settings for all divisions -->
<!-- A style sheet specifically for the defined division -->
<!--[if lte IE 6]><link rel="stylesheet" type="text/css" href="/css/ie.css" media="all"><![endif]-->
<!-- page-specific stylesheet -->
<!--[if gt IE 6]><link rel="stylesheet" type="text/css" href="/css/ie7.css" media="all"><![endif]-->
<script type="text/javascript" src="/css/ie.js"></script>
<!-- adding a meaningless comment to test new check-in script -->
<link rel="alternate" type="application/rss+xml" title="ESRL News Feed" href="/rss/rss.xml" >



<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>PSD2 Data Overlays - Google Maps 3</title>

<style type="text/css">


#media_icons {
        float: left;
        text-align: center;
        padding-top: 5px;
        padding-bottom: 5px;
}

#orgs {
        float: left;
        width: 45%;
        text-align: left;
        padding: 0em 0.2em 0em 0em;
}




 .DataHeader {
 	font-family: Arial, Helvetica, sans-serif;
 	font-size: 11pt;
 	color: #003399;
 	font-weight: bold;
 }


 .SubHeader {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 9pt;
        color: #003399;
        font-weight: bold;
 }

#play, #stop, #reverse {
	height: 30px;
	width:  30px;
}




#Map1RadarTimeStamps,#Map2RadarTimeStamps  { 

	width: 300px;
	height: 40px;
	font-family: Arial, Helvetica, sans-serif;
        font-size: 8pt;
        color: #003399;
        font-weight: bold;
	
} 



#Map1LatestTimeStamp, #Map2LatestTimeStamp {

        font-family: Arial, Helvetica, sans-serif;
	width: 300px;
	height: 35px;
        font-size: 8pt;
        color: #000000;
        font-weight: bold;

}


#MapSynch1, #MapSynch2 { 

float:right;
font-size: 8pt;

}

/* the page footer */
#footer {
	clear: both;
        font-size: 80%;
	background: #000066 url(/img/gradient.gif) top left repeat-y;
	color: white;
	padding: 1.0em 0.7em 0.6em 0.7em;
	margin: 0em;
	line-height: 1.3em;
	width: 1200;
	height: 4em;
	border: none;

}

#footer a {
	color: white;
}


#media_icons .fa {
        margin: 0 8px;
}

/* a div containing policy-type links shown in the footer. */
#policies {
        float: right;
        width: 35%;
        text-align: right;
}



#widgettable {

margin-left:200px; 
margin-right:200px;
}

#widgets { 

height:120px; 

}


#tdslide1, #tdslide2,#tdslide3, #tdslide4 { 


border:0;
width:200px;
} 

#DownloadStatusID { 
font-size: 8pt;
}

#CalendarID { 
font-size: 9pt;
}

</style>


<script>

		// run the currently selected effect
		function runEffect() {
			// get effect type from 

			// most effect types need no options passed by default
			// some effects have required parameters

			var options;

			// run the effect
			$( "#Map1LatestTimeStamp" ).css('color', 'red');
			$( "#Map2LatestTimeStamp" ).css('color', 'red');

			callback1();
			callback2();
		};

		function toggleCalInput(option) { 

			if ( option == "show") {

			 $('#CalendarID').show();

			}

			if ( option == "hide") {

			 $('#CalendarID').hide();

			} 

		} 


		  function toggleDownloadStatus(option) {

                        if ( option == "show") {

                         $('#DownloadStatusID').show();

                        }

                        if ( option == "hide") {

                         $('#DownloadStatusID').hide();

                        }

                }







		//callback function to bring a hidden box back
		function callback1() {
			setTimeout(function() {
				$( "#Map1LatestTimeStamp" ).css( 'color', 'black');
			}, 5000 );
		};

		function callback2() {
                        setTimeout(function() {
                                $( "#Map2LatestTimeStamp" ).css( 'color', 'black');
                        }, 5000 );
                };





</script>



<script src="http://maps.googleapis.com/maps/api/js?client=gme-noaa&sensor=false&v=3.8&channel=OAR.ESRL.PSD.PSD2ScanRadar"
  type="text/javascript"></script>

<link rel="stylesheet" href="/psd/data/obs/src/development-bundle/themes/ui-lightness/jquery.ui.all.css">
<script src="/psd/data/obs/src/development-bundle/jquery-1.8.2.js"></script>
<script src="/psd/data/obs/src/development-bundle/ui/jquery.ui.core.js"></script>
<script src="/psd/data/obs/src/development-bundle/ui/jquery.ui.widget.js"></script>
<script src="/psd/data/obs/src/development-bundle/ui/jquery.ui.mouse.js"></script>
<script src="/psd/data/obs/src/development-bundle/ui/jquery.ui.slider.js"></script>
<script src="/psd/data/obs/src/development-bundle/ui/jquery.ui.button.js"></script>
<script src="/psd/data/obs/src/development-bundle/ui/jquery.ui.datepicker.js"></script>
<script src="/psd/data/obs/src/development-bundle/ui/jquery-ui-timepicker-addon.js"></script>
<link rel="stylesheet" href="/psd/data/obs/src/development-bundle/themes/base/jquery-ui-timepicker-addon.css">
<script src="/psd/data/obs/src/datetimepicker.js"></script>


<script type="text/javascript" src="/psd/data/obs/src/ProgressBar.js"></script>

<script>
	$(function() {


		$( "#slider" ).slider({
			value:-500,
			min: -1000,
			max: -10
		});


		$( "#Opacityslider" ).slider({
                        value:50,
                        min: 1,
                        max: 100
                });



		 $( "#Opacityslider" ).slider({
                        value:50,
                        min: 1,
                        max: 100,
			stop: function(event, ui) {
      			 updateOpacity();
    			}

                });


		var now = new Date();
                var now_utc = new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(),  now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds());
		var CurrentDate = new Date();
//		var BeginFileDate = new Date(1353110400000);
		var BeginFileDate = new Date(1331596800000);


		$('#ArchiveDateID').datetimepicker({
			dateFormat: 'yy-mm-dd',
			defaultValue: CurrentDate.toCalendarString(),
			alwaysSetTime: 'true',
			minDateTime: BeginFileDate, 
			maxDateTime: now_utc
		
		});
//		$("#ArchiveDateID").datetimepicker();



	//	$( "#Opacityslider" ).bind("changed", function(){ alert("Changed")});




	});
</script>




	<script>
	$(function() {
	

		$( "#stepforward" ).button({
                        text: false,
                        icons: {
                                primary: "ui-icon-arrowthick-1-e"
                        }
                })


		 $( "#stepreverse" ).button({
                        text: false,
                        icons: {
                                primary: "ui-icon-arrowthick-1-w"
                        }
                })


	
		$( "#play" ).button({
			text: false,
			icons: {
				primary: "ui-icon-circle-triangle-e"
			}
		})


	

		$( "#stop").button({
			text: false,
			icons: {
				primary: "ui-icon-stop"
			}
		});

		$( "#reverse").button({
                        text: false,
                        icons: {
                                primary: "ui-icon-circle-triangle-w"
                        }
                });

		

	      $('#CalendarID').hide();
	
	      $('#MapSynch1').click(function() { snapView(2,1)  } );
	      $('#MapSynch2').click(function() { snapView(1,2)  } );
	

	});
</script>

<script>


if ( !Date.prototype.toCalendarString ) {

    ( function() {

        function pad(number) {
            var r = String(number);
            if ( r.length === 1 ) {
                r = '0' + r;
            }
            return r;
        }

        Date.prototype.toCalendarString = function() {
            return this.getUTCFullYear()
                + '-' + pad( this.getUTCMonth() + 1 )
                + '-' + pad( this.getUTCDate() )
                + ' ' + pad( this.getUTCHours() )
                + ':' + pad( this.getUTCMinutes() );
        };

    }() );
}






if ( !Date.prototype.toISOString ) {
     
    ( function() {
     
        function pad(number) {
            var r = String(number);
            if ( r.length === 1 ) {
                r = '0' + r;
            }
            return r;
        }
  
        Date.prototype.toISOString = function() {
            return this.getUTCFullYear()
                + '-' + pad( this.getUTCMonth() + 1 )
                + '-' + pad( this.getUTCDate() )
                + 'T' + pad( this.getUTCHours() )
                + ':' + pad( this.getUTCMinutes() )
                + ':' + pad( this.getUTCSeconds() )
                + '.' + String( (this.getUTCMilliseconds()/1000).toFixed(3) ).slice( 2, 5 )
                + 'Z';
        };
   
    }() );
}




function convertTimeStamp(EpochTime) { 

	var TimeObj = new Date(EpochTime * 1000); 

	return TimeObj; 


} 



Object.keys = Object.keys || function(o) {
    var result = [];
    for(var name in o) {
        if (o.hasOwnProperty(name))
          result.push(name);
    }
    return result;
};


</script> 



<script type="text/javascript">
    //<![CDATA[

var CurrentDir = 'forward'; 
var AnimTimer; 
var UpdateFilesTimer; 

function RadarOverLay()
{
this.RadarDataFiles = []; 
}



var MapOverlays ={};

MapOverlays[1] = {}; 
MapOverlays[2] = {}; 


var RadarOverLays =  {};

var RadarDataFiles  = {};

RadarDataFiles['pix1']  = [];
RadarDataFiles['mux1']  = [];
RadarDataFiles['dax1']  = [];
RadarDataFiles['kgo1']  = [];
RadarDataFiles['stc1']  = [];
RadarDataFiles['stv1']  = [];

RadarDataFiles['pix2']  = [];
RadarDataFiles['mux2']  = [];
RadarDataFiles['dax2']  = [];
RadarDataFiles['kgo2']  = [];
RadarDataFiles['stc2']  = [];
RadarDataFiles['stv2']  = [];


var RadarDataCords  = {};

RadarDataCords['pix1']  = [];
RadarDataCords['mux1']  = [];
RadarDataCords['dax1']  = [];
RadarDataCords['kgo1']  = [];
RadarDataCords['stc1']  = [];
RadarDataCords['stv1']  = [];

RadarDataCords['pix2']  = [];
RadarDataCords['mux2']  = [];
RadarDataCords['dax2']  = [];
RadarDataCords['kgo2']  = [];
RadarDataCords['stc2']  = [];
RadarDataCords['stv2']  = [];


var RadarDataTimes  = {};

RadarDataTimes['pix1']  = [];
RadarDataTimes['mux1']  = [];
RadarDataTimes['dax1']  = [];
RadarDataTimes['kgo1']  = [];
RadarDataTimes['stc1']  = [];
RadarDataTimes['stv1']  = [];

RadarDataTimes['pix2']  = [];
RadarDataTimes['mux2']  = [];
RadarDataTimes['dax2']  = [];
RadarDataTimes['kgo2']  = [];
RadarDataTimes['stc2']  = [];
RadarDataTimes['stv2']  = [];



var RadarElevationAngle  = {};

RadarElevationAngle['pix1']  = [];
RadarElevationAngle['mux1']  = [];
RadarElevationAngle['dax1']  = [];
RadarElevationAngle['kgo1']  = [];
RadarElevationAngle['stc1']  = [];
RadarElevationAngle['stv1']  = [];

RadarElevationAngle['pix2']  = [];
RadarElevationAngle['mux2']  = [];
RadarElevationAngle['dax2']  = [];
RadarElevationAngle['kgo2']  = [];
RadarElevationAngle['stc2']  = [];
RadarElevationAngle['stv2']  = [];



var CurrentRadarOptions = {}; 

CurrentRadarOptions[1] = 'none'; 
CurrentRadarOptions[2] = 'none'; 


var ImgNum = 0;
var LoopTime = 60;   // Set default value to 60 minutes.  
var RealTimeMark = "Realtime";  // Default to use realtime.  
var DownloadComplete = "false"; 
var DownloadInProgress = "false"; 
var HasDownloaded = "false"; 
var CurrentTimeDelta = {};
CurrentTimeDelta[1] = 90;
CurrentTimeDelta[2] = 90;


var MasterTimeDelta = 90; 

var Maps = {}; 


var RadarBasePath   = 'http://www.esrl.noaa.gov/psd/data/obs/realtime/ScanningRadar/Images/';

// Set def value for RadarFileXmlUrl for loop timeer

var RadarFileXmlUrl = 'http://www.esrl.noaa.gov/psd/data/obs/sitemap/ScanRadar/ScanningRadarFiles60.xml';

var RadarBaseXmlPath = 'http://www.esrl.noaa.gov/psd/data/obs/sitemap/ScanRadar/';

var RadarBaseArchiveXmlPath = 'http://www.esrl.noaa.gov/psd/data/obs/sitemap/ScanRadar/tmp/';

var MissingRadarFileName = 'http://www.esrl.noaa.gov/psd/data/obs/sitemap/ScanRadar/img/Blank.gif';

var count = 0;
var which  = 0;

function sleep(ms){
		var dt = new Date();
		dt.setTime(dt.getTime() + ms);
		while (new Date().getTime() < dt.getTime());
}

function load() {
       

        Maps[1] = new google.maps.Map(document.getElementById("MapDiv1"), {
        center: new google.maps.LatLng(38.6145, -122.3418),
        zoom: 6,
        overviewMapControl: 1,
        overviewMapControlOptions: {
       opened: 0 },
       mapTypeId: 'terrain'
      });


      Maps[2] = new google.maps.Map(document.getElementById("MapDiv2"), {
        center: new google.maps.LatLng(38.6145, -122.3418),
        zoom: 6,
        overviewMapControl: 1,
        overviewMapControlOptions: {
       opened: 0 },
       mapTypeId: 'terrain'
      });


	
	pb ={};

	pb[1] =  new progressBar();
	pb[2] =  new progressBar();

	
         Maps[1].controls[google.maps.ControlPosition.RIGHT].push(pb[1].getDiv());
         Maps[2].controls[google.maps.ControlPosition.RIGHT].push(pb[2].getDiv());



         var SelMap1ID = document.getElementById('Map1RadarType');
         var SelMap2ID = document.getElementById('Map2RadarType');
         var LoopTimeID = document.getElementById('LoopTime');


         SelMap1ID.options[0].selected= 'true'; 
         SelMap2ID.options[0].selected= 'true'; 
         LoopTimeID.options[1].selected= 'true'; 

	 var radioButtons = document.getElementsByName("RadioTime");

	 radioButtons[0].checked = 1;	


}




function updateLegend(MapNum) {

     var img = document.createElement("IMG");

     if (MapNum == 1 ) {

          var SelMapID = $( "#Map1RadarType" ).val();

      }


     if (MapNum == 2) {

          var SelMapID = $( "#Map2RadarType" ).val();

      }


     if ((SelMapID == 'pix') || (SelMapID == 'kgo') || ( SelMapID == 'dax') || (SelMapID == 'mux') || (SelMapID == 'stc'))   {

       img.src = "./img/ScanningRadarLabelBar2.png";

     }

     if (SelMapID == 'stv') {

       img.src = "./img/RainfallRateLabelBar.png";
     }


     if (MapNum == 1) {

         $('#Legend1').html(img);

        }


     if (MapNum == 2) {

         $('#Legend2').html(img);

     }


}



function snapView(MapNum1, MapNum2) {

	var MapCenter    = Maps[MapNum1].getCenter(); 
	var ZoomLevel    = Maps[MapNum1].getZoom(); 

	Maps[MapNum2].setCenter(MapCenter); 
	Maps[MapNum2].setZoom(ZoomLevel); 
 
}




function loadMap1RadarDataFiles(Radar, MapNumber) { 

	   
	   updateLegend(1);


          var RadarSiteID = Radar.options[Radar.selectedIndex].value;
	  var CurrentMap1RadarSiteID = CurrentRadarOptions[1] + "1";
	  var CurrentMap2RadarSiteID = CurrentRadarOptions[2] + "2" ;	  

     	  	if ( CurrentRadarOptions[1] != "none") {

			if  (  RadarOverLays[CurrentMap1RadarSiteID]) { 

            			clearTimeout(AnimTimer);
            			clearTimeout(UpdateFilesTimer);			
				which = 0;
		
            			for (i=0; i< RadarOverLays[CurrentMap1RadarSiteID].length; i++)  {

	   				RadarOverLays[CurrentMap1RadarSiteID][i].setMap(null);

            			}

             			delete RadarOverLays[CurrentMap1RadarSiteID]; 
            			RadarDataTimes[CurrentMap1RadarSiteID]= [];
             			RadarDataFiles[CurrentMap1RadarSiteID]= [];
             			RadarDataCords[CurrentMap1RadarSiteID]= [];
             			RadarElevationAngle[CurrentMap1RadarSiteID]= [];
           
			}

	 	}


	 CurrentRadarOptions[1] = RadarSiteID;
	 if ( RadarSiteID != "none") {


		var TimePatch = new Date();

		if (RealTimeMark == "Archive" && DownloadComplete == 'true' ) {

                var RadarFileXmlUrlTimer = RadarBaseArchiveXmlPath + "ScanningRadarFiles" + LoopTime + SID + ".xml" + "?Time=" + TimePatch.getTime();
	
		}
		else if (RealTimeMark == "Realtime")  
		 { 

                var RadarFileXmlUrlTimer = RadarBaseXmlPath + "ScanningRadarFiles" + LoopTime +  ".xml" + "?Time=" + TimePatch.getTime();
	

		}
		else {
			return false; 
		} 



                delete TimePatch;

	  	downloadUrl(RadarFileXmlUrlTimer, function(data) {

           		var xml = data.responseXML;
	           	var RadarFiles = xml.documentElement.getElementsByTagName(RadarSiteID);

			calculateTimeDelta(RadarFiles, MapNumber);

          		loadMap1RadarXmlFiles(xml, RadarFiles, RadarSiteID, MapNumber);

         	});

	 }


}




function loadMap2RadarDataFiles(Radar, MapNumber) {

          updateLegend(2);

	 if (ImgNum > 0) { 

	  	alert("Please wait for Map to finish loading"); 
		return false; 

	  }


	  var RadarSiteID = Radar.options[Radar.selectedIndex].value;

          var CurrentMap2RadarSiteID = CurrentRadarOptions[2] + "2";
          
	  var CurrentMap1RadarSiteID = CurrentRadarOptions[1] + "1";
	  

	  if ( CurrentRadarOptions[2] != "none") { 

		clearTimeout(UpdateFilesTimer);
			
			clearTimeout(AnimTimer);
  	 		
			if  (  RadarOverLays[CurrentMap2RadarSiteID]) {

				for (i=0; i < RadarOverLays[CurrentMap2RadarSiteID].length; i++)  {

                                	RadarOverLays[CurrentMap2RadarSiteID][i].setMap(null);

                        	}

                        	delete RadarOverLays[CurrentMap2RadarSiteID];
                        	RadarDataTimes[CurrentMap2RadarSiteID]= [];
                        	RadarDataFiles[CurrentMap2RadarSiteID]= [];
                        	RadarDataCords[CurrentMap2RadarSiteID]= [];
                        	RadarElevationAngle[CurrentMap2RadarSiteID]= [];

				CurrentRadarOptions[2] = RadarSiteID;	

			} 

	 }
	

	if ( CurrentRadarOptions[1] != "none")      { 
		
	  	if ( RadarSiteID != "none") {
	
			CurrentRadarOptions[2] = RadarSiteID;	
		
	                var RadarSiteID = Radar.options[Radar.selectedIndex].value;

			var TimePatch = new Date();


			  if (RealTimeMark == "Archive" && DownloadComplete == 'true' ) {

				RadarOverLays[CurrentMap1RadarSiteID][which].setOpacity(0);	
                		var RadarFileXmlUrlTimer = RadarBaseArchiveXmlPath + "ScanningRadarFiles" + LoopTime + SID + ".xml" + "?Time=" + TimePatch.getTime();

                	  }
                	  else if (RealTimeMark == "Realtime")   {

				RadarOverLays[CurrentMap1RadarSiteID][which].setOpacity(0);	
                		var RadarFileXmlUrlTimer = RadarBaseXmlPath + "ScanningRadarFiles" + LoopTime +  ".xml" + "?Time=" + TimePatch.getTime();


                	}
                	else {
                		return false;
               		 }


			which = 0;
                	delete TimePatch;
			
                        downloadUrl(RadarFileXmlUrlTimer, function(data) {

                        var xml = data.responseXML;
                        var RadarFiles = xml.documentElement.getElementsByTagName(RadarSiteID);
	
			calculateTimeDelta(RadarFiles, MapNumber);

                        loadMap2RadarXmlFiles(xml, RadarFiles, RadarSiteID, MapNumber); });
			

		}
	


	}
	else if  (RadarSiteID != "none") { 

		alert("Please choose Map1 option first");

        	var SelMap2ID = document.getElementById('Map2RadarType');

        	SelMap2ID.options[0].selected= 'true';

		CurrentRadarOptions[2] = 'none';	
	} 

}


function loadMap2RadarXmlFiles(xml, RadarFiles, RadarSiteID, MapNumber) {

    var MapRadarSiteID =  RadarSiteID + MapNumber;   
 
    var Map1RadarSiteID = CurrentRadarOptions[1] + '1'; 

    if ( CurrentRadarOptions[1] != "none") { 

        for (i=0; i< RadarDataFiles[Map1RadarSiteID].length; i++)  {	 

		var MatchedFile = -1; 
    
		var PrevTimeDiff = MasterTimeDelta; 
		  
      	  	for (j=0; j< RadarFiles.length; j++)  {

        		var EpochTime =  RadarFiles[j].getAttribute("epochtime");

			TimeDiff   =    Math.abs(( EpochTime - RadarDataTimes[Map1RadarSiteID][i]));

			if (TimeDiff < MasterTimeDelta) {

				if (TimeDiff < PrevTimeDiff) { 

					MatchedFile = j;  
					PrevTimeDiff = TimeDiff; 
				}
		
			} 
			else {
			
			PrevTimeDiff = MasterTimeDelta; 
			
			} 
	
	        }

		if (MatchedFile >= 0) {

      		var FileName =   RadarFiles[MatchedFile].getAttribute("name");
        	var EpochTime =  RadarFiles[MatchedFile].getAttribute("epochtime");
        	var LatLongBounds =  RadarFiles[MatchedFile].getAttribute("latlongbounds");
        	var ElevationAngle =  RadarFiles[MatchedFile].getAttribute("angle");
			
		RadarDataFiles[MapRadarSiteID].push(FileName);
        	RadarDataTimes[MapRadarSiteID].push(EpochTime);
        	RadarDataCords[MapRadarSiteID].push(LatLongBounds);
        	RadarElevationAngle[MapRadarSiteID].push(ElevationAngle);

		}

		if (MatchedFile < 0) {

		var FileName = MissingRadarFileName;
		var EpochTime = 10000;
		var LatLongBounds = "0,0,0,0";  
		var ElevationAngle = "Not Available";  
		
		RadarDataFiles[MapRadarSiteID].push(FileName);
        	RadarDataTimes[MapRadarSiteID].push(EpochTime);
        	RadarDataCords[MapRadarSiteID].push(LatLongBounds);
        	RadarElevationAngle[MapRadarSiteID].push(ElevationAngle);
		
		}  
	}
    
   	loadOverlaysMap2(RadarSiteID, MapNumber);

	updateLatestTimes();

	if ( RealTimeMark == "Realtime" ) { 
 
   		checkForNewUpdates();    

	}
  
   }

}



function loadMap1RadarXmlFiles(xml, RadarFiles, RadarSiteID, MapNumber) { 

     var MapRadarSiteID = RadarSiteID + MapNumber; 
	
     for (i=0; i< RadarFiles.length; i++)  {

     var FileName =   RadarFiles[i].getAttribute("name");
     var EpochTime =  RadarFiles[i].getAttribute("epochtime");      
     var LatLongBounds =  RadarFiles[i].getAttribute("latlongbounds");      
     var ElevationAngle =  RadarFiles[i].getAttribute("angle");

     var FullFileName = FileName

         RadarDataFiles[MapRadarSiteID].push(FullFileName);
         RadarDataTimes[MapRadarSiteID].push( EpochTime);
         RadarDataCords[MapRadarSiteID].push( LatLongBounds);
         RadarElevationAngle[MapRadarSiteID].push(ElevationAngle);  

    }

   loadOverlaysMap1(RadarSiteID, MapNumber)

}



function calculateTimeDelta(RadarFiles, MapNumber) { 

     var PrevTimeDelta = 0; 
     var Count = 0; 
     var TotalTimeDelta = 0; 

    for (i=0; i< RadarFiles.length; i++)  {

        var EpochTime =  RadarFiles[i].getAttribute("epochtime");      

       	var TimeDelta = (Math.abs(PrevTimeDelta - EpochTime) );

	if  (TimeDelta < 1000) {
	
		TotalTimeDelta += TimeDelta
		Count += 1; 
	} 

	PrevTimeDelta = EpochTime;  	
     } 


    if (Count > 0) { 
	
	var AvgTimeDelta = (TotalTimeDelta / Count); 

	CurrentTimeDelta[MapNumber] = AvgTimeDelta	
     } 



    if (CurrentTimeDelta[1] > CurrentTimeDelta[2]) {

	MasterTimeDelta = CurrentTimeDelta[1];  

     }
    else { 

	MasterTimeDelta = CurrentTimeDelta[2];  
	
	} 
 
}	 


function updateRadarFiles(xml, Map1RadarFiles, Map2RadarFiles) { 

        RadarSiteID1        = CurrentRadarOptions[1];
        RadarSiteID2        = CurrentRadarOptions[2];
	
	Map1RadarSiteID = RadarSiteID1 + '1'; 
	Map2RadarSiteID = RadarSiteID2 + '2'; 


    if (CurrentRadarOptions[1] != 'none' &&  CurrentRadarOptions[2] != 'none') {
 
      for (i=0; i< Map1RadarFiles.length; i++)  {
       
             var Map1FileName =  Map1RadarFiles[i].getAttribute("name");
             var Map1EpochTime = Map1RadarFiles[i].getAttribute("epochtime");
             var Map1LatLongBounds = Map1RadarFiles[i].getAttribute("latlongbounds");
             var Map1ElevationAngle = Map1RadarFiles[i].getAttribute("angle");
	     var PrevTimeDiff = MasterTimeDelta;

	    if (Map1EpochTime > RadarDataTimes[Map1RadarSiteID][ RadarDataTimes[Map1RadarSiteID].length - 1] ) {

                	clearTimeout(AnimTimer)

			MatchedFile = -1; 

			for (j=0; j < Map2RadarFiles.length; j++)  { 

                        	var Map2FileName =   Map2RadarFiles[j].getAttribute("name");
                        	var Map2EpochTime =  Map2RadarFiles[j].getAttribute("epochtime");
                        	var Map2LatLongBounds =  Map2RadarFiles[j].getAttribute("latlongbounds");
                        	var Map2ElevationAngle =  Map2RadarFiles[j].getAttribute("angle");

                        	TimeDiff   =    Math.abs( Map2EpochTime - Map1EpochTime);

				if (TimeDiff < MasterTimeDelta) {

                                	if (TimeDiff < PrevTimeDiff) {

                                        	MatchedFile = j;
                                        	PrevTimeDiff = TimeDiff;
                                	}

                        	}
                        
				else {

                        		PrevTimeDiff = MasterTimeDelta;

                        	}


                   	}

           	 	if (MatchedFile >= 0) {

                		var Map2FileName =   Map2RadarFiles[MatchedFile].getAttribute("name");
                		var Map2EpochTime =  Map2RadarFiles[MatchedFile].getAttribute("epochtime");
                		var Map2LatLongBounds =  Map2RadarFiles[MatchedFile].getAttribute("latlongbounds");
                		var Map2ElevationAngle =  Map2RadarFiles[MatchedFile].getAttribute("angle");

                	}

                	if (MatchedFile < 0) {

                		var Map2FileName = MissingRadarFileName;
                		var Map2EpochTime = 10000;

               		 }


			RadarDataTimes[Map1RadarSiteID].shift();
                        RadarDataFiles[Map1RadarSiteID].shift();
                        RadarDataCords[Map1RadarSiteID].shift();
                        RadarElevationAngle[Map1RadarSiteID].shift();

                        RadarDataFiles[Map1RadarSiteID].push(Map1FileName);
                        RadarDataTimes[Map1RadarSiteID].push(Map1EpochTime);
                        RadarDataCords[Map1RadarSiteID].push(Map1LatLongBounds);
                        RadarElevationAngle[Map1RadarSiteID].push(Map1ElevationAngle);

	
			RadarDataTimes[Map2RadarSiteID].shift();
                        RadarDataFiles[Map2RadarSiteID].shift();
                        RadarDataCords[Map2RadarSiteID].shift();
                        RadarElevationAngle[Map2RadarSiteID].shift();

                        RadarDataFiles[Map2RadarSiteID].push(Map2FileName);
                        RadarDataTimes[Map2RadarSiteID].push(Map2EpochTime);
                        RadarDataCords[Map2RadarSiteID].push(Map2LatLongBounds);
                        RadarElevationAngle[Map2RadarSiteID].push(Map2ElevationAngle);

			Map1ArrSize =  (RadarDataFiles[Map1RadarSiteID].length - 1 );
			Map2ArrSize =  (RadarDataFiles[Map2RadarSiteID].length - 1 );
		
	       		RadarOverLays[Map1RadarSiteID][which].setOpacity(0);
        		RadarOverLays[Map2RadarSiteID][which].setOpacity(0);
		
			RadarOverLays[Map1RadarSiteID].shift();	
			RadarOverLays[Map2RadarSiteID].shift();	


			var Bounds =  RadarDataCords[Map1RadarSiteID][Map1ArrSize].split(","); 
				
			var swBound = new google.maps.LatLng(Bounds[1], Bounds[3]);

                	var neBound = new google.maps.LatLng(Bounds[0], Bounds[2]);

               	 	var MapBounds = new google.maps.LatLngBounds(swBound, neBound);

                	var srcImage = RadarDataFiles[Map1RadarSiteID][Map1ArrSize];
			
	   		var Map1OverLaysArrSize = (RadarOverLays[Map1RadarSiteID].length );  	

                	RadarOverLays[Map1RadarSiteID][Map1OverLaysArrSize] =   new google.maps.GroundOverlay(
                 	srcImage,
                	MapBounds, {opacity: 0.0 });

                	RadarOverLays[Map1RadarSiteID][Map1OverLaysArrSize].setMap(Maps[1]);
	


			var Bounds =  RadarDataCords[Map2RadarSiteID][Map2ArrSize].split(",");

                        var swBound = new google.maps.LatLng(Bounds[1], Bounds[3]);

                        var neBound = new google.maps.LatLng(Bounds[0], Bounds[2]);

                        var MapBounds = new google.maps.LatLngBounds(swBound, neBound);

                        var srcImage = RadarDataFiles[Map2RadarSiteID][Map2ArrSize];

                        var Map2OverLaysArrSize = (RadarOverLays[Map2RadarSiteID].length );

                        RadarOverLays[Map2RadarSiteID][Map2OverLaysArrSize] =   new google.maps.GroundOverlay(
                        srcImage,
                        MapBounds, {opacity: 0.0 });

                        RadarOverLays[Map2RadarSiteID][Map2OverLaysArrSize].setMap(Maps[2]);

			runEffect();

			RadarOverLays[Map1RadarSiteID][which].setOpacity(0);
                        RadarOverLays[Map2RadarSiteID][which].setOpacity(0);

        		var Map1ArrSize =  (RadarDataTimes[Map1RadarSiteID].length - 1 );
        		var Map2ArrSize =  (RadarDataTimes[Map2RadarSiteID].length - 1 );

        		var Map1TimeObj = convertTimeStamp(RadarDataTimes[Map1RadarSiteID][Map1ArrSize]);
        		var Map2TimeObj = convertTimeStamp(RadarDataTimes[Map2RadarSiteID][Map2ArrSize]);


        		updateLatestTimes();


			writeTimeStamps(Map1RadarSiteID,  RadarOverLays[Map1RadarSiteID].length, which)
                        writeTimeStamps(Map2RadarSiteID,  RadarOverLays[Map2RadarSiteID].length, which)

                        runEffect();

        		// Shift array on screen to next element.
	
        		var OpacityValue =  Math.abs($( "#Opacityslider" ).slider( "value" ) / 100);


			if ((CurrentDir == "stop") || (CurrentDir == "stepback") || (CurrentDir == "stepforward")  ) { 
			
				   RadarOverLays[Map1RadarSiteID][which].setOpacity(OpacityValue);
                	           RadarOverLays[Map2RadarSiteID][which].setOpacity(OpacityValue);


			}
			else { 

                        	changeDirection(CurrentDir);


			} 	
	
		}


	}
	

}


	

}



function updateLatestTimes() { 


       var RadarSiteID1        = CurrentRadarOptions[1];
       var RadarSiteID2        = CurrentRadarOptions[2];

       var Map1RadarSiteID = RadarSiteID1 + '1';
       var Map2RadarSiteID = RadarSiteID2 + '2';

       var Map1ArrSize =  (RadarDataTimes[Map1RadarSiteID].length );
       var Map2ArrSize =  (RadarDataTimes[Map2RadarSiteID].length );

       var Map1TimeObj = convertTimeStamp(RadarDataTimes[Map1RadarSiteID][Map1ArrSize]);
       var Map2TimeObj = convertTimeStamp(RadarDataTimes[Map2RadarSiteID][Map2ArrSize]);


       var Map1TimeString = "";
       var Map2TimeString = "";

       var BeginFileDate = new Date(1353110400000);

       for (var i = Map1ArrSize; i > 1; i-- ) { 

	    var Map1TimeObj = convertTimeStamp(RadarDataTimes[Map1RadarSiteID][i])  

            if (Map1TimeObj > BeginFileDate ) {

                Map1TimeString = Map1TimeObj.toUTCString()
		break; 

            } else {

                 Map1TimeString = "Not Available"

            }

        } 


      for (var i = Map2ArrSize; i > 1; i-- ) { 

            var Map2TimeObj = convertTimeStamp(RadarDataTimes[Map2RadarSiteID][i])

            if (Map2TimeObj > BeginFileDate ) {

                Map2TimeString = Map2TimeObj.toUTCString()
                break;

            } else {

                 Map2TimeString = "Not Available"

            }

        }


       var Map1LatestTS = document.getElementById("Map1LatestTimeStamp");

        var Map1Output =  "Latest Time: " + Map1TimeString;

        Map1LatestTS.innerHTML =  Map1Output;

        var Map2LatestTS = document.getElementById("Map2LatestTimeStamp");

        var Map2Output =  "Latest Time: " +  Map2TimeString;

        Map2LatestTS.innerHTML =  Map2Output;



}





function checkForNewUpdates() { 

 
	if ( CurrentRadarOptions[1] != 'none' && CurrentRadarOptions[2] != 'none') { 
			
  		var TimePatch = new Date();

  		var RadarFileXmlUrlTimer = RadarFileXmlUrl + '?Time=' + TimePatch.getTime();

  		delete TimePatch;

        	downloadUrl(RadarFileXmlUrlTimer, function(data) {

           	var xml = data.responseXML;
           	var Map1RadarFiles = xml.documentElement.getElementsByTagName(CurrentRadarOptions[1]);
           	var Map2RadarFiles = xml.documentElement.getElementsByTagName(CurrentRadarOptions[2]);

          	updateRadarFiles(xml, Map1RadarFiles, Map2RadarFiles);

          	});

		
		if (RealTimeMark == "Realtime" ) {

	         	UpdateFilesTimer = setTimeout(function(){checkForNewUpdates();  }, 30000);
		} 
       }


}





function downloadUrl(url, callback) {

        var request = window.ActiveXObject ?
          new ActiveXObject('Microsoft.XMLHTTP') :
          new XMLHttpRequest;

      request.onreadystatechange = function() {
        if (request.readyState == 4) {
          request.onreadystatechange = doNothing;
          callback(request, request.status);
 	}
      
	};

      request.open('GET', url, true);
      request.send(null);
}



function doNothing() {}




function updateOpacity() { 

 var OpacityValue =  Math.abs($( "#Opacityslider" ).slider( "value" ) / 100);

 Keys = Object.keys(RadarOverLays);

                for (var key in RadarOverLays)  {

                        RadarOverLays[key][which].setOpacity(OpacityValue);

		} 

}



function changeDirection(Direction)  { 


if ((Direction == 'stop') || (Direction == 'stepforward') || (Direction == 'stepback'))   {

    clearTimeout(AnimTimer);
    CurrentDir = Direction;
}



if (CurrentRadarOptions[1] == 'none' ) {


 	   alert("Please choose a radar for Map 1");

	   return false; 
} 



if (CurrentRadarOptions[2] == 'none' ) {


           alert("Please choose a radar for Map 2");

           return false;
}



if (Direction == 'forward')  { 

    	clearTimeout(AnimTimer);
	forward();

}		


if (Direction == 'reverse')   {

    clearTimeout(AnimTimer);
     reverse();

}




if (Direction == 'stepforward')   {

     stepForward();

}



if (Direction == 'stepback')   {

     stepReverse();

}

CurrentDir = Direction;


}




Object.keys = Object.keys || function(o) {
    var result = [];
    for(var name in o) {
        if (o.hasOwnProperty(name))
          result.push(name);
    }
    return result;
};







  function forward() {

   var Speed =  Math.abs($( "#slider" ).slider( "value" ));
   var OpacityValue =  Math.abs($( "#Opacityslider" ).slider( "value" ) / 100);


   Keys = Object.keys(RadarOverLays);

 
        if( which < ( RadarOverLays[Keys[0]].length - 1)){


		RadarTime = ""; 

			// loop through the keys in RadarOverlays (e.g.  key = kpix, kmux, kdax, etc) 
  		for (var key in RadarOverLays)  {
			RadarOverLays[key][which].setOpacity(0);
							
			}
        		which++
        		
  		for (var key in RadarOverLays)  {
        		
			RadarOverLays[key][which].setOpacity(OpacityValue);
			
			var Length = RadarOverLays[Keys[0]].length;

			writeTimeStamps(key, Length, which)


		}

	 if ( which == RadarOverLays[Keys[0]].length - 1) {

  		AnimTimer = setTimeout(forward,1250);
	
         }
	else { 

  		AnimTimer = setTimeout(forward,Speed);
	}  

		
     }
    else {
		 for (var key in RadarOverLays)  {

                        RadarOverLays[key][which].setOpacity(0);

                        }
        	which =  0;

		for (var key in RadarOverLays)  {

                        RadarOverLays[key][which].setOpacity(OpacityValue);

			var Length = RadarOverLays[Keys[0]].length;

                        writeTimeStamps(key, Length, which)

			


		 } 
     
  AnimTimer = setTimeout(forward,Speed);
    }
 
 }




function writeTimeStamps(RadarSiteID, Length, which) { 

			MapNumber = RadarSiteID.substring(3,4)

                        TimeObj = convertTimeStamp(RadarDataTimes[RadarSiteID][which]);

			var TimeString = ""; 

			var BeginFileDate = new Date(1353110400000);


			if (TimeObj > BeginFileDate ) { 

				TimeString = TimeObj.toUTCString()   

			} else {

			 	TimeString = "Not Available"

			} 

			 var Map1RadarTS = document.getElementById("Map1RadarTimeStamps");
 			 var Map2RadarTS = document.getElementById("Map2RadarTimeStamps");

                        if (MapNumber == 1) {

                                 RadarTime = "Number:  " + (which + 1) + "/" +  Length + "<br> Time: " + TimeString  + "<br> Beam Elevation: " + RadarElevationAngle[RadarSiteID][which] + " degrees"

                                 Map1RadarTS.innerHTML =  RadarTime;

                        }


                          if (MapNumber == 2) {

                                RadarTime = "Number:  " + (which + 1) + "/" +  Length + "<br> Time: " + TimeString  + "<br> Beam Elevation: " + RadarElevationAngle[RadarSiteID][which] + " degrees"

                                Map2RadarTS.innerHTML =  RadarTime;

                        }

} 




  function reverse() {

  
  var RadarTS = document.getElementById("RadarTimeStamps");

   var Speed =  Math.abs($( "#slider" ).slider( "value" ));
   var OpacityValue =  Math.abs($( "#Opacityslider" ).slider( "value" ) / 100);
   
   Length = Object.keys(RadarDataFiles).length;

   Keys = Object.keys(RadarOverLays);


             // This is assuming that all radar arrays have equal number of images

        if( which > 0 ){


                RadarTime = "";

                        // loop through the keys in RadarOverlays (e.g.  key = kpix, kmux, kdax, etc)
                for (var key in RadarOverLays)  {
                        RadarOverLays[key][which].setOpacity(0);

                        }
                        which--

                for (var key in RadarOverLays)  {

                        RadarOverLays[key][which].setOpacity(OpacityValue);

			MapNumber = key.substring(3,4)
	
                	TimeObj = convertTimeStamp(RadarDataTimes[key][which]);
     		
			var Length = RadarOverLays[Keys[0]].length;

                        writeTimeStamps(key, Length, which)



		}

	  if ( which == 0) {

                AnimTimer = setTimeout(reverse,1250);

         }
        else {

                AnimTimer = setTimeout(reverse,Speed);
        }

     }
    else {

                 for (var key in RadarOverLays)  {
                        RadarOverLays[key][which].setOpacity(0);
                        }
                which = RadarOverLays[Keys[0]].length - 1;
                for (var key in RadarOverLays)  {
                        RadarOverLays[key][which].setOpacity(OpacityValue);


		 	 var Length = RadarOverLays[Keys[0]].length;

                        writeTimeStamps(key, Length, which)




                }

  	AnimTimer = setTimeout(reverse,Speed);
    }

 }





function stepForward() {

  clearTimeout(AnimTimer);

  CurrentDir = 'stop'; 

  var OpacityValue =  Math.abs($( "#Opacityslider" ).slider( "value" ) / 100);

   Keys = Object.keys(RadarOverLays);


        if( which < ( RadarOverLays[Keys[0]].length - 1)){


                RadarTime = "";

                        // loop through the keys in RadarOverlays (e.g.  key = kpix, kmux, kdax, etc)
                for (var key in RadarOverLays)  {
                        RadarOverLays[key][which].setOpacity(0);

                        }
                
			which++;   

                for (var key in RadarOverLays)  {

                        RadarOverLays[key][which].setOpacity(OpacityValue);

			  var Length = RadarOverLays[Keys[0]].length;

	                  writeTimeStamps(key, Length, which)


                }

 }
    else {
                 for (var key in RadarOverLays)  {

                        RadarOverLays[key][which].setOpacity(0);

                        }

			 which = 0; 

                for (var key in RadarOverLays)  {

                         RadarOverLays[key][which].setOpacity(OpacityValue);


			var Length = RadarOverLays[Keys[0]].length;

                        writeTimeStamps(key, Length, which)



                 }

    }

 }






 function stepReverse() {

   clearTimeout(AnimTimer);

   CurrentDir = 'stop';

   var RadarTS = document.getElementById("RadarTimeStamps");

   Length = Object.keys(RadarDataFiles).length;

  var OpacityValue =  Math.abs($( "#Opacityslider" ).slider( "value" ) / 100);


   Keys = Object.keys(RadarOverLays);

             // This is assuming that all radar arrays have equal number of images

        if( which > 0 ){

                RadarTime = "";

                        // loop through the keys in RadarOverlays (e.g.  key = kpix, kmux, kdax, etc)
                for (var key in RadarOverLays)  {
                        RadarOverLays[key][which].setOpacity(0);

                        }
                
	        which--

                for (var key in RadarOverLays)  {

                        RadarOverLays[key][which].setOpacity(OpacityValue);


			var Length = RadarOverLays[Keys[0]].length;

                        writeTimeStamps(key, Length, which)




               }

     }
    else {

                 for (var key in RadarOverLays)  {
                        RadarOverLays[key][which].setOpacity(0);
                        }
                which = RadarOverLays[Keys[0]].length - 1;
                for (var key in RadarOverLays)  {
                        RadarOverLays[key][which].setOpacity(OpacityValue);


			var Length = RadarOverLays[Keys[0]].length;

                        writeTimeStamps(key, Length, which)



                }

    }

 }


function setLoopTime(SelectObj) { 


    LoopTime = SelectObj.options[SelectObj.selectedIndex].value;

    if ( CurrentRadarOptions[1] != "none"  && CurrentRadarOptions[2] != "none") {

	clearTimeout(AnimTimer);
        clearTimeout(UpdateFilesTimer);
        which = 0;
        
	var SelMap1ID = document.getElementById('Map1RadarType');
        var SelMap2ID = document.getElementById('Map2RadarType');

	loadMap1RadarDataFiles(SelMap1ID, 1);	

    } 


}


function setRealTimeMark() { 

      var radioButtons = document.getElementsByName("RadioTime");

      for (var x = 0; x < radioButtons.length; x ++) {

          if (radioButtons[x].checked == 1) {

		RealTimeMark = radioButtons[x].value;  		

          }
      }

     if (RealTimeMark == "Archive") {

	toggleCalInput("show"); 
	toggleDownloadStatus("show")	

	}
     else { 

	toggleCalInput("hide"); 	
	toggleDownloadStatus("hide")

	}


    if ((HasDownloaded == "true")) { 

	 var SelMap1ID = document.getElementById('Map1RadarType');

         loadMap1RadarDataFiles(SelMap1ID, 1);



	} 


} 








function loadArchiveData() {



     if ( DownloadInProgress == "true"  )  {

        alert("Please wait for current download to finish");
        return false;

    }





    if (( CurrentRadarOptions[1] == "none") || (CurrentRadarOptions[2] == "none"))  { 

        alert("Please choose radar options for Map1 and Map2");
        return false; 

    }

    var EndTime = document.getElementById('ArchiveDateID').value;
   

    if (EndTime.length != 16)  {

	alert("Please enter valid time format:  YYYY-MM-DD HH:MM");
	return false; 
    } 

    var CurrentDate = new Date();
    var BeginFileDate = new Date(1353110400000);


     if (EndTime > CurrentDate) {
	
      	alert("Please select a time less the current time")

      } 

	
     if (EndTime < BeginFileDate) {

        alert("Historical data begins after Nov-16-2012")

      }



     clearTimeout(AnimTimer);
     clearTimeout(UpdateFilesTimer);

     var SelMap1ID = document.getElementById('Map1RadarType');

     which = 0;

     var Map1LatestTS = document.getElementById("Map1LatestTimeStamp");
     var Map2LatestTS = document.getElementById("Map2LatestTimeStamp");
     var Map1RadarTS = document.getElementById("Map1RadarTimeStamps");
     var Map2RadarTS = document.getElementById("Map2RadarTimeStamps");

     Map2LatestTS.innerHTML =  "";
     Map1LatestTS.innerHTML =  "";
     Map1RadarTS.innerHTML =  "";
     Map2RadarTS.innerHTML =  "";

     var Year       =  EndTime.slice(0,4)
     var Month      =  EndTime.slice(5,7)
     var Day        =  EndTime.slice(8,10)
     var Hour       =  EndTime.slice(11,13)
     var Min        =  EndTime.slice(14,16)
	            
     var TimeString = Year + Month + Day + Hour + Min; 

     var TimePatch = new Date();

     var ArchiveUrlLink =  RadarBaseXmlPath + "GetArchiveData.php?Date=" + TimeString +"&SID=" + SID  + "&Time=" + TimePatch.getTime();

     delete TimePatch;

     document.getElementById("DownloadStatusID").innerHTML= "Downloading...please wait";

     toggleDownloadStatus("show");

     DownloadInProgress = "true"; 

     $("#LoadArchiveDataID").attr("disabled", "disabled");

     downloadUrl(ArchiveUrlLink, function(data) {

	var xml =  data.responseXML;
	var RequestNode = xml.documentElement.getElementsByTagName("request");
	var RequestCounter =  RequestNode[0].getAttribute("number");
			
	if ((RequestCounter) > 50 ) {
			
		alert("Exceeded number of requests. Please try again later."); 
			
                document.getElementById("DownloadStatusID").innerHTML= "Exceeded number of requests";

		}
		else {  

                document.getElementById("DownloadStatusID").innerHTML= "File loaded: " + EndTime;
		DownloadComplete = "true"; 			
		HasDownloaded = "true"; 			
		loadMap1RadarDataFiles(SelMap1ID,1); 
			
		}

		DownloadInProgress = "false";
		$("#LoadArchiveDataID").removeAttr("disabled");


//		setTimeout(function(){ toggleDownloadStatus("hide");  }, 5000);
	


        });


}








function clearMapRadar(RadarSiteID, MapNumber) { 

    if (RadarSiteID != 'none') { 

    	var MapRadarSiteID = RadarSiteID + MapNumber;

    	for (i=0; i< RadarOverLays[MapRadarSiteID].length; i++)  {

        	RadarOverLays[MapRadarSiteID][i].setMap(null);

   	 }

    	delete RadarOverLays[MapRadarSiteID];
    	RadarDataTimes[MapRadarSiteID]= [];
    	RadarDataFiles[MapRadarSiteID]= [];
    	RadarDataCords[MapRadarSiteID]= [];
    	RadarElevationAngle[MapRadarSiteID]= [];

	CurrentRadarOptions[MapNumber] != 'none'; 

   }

}






function loadOverlaysMap1(RadarSiteID, MapNumber) {

	     var MapRadarSiteID = RadarSiteID + MapNumber;  

	     if (RadarDataFiles[MapRadarSiteID].length > 0) {
	  
             RadarOverLays[MapRadarSiteID] = []; 
       	     pb[MapNumber].start(RadarDataFiles[MapRadarSiteID].length);
	   
	     loadRadarData(RadarSiteID, MapNumber);    

	     }
	     else { 

	     var AlertMssg = "Radar " + RadarSiteID + " currently has no available data. Please choose another. ";  
	     alert(AlertMssg);
	   
	    // CurrentRadarOptions[2] = CurrentRadarOptions[1] = 'none';  
	     var SelMap1ID = document.getElementById('Map1RadarType');
             var SelMap2ID = document.getElementById('Map2RadarType');

	     SelMap1ID.options[0].selected= 'true';
             SelMap2ID.options[0].selected= 'true';

 
             RadarDataTimes[MapRadarSiteID]= [];
             RadarDataFiles[MapRadarSiteID]= [];
             RadarDataCords[MapRadarSiteID]= [];
             RadarElevationAngle[MapRadarSiteID]= [];
				    
	    } 	

}
       	






function loadOverlaysMap2(RadarSiteID, MapNumber) {

             var MapRadarSiteID = RadarSiteID + MapNumber;

             if (RadarDataFiles[MapRadarSiteID].length > 0) {

             RadarOverLays[MapRadarSiteID] = [];
             pb[MapNumber].start(RadarDataFiles[MapRadarSiteID].length);

             loadRadarData(RadarSiteID, MapNumber);

             }
             else {

             var AlertMssg = "Radar " + RadarSiteID + " currently has no available data. Please choose another. ";
             alert(AlertMssg);
             CurrentRadarOptions[2] = CurrentRadarOptions[1] = 'none';
             var SelMap1ID = document.getElementById('Map1RadarType');
             var SelMap2ID = document.getElementById('Map2RadarType');

             SelMap1ID.options[0].selected= 'true';
             SelMap2ID.options[0].selected= 'true';


             RadarDataTimes[MapRadarSiteID]= [];
             RadarDataFiles[MapRadarSiteID]= [];
             RadarDataCords[MapRadarSiteID]= [];
             RadarElevationAngle[MapRadarSiteID]= [];

            }

}






function loadRadarData(RadarSiteID, MapNumber) {

	   
	    var MapRadarSiteID = RadarSiteID + MapNumber;  

	    if (ImgNum <  RadarDataFiles[MapRadarSiteID].length) { 
	
       	
 	   		var Bounds =  RadarDataCords[MapRadarSiteID][ImgNum].split(",");

                        var swBound = new google.maps.LatLng(Bounds[1], Bounds[3]);

                        var neBound = new google.maps.LatLng(Bounds[0], Bounds[2]);

                        var MapBounds = new google.maps.LatLngBounds(swBound, neBound);

                        var srcImage = RadarDataFiles[MapRadarSiteID][ImgNum];

                        RadarOverLays[MapRadarSiteID][ImgNum] =   new google.maps.GroundOverlay(
                        srcImage,
                        MapBounds, {opacity: 0.0 });


	            	RadarOverLays[MapRadarSiteID][ImgNum].setMap(Maps[MapNumber]);

		  	pb[MapNumber].updateBar(1);

     		 	setTimeout(function(){loadRadarData(RadarSiteID, MapNumber );  }, 10);

			ImgNum++;
	    }
	
           else { 

          ImgNum = 0;
	  pb[MapNumber].hide();



		// Auto load Map 2

	    	if (MapNumber == 1 && CurrentRadarOptions[2] != 'none') {

                        var SelMap2ID = document.getElementById('Map2RadarType');

                        loadMap2RadarDataFiles(SelMap2ID, 2);

           	}

		// Check current animation state and set it. 		

		 if (MapNumber == 2 && CurrentRadarOptions[2] != 'none') {


			var RadarSiteID1        = CurrentRadarOptions[1];
     			var RadarSiteID2        = CurrentRadarOptions[2];

		        var Map1RadarSiteID = RadarSiteID1 + '1';
		        var Map2RadarSiteID = RadarSiteID2 + '2';
		
                        var Map1ArrSize =  (RadarDataTimes[Map1RadarSiteID].length - 1 );
                        var Map2ArrSize =  (RadarDataTimes[Map2RadarSiteID].length - 1 );

                        var Map1TimeObj = convertTimeStamp(RadarDataTimes[Map1RadarSiteID][Map1ArrSize]);
                        var Map2TimeObj = convertTimeStamp(RadarDataTimes[Map2RadarSiteID][Map2ArrSize]);

                        updateLatestTimes();

                        // Shift array on screen to next element.

                        var Map1RadarTS = document.getElementById("Map1RadarTimeStamps");
                        var Map2RadarTS = document.getElementById("Map2RadarTimeStamps");

                        var OpacityValue =  Math.abs($( "#Opacityslider" ).slider( "value" ) / 100);

                        var Map1TimeObj = convertTimeStamp(RadarDataTimes[Map1RadarSiteID][which]);
                        var Map2TimeObj = convertTimeStamp(RadarDataTimes[Map2RadarSiteID][which]);


			writeTimeStamps(Map1RadarSiteID,  RadarOverLays[Map1RadarSiteID].length, which)
                        writeTimeStamps(Map2RadarSiteID,  RadarOverLays[Map2RadarSiteID].length, which)


                        RadarOverLays[Map1RadarSiteID][which].setOpacity(OpacityValue);
                        RadarOverLays[Map2RadarSiteID][which].setOpacity(OpacityValue);

			
	                changeDirection(CurrentDir);




		} 




	  } 


}


  </script>
  </head>


<body onload="load()">

<table border=1 id="map_table" width="1200">

<tr>
	<td>
	<div id="Map1RadarTimeStamps"></div>
	</td> 

	<td>
        <div id="Map1LatestTimeStamp"></div>
        </td>

	<td>
	<div id="Map2RadarTimeStamps"></div>
	</td>

	<td>
	<div id="Map2LatestTimeStamp"></div>
	</td>
</tr>

<tr>

	<td id="widgets" colspan="4"> 
	<table id="widgettable" border=0>
	<tr>
	        <td id="tdslide1">

		<center> 
        	<button type"input" id="stepreverse"  value="stepreverse"  name="stepReverse" title="Step Back" onclick="changeDirection('stepback')"> </button>
        	<button type"input" id="reverse"  value="reverse"  name="RadarReflReverse"  title="Play Reverse" onclick="changeDirection('reverse')"> </button>
        	<button type"input" id="stop"  value="stop"  name="RadarReflStop"  title="Stop" onclick="changeDirection('stop')"> </button>
        	<button type"input" id="play"  value="play"  name="RadarRefl"  title="Play Forward" onclick="changeDirection('forward')"> </button>
        	<button type"input" id="stepforward"  value="stepforward"  name="stepForward"  title="Step Forward" onclick="changeDirection('stepforward')"> </button>
		<br> 	
		
		
		<center> 
        	Animation Speed        
        	<table width=200>
        	<tr>
		<td width=50 align="right">
                	Slow
                	</td>
                	<td>
                	<div id="slider"> </div>
                	</td>
                	<td width=50 align="left">
                	Fast
                	</td>
        	</tr>
        	</table>
		<center> 
	
		</td>
        	<td id="tdslide2">
		<center>
		Image Opacity
        	<table width=200>
        		<tr>
                	<td width=50 align="right">
                	0%
                	</td>
                	<td>
                	<div id="Opacityslider"> </div>
                	</td>
                	<td width=50 align="left">
                	100%
                	</td>
        		</tr>
        	</table>
       	 	</center> 
	 	</td>


         	<td id="tdslide3">
         	<center>
  
                Looptime (minutes)
		<br>
		<select id="LoopTime" onchange="setLoopTime(this);"/>
        	<option value="30">30</option>
        	<option value="60">60</option>
        	<option value="120">120</option>
        	<option value="180">180</option>
        	</select>

         	</center>
         	</td>

	
	         <td id="tdslide4">
		<input type="radio" id="RealTimeID" name="RadioTime" value="Realtime" onclick="setRealTimeMark();" >Realtime data <br> 
		<input type="radio" id="ArchiveTimeID" name="RadioTime" value="Archive"  onclick="setRealTimeMark();" >Historical data
		<div id="CalendarID"> 
	        End Date (GMT):<input id="ArchiveDateID" name="ArchiveDate" type="text" style="width: 120px"></a><input type="button" id="LoadArchiveDataID" value="Load Data" name="LoadArchiveData" onclick="loadArchiveData();">
<br>
		</div>
		<div id="DownloadStatusID"> </div> 
                </td>

		

        	</td>


	</tr>
	</table>



	
</tr>




<tr>

	<td colspan="2" >

	Map1:
    	<select id="Map1RadarType" onchange="loadMap1RadarDataFiles(this, 1);"/>
    	<option value="none">-</option>
    	<option value="dax">DAX (0.5 Reflectivity)</option>
    	<option value="kgo">KGO (0.5 Reflectivity)</option>
    	<option value="mux">MUX (0.5 Reflectivity)</option>
    	<option value="pix">PIX (0.5 Reflectivity)</option>
    	<option value="stc">STC (2.0 Reflectivity)</option>
    	<option value="stv">STC (2.0 Rainfall Rate)</option>
    	</select>
	<a id="MapSynch1"  href="#">Match Map 2 View</a>
	</td>
	<td colspan="2">

	Map2:
    	<select id="Map2RadarType" onchange="loadMap2RadarDataFiles(this, 2);"/>
    	<option value="none">-</option>
 	<option value="dax">DAX (0.5 Reflectivity)</option>
        <option value="kgo">KGO (0.5 Reflectivity)</option>
        <option value="mux">MUX (0.5 Reflectivity)</option>
        <option value="pix">PIX (0.5 Reflectivity)</option>
        <option value="stc">STC (2.0 Reflectivity)</option>
        <option value="stv">STC (2.0 Rainfall Rate)</option>
    	</select>
	<a id="MapSynch2" href="#">Match Map 1 View</a>

	</td>

</tr>

<tr>
     <td colspan="2">

        <div id="MapDiv1" style="width: 600px; height: 600px"></div>
     </td>

    <td colspan="2">  
     <div id="MapDiv2" style="width: 600px; height: 600px"></div>
    </td>
</tr>

<tr>
    <td colspan="2">
       <center>
       <div id="Legend1" style="width: 600px;"></div>
       </center>
     </td>
     <td colspan="2">
       <center>
       <div id="Legend2" style="width: 600px;"></div>
       </center>
     </td>
</tr>


<tr> 

 <td  colspan="4"> 
  <div id="footer">
    <div id="orgs">
      <a href="http://www.doc.gov/">U.S. Department of Commerce</a> | <a href="http://www.noaa.gov/">National Oceanic and Atmospheric Administration</a>
      <br>
      <a href="http://www.esrl.noaa.gov">Earth System Research Laboratory</a>
       | <a href="/psd/">Physical Sciences Division</a>

       <br>
       <span class="url"><a href="/psd/about/contacts.html">http://www.esrl.noaa.gov/psd/about/contacts.html</a></span>
    </div>

    <div id="media_icons">
      <a href="https://www.facebook.com/NOAAESRL" title="ESRL Facebook"><i class="fa fa-2x fa-facebook"></i></a>&nbsp;
      <a href="https://twitter.com/NOAA_ESRL" title="ESRL Twitter"> <i class="fa fa-2x fa-twitter"></i></a>&nbsp;
      <a href="https://www.youtube.com/user/NOAAESRL" title="ESRL Youtube Channel"> <i class="fa fa-2x fa-youtube"></i></a>&nbsp;
      <a href="https://www.flickr.com/photos/noaa_esrl" title="ESRL Flickr"> <i class="fa fa-2x fa-flickr"></i></a>
    </div>

    <div id="policies">
      <a href="http://www.noaa.gov/privacy.html">Privacy Policy</a> |
      <a href="http://www.esrl.noaa.gov/about/accessibility.html">Accessibility</a> |
      <a href="/psd/disclaimer/">Disclaimer</a> |

      <a href="http://www.usa.gov/">USA.gov</a>
      <br />
      <a href="/psd/about/contacts.html">Contact Us</a>

      | <a href="mailto:webmaster.psd&#64;noaa.gov">Webmaster</a>

      | <a href="/psd/survey/">Take Our Survey</a>
      <br />
      <a href="/psd/site_index.html">Site Index</a>
    </div>

  </div> <!-- end footer -->
  </td>
</tr> 

</table>

  </body>
</html>
