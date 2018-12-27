import time
import requests
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import numpy as numps
import socket
import urllib2

# Max Nyquist Frequency is about 800Hz

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

api_key = "ZM7FSIDUHXZJYV47"
tweet_api_key = "GP84Y0LQWZ94P8Q0"

samples = 256 
channel = 0
udp_timer = 0

notch_thresh = 1000
avg_thresh = 1000 
det_thresh = [avg_thresh for i in range(samples)]

det_thresh[220] = notch_thresh
det_thresh[221] = notch_thresh
det_thresh[222] = notch_thresh
det_thresh[223] = notch_thresh
det_thresh[224] = notch_thresh



sig_v = [0 for i in range(samples)]

event_index = 0

while True:
  for i in range(len(sig_v)):
      sig_v[i] = mcp.read_adc(channel)
      time.sleep(0.005)
  dft_sig_v = numps.fft.fft(sig_v)
  abs_dft = abs(dft_sig_v[2:])

  max_index = 0
  max_value = det_thresh[0]-1 
  for i in range(len(abs_dft)):
      if abs_dft[i] > det_thresh[i]:
	if abs_dft[i] > max_value:
		max_index = i
		max_value = abs_dft[i]
  if max_index > 0:
	ts = time.ctime()
	print('Event detected', ts, max_index, max_value)
        sig_string = str(sig_v)
        sig_string_clean = sig_string.strip('[]')
	file = open("signal_geograph.txt", "a+")
	file.write(str(ts)+", "+sig_string_clean+"\n")
	file.close()
	fileb = open("log_geograph.txt", "a+")
	fileb.write(str(ts)+", "+str(max_index)+", "+str(max_value)+"\n")
	fileb.close()
	
        myDelay = 20

	udp_timer = 0 

	baseURL = 'https://api.thingspeak.com/update?api_key=%s' % api_key 
        tweetURL = 'https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key=%s'  % tweet_api_key
        tweet_status = 'Seismic Event Detected of Magnitude: %s in Bin: %s' %(max_value,max_index)
        print baseURL
    
        while True:
          try:
            f = urllib2.urlopen(baseURL + 
                                "&field1=%s" % (max_value) +
				"&field2=%s" % (max_index))
	    print f.read()
            f.close()
            
            sleep(int(myDelay))
          except:
            print 'Dumped by thingspeak channel export. Exiting.'
            break

	ff = urllib2.urlopen(tweetURL + 
                             "&status=%s" % (tweet_status)) 
	ff.close
        #sleep(int(1))
	#  except:
	#    print 'thing_tweet except'
	#    break

  UDP_IP = "192.168.0.1"
  UDP_PORT = 5005
  MESSAGE = "Geophone Active."
    
  print "UDP target IP:", UDP_IP, " Port:", UDP_PORT, " Message:",MESSAGE
  sock = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM)   # UDP
  sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	#x=1772 
	#payload = {'api_key': api_key, 'field1': str(x)}
	#r = requests.post('https://api.thingspeak.com/update?', params=payload)

