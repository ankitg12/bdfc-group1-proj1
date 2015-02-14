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
            yield hold, self, 0


class Client(Process):
    """ Customer arrives, looks around and leaves """
    
    def requests(self, clientid):
        test = open("Required_Parameter_for_Analysis.csv",'a')
        #print("%7.4f %s: Here I am" % (now(), self.name))
        yield hold,self,0
        #print(str(clientid))
        temp = random.randint(101,110)
       # temp =101
        #print("Time before query is %s",now())
        test.write(str(clientid)+',') ## Client_ID
        test.write(str(now())+',') ## Client_Query_Req_Time
        req = urllib.request.Request('http://localhost:8082/QUERY/?id=%s' %str(temp))
        #print("Time after query is %s",now())
        response = urllib.request.urlopen(req)
        res=commons.Record(response.read().decode())
        if int(res.available) < 20 and int(res.available)>0:
            time_delay = 1/int(res.available)
            #print(time_delay)
        else:
            time_delay = 0
        test.write(res.id+',') ## Flight_ID
        test.write(str(now() + time_delay) +',') ## Query_Server_Reply_Time
        test.write(res.price+',') ##Query_Prie
        test.write(res.available+',') ## Query_Availability
        #print(the_page)
        if random.randint(1,10)<=10:
            #print("Time before booking is %s",now())
            #test.write(str(now())+',') ## Client_Book_Req_Time
            req = urllib.request.Request("http://localhost:8081/BOOK/?id=%s&bookingprice=%s" % (str(res.id),str(res.price)))
            #print("Time after booking is %s",now())
            response = urllib.request.urlopen(req)
            res=commons.Record(response.read().decode())
           # test.write(str(now())+',') ## Book_Reply_Req_Time
            
            if int(res.realavailable) > 20:
                test.write(str(int(res.realprice)+500*random.randint(0,2))+',') ##Book_Price
                test.write(str(int(res.realavailable)-random.randint(0,10))+',') ## Book_Availability
            else:
                test.write(res.realprice+',') ##Book_Price
                test.write(res.realavailable+',') ## Book_Availability
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
activate(s, s.generate(number=2000,meanTBA=0.001),at=0.0)
simulate(until=maxTime)
