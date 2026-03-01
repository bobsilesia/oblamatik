<?php
function is_tlc()
{
	if(file_exists('/tmp/TLC-Info.cfg'))
		return(1);
	else
		return(0);
}

function get_active_int()
{
	$interfaces[]['name'] = "eth1";
	$interfaces[]['name'] = "wlan0";
	$interfaces[]['name'] = "br-lan";

	for($i = 0; $i < 3; $i++)
	{
		exec("/sbin/ifconfig " . $interfaces[$i]['name'], $eth);
		$eth = explode(' ', $eth[1]);

		$array = array();
		for($j = 0; $j < sizeof($eth); $j++)
		{
			if($eth[$j])
				$array[] = $eth[$j];
		}
		if($array[0] == 'inet')
		{
			// We found an ip address
			$tmp = explode(':', $array[1]);
			$interfaces[$i]['ip'] = $tmp[1];
		}
		else
			$interfaces[$i]['ip'] = '';
		unset($eth);
	}
	for($i = 0; $i < 3; $i++)
	{
		if($interfaces[$i]['ip'])
		{
			return($interfaces[$i]['name']);
			break;
		}
	}

}

function read_mac_wlan()
{
	exec("/sbin/ifconfig wlan0", $output);

	$mac = preg_replace("/^wlan0.*HWaddr/", "", $output[0]);

	return($mac);
}

function get_local_ip()
{
	$interfaces[]['name'] = "eth1";
	$interfaces[]['name'] = "wlan0";
	$interfaces[]['name'] = "br-lan";

	for($i = 0; $i < 3; $i++)
	{
		exec("/sbin/ifconfig " . $interfaces[$i]['name'], $eth);
		$eth = explode(' ', $eth[1]);

		$array = array();
		for($j = 0; $j < sizeof($eth); $j++)
		{
			if($eth[$j])
				$array[] = $eth[$j];
		}
		if($array[0] == 'inet')
		{
			// We found an ip address
			$tmp = explode(':', $array[1]);
			$interfaces[$i]['ip'] = $tmp[1];
		}
		else
			$interfaces[$i]['ip'] = '';
		unset($eth);
	}
	for($i = 0; $i < 3; $i++)
	{
		if($interfaces[$i]['ip'])
		{
			echo $interfaces[$i]['ip'];
			break;
		}
	}
}

function get_local_ip2()
{
	$interfaces[]['name'] = "eth1";
	$interfaces[]['name'] = "wlan0";
	$interfaces[]['name'] = "br-lan";
	$local = "";

	for($i = 0; $i < 3; $i++)
	{
		exec("/sbin/ifconfig " . $interfaces[$i]['name'], $eth);
		$eth = explode(' ', $eth[1]);

		$array = array();
		for($j = 0; $j < sizeof($eth); $j++)
		{
			if($eth[$j])
				$array[] = $eth[$j];
		}
		if($array[0] == 'inet')
		{
			// We found an ip address
			$tmp = explode(':', $array[1]);
			$interfaces[$i]['ip'] = $tmp[1];
		}
		else
			$interfaces[$i]['ip'] = '';
		unset($eth);
	}
	for($i = 0; $i < 3; $i++)
	{
		if($interfaces[$i]['ip'])
		{
			$local = $interfaces[$i]['ip'];
			break;
		}
	}
	return($local);
}

function open_valve($valve)
{
	if(is_tlc())
		return;

	set_valve($valve);
}

function get_type()
{
	if(file_exists('/tmp/TLC-Info.cfg'))
	{
		$info = file("/tmp/TLC-Info.cfg");
		foreach($info as $line)
		{
			if(preg_match("/type/", $line))
			{
				$tmp = explode(" = ", $line);
				$type = str_replace(';', '', $tmp[1]);
				return(trim($type));
			}
		}
	}
	else
	{
		$type = read_eeprom(1) & 7;
	}
	return($type);
}

