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

AGE=2000
PORT_NUMBER = 8082
SERVER_PORT_NUMBER = "8081"

ID=0
CAPCITY=1
AVAILABLE=2
PMIN=3
SEATSTEP=4
PRICESTEP=5
cache={}

class Handler(BaseHTTPRequestHandler):
    def getrealprice(self,id,res):
            print ('Querying db for price')
            conn = sqlite3.connect('flightrecords.db')
            c = conn.cursor()
            cursor = c.execute('SELECT *  from flights WHERE id ='+id)
            row=cursor.fetchone()
            conn.close()
            price = row[PMIN] + row[PRICESTEP] *  ((row[CAPCITY] - row[AVAILABLE]) // row[SEATSTEP])
            res.realavailable=row[AVAILABLE]
            res.realprice = price
            return res
            
    def queryServer(self,id):
            response = urlopen("http://localhost:"+ SERVER_PORT_NUMBER+ self.path)
            res=commons.Record(response.read().decode())
            return res
            
    def checkCache(self,id):
            res=0
            print ('Checking cache for price of ',id)
            if (id in cache):
                    res=cache[id]   
                    res.cached="1"
                    age= commons.currenttimemillis() - int(res.serverendtime) 
                    print("Cache age ", age)
                    if (age > AGE ):
                        res=0
            if (res==0):
                    res=self.queryServer(id)
                    res.cached="0"
                    self.getrealprice(id,res)
                    cache[id]=res
                    print("Cache miss")
            res.printLog()                    
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
        res = self.checkCache(params["id"][0])
#        res.serverendtime=commons.currenttimemillis()
#        res.serverstartime=serverstartime
        self.wfile.write(res.serialize().encode('utf-8'))
        print ('EXIT,', threadname)
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    """Handle requests in a separate thread."""
if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT_NUMBER), Handler)
    print ('Started cache server on port ', PORT_NUMBER)
    server.request_queue_size = 5

    server.serve_forever()

