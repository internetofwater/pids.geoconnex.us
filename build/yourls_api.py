# =================================================================
#
# Authors: Benjamin Webb <bwebb@lincolninst.edu>
#
# Copyright (c) 2023 Benjamin Webb
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


import csv
from git import Repo
import json
from datetime import datetime as dt
import mysql.connector
import os
from pathlib import Path
from pyourls3.client import exceptions, Yourls
import requests
from shutil import copy2
import time
import xml.etree.ElementTree as ET

URI_STEM = os.environ.get('URI_STEM', 'https://geoconnex.us')
SITEMAP = Path('/sitemap')
SITEMAP_ARGS = {'encoding': 'utf-8', 'xml_declaration': True}
SITEMAP_FOREACH = '''
<sitemap>
    <loc>{}</loc>
    <lastmod>{}</lastmod>
</sitemap>\n
'''
URLSET_FOREACH = '''
<url>
    <loc>{}</loc>
    <lastmod>{}</lastmod>
</url>
'''


try:
    # https://stackoverflow.com/questions/60286623/python-loses-connection-to-mysql-database-after-about-a-day
    mysql.connector.connect(
        host=os.environ.get('YOURLS_DB_HOST') or 'mysql',
        user=os.environ.get('YOURLS_DB_USER') or 'root',
        password=os.environ.get('YOURLS_DB_PASSWORD') or 'arootpassword',
        database="yourls",
        pool_name="yourls_loader",
        pool_size=3
    )
except Exception as err:
    print(err)
    print('Unable to connect to database')


