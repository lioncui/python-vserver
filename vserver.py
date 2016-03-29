'''
    Copyright (C) 2016 Lion Cui <lioncui@163.com>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#!/usr/bin/python
# -*- coding:UTF-8 -*-

from flask import Flask, request, Response
import random
import time
import thread
from werkzeug.routing import BaseConverter
import ssl
from config import *

app = Flask('__name__')

def make_random_str(num):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in xrange(int(num)):
        sa.append(random.choice(seed))
    salt = "".join(sa)
    return salt

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/<regex(".*"):url>', methods = ['GET', 'POST'])
def index(url):
    redata = {}
    format_request_headers = {}
    unfilter_headers = {}

    for i in request.headers:
        format_request_headers[str(i[0]).lower()] = i[1]

    status_code = format_request_headers.get('x-vs-ctrl-status-code', 200)
    content_type = format_request_headers.get('content-type')
    content_random = format_request_headers.get('x-vs-ctrl-body-content-israndom', 'false')
    length = format_request_headers.get('x-vs-ctrl-body-content-length', '-1')
    interval = format_request_headers.get('x-vs-ctrl-response-interval', '-1')
    isclean = format_request_headers.get('x-vs-ctrl-header-isclean', 'false')
    redata = str(request.get_data())

    try:
        if length[-1] == 'k':
            length = int(length[:-1]) * 1024
        elif length[-1] == 'm':
            length = int(length[:-1]) * 1024 * 1024
        else:
            length = int(length)
    except ValueError:
        length = -1

    try:
        interval = int(interval)
    except ValueError:
        interval = -1

    if content_random == "true":
        if length >= 0:
            redata = make_random_str(length)
        else:
            redata = make_random_str(128)
        content_type = "text/plain; charset=utf8"

    resp = Response(redata)

    if length >= 0:
        if length <= len(redata):
            resp.headers['Content-Length'] = length
        elif 0 < len(redata) < length:
            i = length / len(redata)
            j = length % len(redata)
            resp.data = redata * i + redata[:j]
        else:
            resp.headers['Content-Length'] = 0

    if isclean != "true":
        for i in format_request_headers:
            if 'x-vs-ctrl-' not in i and i not in FILTER_HEADERS:
                resp.headers[i] =  format_request_headers[i]

    try:
        resp.status_code = int(status_code)
    except ValueError:
        resp.status = status_code + " unknow"

    resp.content_type = content_type

    if interval >= 0:
        time.sleep(interval)
    return resp

app.debug = DEBUG
ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_ctx.load_cert_chain(SERVER_SSL_CERT, SERVER_SSL_KEY, SERVER_SSL_PASS)
ssl_ctx.verify_mode = ssl.CERT_REQUIRED
ssl_ctx.load_verify_locations(cafile = TRUSTED_CACERT)
app.threaded = True
#thread.start_new_thread(app.run, (SERVER_BIND,HTTP_PORT,))
app.run(SERVER_BIND, HTTPS_PORT, ssl_context = ssl_ctx)