# =================================================================
#
# Authors: Benjamin Webb <benjamin.miller.webb@gmail.com>
#
# Copyright (c) 2021 Benjamin Webb
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import os
import yourls_api
import time
import argparse

CSV = 'csv'
XML = 'xml'

def walk_path(path, t=CSV):
    """
    Walks os directory path collecting all CSV files.

    :param path: required, string. os directory.
    :return: list. List of csv paths.
    """
    file_list = []
    for root, _, files in os.walk(path, topdown=False):
        for name in files:
            if name.startswith('example'):
                continue
            elif name.endswith(t):
                file_list.append(os.path.join(root, name))

    return file_list

def make_parser():
    """
    Creates and argv parser object.

    :return: ArgumentParser. with defaults if not specified.
    """
    parser = argparse.ArgumentParser(description='Upload csv files to yourls database')

    parser.add_argument('path', type=str, nargs='+',
                        help='path to csv files. accepts directory, url, and .csv paths')
    parser.add_argument('-s','--uri_stem', action='store', dest='uri_stem', type=str,
                        default='https://geoconnex.us/',
                        help='uri stem to be removed from short url for keyword')
    parser.add_argument('-k','--keyword', action='store', dest='keyword', type=str,
                        default='id',
                        help='field in CSV to be used as keyword')
    parser.add_argument('-l','--long_url', action='store', dest='url', type=str,
                        default='target',
                        help='field in CSV to be used as long url')
    parser.add_argument('-t','--title', action='store', dest='title', type=str,
                        default='description',
                        help='field in CSV to be used as title')
    parser.add_argument('-a','--addr', action='store', dest='addr', type=str,
                        default='http://localhost:8082/',
                        help='yourls database hostname')
    parser.add_argument('-u','--user', action='store', dest='user', type=str,
                        default='yourls-admin',
                        help='user for yourls database')
    parser.add_argument('-p','--pass', action='store', dest='passwd', type=str,
                        default='apassword',
                        help='password for yourls database')  
    parser.add_argument('--key', action='store', dest='key', 
                        default=None,
                        help='password for yourls database') 
    return parser

def main():
    parser = make_parser()
    kwargs = parser.parse_args()

    urls = yourls_api.yourls( **vars(kwargs) )
    time.sleep(10)
    for p in kwargs.path:
        if p.endswith('.csv'):
            urls.handle_csv( p )
        else:
            urls.handle_csv(walk_path(p))
            urls.make_sitemap(walk_path(p,t=XML))

if __name__ == "__main__":
    main()
