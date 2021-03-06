#!/usr/bin/env python3

import websockets, asyncio, serial

ser = serial.Serial("/dev/ttyUSB0", 9600)

@asyncio.coroutine
def sendSensorData(websocket, path):
	while True:
		i = 0
		messages = []
		message_str = ""
		for i in range(7):
			messages[i] = str(ser.readine()).decode('utf-8')
		for message in messages:
			message_str = message_str + " " + message
		print(message_str)
		yield from websocket.send(message_str)
			
			
		
		
start_server = websockets.serve(sendSensorData, "10.0.2.3", 5557)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
	


