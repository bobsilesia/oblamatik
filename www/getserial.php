<?php

	include("/www/inc/functions.php");

	sleep(15);

	exec('/usr/sbin/fw_printenv serialnum', $iot);
	$serialiot = explode("=", $iot[0]);
	$serialiot = trim($serialiot[1]);
	if(!$serialiot)
		$serialiot = 'none';

	$avahi = file_get_contents("/www/config/http.service");
	$version = trim(file_get_contents("/www/inc/version.txt"));
	$avahi = str_replace("%h", "crosswater-" . $serialiot, $avahi);
	$avahi = str_replace("%v", $version, $avahi);
	file_put_contents("/etc/avahi/services/http.service", $avahi);
	$avahi = file_get_contents("/www/config/https.service");
	$avahi = str_replace("%h", "crosswater-" . $serialiot, $avahi);
	$avahi = str_replace("%v", $version, $avahi);
	file_put_contents("/etc/avahi/services/https.service", $avahi);

	if(!file_exists("/www/config/server.pem"))
	{
		exec('/bin/echo "Generating web server certificate" > /dev/ttyATH0');
		// Generate lighttpd server certificate and key
		exec("/usr/bin/openssl genrsa -des3 -passout pass:" . $serialiot . " -out /tmp/server.pass.key 2048");
		exec("/usr/bin/openssl rsa -passin pass:" . $serialiot . " -in /tmp/server.pass.key -out /tmp/server.key");
		exec("/bin/rm /tmp/server.pass.key");
		exec('/usr/bin/openssl req -new -key /tmp/server.key -out /tmp/server.csr -sha256 -subj "/C=CH/ST=Graubuenden/L=Chur/O=Oblamatik AG/OU=Development/CN=oblamatik.ch"');
		exec("/usr/bin/openssl x509 -req -days 3650 -in /tmp/server.csr -signkey /tmp/server.key -out /tmp/server.crt");
		exec("/bin/cat /tmp/server.key /tmp/server.crt > /www/config/server.pem");
	}
	exec('/bin/echo "Done" > /dev/ttyATH0');
	$str = file_get_contents('/etc/config/wireless');

	if(preg_match('/wwan/', $str))
	{
		// It is configured as WLAN client
		exec('/bin/echo "Configured as WLAN client" > /dev/ttyATH0');
		echo "Configured as WLAN CLient...\n";
		file_put_contents('/etc/config/wireless', $str);

//		Try several times to read the serial number during startup
		file_put_contents('/tmp/serial.txt', "Serial Read from Basestation:\n");
		for($i = 0; $i < 5; $i++)
		{
			$serial = read_serial();
			file_put_contents('/tmp/serial.txt', "Try " . ($i + 1) . " of 5, Serial: " . $serial . "\n", FILE_APPEND);
			if((strlen($serial) > 0) && ($serial != 0))
				break;
			sleep(2);
			$serial = 'none';
		}
		if(strlen($serial) < 2)
			$serial = 'none';

		// Now try to see if we have a TLC instead of TLC-Temp
		if(($serial == '0') || ($serial == 'none'))
		{
			exec('/bin/rm /tmp/TLC-Info.cfg');
			exec('/usr/bin/killall tlc-iot');
			exec('/usr/bin/killall ser2net');
			sleep(2);
			file_put_contents("/tmp/startup.txt", "Starting tlc-iot...\n");
			exec('/usr/bin/tlc-iot -p /dev/ttyATH0 > /var/log/tlc-iot.log &');
			file_put_contents("/tmp/startup.txt", "tlc-iot started...\n", FILE_APPEND);
			$tlc = 0;
			for($i = 0; $i < 40; $i++)
			{
				// Check for 20 seconds if the /tmp/TLC-Info.cfg file is created
				file_put_contents("/tmp/startup.txt", "Looking for TLC-Info.cfg, try: " . ($i + 1) . "\n", FILE_APPEND);
				if(file_exists('/tmp/TLC-Info.cfg'))
				{
					sleep(5);
					file_put_contents("/tmp/startup.txt", "Found...\n", FILE_APPEND);
					$tlc = 1;
					$tlc_config = file('/tmp/TLC-Info.cfg');
					foreach($tlc_config as $tlc_line)
					{
						if(preg_match("/serial_num/", $tlc_line))
						{
							$tmp = explode(" = ", $tlc_line);
							$serial = str_replace(';', '', $tmp[1]);
							$serial = str_replace('"', '', $serial);
						}
						if(preg_match("/pty/", $tlc_line))
						{
							$tmp = explode(" = ", $tlc_line);
							$port = str_replace(';', '', $tmp[1]);
							$port = str_replace('"', '', $port);
						}
					}
					file_put_contents("/etc/ser2net.conf", "127.0.0.1,2001:raw:1:" . trim($port) . ":9600 NONE 1STOPBIT 8DATABITS LOCAL -RTSCTS\n");
					exec("/usr/sbin/ser2net -c /etc/ser2net.conf");
					print_r($ser);
					print_r($pty);
					break;
				}
				sleep(1);
			}
			if(!file_exists('/tmp/TLC-Info.cfg'))
			{
				exec('/usr/bin/killall tlc-iot');
				exec('/usr/sbin/ser2net');
			}
		}	
	}
	else
	{
		exec('/bin/echo "Configured as WLAN AP" > /dev/ttyATH0');
		// It is configured as WLAN AP
		$str = file_get_contents('/www/config/wireless_ap');

		exec('/usr/sbin/fw_printenv passwd', $result);
		$key = explode('=', $result[0]);

		if(strlen($key[1]) > 7)
			$wlankey = $key[1];
		else
			$wlankey = "12341234";

//		Try several times to read the serial number during startup
		exec('/bin/echo "Trying to read serial from TLC-Temp" > /dev/ttyATH0');
		file_put_contents('/tmp/serial.txt', "Serial Read from Basestation:\n");
		for($i = 0; $i < 5; $i++)
		{
			$serial = read_serial();
			file_put_contents('/tmp/serial.txt', "Try " . ($i + 1) . " of 5, Serial: " . $serial . "\n", FILE_APPEND);
			if((strlen($serial) > 0) && ($serial != 0))
				break;
			sleep(2);
			$serial = 'none';
		}
		if(strlen($serial) < 2)
			$serial = 'none';

		// Now try to see if we have a TLC instead of TLC-Temp
		if(($serial == '0') || ($serial == 'none'))
		{
			exec('/bin/echo "No answer from TLC-Temp, trying TLC now" > /dev/ttyATH0');
			exec('/bin/rm /tmp/TLC-Info.cfg');
			exec('/usr/bin/killall tlc-iot');
			exec('/usr/bin/killall ser2net');
			sleep(2);
			file_put_contents("/tmp/startup.txt", "Starting tlc-iot...\n");
			exec('/usr/bin/tlc-iot -p /dev/ttyATH0 > /var/log/tlc-iot.log &');
			file_put_contents("/tmp/startup.txt", "tlc-iot started...\n", FILE_APPEND);
			$tlc = 0;
			for($i = 0; $i < 40; $i++)
			{
				// Check for 20 seconds if the /tmp/TLC-Info.cfg file is created
				file_put_contents("/tmp/startup.txt", "Looking for TLC-Info.cfg, try: " . ($i + 1) . "\n", FILE_APPEND);
				if(file_exists('/tmp/TLC-Info.cfg'))
				{
					sleep(5);
					file_put_contents("/tmp/startup.txt", "Found...\n", FILE_APPEND);
					$tlc = 1;
					$tlc_config = file('/tmp/TLC-Info.cfg');
					foreach($tlc_config as $tlc_line)
					{
						if(preg_match("/serial_num/", $tlc_line))
						{
							$tmp = explode(" = ", $tlc_line);
							$serial = str_replace(';', '', $tmp[1]);
							$serial = str_replace('"', '', $serial);
						}
						if(preg_match("/pty/", $tlc_line))
						{
							$tmp = explode(" = ", $tlc_line);
							$port = str_replace(';', '', $tmp[1]);
							$port = str_replace('"', '', $port);
						}
					}
					file_put_contents("/etc/ser2net.conf", "127.0.0.1,2001:raw:1:" . trim($port) . ":9600 NONE 1STOPBIT 8DATABITS LOCAL -RTSCTS\n");
					exec("/usr/sbin/ser2net -c /etc/ser2net.conf");
					print_r($ser);
					print_r($pty);
					break;
				}
				sleep(1);
			}
			if(!file_exists('/tmp/TLC-Info.cfg'))
			{
				exec('/usr/bin/killall tlc-iot');
				exec('/usr/sbin/ser2net');
			}
		}	

		exec('/usr/sbin/fw_printenv serialnum', $iot);
		$serialiot = explode("=", $iot[0]);
		$serialiot = trim($serialiot[1]);
		if(!$serialiot)
			$serialiot = 'none';

		exec('/bin/echo "Configuring WLAN AP SSID" > /dev/ttyATH0');
		$str = str_replace("SSID", "crosswater-" . $serialiot, $str);
		$str = str_replace("KEY", $wlankey, $str);
		file_put_contents('/etc/config/wireless', $str);
		switch_to_ap();
		exec("/etc/init.d/network restart");
	}
?>
