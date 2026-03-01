<?php
	$info = array();
	$info['version'] = read_version();
	$info['serial'] = read_serial();
	$info['name'] = read_base();

	echo json_encode($info);
?>
