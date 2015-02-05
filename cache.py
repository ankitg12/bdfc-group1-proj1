#!/usr/bin/python
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
from socketserver import ThreadingMixIn
import threading
import time
from urllib.request import urlopen
import json
import sqlite3
import commons

PORT_NUMBER = 8082

ID=0
CAPCITY=1
AVAILABLE=2
PMIN=3
SEATSTEP=4
PRICESTEP=5

class Handler(BaseHTTPRequestHandler):
    def getprice(self,id):
            print ('Querying db for price')
            conn = sqlite3.connect('flightrecords.db')
            c = conn.cursor()
            cursor = c.execute('SELECT *  from flights WHERE id ='+id)
            row=cursor.fetchone()
            conn.close()
            res=commons.Record("")
            price = row[PMIN] + row[PRICESTEP] *  ((row[CAPCITY] - row[AVAILABLE]) // row[SEATSTEP])
            res.id=row[ID]
            res.capacity=row[CAPCITY]
            res.available=row[AVAILABLE]
            res.price = price
            res.api='QUERY'
            return res


    def do_GET(self):
        threadname = threading.currentThread().getName()
        serverstartime=commons.currenttimemillis()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        parsedURL = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsedURL.query)
        print (params, threadname)
        time.sleep(0)
        res = self.getprice(params["id"][0])
        self.wfile.write(res.serialize().encode('utf-8'))
        print ('EXIT,', threadname)
        res.serverendtime=commons.currenttimemillis()
        res.serverstartime=serverstartime
        res.cached="1"
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    """Handle requests in a separate thread."""
if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT_NUMBER), Handler)
    print ('Started cache server on port ', PORT_NUMBER)
    server.request_queue_size = 5

    server.serve_forever()

