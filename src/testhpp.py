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
from hppserv import HPPController

hppcontroller = HPPController()

kwargs = dict()
hppcontroller.setproxy(proxy=False, proxysystem=False, proxyurl='http://127.0.0.1:8888')
hppcontroller.config.proxykeepalive = kwargs.get('proxykeepalive', True)
hppcontroller.config.keepalive = kwargs.get('keepalive', True)
hppcontroller.config.timeout = kwargs.get('timeout', 10)
hppcontroller.config.dnslocal = kwargs.get('dnslocal', False)
hppcontroller.config.dnsconnect = kwargs.get('dnsconnect', True)
hppcontroller.config.connectUse10 = kwargs.get('connectUse10', True)
hppcontroller.config.connectNoHost = kwargs.get('connectNoHost', True)
hppcontroller.config.sendFullUrl = kwargs.get('sendFullUrl', False)
hppcontroller.config.connRetry = kwargs.get('connRetry', 0)

hppcontroller.config.connRetry = kwargs.get('debughpp', 0)

hppcontroller.hppstart(host='localhost', port=9000)
