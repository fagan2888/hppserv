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
from BaseHTTPServer import HTTPServer
from collections import defaultdict, deque
from socket import SHUT_RDWR
from SocketServer import ThreadingMixIn

from hppconfig import HPPConfig
from hpphandler import HPPHandler


class HPPServer(ThreadingMixIn, HTTPServer):

    def __init__(self, handlerclass=HPPHandler, controller=None, **kwargs):

        self.config = controller.config if controller else HPPConfig(**kwargs)
        HTTPServer.__init__(self, (self.config.host, self.config.port), handlerclass)

        self.ldesc = deque()
        self.connq = defaultdict(deque)
        self.controller = controller


    def process_request_thread(self, request, client_address):
        """Same as in BaseServer but as a thread.

        In addition, exception handling is done here.

        """
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except Exception, e:
            self.handle_error(request, client_address, exc=e)
            self.shutdown_request(request)


    def handle_error(self, request, client_address, exc=None):
        if False and exc:
            print 'Exception happened: %s' % str(exc)
        else:
            HTTPServer.handle_error(self, request, client_address)


    def setproxy(self, **kwargs):
        self.config.setproxy(**kwargs)


    def postMsg(self, action, **kwargs):
        if self.controller:
            self.controller.postMsg(action, **kwargs)


    def hppstop(self):
        self.shutdown()
        # Close the descriptor of threads to force them out
        # of the loop and die - this allows full restart of the server
        for desc in self.ldesc:
            if hasattr(desc, 'shutdown'):
                # close a socket properly
                try:
                    desc.shutdown(SHUT_RDWR)
                except:
                    pass
            try:
                desc.close()
            except Exception, e:
                pass