def connection():
    """Get a connection and a cursor from the pool"""
    db = mysql.connector.connect(pool_name='yourls_loader')
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
    geoconnex = Repo('/geoconnex.us')

    def __init__(self, **kwargs):
        self.tree = self.geoconnex.heads.master.commit.tree
        self.kwargs = kwargs
        self.__to_db = kwargs.get('to_db', True)
        if self.__to_db:
            mydb, cursor = connection()
            sql_statement = 'DELETE FROM yourls_url WHERE ip = "0.0.0.0"'
            cursor.execute(sql_statement)
            mydb.commit()
            print(cursor.rowcount, "was deleted.")
            cursor.close()
            mydb.close()
        else:
            _ = self._check_kwargs(('addr', 'user', 'passwd'))
            Yourls.__init__(self, *[v for k, v in _])

    def _check_kwargs(self, keys):
        """
        Parses kwargs for desired keys.

        :param keys: required, list. List of keys to retried from **kwargs.

        :return: generator. key value pairs for each key in **kwargs.

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

        :return: generator. key value pairs for each key in **kwargs.

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

        :param **kwargs: required, dict. Expects url, keyword, and title.

        :return: dictionary. Full JSON response from the API

        :raises: pyourls3.exceptions.Pyourls3ParamError,
          pyourls3.exceptions.Pyourls3APIError
        """
        _ = self.check_kwargs(('url', 'keyword', 'title'), **kwargs)
        specific_args = {'action': 'shorten_quick', **{k: v for k, v in _}}

        r = requests.post(self.api_endpoint, data={
                          **self.global_args, **specific_args})
        try:
            j = r.json()
        except json.decoder.JSONDecodeError:
            raise exceptions.Pyourls3HTTPError(
                r.status_code, self.api_endpoint)

        if j.get("status") == "success":
            return j
        else:
            raise exceptions.Pyourls3APIError(
                j["message"], j.get("code", j.get("errorCode")))

    def shorten_csv(self, filename, csv=''):
        """
        Sends an API request to shorten a specified CSV.

        :param filename: required, string. Name of CSV to be shortened.
        :param csv: optional, list. Pre-parsed csv as list of strings.

        :return: dictionary. Full JSON response from the API

        :raises: pyourls3.exceptions.Pyourls3ParamError,
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
            raise exceptions.Pyourls3HTTPError(
                r.status_code, self.api_endpoint)

        if j.get("status") == "success":
            return j
        else:
            raise exceptions.Pyourls3APIError(
                j["message"], j.get("code", j.get("errorCode")))

    def post_mysql(self, filename, csv_=''):
        """
        Sends an API request to shorten a specified CSV.

        :param filename: required, string. Name of CSV to be shortened.
        :param csv_: optional, list. Pre-parsed csv as list of strings.

        :return: dictionary. Full JSON response from the API

        :raises: pyourls3.exceptions.Pyourls3ParamError,
          pyourls3.exceptions.Pyourls3APIError
        """
        print(filename)
        if not filename:
            raise exceptions.Pyourls3ParamError('filename')

        # Clean input for inserting
        time_ = self._get_filetime(filename)
        extra = [time_, '0.0.0.0', 0]
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

        # Commit file to database
        SQL_STATEMENT = ("INSERT INTO yourls_url "
                         "(`keyword`, `url`, `title`, `timestamp`, `ip`, `clicks`)"  # noqa
                         "VALUES (%s, %s, %s, %s, %s, %s)")
        mydb, cursor = connection()
        try:
            cursor.executemany(SQL_STATEMENT, split_)
        except mysql.connector.errors.ProgrammingError:
            print(split_)

        mydb.commit()
        # print(cursor.rowcount, "was inserted.")
        cursor.close()
        mydb.close()

    def _make_sitemap(self, filename, csv_=''):
        """
        Create sitmap.xml from csv file.

        :param filename: required, string. Name of CSV to be shortened.
        :param csv_: optional, list. Pre-parsed csv as list of strings.
        :return: None.

        :raises: pyourls3.exceptions.Pyourls3ParamError,
          pyourls3.exceptions.Pyourls3APIError
        """
        if not filename:
            raise exceptions.Pyourls3ParamError('filename')

        file = csv_ if csv_ else open(filename, 'r')
        chunky_parsed = self.chunkify(file, 50000)
        file_time = self._get_filetime(filename)
        for i, chunk in enumerate(chunky_parsed):
            lines = chunk.split("\n")
            split_ = [line.split(',').pop(0) for line in lines[:-1]]

            # Build sitemaps for each csv file
            tree = ET.parse('./sitemap-url.xml')
            ET.indent(tree, '  ')
            sitemap = tree.getroot()
            for line in split_:
                if '$' in line:
                    return

                url_ = url_join(URI_STEM, line)
                t = URLSET_FOREACH.format(
                    url_, file_time.strftime('%Y-%m-%dT%H:%M:%SZ'))

                link_xml = ET.fromstring(t)
                sitemap.append(link_xml)

            # Write sitemap.xml
            fidx = f'{filename.stem}__{i}'
            sitemap_file = (filename.parent / fidx).with_suffix('.xml')
            tree.write(sitemap_file, **SITEMAP_ARGS)
            os.utime(sitemap_file, (time.time(), file_time.timestamp()))

    def make_sitemap(self, files):
        tree = ET.parse('./sitemap-schema.xml')
        sitemap = tree.getroot()
        for f in files:
            # Make sure file is sitemap
            try:
                int(f.stem.split('__').pop())
            except ValueError:
                continue

            # Check buildpath
            try:
                parent = f.parent.relative_to("namespaces")
            except ValueError:
                parent = f.parent.relative_to("/build/namespaces")
            path_ = (SITEMAP / parent)
            path_.mkdir(parents=True, exist_ok=True)

            # Copy xml to /sitemaps
            fpath_ = path_ / f.name
            copy2(f, fpath_)

            # create to link /sitemap/_sitemap.xml
            time_ = self._get_filetime(fpath_).strftime('%Y-%m-%dT%H:%M:%SZ')
            url_ = url_join(URI_STEM, str(fpath_))
            t = SITEMAP_FOREACH.format(url_, time_)

            link_xml = ET.fromstring(t)
            sitemap.append(link_xml)
            ET.indent(tree, '  ')

        sitemap_out = SITEMAP / '_sitemap.xml'
        tree.write(sitemap_out, **SITEMAP_ARGS)
        print('finished task')

    def _get_filetime(self, fpath_):
        try:
            path_ = fpath_.relative_to(SITEMAP)
        except ValueError:
            path_ = fpath_.relative_to("/build/namespaces")

        try:
            blob = (self.tree / "namespaces" / f"{path_}")
            commit = next(self.geoconnex.iter_commits(
                paths=blob.path, max_count=1))
            time_ = commit.committed_datetime
        except KeyError:
            _ = os.path.getmtime(fpath_)
            time_ = dt.fromtimestamp(_)
        except OSError:
            time_ = dt.now()
        return time_

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

        :param file: required, name of csv to be shortened
        """
        if isinstance(file, list):
            self._handle_csvs(file)
            return

        parsed_csv = self.parse_csv(file)
        if self.__to_db:
            chunky_parsed = self.chunkify(parsed_csv, 10000)
            for chunk in chunky_parsed:
                self.post_mysql(file, chunk)
        else:
            chunky_parsed = self.chunkify(parsed_csv)

            for chunk in chunky_parsed:
                self.shorten_csv(file, chunk)

        self._make_sitemap(file, parsed_csv)

    def parse_csv(self, filename):
        """
        Parse CSV file into yourls-friendly csv.

        :param filename: required, string. URL to be shortened.
        :return: list. Parsed csv.
        """
        _ = self._check_kwargs(('keyword', 'long_url', 'title'))
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
                    parsed_line.append(line[headers.index(v)].strip())
                except (ValueError, IndexError):
                    continue
            _ = self._check_kwargs(['uri_stem', ])
            ret_csv.append(
                (','.join(parsed_line) + '\n').replace(*[v for k, v in _], ''))

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
