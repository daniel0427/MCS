#!/usr/bin/env python3
import sys
import time
import http.client as http
import urllib
import json
import Adafruit_DHT
import RPo.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
deviceId = "DHdzYoP0"
deviceKey ="8xsMRJdmpJ4TleD3"
def post_to_mcs(payload): 
	headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
	not_connected = 1 
	while (not_connected):
		try:
			conn = http.HTTPConnection("api.mediatek.com:80")
			conn.connect() 
			not_connected = 0 
		except (http.HTTPException, socket.error) as ex: 
			print ("Error: %s" % ex)
			time.sleep(10)
			 # sleep 10 seconds 
	conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
	response = conn.getresponse() 
	print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
	data = response.read() 
	conn.close() 
while True:

	SwitchStatus = GPIO.input(24)
	payload = {"datapoints":[{"dataChnId":"SwitchStatus","values":{"value":SwitchStatus}}]}
	post_to_mcs(payload)
	if( SwitchStatus == 0)
		print('Button pressed')
	else:
		print('Button released')




