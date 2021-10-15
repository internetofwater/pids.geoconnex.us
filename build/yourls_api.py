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

from pyourls3.client import *
import mysql.connector
from datetime import date, datetime, timedelta
import os
import csv
import json
import xml.etree.ElementTree as ET

SITEMAP = '/sitemap/'

# https://stackoverflow.com/questions/60286623/python-loses-connection-to-mysql-database-after-about-a-day
mydb = mysql.connector.connect(
    host=os.environ.get('YOURLS_HOST', 'mysql'),
    user=os.environ.get('YOURLS_USER', 'root'),
    password=os.environ.get('YOURLS_DB_PASSWORD', 'arootpassword'),
    database="yourls",
    pool_name="yourls_loader",
    pool_size = 3
)
def connection():
    """Get a connection and a cursor from the pool"""
    db = mysql.connector.connect(pool_name = 'yourls_loader')
    return (db, db.cursor())

def url_join(*parts):
    """
    helper function to join a URL from a number of parts/fragments.
    Implemented because urllib.parse.urljoin strips subpaths from
    host urls if they are specified
    Per https://github.com/geopython/pygeoapi/issues/695
    :param parts: list of parts to join
    :returns: str of resulting URL
    """
    return '/'.join([p.strip().strip('/') for p in parts])

