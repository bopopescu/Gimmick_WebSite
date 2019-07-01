<?php
	$username = $_POST['username'];
	$password = $_POST['password'];

	$username = stripcslashes($username);
	$password = stripcslashes($password);
	$username = mysql_real_escape_string($username);
	$password = mysql_real_escape_string($password);

	mysql_connect("localhost", "root", "");
	mysql_select_db("projectchat");

	$result = mysql_query("select * from signup where username = '$username' and password = '$password'") or die("Failed to query database ".mysql_error());
	if ($row['username'] ==$username && $row['password'] == $password) {
		echo "Login success!!! Welcome ".$row['username'];
	}  else {
		echo "Failed to login!";
	}

	?>