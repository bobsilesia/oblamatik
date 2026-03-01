<?php
	$data = $_POST;

	$post = print_r($data, true);
	file_put_contents($logdir . "wlanpost_disconnect.txt", $post);

	file_put_contents("/var/log/lighttpd/headers.txt", print_r(getallheaders(), true));
	if(!check_token())
		exit;

	$str = file_get_contents('/www/config/wireless_ap');
	
	exec('/usr/bin/sudo /usr/sbin/fw_printenv serialnum', $iot);
	$serialiot = explode("=", $iot[0]);
	$serialiot = trim($serialiot[1]);
	if(!$serialiot)
		$serialiot = 'none';

	echo $serialiot . "\n";

	exec('/usr/bin/sudo /usr/sbin/fw_printenv passwd', $result);
	$key = explode('=', $result[0]);

	if(strlen($key[1]) > 7)
		$wlankey = $key[1];
	else
		$wlankey = "12341234";

	$str = str_replace("SSID", "crosswater-" . $serialiot, $str);
	$str = str_replace("KEY", $wlankey, $str);
	file_put_contents('/etc/config/wireless', $str);

	if(file_exists("/etc/config/wireless.old"))
		exec('/bin/rm /etc/config/wireless.old');
	switch_to_ap();
	exec('/usr/bin/sudo /etc/init.d/network restart');
?>
