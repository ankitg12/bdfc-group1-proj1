#!/usr/bin/python
# print grid of all colors and brightnesses
# uses stdout.write to write chars with no newline nor spaces between them
# This should run more-or-less identically on Windows and Unix.
from __future__ import print_function
import sys

# Add parent dir to sys path, so the following 'import colorama' always finds
# the local source in preference to any installed version of colorama.
from colorama import init, Fore, Back, Style
import time

currenttimemillis = lambda: int(round(time.time() * 1000))

class Record(object):
        id=0
        price=0
        bookingprice=0
        available=0
        capacity=0
        source=""
        dest=""
        bookingstatus=""
        cached=""
        serverstartime=0
        serverendtime=0
        gatewaystartime=0
        gatewayendtime=0
        clientstarttime=0
        clientendtime=0        
        thread=0
        api=0
        customerid=""
        realprice=""
        realavailable=""
        def __init__(self, str):
                values=str.split(',')
                if (len(values)<19): values=["","","","","","","","","","","","","","","","","","","","","",""] 
                self.id=values[0]
                self.price=values[1]
                self.bookingprice=values[2]
                self.available=values[3]
                self.capacity=values[4]
                self.source=values[5]
                self.dest=values[6]
                self.bookingstatus=values[7]
                self.cached=values[8]
                self.serverstartime=values[9]
                self.serverendtime=values[10]
                self.gatewaystartime=values[11]
                self.gatewayendtime=values[12]
                self.clientstarttime=values[13]
                self.clientendtime=values[14]
                self.thread=values[15]
                self.api=values[16]
                self.customerid=values[17]
                self.realprice=values[18]
                self.realavailable=values[19]
        def log(self):
                 print(self.serialize())
        def serialize(self):
                return(str(self.id)+','+str(self.price)+','+str(self.bookingprice)+','+str(self.available)+','+str(self.capacity)+','+str(self.source)+','+
                str(self.dest)+','+str(self.bookingstatus)+','+str(self.cached)+','+str(self.serverstartime)+','+str(self.serverendtime)+','+
                str(self.gatewaystartime)+','+str(self.gatewayendtime)+','+str(self.clientstarttime)+','+str(self.clientendtime)+','+str(self.thread)+','+str(self.api)
                +','+str(self.customerid)+','+str(self.realprice)+','+str(self.realavailable)
                )
def printH1(s):
                print(Back.GREEN+s+ Fore.RESET + Back.RESET + Style.RESET_ALL)

init()

mystructure=Record('first,name,,,,,,,,,,,,,,,,,,,,,')
print(mystructure.serialize())
mystructure.log()

