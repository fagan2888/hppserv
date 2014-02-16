# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class HPPFrame
###########################################################################

class HPPFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"HPP Serv", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Local Network" ), wx.VERTICAL )
		
		self.m_checkBoxLocalConn = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Only local connections", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.m_checkBoxLocalConn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )
		
		self.m_textCtrlLocalPort = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlLocalPort.SetMaxLength( 0 ) 
		bSizer2.Add( self.m_textCtrlLocalPort, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )
		
		
		sbSizer2.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( sbSizer2, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Upstream Proxy" ), wx.VERTICAL )
		
		self.m_checkBoxUseProxySystem = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Use System Proxy", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer3.Add( self.m_checkBoxUseProxySystem, 0, wx.ALL, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBoxUseProxyOther = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Use other", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_checkBoxUseProxyOther, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )
		
		self.m_textCtrlProxyUrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlProxyUrl.SetMaxLength( 0 ) 
		bSizer4.Add( self.m_textCtrlProxyUrl, 1, wx.ALL, 5 )
		
		
		sbSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( sbSizer3, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer13.Add( bSizer3, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Standard Settings" ), wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_checkBoxDNSLocal = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Resolve DNS Locally", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxDNSLocal.Enable( False )
		
		gSizer1.Add( self.m_checkBoxDNSLocal, 0, wx.ALL, 5 )
		
		self.m_checkBoxKeepAlive = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Send KeepAlive", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_checkBoxKeepAlive, 0, wx.ALL, 5 )
		
		self.m_checkBoxSendFullUrl = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Send Full URL", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_checkBoxSendFullUrl, 0, wx.ALL, 5 )
		
		self.m_checkBoxKeepAliveProxy = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Send Proxy KeepAlive", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_checkBoxKeepAliveProxy, 0, wx.ALL, 5 )
		
		self.m_checkBoxDeChunk = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Dechunk chunked", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_checkBoxDeChunk, 0, wx.ALL, 5 )
		
		self.m_checkBoxChunkNoLength = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Chunk no-length body", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxChunkNoLength.Enable( False )
		
		gSizer1.Add( self.m_checkBoxChunkNoLength, 0, wx.ALL, 5 )
		
		
		sbSizer4.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		self.m_staticline51 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		sbSizer4.Add( self.m_staticline51, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer1411 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText21 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Socket Timeout", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		bSizer1411.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinCtrlSocketTimeout = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 9999, 0 )
		bSizer1411.Add( self.m_spinCtrlSocketTimeout, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer9.Add( bSizer1411, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticline9 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer9.Add( self.m_staticline9, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		bSizer141 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Connection retries", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer141.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )
		
		self.m_spinCtrlConnRetries = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 45,-1 ), wx.SP_ARROW_KEYS, 0, 10, 0 )
		bSizer141.Add( self.m_spinCtrlConnRetries, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer9.Add( bSizer141, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer4.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		
		bSizer7.Add( sbSizer4, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5 )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Connect Settings" ), wx.VERTICAL )
		
		self.m_checkBoxConnectLocalDNS = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Local DNS", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer8.Add( self.m_checkBoxConnectLocalDNS, 0, wx.ALL, 5 )
		
		self.m_checkBoxConnectRemoveHost = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Remove 'Host'", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer8.Add( self.m_checkBoxConnectRemoveHost, 0, wx.ALL, 5 )
		
		self.m_checkBoxConnectUseHttp10 = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Use HTTP/1.0", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer8.Add( self.m_checkBoxConnectUseHttp10, 0, wx.ALL, 5 )
		
		
		sbSizer8.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer17.Add( sbSizer8, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Buffering settings" ), wx.VERTICAL )
		
		self.m_checkBoxBufferBody = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Buffer body", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxBufferBody.Enable( False )
		
		sbSizer6.Add( self.m_checkBoxBufferBody, 0, wx.ALL, 5 )
		
		
		bSizer17.Add( sbSizer6, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer7.Add( bSizer17, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer13.Add( bSizer7, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Debug" ), wx.HORIZONTAL )
		
		self.m_checkBoxDebugClient = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Client -> HPPServer", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer5.Add( self.m_checkBoxDebugClient, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticline31 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		sbSizer5.Add( self.m_staticline31, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_checkBoxDebugHPP = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Client <- HPPServer", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer5.Add( self.m_checkBoxDebugHPP, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticline311 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		sbSizer5.Add( self.m_staticline311, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_checkBoxDebugHttpConnection = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"HPPServer <-> Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer5.Add( self.m_checkBoxDebugHttpConnection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer13.Add( sbSizer5, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText4 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Remember to restart the server to apply configuration changes", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.m_staticText4.Wrap( -1 )
		bSizer16.Add( self.m_staticText4, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5 )
		
		
		bSizer13.Add( bSizer16, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer5.Add( bSizer13, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_staticline10 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer5.Add( self.m_staticline10, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 5 )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_buttonStart = wx.Button( self.m_panel1, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_buttonStart, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.m_buttonStop = wx.Button( self.m_panel1, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonStop.Enable( False )
		
		bSizer14.Add( self.m_buttonStop, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.m_staticline4 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer14.Add( self.m_staticline4, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_buttonSettingsStore = wx.Button( self.m_panel1, wx.ID_ANY, u"Store Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonSettingsStore.Enable( False )
		
		bSizer14.Add( self.m_buttonSettingsStore, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_buttonSettingsRetrieve = wx.Button( self.m_panel1, wx.ID_ANY, u"Load Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonSettingsRetrieve.Enable( False )
		
		bSizer14.Add( self.m_buttonSettingsRetrieve, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticline7 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer14.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self.m_panel1, wx.ID_ANY, u"About ...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALL, 5 )
		
		
		bSizer14.AddSpacer( ( 0, 0), 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer5.Add( bSizer14, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.TOP, 5 )
		
		
		self.m_panel1.SetSizer( bSizer5 )
		self.m_panel1.Layout()
		bSizer5.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_checkBoxUseProxySystem.Bind( wx.EVT_CHECKBOX, self.OnCheckBoxUseProxySystem )
		self.m_buttonStart.Bind( wx.EVT_BUTTON, self.OnButtonClickStart )
		self.m_buttonStop.Bind( wx.EVT_BUTTON, self.OnButtonClickStop )
		self.m_buttonSettingsStore.Bind( wx.EVT_BUTTON, self.OnButtonClickSettingsStore )
		self.m_buttonSettingsRetrieve.Bind( wx.EVT_BUTTON, self.OnButtonClickSettingsLoad )
		self.m_button5.Bind( wx.EVT_BUTTON, self.OnButtonClickAbout )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnCheckBoxUseProxySystem( self, event ):
		event.Skip()
	
	def OnButtonClickStart( self, event ):
		event.Skip()
	
	def OnButtonClickStop( self, event ):
		event.Skip()
	
	def OnButtonClickSettingsStore( self, event ):
		event.Skip()
	
	def OnButtonClickSettingsLoad( self, event ):
		event.Skip()
	
	def OnButtonClickAbout( self, event ):
		event.Skip()
	

###########################################################################
## Class AboutDialog
###########################################################################

class AboutDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"About HPPServ", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer7 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Python Proxy with some protocol tweaks", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		sbSizer7.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		sbSizer7.Add( self.m_staticline8, 0, wx.EXPAND, 5 )
		
		self.m_hyperlink1 = wx.HyperlinkCtrl( self, wx.ID_ANY, u"http://www.github.com/mementum/hppserv", u"http://www.github.com/mementum/hppserv", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		sbSizer7.Add( self.m_hyperlink1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticline10 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		sbSizer7.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"(C) 2012-2014 Daniel Rodriguez", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		sbSizer7.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer14.Add( sbSizer7, 1, wx.EXPAND|wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_OK, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button7, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer14 )
		self.Layout()
		bSizer14.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

