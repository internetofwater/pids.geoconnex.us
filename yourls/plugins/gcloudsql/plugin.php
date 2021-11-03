<?php
/*
Plugin Name: gcloudsql
Plugin URI: https://github.com/webb-ben/pids.geoconnex.us/yourls
Description: Attempts to remove decode a socket. Because class-msyql.php eats the gcloud connection.
Version: 1.0
Author: Ben Webb
*/

// No direct call
if( !defined( 'YOURLS_ABSPATH' ) ) die();

// Remove extension from keyword during sanitazation
yourls_add_filter('db_connect_custom_dsn', 'decode_db_host');
function decode_db_host( $dsn ) {
	return urldecode( $dsn );
}