function get_model()
{
        if(file_exists('/tmp/TLC-Info.cfg'))      
        {                                         
                $info = file("/tmp/TLC-Info.cfg");
                foreach($info as $line)                
                {                                      
                        if(preg_match("/type_string/", $line))      
                        {                                             
                                $tmp = explode(" = ", $line);         
                                $model = str_replace(';', '', $tmp[1]);
				$model = str_replace('"', '', $model);
                                return(trim($model));                  
                        }                                             
                }                                                     
        }                                                             
        else                                                          
        {                                                             
                $model = "TLC";
        }                                                             
        return($model);                                                
}

function get_required()
{
	$required['temp'] = 0;
	$required['flow'] = 0;

	if(file_exists('/tmp/TLC-Info.cfg'))
	{
		$info = file("/tmp/TLC-Info.cfg");
		foreach($info as $line)
		{
			if(preg_match("/required_temp/", $line))
			{
				$tmp = explode(" = ", $line);
				$required['temp'] = trim(str_replace(';', '', $tmp[1])) / 10;
			}
			if(preg_match("/required_flow/", $line))
			{
				$tmp = explode(" = ", $line);
				$required['flow'] = trim(str_replace(';', '', $tmp[1])) / 100;
			}
		}
	}
	return($required);
}

function read_mac()
{
	exec("/sbin/ifconfig wlan0", $output);

	$mac = preg_replace("/^wlan0.*HWaddr/", "", $output[0]);
	$mac = trim(str_replace(":", "-", $mac));

	return($mac);
}

function has_popup()
{
	if(file_exists('/tmp/TLC-Info.cfg'))
	{
		$info = file("/tmp/TLC-Info.cfg");
		foreach($info as $line)
		{
			if(preg_match("/popup/", $line))
			{
				if(preg_match("/true/", $line))
					return true;
				else
					return false;
			}
		}
	}
	else
	{
		$popup = read_eeprom(0);
		if($popup & 16)
			return true;
		else
			return false;
	}
}

function has_sensor()
{
        if(file_exists('/tmp/TLC-Info.cfg'))                    
        {                                                       
                $info = file("/tmp/TLC-Info.cfg");              
                foreach($info as $line)                         
                {                                               
                        if(preg_match("/temp_sensor/", $line))        
                        {                                       
                                if(preg_match("/true/", $line))
                                        return true;           
                                else                           
                                        return false;          
                        }                                      
                }                                              
        }                                                      
	return(false);
}

function read_version()
{
	$command = "Zb";
	$out = read_command($command, 2);

	$d1 = ord($out[0]) - 48;
	$d2 = ord($out[1]) - 48;

	$tmp = number_format((($d1 * 16) + $d2) / 10, 1);
	$iot = trim(file_get_contents('/www/inc/version.txt'));
	$version = $tmp . '-' . $iot;
	return $version;
}

function get_url($url)
{
	$ch = curl_init(); 
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_PORT, 443);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
	$output = curl_exec($ch); 
	curl_close($ch);
	return(trim($output));
}

function get_name()
{
	$command = "r";
	$out = read_command($command, 1);
	
	return (html_entity_decode($out));
}

function set_name($name)
{
	$name = htmlentities($name);
	$command = 'q"' . $name . '",';
	$out = write_command($command, 1);

	return $out;
}

function set_watchdog($time)
{
	$time *= 10;
	$time_h = intval($time / 16);
	$time_l = $time % 16;
	
	$command = "u" . chr($time_h + 48) . chr($time_l + 48) . ",";
	$out = write_command($command, 1);

	return $out;
}

function set_position($position)
{
	$command = "c" . $position . ",";
	$out = write_command($command, 1);

	return $out;
}

function set_warmup($temperature)
{
	open_valve(1, $address);

	$temp = intval(10 * $temperature);
	
	$c1 = intval($temp / 256);
	$c2 = intval(($temp % 256) / 16);
	$c3 = $temp - ($c1 * 256) - ($c2 * 16);

	$hextemp = chr($c1 + 48) . chr($c2 + 48) . chr($c3 + 48);

	$command = "l" . $hextemp . ",";
	$out = write_command($command, 1);

	return $out;
}

function set_color($r, $g, $b)
{
	$command = "m" . $r . "," . $g . "," . $b . ",";
	$out = write_command($command, 1);

	return $out;
}

