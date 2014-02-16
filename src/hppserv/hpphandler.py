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
from BaseHTTPServer import BaseHTTPRequestHandler
from collections import OrderedDict
from datetime import datetime, timedelta
from httplib import HTTPMessage
import select
import socket
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
import threading
from urlparse import urlsplit, urlunsplit

from hppresponse import HPPConnection, HPPResponseConnect
import hppflushfile


lock = threading.Lock()
def logMessageT(msg):
    with lock:
        sys.stdout.write('%s\n' % msg)


class HPPHandler(BaseHTTPRequestHandler):
    MessageClass = HTTPMessage
    server_version = "HPPServer"
    sys_version = '0.0.1'

    # To ensure that the connection remains open
    protocol_version = 'HTTP/1.1'

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        # Put descriptors into the server to let it finish us
        # Tests have shown that the 3 objects referencing the system
        # socket descriptor have to be closed
        self.server.ldesc.append(self.rfile)
        self.server.ldesc.append(self.wfile)
        self.server.ldesc.append(self.request)

        self.config = self.server.config
        self.connq = self.server.connq
        self.conn = None
        self.connts = None
        self.parsed = urlsplit('')
        self.keepaliveout = timedelta(seconds=self.config.keepaliveOutTimeout)

        hppflushfile.FlushFile.reqdata.client_address = self.client_address


    def log_message(self, format, *args):
        # To avoid unnecessary logging from the base class
        pass


    def logClient(self, logmsg):
        if self.server.config.debugclient:
            # logMessageT('%s, %s: %s' % (datetime.utcnow().isoformat(), self.client_address, logmsg))
            logMessageT('%s' % logmsg)


    def logHpp(self, logmsg):
        if self.server.config.debughpp:
            logMessageT('%s' % logmsg)


    def finish(self):
        self.logHpp('finish got called ... working')
        # override and protect
        try:
            self.wfile.flush()
        finally:
            for xfile in [self.wfile, self.rfile]:
                try:
                    xfile.close()
                except:
                    pass
        try:
            self.request.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.closeConnOut()


    def parse_request(self):
        retval = BaseHTTPRequestHandler.parse_request(self)
        # Add support for proxy-connection before the
        conntype = self.headers.get('proxy-connection', "")
        if conntype.lower() == 'close':
            self.close_connection = 1
        elif (conntype.lower() == 'keep-alive' and
              self.protocol_version >= "HTTP/1.1"):
            self.close_connection = 0
        return retval


    def handle_one_request(self):
        # Wait before going to "readline" to ensure we may escape on
        # server shutdown or socket exception
        lsock = [self.request]
        isock, osock, esock = select.select(lsock, [], lsock, self.config.keepaliveInTimeout)
        if esock or self.config.doExit:
            self.logHpp('Exiting on: esock %d or doExit ' % (len(esock), self.config.doExit))
            self.close_connection = 1
            self.closeConnOut()
            return

        if not isock and not osock and not esock:
            self.logHpp('Exiting on timeout')
            # timeout - we close the connection
            self.close_connection = 1
            # store any existing outgoing
            self.closeConnOut()
            return

        BaseHTTPRequestHandler.handle_one_request(self)


    def send_response(self, code, message=None, hppresp=None):
        """Send the response header and log the response code.

        Also send two standard headers with the server software
        version and the current date.

        """
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s %d %s\r\n" %
                             (self.protocol_version, code, message))
            # print (self.protocol_version, code, message)
        if not hppresp:
            # To avoid duplication in normal responses
            self.send_header('Server', self.version_string())
            self.send_header('Date', self.date_time_string())


    def expireConnOut(self):
        if self.conn:
            if datetime.utcnow() - self.connts > self.keepaliveout:
                self.closeConnOut()
                return True
        return False


    def closeConnOut(self, dest=None):
        if not self.conn:
            return
        if not dest:
            try:
                if self.conn.sock:
                    self.conn.sock.shutdown(socket.SHUT_RDWR)
            finally:
                self.conn.close()
        else:
            self.connq[dest].appendleft((self.conn, self.connts))
            
        self.conn = None


    def createConnOut(self, connparsed):
        # need a new connection
        try:
            # try from connection storage
            self.conn, self.connts = self.connq[connparsed.netloc].pop()
            if self.expireConnOut():
                raise IndexError
        except IndexError:
            # create a new one
            self.conn = HPPConnection(host=connparsed.hostname, port=connparsed.port, timeout=self.config.timeout)

        if self.config.debughttpconn:
            self.conn.set_debuglevel(1)


    def do_GET(self):
        # Request line: self.command, self.path, self.request_version
        # Headers: self.headers (HTTPMessage - really a subclass of it)
        # self.client_address: calling party (ip_addr, port)
        # self.request (or self.connection): request socket (from the client)
        # self.rfile, self.wfile: files opened on top of the request socket
        # self.close_connection: to indicate that the connection shall be closed
        # self.server: to access the main server instance (the thread listening on the main socket)

        # Remove the fp reference in the headers to avoid dangling reference
        self.headers.fp = None

        self.logClient('Request: %s %s %s' % (self.command, self.path, self.request_version))

        for header in self.headers.headers:
            self.logClient('Request header %s' % header.rstrip('\r\n'))

        isConnect = (self.command == 'CONNECT')
        self.logClient('Connect is: %s' % str(isConnect))
        # Guarantee a correct parsing of the "connect" path
        parsepath = self.path if not isConnect else 'https://%s' % self.path
        parsed = urlsplit(parsepath)

        if self.config.proxy:
            self.logHpp('config proxy is true')
            # All connections point to the same destination: the proxy
            connparsed = self.config.proxyparsed
            self.logHpp('connparsed is %s' % str(connparsed))
            self.expireConnOut()
        else:
            connparsed = parsed
            if self.parsed.netloc != connparsed.netloc:
                # New direct destination - the current (if existing) connection is not valid
                if not self.expireConnOut():
                    self.closeConnOut(dest=self.parsed.netloc)
                self.parsed = connparsed
            else:
                # Old destination still valid, check age
                self.expireConnOut()

        if not self.conn:
            self.createConnOut(connparsed)
        self.logHpp('Created connection to: %s' % connparsed.netloc)

        # copy of request headers to keep original intact for later reference
        # headers = self.headers.dict.copy()
        headers = self.headers.clone()

        # Both are 1-hop, so we don't carry them over
        # We may want to add our own
        if self.config.keepalive:
            # We may want to issue it in case we hit a 1.0 HTTP server
            self.logHpp('Added connection header: keep-alive')
            headers['connection'] = 'keep-alive'
        elif 'connection' in headers:
            self.logHpp('Removed connection header: %s' % headers['connection'])
            del headers['connection']
            
        if self.config.proxy and self.config.proxykeepalive:
            # We may want to issue it in case we hit a 1.0 HTTP proxy
            self.logHpp('Added proxy-connection header: keep-alive')
            headers['proxy-connection'] = 'keep-alive'
        elif 'proxy-connection' in headers:
            self.logClient('Removed proxy-connection header: %s' % headers['proxy-connection'])
            del headers['proxy-connection']

        body = None
        # nicer -- allows insertion of "OnRequest" that modifies path, body, headers ...
        command, path, body, headers = self.command, self.path, body, headers

        toLocalHost = False
        if self.config.proxy:
            if isConnect:
                if self.config.dnsconnect:
                    # Solve the address of connect host - this only support IPV4
                    try:
                        connectaddr = socket.gethostbyname(parsed.hostname)
                    except Exception, e:
                        self.closeConnOut()
                        self.send_error(400, str(e))
                        return

                    if parsed.port == 443:
                        path = '%s:%d' % (connectaddr, parsed.port)
                    else:
                        toLocalHost = True
                        path = '127.0.0.1:%d' % parsed.port
                        print "CONNECTING TO %s" % path

                if self.config.connectUse10:
                    self.conn._http_vsn_str = 'HTTP/1.0'
                    self.conn._http_vsn = 10

                if self.config.connectNoHost and 'host' in headers:
                    del headers['host']
        else:
            if not self.config.sendFullUrl:
                # Unless told so, do not send the full URL for a direct connection
                path = urlunsplit(('', '', parsed.path, parsed.query, parsed.fragment))

        try:
            if not toLocalHost and (self.config.proxy or not isConnect):
                self.logHpp('sending request over self.conn (proxy or not isConnect)')
                self.conn.request(method=command, url=path, body=body, headers=headers)
            else:
                # Direct "Connect" connection, we connect ... issuing headers would be senseless
                self.logHpp('telling connection to connect')
                self.conn.connect()

            # For POST ... I could write to the socket from the other socket whatever "content-length" arrived
            # Although theoretically the request could also be "chunked"
        except Exception, e:
            self.logHpp('Exception happened during request/connect: %s: %s:%s' % (e.__class__.__name__, str(e), str(e.args)))
            self.closeConnOut()
            if False:
                self.send_error(400, str(e))
            else:
                # return closing the connection and therefore indicating a problem
                self.close_connection = 1
            return
        finally:
            if isConnect:
                if self.config.connectUse10:
                    self.conn._http_vsn_str = 'HTTP/1.1'
                    self.conn._vsn_str = 11

        if self.command == 'POST':
            # send the body
            try:
                ofile = self.conn.sock.makefile('wb')

                trenc = headers.get('transfer-encoding')
                if trenc and 'chunked' in trenc.lower():
                    totaldata, _ = self.readbodychunked(ifile=self.rfile, ofile=ofile)
                else:
                    clength = headers.get('content-length')
                    if clength:
                        totaldata = self.readbody(ifile=self.rfile, ofile=ofile, clength=int(clength))
            except Exception, e:
                self.logHpp('Exception happened during body send: %s: %s:%s' % (e.__class__.__name__, str(e), str(e.args)))
                if False:
                    self.send_error(400, str(e))
                else:
                    # return closing the connection and therefore indicating a problem
                    self.close_connection = 1
            finally:
                ofile.close()

        try:
            if self.config.proxy or not isConnect:
                hppresp = self.conn.getresponse()
            else:
                # Fake a response for the direct Connect method
                hppresp = HPPResponseConnect(self.conn)
        except Exception, e:
            self.logHpp('Exception happened during response: %s: %s:%s' % (e.__class__.__name__, str(e), str(e.args)))
            self.closeConnOut()
            if False:
                self.send_error(400, str(e))
            else:
                # return closing the connection and therefore indicating a problem - hopefully the client will retry
                self.close_connection = 1
            return

        if hasattr(self, 'OnResponseReceived'):
            self.OnResponseReceived(command, path, body, headers, hppresp)
        # Prepare and send response
        self.logHpp('Statusline: %s %s' % (hppresp.status, hppresp.reason))
        self.send_response(hppresp.status, hppresp.reason, hppresp=hppresp)

        self.logHpp('hppresp.length is %s' % str(hppresp.length))
        self.logHpp('hppresp.chunked is %s' % str(hppresp.chunked))
        self.logHpp('hppresp.will_close is %s' % str(hppresp.will_close))

        if hppresp.will_close and (not hppresp.chunked and hppresp.length is None):
            # no content-length has been set and not chunked but told to close
            # there may be data of unbounded length and the close is the indication
            # to read until the end of the socket
            # because we are not buffering, the length is unknown and we can't signal
            # it ... we could always send it chunked ... and keep the connection open
            # TODO: transform these answers into chunked if request_version is > HTTP/1.0
            self.logHpp('will_close and (not chunked and length not None: close_connection = 1')
            self.close_connection = 1
            
        if False:
            for header in hppresp.msg:
                values = hppresp.msg.getheaders(header)
                for value in values:
                    valuelow = value.lower()
                    if self.config.dechunk:
                        if header == 'transfer-encoding' and 'chunked' in valuelow:
                            # we will be dechunking
                            self.logHpp('Header: Dechunking is active - skipping transfer encoding header')
                            continue
                    # connection is 1-hop
                    if header in ['connection', 'proxy-connection']:
                        # 1 hop ... don't carry them over
                        self.logHpp('Header: removing %s:%s' % (header, value))
                        continue
                    # Send the header: self.logMsg('Sending header %s:%s' % (key, header), 2)
                    self.logHpp('Header: sending %s:%s' % (header.capitalize(), value))
                    self.send_header(header.capitalize(), value)
        else:
            # copy the headers
            headersresp = hppresp.msg.clone()

            # Connection: Reply with whatever it was requested, but adapted
            if 'connection' in self.headers:
                pvalue = 'close' if self.close_connection else self.headers['connection']
                self.logHpp('client sent connection=%s, we answer' % pvalue)
                headersresp['connection'] = pvalue
            else:
                # the server may have answered with a connection ... we remove it
                # There was no connection "header", so if HTTP/1.0 it will be closed
                # and if HTTP 1.1 it will remain alive
                del headersresp['connection']

            if 'proxy-connection' in self.headers:
                pvalue = 'close' if self.close_connection else self.headers['proxy-connection']
                self.logHpp('client sent proxyconnection=%s, we answer with %s' % (self.headers['proxy-connection'], pvalue))
                headersresp['proxy-connection'] = pvalue
            else:
                # The server may have answered with a proxy connection ... but only if we use it ...
                # if the client didn't ask for it ... remove it
                del headersresp['proxy-connection']

            if self.config.dechunk:
                trenc = headersresp.get('transfer-encoding')
                if trenc and 'chunked' in trenc.lower():
                    del headersresp['transfer-encoding']
                    self.logHpp('Header: Dechunking is active - skipping transfer encoding header')

            for header, value in headersresp.iteritems():
                # Send the header: self.logMsg('Sending header %s:%s' % (key, header), 2)
                self.logHpp('Header: sending %s:%s' % (header.capitalize(), value))
                self.send_header(header.capitalize(), value)
                
        # add content-length if needed
        if self.config.dechunk and hppresp.chunked:
            # We are not sending the chunks so we need to add the "content-length header"
            body = hppresp._read_chunked(None)
            hppresp.close()
            hppresp.chunked = False
            hppresp.length = len(body)
            hppresp.fp = StringIO(body)
            self.send_header('Content-length', '%d' % hppresp.length)
            self.logHpp('dechunked %d bytes' % hppresp.length)

        self.logHpp('header: finishing headers')
        # Finish headers
        self.end_headers()

        # Go with the body
        if hppresp.chunked:
            # Use "fp" from hppresp to switch between read and readline
            totaldata, _ = self.readbodychunked(ifile=hppresp.fp, ofile=self.wfile)
            self.logHpp('body: sent %d chunk bytes (+ CRFL + trailers)' % totaldata)

        elif hppresp.length or (hppresp.length is None and hppresp.will_close):
            totaldata = self.readbody(ifile=hppresp.fp, ofile=self.wfile, clength=hppresp.length)
            self.logHpp('body: sent %d content.length bytes' % totaldata)

        else:
            # Possibly "HEAD" or NOT_MODIFIED or NO_CONTENT, in any case ... no read
            self.logHpp('body: apparently .. no content')
            pass

        if hppresp.will_close:
            self.logHpp('hppresp will close ... closing own connection')
            self.closeConnOut()

        elif isConnect and hppresp.status == 200:
            self.logHpp('connect ... ')
            self.doConnect()
            # A binary connection is not reusable - obviously ...
            self.closeConnOut()

            # close also the connection to the client
            self.close_connection = 1

        else:
            self.logHpp('end of operation ... and connection still in thread and alive ... timestamping')
            self.connts = datetime.utcnow()

            if self.close_connection:
                self.logHpp('closing connection to client ... saving connection to pool of connections')
                self.closeConnOut(dest=connparsed.netloc)

        # ensure the response is closed (and detached from the connection)
        hppresp.close()
        hppresp = None


    def readbody(self, ifile, ofile, clength, deflength=4096):
        totaldata = 0
        while clength or clength is None:
            data = ifile.read(min(clength or deflength, deflength)) # min (None, 4096) = None
            if not data:
                break
            ldata = len(data)
            if clength:
                clength -= ldata
            totaldata += ldata
            ofile.write(data)
            ofile.flush()

        return totaldata


    def readbodychunked(self, ifile, ofile, dechunk=False, deflength=4096):
        totaldata = 0
        while True:
            # Chunk length (discard trailing ';....')
            clength = ifile.readline()
            if not dechunk:
                ofile.write(clength)
            clength = clength.rstrip('\r\n').split(';', 1)[0]
            clength = int(clength, 16)
            if not clength:
                break

            # Chunk data
            while clength:
                data = ifile.read(min(clength, deflength))
                ldata = len(data)
                clength -= ldata
                totaldata += ldata
                ofile.write(data)

            # Chunk end - trailing newline
            chunkend = ifile.readline()
            if not dechunk:
                ofile.write(chunkend)
            ofile.flush()

        # Chunk trailers
        if dechunk:
            ofile = StringIO()
        while True:
            line = ifile.readline()
            ofile.write(line)
            if line == '\r\n' or line == '\r':
                break

        ofile.flush()

        footers = None if not dechunk else HTTPMessage(ofile, seekable=0)
        return (totaldata, footers)


    ################################
    do_HEAD = do_GET
    do_POST = do_GET
    do_CONNECT = do_GET
    ################################


    def doConnect(self):
        try:
            sockclient = self.request
            sockserver = self.conn.sock
            iw = [sockclient, sockserver]
            while True:
                insocks, outsocks, exsocks = select.select(iw, [], iw)
                if exsocks:
                    print "RETURNING"
                    return
                for insock in insocks:
                    outsock = sockserver if insock is sockclient else sockclient
                    data = insock.recv(4096)
                    if not data:
                        return
                    outsock.send(data)
        except Exception, e:
            pass


    def postMsg(self, action, **kwargs):
        self.server.postMsg(action, **kwargs)


    def logMsg(self, logmsg, debuglevel=1):
        self.postMsg(action='log', logmsg=logmsg, debuglevel=debuglevel)
