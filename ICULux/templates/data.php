<?php
	
    if(isset($_SESSION['Name']))
    	echo "Name: ".$_SESSION['Name']."<br>";
    if(isset($_SESSION['Age']))
    	echo "Age: ".$_SESSION['Age']."<br>";
    if(isset($_SESSION['pid']))
    	echo "Patient ID: ".$_SESSION['pid']."<br>";
    if(isset($_SESSION['Gender']))
    	echo "Gender: ".$_SESSION['Gender']."<br>";
    if(isset($_SESSION['DOI']))
    	echo "Date of Arrival".$_SESSION['DOI']."<br>";
    if(isset($_SESSION['Disease']))
    	echo "Disease: ".$_SESSION['Disease']."<br>";
?>