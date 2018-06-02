# Import necessary files
import serial
import pet_parameters
from twisted.web.resource import Resource

import RPi.GPIO as GPIO

on = pet_parameters.on
off = pet_parameters.off

LASER = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LASER, GPIO.OUT)

# Setup Arduino at correct speed
try:
        arduino = serial.Serial('/dev/ttyUSB0', 9600)
except:
        arduino = serial.Serial('/dev/ttyUSB1', 9600)

class MoveServo(Resource):
        isLeaf = True
        def render_GET(self,request):
                try:
               		# If we get "0L" or "1L" we need to switch the laser
			if request.args['value'][0] == "0L":
			    GPIO.output(LASER, off)
			elif request.args['value'][0] == "1L":
			    GPIO.output(LASER, on)

               		# Else send value over serial to the Arduino
			else:
                            arduino.write(request.args['value'][0])

                        return 'Success'
                except:
                        return 'Failure'

resource = MoveServo()