class yourls(Yourls):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.__to_db = kwargs.get('_via_yourls_', True)

        if self.__to_db:
            mydb = mysql.connector.connect(
                host=os.environ.get('YOURLS_HOST', 'mysql'),
                user=os.environ.get('YOURLS_USER', 'root'),
                password=os.environ.get('YOURLS_DB_PASSWORD', 'arootpassword'),
                database="yourls"
            )
            sql_statement = 'DELETE FROM yourls_url WHERE ip = "0.0.0.0"'
            cursor = mydb.cursor()
            cursor.execute(sql_statement)
            mydb.commit()
            print(cursor.rowcount, "was deleted.")
            cursor.close()
            mydb.close()
        else:
            _ = self._check_kwargs(('addr', 'user', 'passwd', 'key'))
            Yourls.__init__(self, *[v for k, v in _])

    def _check_kwargs(self, keys):
        """
        Parses kwargs for desired keys.

        :param keys: required, list. List of keys to retried from **kwargs.
        :return: generator. Generator of key value pairs for each key in **kwargs.

        :raises: pyourls3.exceptions.Pyourls3ParamError
        """
        for key in keys:
            if key in self.kwargs.keys():
                yield key, self.kwargs.get(key)
            else:
                raise exceptions.Pyourls3ParamError(key)

    def check_kwargs(self, keys, **kwargs):
        """
        Parses kwargs for desired keys.

        :param keys: required, list. List of keys to retried from **kwargs.
        :param **kwargs: required, dict.
        :return: generator. Generator of key value pairs for each key in **kwargs.

        :raises: pyourls3.exceptions.Pyourls3ParamError
        """
        for key in keys:
            if key in kwargs.keys():
                yield key, kwargs.get(key)
            else:
                raise exceptions.Pyourls3ParamError(key)

    def shorten_quick(self, **kwargs):
        """
        Sends an API request to shorten a specified URL.

        :param **kwargs: required, dict. Expects url, keyword, and title to be specified.
        :return: dictionary. Full JSON response from the API, parsed into a dict

        :raises: pyourls3.exceptions.Pyourls3ParamError, pyourls3.exceptions.Pyourls3HTTPError,
          pyourls3.exceptions.Pyourls3APIError
        """
        _ = self.check_kwargs(('url', 'keyword', 'title'), **kwargs)
        specific_args = {'action': 'shorten_quick', **{k: v for k, v in _}}

        r = requests.post(self.api_endpoint, data={**self.global_args, **specific_args})
        try:
            j = r.json()
        except json.decoder.JSONDecodeError:
            raise exceptions.Pyourls3HTTPError(r.status_code, self.api_endpoint)

        if j.get("status") == "success":
            return j
        else:
            raise exceptions.Pyourls3APIError(j["message"], j.get("code", j.get("errorCode")))


    def shorten_csv(self, filename, csv = ''):
        """
        Sends an API request to shorten a specified CSV.

        :param filename: required, string. Name of CSV to be shortened.
        :param csv: optional, list. Pre-parsed csv as list of strings.
        :return: dictionary. Full JSON response from the API, parsed into a dict

        :raises: pyourls3.exceptions.Pyourls3ParamError, pyourls3.exceptions.Pyourls3HTTPError,
          pyourls3.exceptions.Pyourls3APIError
        """
        if not filename:
            raise exceptions.Pyourls3ParamError('filename')

        specific_args = {'action': 'shorten_csv'}

        if csv:
            file = {'import': (filename, csv, 'text/csv')}
        else:
            file = {'import': (filename, open(filename, 'r'), 'text/csv')}

        r = requests.post(self.api_endpoint,
                          data={**self.global_args, **specific_args},
                          files=file)

        try:
            j = r.json()
        except json.decoder.JSONDecodeError:
            raise exceptions.Pyourls3HTTPError(r.status_code, self.api_endpoint)

        if j.get("status") == "success":
            return j
        else:
            raise exceptions.Pyourls3APIError(j["message"], j.get("code", j.get("errorCode")))

    def post_mysql(self, filename, csv_ = ''):
        """
        Sends an API request to shorten a specified CSV.

        :param filename: required, string. Name of CSV to be shortened.
        :param csv_: optional, list. Pre-parsed csv as list of strings.
        :return: dictionary. Full JSON response from the API, parsed into a dict

        :raises: pyourls3.exceptions.Pyourls3ParamError, pyourls3.exceptions.Pyourls3HTTPError,
          pyourls3.exceptions.Pyourls3APIError
        """
        print(filename)
        if not filename:
            raise exceptions.Pyourls3ParamError('filename')

        extra = [datetime.now().date(),'0.0.0.0', 0]
        file = csv_ if csv_ else open(filename, 'r')
        lines = file.split("\n")
        split_ = [line.split(',') for line in lines[:-1]]
        for line in split_:
            if len(line) > 3:
                line[2] = ','.join(line[2:])
                while len(line) > 3:
                    line.pop(-1)

            if len(line) == 3:
                line.extend(extra)

        sql_statement = ("INSERT INTO yourls_url "
                    "(`keyword`, `url`, `title`, `timestamp`, `ip`, `clicks`)"
                    "VALUES (%s, %s, %s, %s, %s, %s)")

        mydb, cursor = connection()
        try:
            cursor.executemany(sql_statement, split_)
        except mysql.connector.errors.ProgrammingError:
            for l in split_:
                if len(l) != 6:
                    print(l)

        mydb.commit()
        print(cursor.rowcount, "was inserted.")
        cursor.close()
        mydb.close()

    def _make_sitemap(self, filename, csv_ = ''):
        """
        Create sitmap.xml from csv file.

        :param filename: required, string. Name of CSV to be shortened.
        :param csv_: optional, list. Pre-parsed csv as list of strings.
        :return: None.

        :raises: pyourls3.exceptions.Pyourls3ParamError, pyourls3.exceptions.Pyourls3HTTPError,
          pyourls3.exceptions.Pyourls3APIError
        """
        if not filename:
            raise exceptions.Pyourls3ParamError('filename')

        file = csv_ if csv_ else open(filename.split('_')[0], 'r')
        lines = file.split("\n")
        split_ = [line.split(',').pop(0) for line in lines[:-1]]
        uri_stem = self.kwargs.get('uri_stem')
        txt = "<url>\n\t\t<loc> {} </loc>\n\t\t<lastmod> {} </lastmod>\n</url>\n"

        tree = ET.parse('./sitemap-url.xml')
        sitemap = tree.getroot()[0]
        for i in range(len(split_)):
            name_ = split_[i]
            if not name_.startswith('/'):
                url_ = url_join(uri_stem, name_)
                t = txt.format(url_, datetime.now())
                link_xml = ET.fromstring(t)
                sitemap.append(link_xml)
        tree.write(f'{filename}.xml')

    def make_sitemap(self, files):
        # Setup file system:
        if not os.path.isdir(SITEMAP):
            os.makedirs(SITEMAP)

        tree = ET.parse('./sitemap-url.xml')
        sitemap = tree.getroot()[0]
        uri_stem = self.kwargs.get('uri_stem')
        txt = "<url>\n\t\t<loc> {} </loc>\n\t\t<lastmod> {} </lastmod>\n</url>\n"
        for f in files:
            tree_ = ET.parse(f)
            name_ = url_join(SITEMAP,f.split('/').pop())
            tree_.write(f'/{name_}')
            url_ = url_join(uri_stem, name_)
            t = txt.format(url_, datetime.now())
            link_xml = ET.fromstring(t)
            sitemap.append(link_xml)
        tree.write('/sitemap/_sitemap.xml')
        print('finished task')

    def _handle_csvs(self, files):
        """
        Splits list of csv files into individual csv files.

        :param files: required, string. URL to be shortened.
        """
        for f in files:
            self.handle_csv(f)

    def handle_csv(self, file):
        """
        Parses and shortens CSV file.

        :param file: required, string or list of strings. Name of csv files to be shortened
        """
        if isinstance(file, list):
            self._handle_csvs(file)
            return

        parsed_csv = self.parse_csv(file)
        if self.__to_db:
            chunky_parsed = self.chunkify( parsed_csv, 10000)
            for chunk in chunky_parsed:
                self.post_mysql(file, chunk)
        else:
            chunky_parsed = self.chunkify( parsed_csv )

            for chunk in chunky_parsed:
                self.shorten_csv(file, chunk)
        
        chunky_parsed = self.chunkify( parsed_csv, 50000)
        for i, chunk in enumerate(chunky_parsed):
            self._make_sitemap(f'{file[:-4]}__{i}', chunk)
    
    def parse_csv(self, filename):
        """
        Parse CSV file into yourls-friendly csv.

        :param filename: required, string. URL to be shortened.
        :return: list. Parsed csv.
        """
        _ = self._check_kwargs(('keyword', 'url', 'title'))
        vals = {k: v for k, v in _}

        try:
            r = requests.get(filename)
            fp = r.content.decode().splitlines()
        except requests.exceptions.MissingSchema:
            r = None
            fp = open(filename, mode='r')

        csv_reader = csv.reader(fp)
        headers = [h.strip() for h in next(csv_reader)]
        ret_csv = []
        for line in csv_reader:
            parsed_line = []
            for k, v in vals.items():
                try:
                    parsed_line.append( line[headers.index(v)].strip() )
                except (ValueError, IndexError):
                    continue
            _ = self._check_kwargs(['uri_stem',])
            ret_csv.append((','.join(parsed_line) + '\n').replace(*[v for k, v in _], ''))

        if not r:
            fp.close()

        return ret_csv

    def chunkify(self, input, n=500):
        """
        Breaks a list of strings into chunks.

        :param input: required, list. List to be chunkified.
        :param n: optional, int. Size of each chunk.
        :return: list. Input list with each sublist length up to the size of n.
        """
        return [''.join(input[i:i + n]) for i in range(0, len(input), n)]
