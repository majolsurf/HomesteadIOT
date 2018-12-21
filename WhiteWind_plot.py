#this example reads and prints CO2 equiv. measurement, TVOC measurement, and temp every 2 seconds

import time
from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
import matplotlib.pyplot as plt
import numpy as numps

ccs =  Adafruit_CCS811()
samples = 1024;
sig_co2 = [0 for i in range(samples)]
sig_tvoc = [0 for i in range(samples)]
sig_temp = [24 for i in range(samples)]
plt.ion()

while not ccs.available():
	pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

while(1):
	if ccs.available():
	    temp = ccs.calculateTemperature()
	    if not ccs.readData():
              stor_tvoc = ccs.getTVOC();
              stor_co2 = ccs.geteCO2()
	      print "CO2: ", stor_co2, "ppm, TVOC: ", stor_tvoc, " temp: ", temp
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
              
              plt.clf()
              plt.subplot(3,1,1)
              plt.plot(sig_temp)
              plt.show()
              plt.pause(0.0001)
              #plt.clf()
              
              plt.subplot(3,1,2)
              plt.plot(sig_co2)
              plt.show()
              plt.pause(0.0001)
              #plt.clf()
              
              plt.subplot(3,1,3)
              plt.plot(sig_tvoc)
              plt.show()
              plt.pause(0.0001)
              #plt.clf()
              
	    else:
	      print "ERROR!"
	      while(1):
	      	pass
	sleep(5)
