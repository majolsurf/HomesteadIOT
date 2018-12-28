#this example reads and prints CO2 equiv. measurement, TVOC measurement, and temp every 2 seconds
  
import time
from time import sleep
from datetime import datetime
from Adafruit_CCS811 import Adafruit_CCS811
import numpy as numps
from numpy import median
from numpy import average
import urllib2

enableMedianFilter = 1;

api_key = "4XDQTWMA445DHJNV"
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % api_key

ccs =  Adafruit_CCS811()
sleep_time = 15;
longest_ts = 60*60/15; #Update Every 15 minutes
samples = 4*longest_ts/sleep_time;#1024;
minibuffSamples = 4;
sig_co2 = [0 for i in range(samples)]
sig_tvoc = [0 for i in range(samples)]
sig_temp = [24 for i in range(samples)]
minibuff_co2 = [0 for i in range(minibuffSamples)]
minibuff_tvoc = [0 for i in range(minibuffSamples)]
minibuff_temp = [24 for i in range(minibuffSamples)]

while not ccs.available():
        print "Inside While Loop 1"    
	pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

samp_i = 0;

while(1):
	try:
            ccs_avail = ccs.available();
        except:
            ccs_avail = 0;
	#if ccs.available():
        if ccs_avail:
            try:
                temp = ccs.calculateTemperature()
	    except:
                temp = temp;
            try:
                ccsReadData = ccs.readData();
            except:
                ccsReadData = ccsReadData;
            
	    if not ccsReadData:
              try:  
                  stor_tvoc = ccs.getTVOC();
              except:
                  stor_tvoc = stor_tvoc;
              try:
                  stor_co2 = ccs.geteCO2();
              except:
                  stor_co2 = stor_co2;
                
              if enableMedianFilter == 1:  
                  minibuff_temp = minibuff_temp[1::] + minibuff_temp[:1:];
                  minibuff_tvoc = minibuff_tvoc[1::] + minibuff_tvoc[:1:];
                  minibuff_co2 = minibuff_co2[1::] + minibuff_co2[:1:];
                  minibuff_temp[-1] = temp;
                  minibuff_tvoc[-1] = stor_tvoc;
                  minibuff_co2[-1] = stor_co2;
              
                  temp = median(minibuff_temp);
                  stor_tvoc = median(minibuff_tvoc);
                  stor_co2 = median(minibuff_co2);
            
              stor_datetime = str(datetime.now());
	      print "Time: ",stor_datetime,"  CO2: ", stor_co2, "ppm, TVOC: ", stor_tvoc, " temp: ", temp
	      wfile = open("log_air_quality.txt", "a+")
              wfile.write(str(stor_datetime)+","+str(temp)+","+str(stor_co2)+","+str(stor_tvoc)+"\n")
              wfile.close()
              sig_temp = sig_temp[1::] + sig_temp[:1:];
              sig_tvoc = sig_tvoc[1::] + sig_tvoc[:1:];
              sig_co2 = sig_co2[1::] + sig_co2[:1:];
              sig_temp[-1] = temp;
              if stor_tvoc < 65535:
                  sig_tvoc[-1] = stor_tvoc;
              else:
                  sig_tvoc[-1] = sig_tvoc[-2];
              if stor_co2 < 65535:
                  sig_co2[-1] = stor_co2;
              else:
                  sig_co2[-1] = sig_co2[-2];
          
	    else:
	      print "ERROR!"
	      while(1):
	      	pass
	
        try:
          f = urllib2.urlopen(baseURL + 
                                "&field1=%s" % (temp) +
                                "&field3=%s" % (stor_co2) +
				"&field5=%s" % (stor_tvoc))
          print f.read()
          f.close()
        except:
          print 'Dumped by thingspeak channel export.'
          #break

	sleep(sleep_time)
	
	if samp_i < samples:
            samp_i = samp_i+1;
        else:
            samp_i = 0;
            try:
              f = urllib2.urlopen(baseURL + 
                                    "&field2=%s" % (average(sig_temp)) +
                                    "&field4=%s" % (average(sig_co2)) +
                                    "&field6=%s" % (average(sig_tvoc)))
              print f.read()
              f.close()
            except:
              print 'Dumped by thingspeak channel export.'
            
