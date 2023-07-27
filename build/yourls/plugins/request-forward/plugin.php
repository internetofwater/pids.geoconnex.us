<?php
/*
Plugin Name: Request Forwarder
Plugin URI: https://github.com/webb-ben/plugins/request-forward
Description: Attempts to remove file extensions from the short URL and forwards extension in the long URL.
Version: 1.0
Author: Ben Webb
*/

// No direct call
if( !defined( 'YOURLS_ABSPATH' ) ) die();

// Remove extension from keyword during sanitazation
yourls_add_filter('sanitize_string', 'remove_extension');
function remove_extension( $keyword ) {
    preg_match("/[.][a-zA-Z]*$/i", $keyword, $e);
    if (isset($e[0])){
      return str_replace($e[0], '', $keyword);
    } else {
      return $keyword;
    }
}

// Add extension during redirect
yourls_add_filter('redirect_location', 'extension_forward' );
function extension_forward($long_url) {
    preg_match("/[.][a-zA-Z]*$/i", $_SERVER['REQUEST_URI'], $e);
    if (isset($e[0])){
      return $long_url.$e[0];
    } else {
      return $long_url;
    }
}