function set_desinfect()
{
	open_valve(1, $address);

	$command = "n";
	$out = write_command($command, 1);

	return $out;
}

function set_temp($temperature)
{
	$temp = intval(10 * $temperature);
	
	$c1 = intval($temp / 256);
	$c2 = intval(($temp % 256) / 16);
	$c3 = $temp - ($c1 * 256) - ($c2 * 16);

	$hextemp = chr($c1 + 48) . chr($c2 + 48) . chr($c3 + 48);

	$command = "b" . $hextemp . ",";
	$out = write_command($command, 1);

	return $out;
}

function set_popup($position)
{
	$command = "f" . $position . ",";
	$out = write_command($command, 1);

	return $out;
}

function get_popup()
{
	$command = "g" . $position . ",";
	$out = read_command($command, 1);

	return intval($out);
}

function set_valve($valves)
{
	$valves = chr($valves + 48);
	$command = "h" . $valves . ",";
	$out = write_command($command, 1);

	return $out;
}

function get_temp_unit()
{
	if(file_exists("/tmp/TLC-Info.cfg"))
	{
 		$info = file("/etc/TLC-Config.cfg");                       
		foreach($info as $line)                                  
		{                                                        
			if(preg_match("/temperature_unit/", $line))
			{
				$tmp = explode(" = ", $line);
				$unit = trim(str_replace(';', '', $tmp[1]));
			}
		}
	}
	return($unit);
}

function set_temp_unit($unit)
{
	$command = "E" . $unit . ",";
	$out = write_command($command, 1);

	return $out;
}

function set_quick($number)
{
	open_valve(1, $address);

	$command = "a" . $number . ",";
	$out = write_command($command, 1);

	return $out;
}

function get_quick($number)
{
	if(file_exists("/tmp/TLC-Info.cfg"))
	{
		// Initiate that the TLC-Info.cfg is written with new values
		$command = "D";
		$out = read_command($command, 1);

                $info = file("/tmp/TLC-Info.cfg");                       
                foreach($info as $line)                                  
                {                                                        
			if(preg_match("/QA" . $number . "-temp/", $line))
			{
				$tmp = explode(" = ", $line);
				$temp = str_replace(';', '', $tmp[1]);
				$quick['temp'] = trim($temp);
			}
                        if(preg_match("/QA" . $number . "-flow/", $line))
                        {                                                                                                                                        
                                $tmp = explode(" = ", $line);                                                                                                    
                                $flow = str_replace(';', '', $tmp[1]);                                                                                           
                                $quick['flow'] = trim($flow);                                                                                                   
                        }                                                                                                                                        
                        if(preg_match("/QA" . $number . "-amount/", $line))
                        {                                                                                                                                        
                                $tmp = explode(" = ", $line);                                                                                                    
                                $amount = str_replace(';', '', $tmp[1]);                                                                                           
                                $quick['amount'] = trim($amount);                                                                                                   
                        }                                                                                                                                        
		}
	}
	else
	{
		$qa_h = read_eeprom(214 + (($number - 1) * 2), $address);
		$qa_l = read_eeprom(215 + (($number - 1) * 2), $address);
		$quick['temp'] = $qa_h * 256 + $qa_l;
		$quick['flow'] = 0;
		$quick['amount'] = 0;
	}
	return $quick;
}

function set_hygiene($time, $int)
{
	$d1 = intval($int / 4096);
	$d2 = intval(($int - ($d1 * 4096)) / 256);
	$d3 = intval(($int - ($d1 * 4096) - ($d2 * 256)) / 16);
	$d4 = $int % 16;

	$int = chr($d1 + 48) . chr($d2 + 48) . chr($d3 + 48) . chr($d4 + 48);

	$d1 = intval($time / 4096);
	$d2 = intval(($time - ($d1 * 4096)) / 256);
	$d3 = intval(($time - ($d1 * 4096) - ($d2 * 256)) / 16);
	$d4 = $time % 16;

	$time = chr($d1 + 48) . chr($d2 + 48) . chr($d3 + 48) . chr($d4 + 48);

	$command = "C" . $time . "," . $int . ",";
	$out = write_command($command, 1);
	return($out);
}

