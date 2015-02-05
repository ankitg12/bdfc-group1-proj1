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

PORT_NUMBER = 8081

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

    def book(self,id,bookingPrice):
            print ('booking')
            res=commons.Record("")
            conn = sqlite3.connect('flightrecords.db')
            c = conn.cursor()
            cursor = c.execute('SELECT *  from flights WHERE id ='+id)
            row=cursor.fetchone()
            price = row[PMIN] + row[PRICESTEP] *  ((row[CAPCITY] - row[AVAILABLE]) // row[SEATSTEP])
            if(bookingPrice!=str(price)):           
                    res.bookingstatus="FAILED"
            else:
                    cursor = c.execute('UPDATE flights SET available = available - 1 WHERE id ='+id)
                    conn.commit()
                    res.bookingstatus="SUCCESS"
            conn.close()
            res.id=row[ID]
            res.capacity=row[CAPCITY]
            res.available=row[AVAILABLE]
            res.price = price
            res.api='BOOK'
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
        time.sleep(10)

        if self.path.startswith('/QUERY/'):
            res = self.getprice(params["id"][0])
        elif self.path.startswith('/BOOK/'):
            res = self.book(params["id"][0], params["bookingprice"][0])
        res.thread=threadname
        res.serverendtime=commons.currenttimemillis()
        res.serverstartime=serverstartime
        self.wfile.write(res.serialize().encode('utf-8'))
        print ('EXIT,', threadname)
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    """Handle requests in a separate thread."""

    def initdb(self):
        conn = sqlite3.connect('flightrecords.db')
        c = conn.cursor()
        print ('initializing db')
        c.execute('DROP TABLE IF EXISTS  flights')
        c.execute('''CREATE TABLE flights
                (id integer primary key,  capacity integer, available integer,   pMin integer,   seatStep integer,  priceStep integer)'''
                  )
        for x in range(100, 1100):
            c.execute("INSERT INTO flights (id,capacity,available,pMin,seatStep,priceStep) \
             VALUES ("+ str(x) + ', 300, 201 ,1000,50, 1000 )')
        conn.commit()
        conn.close()              


    def dumpdb(self):
        print ('dumping db')
        conn = sqlite3.connect('flightrecords.db')
        c = conn.cursor()
        cursor = c.execute('SELECT *  from flights')
        for row in cursor:
            print ('id = ', row[ID])
            print ('capacity = ', row[CAPCITY])
            print ('available = ', row[AVAILABLE])
            print ('seatTiers = ', row[SEATSTEP])
            print ('startPrice = ', row[PMIN])
            print ('priceTiers = ', row[PRICESTEP], '\n')
        conn.close()

if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT_NUMBER), Handler)
    server.initdb()
    server.dumpdb()

    print ('Started database server on port ', PORT_NUMBER)
    server.request_queue_size = 5

    server.serve_forever()

