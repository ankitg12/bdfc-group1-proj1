import urllib.request
import csv
import commons
from SimPy.Simulation import *
from random import expovariate, seed
import time

class Source(Process):
    """ Source generates customers at random """
    def generate(self, number, meanTBA):
        print("%7.4f" % (float(random.choice('01'))))
        for i in range(number):
            c = Client(name="Clent %02d" % (i))
            #print("Time at Client generation is %7.4f " % now())
            activate(c, c.requests(clientid=i))
            t = expovariate(1.0/meanTBA) #1
            yield hold, self, t


class Client(Process):
    """ Customer arrives, looks around and leaves """
    
    def requests(self, clientid):
        test = open("Required_Parameter_for_Analysis.csv",'a')
        #print("%7.4f %s: Here I am" % (now(), self.name))
        yield hold,self,random.randint(1,10)
        #print(str(clientid))
        temp = random.randint(100,600)
        #print("Time before query is %s",now())
        test.write(str(clientid)+',') ## Client_ID
        test.write(str(now())+',') ## Client_Query_Req_Time
        req = urllib.request.Request('http://localhost:8082/QUERY/?id=%s' %str(temp))
        #print("Time after query is %s",now())
        response = urllib.request.urlopen(req)
        res=commons.Record(response.read().decode())
        test.write(res.id+',') ## Flight_ID
        test.write(str(now())+',') ## Query_Server_Reply_Time
        test.write(res.price+',') ##Query_Price
        test.write(res.available+',') ## Query_Availability
        #print(the_page)
        if random.randint(1,6)<=5:
            #print("Time before booking is %s",now())
            test.write(str(now())+',') ## Client_Book_Req_Time
            req = urllib.request.Request("http://localhost:8081/BOOK/?id=%s&bookingprice=%s" % (str(res.id),str(res.price)))
            #print("Time after booking is %s",now())
            response = urllib.request.urlopen(req)
            res=commons.Record(response.read().decode())
            test.write(str(now())+',') ## Book_Reply_Req_Time
            test.write(res.price+',') ##Book_Price
            test.write(res.available+',') ## Book_Availability
            test.write(res.bookingstatus+'\n')##Book_Status
            test.close()
        else:
            test.write(','+','+','+','+"CR"+'\n')
            test.close()
            
        

maxTime = 400.0 # minutes
ARRint = 10.0 # mean arrival interval, minutes
## Model/Experiment ------------------------------
seed(99999) #3
initialize()
s = Source(name='Source')
activate(s, s.generate(number=5,meanTBA=0.001),at=0.0)
simulate(until=maxTime)