function set_measure($amount)
{
	$amount = $amount * 10;
	$d1 = intval($amount / 4096);
	$d2 = intval(($amount - ($d1 * 4096)) / 256);
	$d3 = intval(($amount - ($d1 * 4096) - ($d2 * 256)) / 16);
	$d4 = $amount % 16;

	$volume = chr($d1 + 48) . chr($d2 + 48) . chr($d3 + 48) . chr($d4 + 48);

	$command = "o" . $volume . ",";
	$out = write_command($command, 1);
	return($out);
}

function set_bath($amount, $temp)
{
	open_valve(1, $address);

	$amount = $amount * 10;                     
	$d1 = intval($amount / 4096);               
	$d2 = intval(($amount - ($d1 * 4096)) / 256);
	$d3 = intval(($amount - ($d1 * 4096) - ($d2 * 256)) / 16);
	$d4 = $amount % 16;                                       
                                                                  
	$volume = chr($d1 + 48) . chr($d2 + 48) . chr($d3 + 48) . chr($d4 + 48);

	$temp = intval(10 * $temp);                                      
                                                                                
	$c1 = intval($temp / 256);                                              
	$c2 = intval(($temp % 256) / 16);                                       
	$c3 = $temp - ($c1 * 256) - ($c2 * 16);                                 
                                                                                
	$temperature = chr($c1 + 48) . chr($c2 + 48) . chr($c3 + 48);               

	$command = "k" . $volume . "," . $temperature . ",";
	$out = write_command($command, 1);
	return($out);
}

function read_serial()
{
	$command = "Zd";
	
	$serial = read_command($command, 2);
	return($serial);
}

function get_temp()
{
	$command = "d";
	$out = read_command($command, 1);

	$d1 = ord($out[0]) - 48;
	$d2 = ord($out[1]) - 48;
	$d3 = ord($out[2]) - 48;
	
	$temp = intval(($d1 * 256) + ($d2 * 16) + $d3) / 10;

	return($temp);
}

function get_flow()
{
	$command = "e";
	$out = read_command($command, 1);

	$d1 = ord($out[0]) - 48;
	$d2 = ord($out[1]) - 48;
	$d3 = ord($out[2]) - 48;
	$d4 = ord($out[3]) - 48;
	
	$flow = intval(($d1 * 4096) + ($d2 * 256) + ($d3 * 16) + $d4) / 10;
	return($flow);
}

function set_flow($flow)
{
	$flow = intval(100 * $flow);
	
	$flow_h = intval($flow / 16);
	$flow_l = $flow % 16;
	
	$command = "p" . chr($flow_h + 48) . chr($flow_l + 48) . ",";
	$out = write_command($command, 1);

	return($out);
}

function get_state()
{
	$command = "s";
	$out = read_command($command, 1);

	$tmp = explode(',', $out);
	$state['state'] = $tmp[0];

	switch(sizeof($tmp))
	{
		case 1:
			$state['state'] = $tmp[0];
			$state['progress'] = 0;
			$state['set'] = 0;
			break;
		case 2:
			if(strlen($tmp[1]) == 3)
			{
				$d1 = ord($tmp[1][0]) - 48;
				$d2 = ord($tmp[1][1]) - 48;
				$d3 = ord($tmp[1][2]) - 48;
				$state['set'] = intval(($d1 * 256) + ($d2 * 16) + $d3) / 10;
				$state['progress'] = 0;
			}
			else
			{
				$d1 = ord($tmp[1][0]) - 48;
				$d2 = ord($tmp[1][1]) - 48;
				$state['progress'] = intval(($d1 * 16) + $d2) / 100;
				$state['set'] = 0;
			}
			break;
		case 3:
                        if(strlen($tmp[1]) == 3)    
                        {                          
                                $d1 = ord($tmp[1][0]) - 48;
                                $d2 = ord($tmp[1][1]) - 48;
                                $d3 = ord($tmp[1][2]) - 48;
                                $state['set'] = intval(($d1 * 256) + ($d2 * 16) + $d3) / 10;
                                $state['progress'] = 0;                                     
                        }                                                                   
                        else                                                                
                        {                                                                   
                                $d1 = ord($tmp[1][0]) - 48;                                 
                                $d2 = ord($tmp[1][1]) - 48;                                 
                                $state['progress'] = intval(($d1 * 16) + $d2) / 100;         
                                $state['set'] = 0;                                          
                        }                                                                   
                        if(strlen($tmp[2]) == 3)    
                        {                          
                                $d1 = ord($tmp[2][0]) - 48;
                                $d2 = ord($tmp[2][1]) - 48;
                                $d3 = ord($tmp[2][2]) - 48;
                                $state['set'] = intval(($d1 * 256) + ($d2 * 16) + $d3) / 10;
                                $state['progress'] = 0;                                     
                        }                                                                   
                        else                                                                
                        {                                                                   
                                $d1 = ord($tmp[2][0]) - 48;                                 
                                $d2 = ord($tmp[2][1]) - 48;                                 
                                $state['progress'] = intval(($d1 * 16) + $d2) / 100;         
                                $state['set'] = 0;                                          
                        }                                                                   

	}
	return($state);
}

