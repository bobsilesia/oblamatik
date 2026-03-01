<?php
	$command = explode('/', $_GET['url']);
	
	$out = print_r($command, true);
	file_put_contents("/tmp/get.txt", $out);

	if($command[0])
	{
		if($command[0] == 'authenticate')
		{
			include("/www/inc/" . $command[0] . ".php");
		}
		else
		{
			$size = sizeof($command);
			include("/www/inc/functions.php");
			include("/www/inc/" . $command[0] . ".php");
		}
	}
?>
