#!/usr/bin/python
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
from socketserver import ThreadingMixIn
import threading
import time
from urllib.request import urlopen
import json




PORT_NUMBER = 8080
SERVER_PORT_NUMBER = "8081"
CACHE_PORT_NUMBER = "8081"


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        threadname = threading.currentThread().getName()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        parsedURL = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsedURL.query)
        print (params, threadname)
        time.sleep(0)

        if self.path.startswith('/QUERY/'):
            response = urlopen("http://localhost:"+ CACHE_PORT_NUMBER+ self.path)
            self.wfile.write (response.read())
        elif self.path.startswith('/BOOK/'):
            response = urlopen("http://localhost:"+ SERVER_PORT_NUMBER+ self.path)
            self.wfile.write(response.read())
        print ('EXIT,', threadname)
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    """Handle requests in a separate thread."""


if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT_NUMBER), Handler)
    print ('Started appgateway on port ', PORT_NUMBER)
    server.request_queue_size = 5

    server.serve_forever()
