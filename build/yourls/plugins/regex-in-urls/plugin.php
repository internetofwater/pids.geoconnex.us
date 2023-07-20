<?php
/*
Plugin Name: Regex Character Matching in Short URLs
Plugin URI: https://github.com/webb-ben/plugins/tree/main/regex-in-urls
Description: Regex characters and metacharacters in Short URLs
Version: 1.1
Author: Ben Webb
Author URI: http://github.com/Webb-Ben
*/

// No direct calls
if( !defined( 'YOURLS_ABSPATH' ) ) die();

yourls_add_filter( 'get_shorturl_charset', 'regex_in_charset' );
function regex_in_charset( $in ) {
    return $in.'_[]{}()^*\/-+?|$.';
}

yourls_add_filter( 'is_GO', 'go_regex' );
function go_regex(){
    return true;
}

yourls_add_action( 'redirect_keyword_not_found', 'try_regex' );
function try_regex( $args ) {
    $table         = YOURLS_DB_TABLE_URL;
    $keyword       = $args[0];
    $sanitized_val = '/' . yourls_sanitize_keyword($keyword);
    $pattern       = '/%$';
    $sql           = "SELECT * FROM `$table` WHERE `keyword` LIKE :pattern AND :sanitized_val REGEXP `keyword`";
    $binds         = array('pattern' => $pattern, 'sanitized_val' => $sanitized_val);
    $sql_result    = yourls_get_db()->fetchObject($sql, $binds);

    if ($sql_result !== false) {
        $redirect_url = $sql_result->{'url'};
        $regex        = '/' . preg_replace("/\//", "\\/", $sql_result->{'keyword'}) . '/';

        preg_match($regex, $sanitized_val, $capture_groups);
        foreach ($capture_groups as $i => $group) {
            $redirect_url = str_replace('$' . $i, $group, $redirect_url);
        }

        yourls_redirect($redirect_url);
        die();
    }
}
