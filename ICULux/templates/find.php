<?php
include 'connection.php';

$pid = "";
$piderr = "";
$name ="";
$age = "";
$doi = "";
$gender = "";
$disease = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
	if (empty($_POST["pid"]))
	{
		$piderr = "Patient ID is required.";
		echo $piderr;
	}
	else{
		$pid = test_input($_POST["pid"]);
		if(!is_numeric($pid))
		{
			$piderr = "Patient ID should be numeric value.";
			echo $piderr;
		}
		else if(strlen($pid) > 3)
		{
			$piderr = "Patient ID should be less than 1000.";
			echo $piderr;
		}
		else{
			$conn = OpenCon();
			if($conn == false)
			{
				echo "Not connected to database.";
				
			}
			$sql = "SELECT * from Patient_Information where `pid`='".$pid."'";
			$result = $conn->query($sql);

			if ($result->num_rows > 0) {
 			
  				while($row = $result->fetch_assoc()) {
  					if(isset($row['Name']))
  						$name = $row['Name'];
  					if(isset($row['Age']))
  						$age = $row['Age'];
  					if(isset($row['DOI']))
  						$doi = $row['DOI'];
  					if(isset($row['Gender']))
  						$gender = $row['Gender'];
  					if(isset($row['Disease']))
  						$disease = $row['Disease'];


  					
  					
    				$_SESSION['Name'] = $name;
    				$_SESSION['Age'] = $age;
    				$_SESSION['DOI'] = $doi;
    				$_SESSION['Gender'] = $gender;
    				$_SESSION['Disease'] = $disease;
    				$_SESSION['pid'] = $pid;
    				
    				header("Location: data.php");
    				die();
  				}
			} 
			else {
  				echo "No results found";
  				
			}
			CloseCon($conn);
			
		}

	}
}
function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

?>