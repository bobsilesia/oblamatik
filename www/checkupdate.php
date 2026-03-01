<?php
	include("/www/inc/functions.php");

	if(file_exists("/etc/socket.conf"))
		$server = trim(file_get_contents("/etc/socket.conf"));
	else
	{
		$server = 'stage-oblamatik.impac.ch';
	}

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL,"https://" . $server . "/api/versions/1");
	curl_setopt($ch, CURLOPT_PORT, 443);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 1);
	curl_setopt($ch, CURLOPT_CAINFO, "/etc/certs/ca-bundle.crt");

	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

	$info = curl_exec($ch);
	$error = curl_errno($ch);
	if($error)
	{
		echo "Error nbr.: " . $error . "\n";
		echo "Error: " . curl_error($ch) . "\n";
		curl_close($ch);
		exit;
	}
	curl_close($ch);

	$data = json_decode($info);
	print_r($data->fields);

	$info = json_decode(file_get_contents("/www/inc/info.txt"));
	$local = $info->version;
	$tmp = explode("-", $local);
	$local_iot = $tmp[1];
	$local_base = $tmp[0];
	
	$remote_iot = $data->fields->framework_version;
	$remote_base = $data->fields->basestation_version;
 
	$filesize = $data->fields->file_size;
	if($filesize > 16000000)
	{
		echo "Filesize too large to download...\n";
		exit;
	}

	echo "Local version:  " . $local_base . "-" . $local_iot . "\n";
	echo "Remote version: " . $remote_base . "-" . $remote_iot . "\n";

	$downloaded = "0-0";

	$message = array();
	$message['local'] = $local_base . "-" . $local_iot;
	$message['remote'] = $remote_base . "-" . $remote_iot;
	
	post_log('checkupdate', $message);

	if(($remote_base > $local_base) || ($remote_iot > $local_iot))
	{
		if(file_exists("/tmp/firmware.bin"))
		{
			$md5 = md5_file("/tmp/firmware.bin");
			if($md5 == $data->fields->checksum)
			{
				echo "Already latest version downloaded...\n";
				exit;
			}
		}
		echo "Downloading new firmware version...\n";
		$url = "https://" . $server . $data->fields->download_url;
		exec("/usr/bin/wget -O /tmp/firmware.bin --ca-certificate=/etc/certs/ca-bundle.crt " . $url, $out, $result);

		if(file_exists("/tmp/firmware.bin"))
		{
			$md5 = md5_file("/tmp/firmware.bin");
			if($md5 == $data->fields->checksum)
			{
				echo "Checksum verify okay...\n";
				$downloaded = $data->fields->basestation_version . "-" . $data->fields->framework_version;
				post_log('download', 'Download MD5 okay');
			}
			else
			{
				exec("/bin/rm /tmp/firmware.bin");
			}
		}
	}

	file_put_contents("/tmp/downloaded.txt", $downloaded);

?>
