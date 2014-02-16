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
from itertools import imap
from operator import itemgetter


class HPPHeaders(object):

    def __init__(self, *rawheaders):
        self.keys = defaultdict(list)
        self.headers = list()
        self.update(*rawheaders)


    def update(self, *rawheaders):
        for rawheader in rawheaders:
            name, wsvalue = rawheader.split(':', 1)
            value = wsvalue.lstrip().rstrip('\r\n')

            self.keys[name].append(len(self.headers))
            self.headers.append((name, value))
        

    def get(self, key, default=None):
        if key in self.keys:
            return map(lambda x: self.headers[x][1], self.keys[key])
        return default


    def __len__(self):
        return len(self.headers)


    def iteritems(self):
        return iter(self.headers)


    def __iter__(self):
        return imap(itemgetter(0), self.headers)


    def __contains__(self, item):
        return item in self.keys


    def __delitem__(self, key):
        # Deletes all headers that correspond to key
        if key in self.keys:
            for index in reversed(self.keys[key]):
                del self.headers[index]
            del self.keys[key]
        

    def __getitem__(self, key):
        if key in self.keys:
            return map(lambda x: self.headers[x][1], self.keys[key])
        raise KeyError


    def __setitem__(self, key, value):
        # Replaces all values and keeps the position of the 1st seen header
        try:
            index = self.keys[key][0]
            for todel in reversed(self.keys[key][1:]):
                del self.headers[todel]
            # reduce the number of indexes to 1
        except (IndexError, KeyError):
            index = len(self.headers)

        self.keys[key] = [index]
        self.headers.insert(index, (key, value))
b
            

