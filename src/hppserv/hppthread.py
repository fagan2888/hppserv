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
from Queue import Queue
from threading import Thread

from hppcontroller import HPPController
from hpputil import ObjectHolder


class HPPThread(Thread, HPPController):
    def __init__(self, qout=None, **kwargs):
        Thread.__init__(self)
        HPPController.__init__(self, **kwargs)

        self.qout = qout if qout else Queue()
        self.qin = Queue()

        self.daemon = True
        self.start()


    def run(self):
        while True:
            msg = self.qin.get(block=True)
            if msg is None:
                return
            self.runhpp(**msg.kwargs)


    def postMsg(self, action, **kwargs):
        msg = ObjectHolder(action=action, **kwargs)
        self.qobj.put(msg)


    def hppstart(self, **kwargs):
        if not kwargs:
            kwargs = dict()
        self.qin.put(ObjectHolder(kwargs=kwargs))


    def hppexit(self):
        self.qin.put(None)

