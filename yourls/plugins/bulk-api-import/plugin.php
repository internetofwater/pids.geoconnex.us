<?php
/*
Plugin Name: Bulk API Import
Plugin URI: https://github.com/webb-ben/plugins/bulk-api-import
Description: Quickly shortens csv files of urls via api (without default yourls checks).
Version: 1.0
Author: Ben Webb
Author URI: http://github.com/Webb-Ben
*/

// No direct call
if( !defined( 'YOURLS_ABSPATH' ) ) die();

// Define custom api action 'quick_shorten'
yourls_add_filter( 'api_action_shorten_quick', 'quick_shorten' );
// Quick Shorten
function quick_shorten() {
    // Retrieve vals from HTTP request
	$url = ( isset( $_REQUEST['url'] ) ? $_REQUEST['url'] : '' );
	$keyword = ( isset( $_REQUEST['keyword'] ) ? $_REQUEST['keyword'] : '' );
	$title = ( isset( $_REQUEST['title'] ) ? $_REQUEST['title'] : '' );

	if (yourls_insert_link_in_db( $url, $keyword, $title )){
    // If link added, populate response vals
        $return['url']      = array('keyword' => $keyword, 'url' => $url, 'title' => $title, 'date' => $timestamp, 'ip' => $ip );
        $return['status']   = 'success';
        $return['title']    = $title;
        $return['shorturl'] = yourls_link($keyword);
    } 
    else {
    // Couldnt store result
        $return['status']   = 'fail';
        $return['code']     = 'error:db';
        $return['message']  = yourls_s( 'Error saving url to database' );
    }

    // Return response
	return $return;
}

// Define custom api action 'csv_shorten'
yourls_add_filter( 'api_action_shorten_csv', 'csv_shorten' );
// CSV Shorten
function csv_shorten() {
    // Retrieve file from HTTP request
    $file = $_FILES['import'];
    list($added, $updated) = import_urls( $file );

    // Form response with count of urls added from csv
    $return['status'] = 'success';
    $return['request'] = $_REQUEST;
    $return['message'] = yourls_s( 'Added '.$added.' links, Updated '.$updated.' links to database');

    // Return response
    return $return;
}

// Adapted from from yourls-bulk-import-and-shorten
// https://github.com/vaughany/yourls-bulk-import-and-shorten).
// Import csv of urls
function import_urls( $file ) {
    // Check if file was uploaded
    if ( !is_uploaded_file( $file['tmp_name'] ) ) {
        yourls_add_notice('Not an uploaded file.');
    }

    // Only handle .csv files
    if ($file['type'] !== 'text/csv') {
        yourls_add_notice('Not a .csv file.');
        return 0;
    }

    ini_set( 'auto_detect_line_endings', true );
    $added = $updated = 0;
    $fh     = fopen( $file['tmp_name'], 'r' );
    $table  = YOURLS_DB_TABLE_URL;

    // If the file handle is okay.
    if ( $fh ) {

        // Get each line in turn as an array, comma-separated.
        while ( $csv = fgetcsv( $fh, 1000, ',' ) ) {

            if ( isset( $csv[0] ) && !empty( $csv[0] ) ) {
                $url = trim( $csv[0] );
                $url = yourls_sanitize_url( $url );
            }
            else {
                continue;
            }

            if ( isset( $csv[1] ) && !empty( $csv[1] ) ) {
                $keyword = trim( $csv[1] );
                $keyword = yourls_sanitize_keyword( $keyword );
            }
            else {
                continue;
            }

            if ( isset( $csv[2] ) && !empty( $csv[2] ) ) {
                $title = trim( $csv[2] );
                $title = yourls_sanitize_title($title);
            }

            // If the requested keyword is free, shorten url.
            if ( yourls_keyword_is_free( $keyword ) ) {
                // Ignore incomplete lines
                if (yourls_insert_link_in_db( $url, $keyword, $title )){
                    $added++;
                }
            }
            else if (yourls_get_keyword_longurl($keyword) !== $url){
                if (yourls_api_edit_link( $url, $keyword, $keyword, $title )){
                    $updated++;
                }
            }
        }

    } else {
        yourls_add_notice('File handle is bad.');
    }

    // Return count of urls added
    return array($added, $updated);
}

// Copy of yourls_edit_link() but with plug-in friendly sanitization
function yourls_api_edit_link( $url, $keyword, $newkeyword='', $title='' ) {
    // Allow plugins to short-circuit the whole function
    $pre = yourls_apply_filter( 'shunt_edit_link', null, $keyword, $url, $keyword, $newkeyword, $title );
    if ( null !== $pre )
        return $pre;

    $ydb = yourls_get_db();

    $table = YOURLS_DB_TABLE_URL;
    $url = yourls_sanitize_url($url);
    $keyword = yourls_sanitize_keyword($keyword);
    $title = yourls_sanitize_title($title);
    $newkeyword = yourls_sanitize_keyword($newkeyword);
    $strip_url = stripslashes( $url );
    $strip_title = stripslashes( $title );

    if(!$url OR !$newkeyword) {
        $return['status']  = 'fail';
        $return['message'] = yourls__( 'Long URL or Short URL cannot be blank' );
        return yourls_apply_filter( 'edit_link', $return, $url, $keyword, $newkeyword, $title );
    }

    $old_url = $ydb->fetchValue("SELECT `url` FROM `$table` WHERE `keyword` = :keyword", array('keyword' => $keyword));

    // Check if new URL is not here already
    if ( $old_url != $url && !yourls_allow_duplicate_longurls() ) {
        $new_url_already_there = intval($ydb->fetchValue("SELECT COUNT(keyword) FROM `$table` WHERE `url` = :url;", array('url' => $url)));
    } else {
        $new_url_already_there = false;
    }

    // Check if the new keyword is not here already
    if ( $newkeyword != $keyword ) {
        $keyword_is_ok = yourls_keyword_is_free( $newkeyword );
    } else {
        $keyword_is_ok = true;
    }

    yourls_do_action( 'pre_edit_link', $url, $keyword, $newkeyword, $new_url_already_there, $keyword_is_ok );

    // All clear, update
    if ( ( !$new_url_already_there || yourls_allow_duplicate_longurls() ) && $keyword_is_ok ) {
            $sql   = "UPDATE `$table` SET `url` = :url, `keyword` = :newkeyword, `title` = :title WHERE `keyword` = :keyword";
            $binds = array('url' => $url, 'newkeyword' => $newkeyword, 'title' => $title, 'keyword' => $keyword);
            $update_url = $ydb->fetchAffected($sql, $binds);
        if( $update_url ) {
            $return['url']     = array( 'keyword' => $newkeyword, 'shorturl' => yourls_link($newkeyword), 'url' => $strip_url, 'display_url' => yourls_trim_long_string( $strip_url ), 'title' => $strip_title, 'display_title' => yourls_trim_long_string( $strip_title ) );
            $return['status']  = 'success';
            $return['message'] = yourls__( 'Link updated in database' );
        } else {
            $return['status']  = 'fail';
            $return['message'] = /* //translators: "Error updating http://someurl/ (Shorturl: http://sho.rt/blah)" */ yourls_s( 'Error updating %s (Short URL: %s)', yourls_trim_long_string( $strip_url ), $keyword ) ;
        }

    // Nope
    } else {
        $return['status']  = 'fail';
        $return['message'] = yourls__( 'URL or keyword already exists in database' );
    }

    return yourls_apply_filter( 'edit_link', $return, $url, $keyword, $newkeyword, $title, $new_url_already_there, $keyword_is_ok );
}