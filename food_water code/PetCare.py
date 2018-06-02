#PetCare.py
import pet_parameters
import time
import sys
import RPi.GPIO as GPIO
from twilio.rest import TwilioRestClient

waterWL = pet_parameters.waterWL
enable_dispense_warning = pet_parameters.enable_dispense_warning
enable_level_warning = pet_parameters.enable_level_warning
phone_number = pet_parameters.phone_number


account_sid = "AC896072c13ab71360041195c15c7148dd"
auth_token = "e2abc9840535f491ad56df638c3629a3"

client = TwilioRestClient(account_sid, auth_token)

GPIO.setup(18,GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Water Reservoir Sensor
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Water Bowl Sensor
print GPIO.input(7)
print GPIO.input(8)



WATER_FEED_FILE = "/home/pi/Food_Water_Files/water-feed-status.txt"

# time to sleep between operations in the main loop
SleepTimeWater = 14 # Length of time, in seconds, solenoid valve remains open
SleepTimeDelay = 5 # Length of time, in seconds, between feedings



# Main Loop
while True:

  time.sleep(SleepTimeDelay); # Delay
 

  # Turn on LED if water reservoir is empty
  #GPIO.setmode(GPIO.BCM)
  
  if (GPIO.input(7) == 0):
    #GPIO.setup(18,GPIO.OUT)
    print "LED on"
    GPIO.output(18,GPIO.HIGH)
    #GPIO.cleanup()
  else:
    print "LED off"
    GPIO.output(18,GPIO.LOW)

  if ((GPIO.input(8) == 1) & (GPIO.input(7) == 1)):
    #GPIO.setmode(GPIO.BCM)
	
    
    statusFile = open(WATER_FEED_FILE, "r")
    print("file opened")
    food_percent = statusFile.readline()
    water_percent = statusFile.readline()
    statusFile.close()
	  
	# x = percentage of water left before a watering occured = x
    x = float(water_percent)
	
	# y is the flow rate of water estimated from our linear estimation below
    y = 0.0067*x + 0.2063
	
	# z is the oz or % of water delivered for our SleepTimeWater watering time
    z = y*SleepTimeWater
    	
    #check if the % remaining was 0 before a watering and set water delivered to 0
    if (x == 0):
        y = 0
        z = 0


    print("wateringPercent: " + str(x))		
      

		

    # init list with pin numbers
	#left the pinlist here to have access to all 8 relays if need be
    #pinList = [17, 27, 22, 10, 9, 11, 24, 25]
    # loop through pins and set mode and state to 'low'
    #for i in pinList:
	
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
	
	
    print "Watering"
    GPIO.output(27, GPIO.LOW)   # Open Solenoid Valve
    time.sleep(SleepTimeWater); # Keep Solenoid Valve open
    GPIO.output(27, GPIO.HIGH)  # Close Solenoid Valve
    print "End Watering"
    #GPIO.cleanup() #may not need here
	  
    if enable_dispense_warning:
        print("alerting user of a watering that took place")
        client.messages.create(to="+1" + phone_number,
        from_="+14128880750",
        body="A watering just occured! To turn off this text warning run the command Settings and set (enable_dispense_warning = false) rather than true")
		
    x = x - z # subtract the ater percent that we started the watering at with the percent we estimated that we delivered
	
    #check if the water remining in the reservoir was less than or = to zero	
    if x <= 0: 
      x = 0
      print("waterRemaining is potentially 0")  
    #check to see if we need to text the user of a food % remaining that is below their Warning Level	
    if x <= waterWL and enable_level_warning:
        time.sleep(5);
        print("trying to warn")
        client.messages.create(to="+1" + phone_number,
        from_="+14128880750",
        body="your water remaining % is " + str(x) + " which is below your current warning level of: " + str(waterWL) + "#")   
           

    print("New waterRemaining = " + str(x))
    water_percent = str(x) + "\n"
    
	#update the water % remaining in the reservoir
    statusFile = open(WATER_FEED_FILE, "w")
    statusFile.write(food_percent)
    statusFile.write(water_percent)
    statusFile.close()
	  
   
    print "ending Watering cycle"	
    SleepTimeDelay = 5
    print "SleepTimeDelay reset to its standard 5 second interval"
	
	
	
  else:
    #GPIO.cleanup()
    print "Waiting To Water"
    #incrememnt time delay so that the system isnt checking so frequently when user is away
    #for a long period of time or when system has no function to activate
    SleepTimeDelay = SleepTimeDelay + .5
    print "SleepTimeDelay was increased by a half of a second"
    if SleepTimeDelay >= 20:
       SleepTimeDelay = 20	
       print "SleepTimeDelay was truncated to its maximum of 20 seconds"
#End Loop
