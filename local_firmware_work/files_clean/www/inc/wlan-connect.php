<?php
	$data = $_POST;

	file_put_contents("/var/log/lighttpd/headers.txt", print_r(getallheaders(), true));
//	if(!check_token())
//		exit;

	$post = print_r($data, true);
	file_put_contents($logdir . "wlanpost.txt", $post);
	
	$str = file_get_contents('/www/config/wireless_sta');
	
	$str = str_replace('SSID', "'" . $data['name'] . "'", $str);
	$str = str_replace('KEY', $data['password'], $str);

	file_put_contents('/etc/config/wireless', $str);
	if(file_exists("/etc/config/wireless.old"))
		exec("/bin/rm /etc/config/wireless.old");

	switch_to_sta();

	exec('/usr/bin/sudo /etc/init.d/network restart');

	$status = "FAILED";
	for($i = 0; $i < 12; $i++)
	{
		exec("/usr/bin/sudo /usr/sbin/wpa_cli status", $output, $return);
//		print_r($output);
		foreach($output as $line)
		{
			if(preg_match("/^wpa_state/", $line))
			{
				$state = explode("=", $line);
				if($state[1] == "COMPLETED")
					$status = "CONNECTED";
				else
					$status = "FAILED";
			}
		}
		sleep(1);
		$output = array();
	}
	$array['status'] = $status;
	$array['message'] = "Unsuccessful";
	echo json_encode($array);

?>
