<?php
	$data = $_POST;

	$out = print_r($data, true);
	$out .= print_r($_FILES, true);

	$uploaddir = '/tmp/';
	$uploadfile = $uploaddir . basename($_FILES['file']['name']);

	move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile);

	$array['status'] = "900";
	$array['duration'] = 0;
	
	$info = json_decode(file_get_contents("/www/inc/info.txt"));
	$versions = explode('-', $info->version);
	$base_version = $versions[0];
	$iot_version = $versions[1];

	// Now the file is uploaded into /tmp directory

	if(file_exists('/tmp/firmware.bin'))
	{
		// Extract firmware image and signature from firmware.bin file
		exec("/bin/dd if=/tmp/firmware.bin of=/tmp/firmware.asc count=819 bs=1");
		exec("/bin/dd skip=1 bs=1024 if=/tmp/firmware.bin of=/tmp/firmware");
		exec("/bin/rm /tmp/firmware.bin");

		// Verify signature
		exec("/usr/bin/sudo /usr/bin/gpg --verify /tmp/firmware.asc", $out, $return);
		file_put_contents("/var/log/lighttpd/gpg.txt", $out);
		file_put_contents("/var/log/lighttpd/gpg.txt", $return, FILE_APPEND);
		if($return)
		{
			file_put_contents("/var/log/lighttpd/gpg.txt", "\nGnuPG signature wrong for firmware.bin!!!\n", FILE_APPEND);
			$array['status'] = "901";
			echo json_encode($array);
			post_log('update', 'GnuPG signature wrong for firmware.bin');
			exec("/bin/rm /tmp/firmware*");
			exit;
		}
		else
		{
			$path = md5(uniqid());
			exec("/bin/mkdir /tmp/" . $path);
			exec('/bin/tar xvf /tmp/firmware -C /tmp/' . $path);
			exec("/bin/rm /tmp/firmware*");
			post_log('update', 'extracting into directory "/tmp/' . $path . '"');
		}

		// Check now if we have a valid software image for the iot module
		$iot = check_iot($path);
		if($iot['status'] != 200)
		{
			post_log('update', 'iot module software verification failed');
			$array['status'] = 901;
			$array['duration'] = 0;
			echo json_encode($array);
			exec("/bin/rm -rf /tmp/" . $path);
			exit;
		}
		else
		{
			post_log('update', 'iot module software verified successfully');
			$array['status'] = 200;
			if($iot['version'] > $iot_version)
				$array['duration'] += 300;
			else
				post_log('update', 'iot module software will not be updated');
		}

		// Start now any upgrade process through AT command
		exec('/bin/date +"%H:%M"', $result);
		$time = trim($result[0]) . ':55';
		exec("/usr/bin/sudo /bin/date -s " . $time);
		exec('/bin/echo "/usr/bin/php-cli /www/inc/update.php ' . $path . '" | /usr/bin/sudo /usr/bin/at now + 1 min');
		exec ("/usr/bin/sudo /usr/bin/atq", $out);
		post_log('update', 'Scheduling update in directory ' . $path);

		echo json_encode($array);
	}
	else
	{
		exec("/bin/rm " . $uploadfile);
		echo json_encode($array);
	}
?>
