#!/usr/bin/python
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
from socketserver import ThreadingMixIn
import threading
import time
from urllib.request import urlopen
import json
import commons



PORT_NUMBER = 8080
SERVER_PORT_NUMBER = "8081"
CACHE_PORT_NUMBER = "8082"


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        clientstartime=commons.currenttimemillis()
        threadname = threading.currentThread().getName()
        time.sleep(0)
        gatewaystartime=commons.currenttimemillis()
        time.sleep(0)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        parsedURL = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsedURL.query)
        print (params, threadname)

        if self.path.startswith('/QUERY/'):
            response = urlopen("http://localhost:"+ CACHE_PORT_NUMBER+ self.path)
            
        elif self.path.startswith('/BOOK/'):
            response = urlopen("http://localhost:"+ SERVER_PORT_NUMBER+ self.path)
        
        res=commons.Record(response.read().decode())
        res.customerid=params["id"][0]
        res.gatewayendtime=commons.currenttimemillis()
        res.gatewaystartime=gatewaystartime
        res.clientendtime=commons.currenttimemillis()
        res.clientstarttime=clientstartime
        self.wfile.write (res.serialize().encode('utf-8'))
        res.printLog()        
        print ('EXIT,', threadname)
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    """Handle requests in a separate thread."""


if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT_NUMBER), Handler)
    commons.printH1 ('Started appgateway on port '+str(PORT_NUMBER))
    server.request_queue_size = 5

    server.serve_forever()
