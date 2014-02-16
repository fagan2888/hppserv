#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
################################################################################
# 
#  Copyright (C) 2012-2014 Daniel Rodriguez
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from collections import defaultdict
from copy import copy
from httplib import HTTPConnection, HTTPMessage, HTTPResponse
from itertools import imap, izip
from operator import itemgetter
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


def clone(self):
    cloneobj = HTTPMessage(StringIO(), seekable=0)
    cloneobj.dict = self.dict.copy()
    cloneobj.headers = copy(self.headers)
    return cloneobj
    
# HTTPResponse instantiates directly HTTPMessage, leaving no room for
# subclassing HTTPResponse
HTTPMessage.clone = clone

def iteritems(self):
    items = list()
    for header in self.headers:
        name, wsvalue = header.split(':', 1)
        items.append((name, wsvalue.rstrip('\r\n')))
    return items
    
# HTTPResponse instantiates directly HTTPMessage, leaving no room for
# subclassing HTTPResponse
HTTPMessage.iteritems = iteritems


class HPPResponse(HTTPResponse):
    def begin(self):
        HTTPResponse.begin(self)
        # To void the broken logic at the end of begin, because
        # but the connection may stay explicitly open with a connect
        # of for some other reason
        self.will_close = self._check_close()

        # it is sensible to assume that after a connect if
        # 200 is returned, the connection will not close
        # even if issued as 1.0 and no specific connection
        # header came back - a binary connection is now open
        if self._method == 'CONNECT' and self.status == 200:
            self.will_close = 0


class HPPResponseConnect(HPPResponse):
    # Empty response object for direct CONNECTS simulating a 200 OK
    def __init__(self, conn):
        HPPResponse.__init__(self, sock=conn.sock, debuglevel=conn.debuglevel, strict=conn.strict, method=conn._method)
        self.chunked = False
        self.will_close = False
        self.length = 0
        self.status = 200
        self.reason = 'OK'
        self.msg = HTTPMessage(StringIO(), seekable=0)
        self.msg.fp = None
        

# Patch HTTPConnection to use our subclass
HTTPConnection.response_class = HPPResponse

class HPPConnection(HTTPConnection):
    response_class = HPPResponse

    def putheader(self, header, *values):
        # Capitalize the headers for a nicer output
        HTTPConnection.putheader(self, header.capitalize(), *values)


    def putrequest(self, method, url, skip_host=0, skip_accept_encoding=0):
        # Avoid any host and/or accept-encoding addtion from HTTPConnection
        HTTPConnection.putrequest(self, method, url, skip_host=True, skip_accept_encoding=True)
