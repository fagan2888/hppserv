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
import wx

import appconstants
import mainframe

def Run():
    hppApp = HPPApp(redirect=False)
    hppApp.MainLoop()


class HPPApp(wx.App):
    def OnInit(self):
        wx.Log_SetActiveTarget(wx.LogStderr())
        # wx.Log_SetActiveTarget(wx.LogBuffer())

        self.SetAppName(appconstants.AppName)
        self.SetVendorName(appconstants.VendorName)

        frame = mainframe.HPPFrame(parent=None)
        title = appconstants.AppTitle + ' - ' + appconstants.AppVersion
        frame.SetTitle(title)
        self.SetTopWindow(frame)
        frame.Show(True)

        return True
