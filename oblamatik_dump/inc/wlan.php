<?php
	switch($size)
	{
		case 1:
			get_wlans();
			break;

		case 2:
		case 3:
			include("/www/inc/wlan-" . $command[1] . ".php");
			break;
			
		default:
			get_wlans();
			break;
	}


function get_wlans()
{
	$logdir = ini_get("user_dir");
	exec('/usr/bin/sudo /usr/sbin/iwlist wlan0 scan', $return);
	
	$wlans = array();
	
	$lastname = '';
	$laststrength = 0;

	foreach($return as $value)
	{
		$wlan = ltrim($value);

		if(preg_match('/Quality/', $wlan))
		{
			// We found the SSID name
			$signal = str_replace('Quality=', '', $wlan);
			$signal = explode(' ', $signal);
			$signal = explode('/', $signal[0]);
			$rawsignal = $signal[0];
			$signal = floor(($rawsignal + 17) / 17.5);
//				print_r($signal);
		}

		if(preg_match('/ESSID/', $wlan))
		{
			// We found the SSID name
			$wlan = str_replace('ESSID:', '', $wlan);
			$wlan = str_replace('"', '', $wlan);
//				echo "WLAN: " . $wlan . "\n";
			if(!preg_match('/smart-/', $wlan) && !preg_match('/tlc-/', $wlan) && !preg_match('/crosswater-/', $wlan) && !preg_match('/trio-e-/', $wlan))
				$wlans[] = array('name' => $wlan, 'strength' => $signal, 'rawsignal' => $rawsignal);
		}
	}
	
	$array = $wlans;
	
	usort($array, function($a, $b)
	{
		return $b['rawsignal'] - $a['rawsignal'];
	});

	$out = print_r($array, true);
	post_log('wlanscan', $array);
	file_put_contents($logdir . "wlanscan.txt", $out);
	echo json_encode((object)$array);
}
?>

