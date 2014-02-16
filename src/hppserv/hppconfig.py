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
from urllib import getproxies
from urlparse import urlsplit, urlunsplit


class HPPConfig(dict):
    CONFIGURATION = {
        'debugclient': False,
        'debughpp': False,
        'debughttpconn': False,

        'host': 'localhost',
        'port': 9000,

        'proxysystem': False,
        'proxyparsed': urlsplit('http://127.0.0.1:8888/'),
        'proxy': False,

        'proxykeepalive': True,
        'keepalive': True,
        'keepaliveInTimeout': 60,
        'keepaliveOutTimeout': 60,

        'timeout': 15,

        'dnsconnect': False,
        'connectUse10': False,
        'connectNoHost': False,

        'dnslocal': False,

        'sendFullUrl': False,
        'connRetry': 0,
        'dechunk': False,
        'chunknolength': False,
        'bufferbody': False,
        }


    def __init__(self, *args, **kwargs):
        dict.__init__(self, doExit=False, **self.CONFIGURATION) # default values
        self.update(*args, **kwargs) # potential update values


    def __getattr__(self, name):
        try:
            return self[name]
        except (KeyError, IndexError):
            raise AttributeError


    def __setattr__(self, name, value):
        self[name] = value


    def update(self, *args, **kwargs):
        dict.update(self, *args, **kwargs)
        proxy = kwargs.get('proxy', self.proxy)
        proxysystem = kwargs.get('proxysystem', self.proxysystem)
        proxyurl = kwargs.get('proxyurl', urlunsplit(self.proxyparsed))
        self.setproxy(proxy, proxysystem, proxyurl)
        return self


    def setproxy(self, proxy=False, proxysystem=False, proxyurl='http://127.0.0.1:8888/'):
        self.proxyurl = proxyurl
        self.proxysystem = proxysystem
        proxyurl = self.proxyurl if not proxysystem else HPPConfig.getproxysystem()
        self.proxyparsed = urlsplit(proxyurl)
        self.proxy = proxy


    @staticmethod
    def getproxysystem():
        for scheme, url in getproxies().iteritems():
            if scheme.lower() == 'http':
                return url

        return ''