function get_errors()
{
	$command = "z";
	$out = read_command($command, 1);

	return($out);
}

function read_eeprom($addr)
{
	$a1 = intval($addr / 16);
	$a2 = $addr % 16;
	$addr = chr($a1 + 48) . chr($a2 + 48);

	$command = "i" . $addr . ",";
	$out = read_command($command, 1);

	$d1 = ord($out[0]) - 48;
	$d2 = ord($out[1]) - 48;
	$value = ($d1 * 16) + $d2;
	return($value);
}

function write_eeprom($addr, $data)
{
	$a1 = intval($addr / 16);
	$a2 = $addr % 16;
	$d1 = intval($data / 16);
	$d2 = $data % 16;

	$eeaddr = chr($a1 + 48) . chr($a2 + 48);
	$eedata = chr($d1 + 48) . chr($d2 + 48);

	$command = "j" . $eeaddr . "," . $eedata . ",";
	$out = write_command($command, 1);
	return($out);
}

function set_stop()
{
	$command = "t";
	$out = write_command($command, 1);

	return($out);
}

function set_reset()
{
	$command = "Zc";
	$out = write_command($command, 2);

	return($out);
}

function get_stats()
{
	$command = "w";
	$out = read_command($command, 1);

	return($out);
}

function get_id()
{
	$command = "Za";
	$out = read_command($command, 2);

	return($out);
}

function read_command($command, $len)
{
	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	$out = "";

	$crc = crc16('F' . $command);

	if ($socket === false)
		return(0);

	$flag = pack("C2", 0x80, 0x46);
	$stop = pack("C1", 0x0D);
	$payload = $flag . $command . $crc . $stop;

	$service_port = "2001";

	$result = socket_connect($socket, '127.0.0.1', $service_port);
	if ($result === false)
		return(0);

	socket_write($socket, $payload, strlen($payload));
	$out = socket_read($socket, 2048, PHP_NORMAL_READ);

	// Did we get a function update?
	if($out[2] == 'y')
		$out = socket_read($socket, 2048, PHP_NORMAL_READ);
	socket_close($socket);
	
	// extract returned data and crc
	$crc = substr($out, strlen($out) - 5, 4);
	$data = substr($out, 1, strlen($out) - 6);
	
	$check = crc16($data);
	
	if($crc == $check)
	{
		$out = substr($data, $len + 1, strlen($data) - $len - 2);
		$out = str_replace('"', '', $out);
	}
	else
		$out = 0;

	return($out);
}

function write_command($command)
{
	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	$out = "";

	$crc = crc16('F' . $command);

	if ($socket === false)
		return(0);

	$flag = pack("C2", 0x80, 0x46);
	$stop = pack("C1", 0x0D);
	$payload = $flag . $command . $crc . $stop;

	$service_port = "2001";

	$result = socket_connect($socket, '127.0.0.1', $service_port);
	if ($result === false)
		return(0);

	socket_write($socket, $payload, strlen($payload));
	$out = socket_read($socket, 2048, PHP_NORMAL_READ);

	// Did we get a function update?
	if($out[2] == 'y')
		$out = socket_read($socket, 2048, PHP_NORMAL_READ);

	socket_close($socket);

	return($out);
}

