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

DEBUG = False
SERVER_BIND = '0.0.0.0'
HTTP_PORT = 8080
HTTPS_PORT = 8443

SERVER_SSL_CERT = 'certs/vserver.crt.pem'
SERVER_SSL_KEY = 'certs/vserver.pri.pem'
SERVER_SSL_PASS = 'nu5/SM/JIRHa=pi8'
TRUSTED_CACERT = 'certs/vserver-client.crt.pem'

FILTER_HEADERS = [
                    "transfer-encoding", "server", "set-cookie", "user-agent"
                    , "cookie", "connection", "host", "content-type"
                    , "content-length", "accept"
                ]
