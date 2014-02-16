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
import threading
import sys

class FlushFile(object):
    lock = threading.Lock()
    reqdata = threading.local()

    def __init__(self, f):
        self.f = f

    def write(self, x):
        with self.lock:
            self.f.write('%s: ' % datetime.utcnow().isoformat())
            if 'client_address' in self.reqdata.__dict__:
                self.f.write('%s: ' % str(self.reqdata.client_address))
            self.f.write(x)
            self.f.flush()

sys.stdout = FlushFile(sys.stdout)
sys.stderr = FlushFile(sys.stderr)