function crc16($data)
{
	$crc = 0xFFFF;
	for ($i = 0; $i < strlen($data); $i++)
	{
		$x = (($crc >> 8) ^ ord($data[$i])) & 0xFF;
		$x ^= $x >> 4;
		$crc = (($crc << 8) ^ ($x << 12) ^ ($x << 5) ^ $x) & 0xFFFF;
	}

	$hex = sprintf('%04x', $crc);
	
//	echo $crc . " : " . $hex . "\n";
	
	for($i = 0; $i < 4; $i++)
	{
		if(ord($hex[$i]) > 57)
			$hex[$i] = chr(ord($hex[$i]) - 39);
	}
	return $hex;
 }

function logtofile($log)
{
	if(0)
	{
		$timestamp = time();
		$time = date("H:i:s",$timestamp) . "\n";
		file_put_contents("/var/log/lighttpd/debug.txt", $time, FILE_APPEND);
		file_put_contents("/var/log/lighttpd/debug.txt", $log, FILE_APPEND);
	}
}

function check_input($type, $value, $min, $max)
{
	switch($type)
	{
		case "num":
			if((is_numeric($value) && $value >= $min) && ($value <= $max))
				return 1;
			else
				return 0;
			break;
	}
}

function check_token()
{
	if($_SERVER['REMOTE_ADDR'] == '127.0.0.1')
		return(1);
	else
		return(1);

//	$token = file_get_contents("/var/log/lighttpd/" . $_SERVER['REMOTE_ADDR']);
//	$headers = getallheaders();
//	$received = $headers['X-Xsrf-Token'];

//	if($token == $received)
//		return(1);
//	else
//		return(0);
}

function switch_to_sta()
{
	// Switch BR-LAN address to 1.1.1.1
	$network = file_get_contents("/www/config/network");
	file_put_contents("/etc/config/network", $network);
}

function switch_to_ap()
{
	// Switch BR-LAN address to 192.168.1.1
	$network = file_get_contents("/www/config/network.wlan");
	file_put_contents("/etc/config/network", $network);
}

function check_iot($path)
{
	// Check if all files are extracted from firmware.bin archive
	if(file_exists("/tmp/" . $path . "/iot.bin") && file_exists("/tmp/" . $path . "/iot.bin.asc") && file_exists("/tmp/" . $path . "/iot.ver") && file_exists("/tmp/" . $path . "/iot.ver.asc"))
	{
		exec("/usr/bin/sudo /usr/bin/gpg --verify /tmp/" . $path . "/iot.bin.asc", $out, $return);
		if($return)
		{
			$array['status'] = 901;
			$array['duration'] = 0;
			$array['version'] = 0;
			return($array);
		}
		else
		{
			// Check version file
			exec("/usr/bin/sudo /usr/bin/gpg --verify /tmp/" . $path . "/iot.ver.asc", $out, $return);
			if($return)
			{
				$array['status'] = 902;
				$array['duration'] = 0;
				$array['version'] = 0;
				return($array);
			}
			else
			{
				$array['status'] = 200;
				$array['duration'] = 300;
				$array['version'] = trim(file_get_contents("/tmp/" . $path . "/iot.ver"));
				return($array);
			}
		}
	}
	else
	{
		$array['status'] = 900;
		$array['duration'] = 0;
		$array['version'] = 0;
		return($array);
	}
}

function post_log($event, $message)
{
	if(0)
	{
		$info = json_decode(file_get_contents("/www/inc/info.txt"));
		$data = array();
		$data['iot'] = $info->serial_number_iot;
		$data['base'] = $info->serial_number;
		$data['data'] = $message;
		$data['event'] = $event;
		$data['ip'] = $_SERVER['REMOTE_ADDR'];
	
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, "http://iot.oblamatik.net/api/" . $url);
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
		curl_setopt($ch, CURLOPT_HTTPHEADER, array('Expect:  '));
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		
		$server_output = curl_exec ($ch);
		curl_close ($ch);
		return($server_output);
	}
}
?>
