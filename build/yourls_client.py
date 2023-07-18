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

import click
import os
from pathlib import Path
import yourls_api

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
                file_list.append(Path(os.path.join(root, name)))

    return file_list


@click.command()
@click.pass_context
@click.argument('path', type=str, nargs=-1)
@click.option('-s', '--uri_stem', type=str, default='https://geoconnex.us/',
              help='uri stem to be removed from short url for keyword')
@click.option('-k', '--keyword', type=str, default='id',
              help='field in CSV to be used as keyword')
@click.option('-l', '--long_url', type=str, default='target',
              help='field in CSV to be used as long url')
@click.option('-t', '--title', type=str, default='description',
              help='field in CSV to be used as title')
@click.option('-a', '--addr', type=str, default='http://localhost:8082/',
              help='yourls database hostname')
@click.option('-u', '--user', type=str, default='yourls-admin',
              help='user for yourls database')
@click.option('-p', '--passwd', type=str, default='apassword',
              help='password for yourls database')
@click.option('--to-db', type=bool, default=True,
              help='Attempt to connect to database')
def run(ctx, **kwargs):
    urls = yourls_api.yourls(**kwargs)
    for p in kwargs['path']:
        if p.endswith('.csv'):
            urls.handle_csv(p)
        else:
            urls.handle_csv(walk_path(p))
            urls.make_sitemap(walk_path(p, t=XML))


if __name__ == "__main__":
    run()
