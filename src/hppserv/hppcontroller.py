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
from datetime import datetime

from hppconfig import HPPConfig
from hpphandler import HPPHandler
from hppserver import HPPServer


class HPPController(object):
    def __init__(self, hppclass=HPPServer, handlerclass=HPPHandler, config=None, **kwargs):
        self.hppclass = hppclass
        self.handlerclass = handlerclass
        self.config = config.update(**kwargs) if config else HPPConfig(**kwargs)


    def runhpp(self, **kwargs):
        self.config.update(**kwargs)
        self.hppserver = self.hppclass(handlerclass=self.handlerclass,
                                       controller=self,
                                       **self.config)

        self.hppserver.serve_forever()
        self.hppserver.server_close()
        self.hppserver = None


    def postMsg(self, action, **kwargs):
        if action == 'log':
            if kwargs.get('debuglevel', 1) <= self.config.debuglevel:
                print '%s: %s' % (datetime.now().isoformat(), kwargs.get('logmsg', ''))


    def setproxy(self, **kwargs):
        self.config.setproxy(**kwargs)


    def hppstart(self, **kwargs):
        self.runhpp(**kwargs)


    def hppstop(self):
        self.config.doExit = True
        self.hppserver.hppstop()
        self.hppserver = None
        self.config.doExit = False


    def hppexit(self):
        pass
