#!/usr/bin/env python

import pet_parameters
import time
import sys
import RPi.GPIO as GPIO
from twilio.rest import TwilioRestClient

on = pet_parameters.on
off = pet_parameters.off
foodWL = pet_parameters.foodWL
enable_dispense_warning = pet_parameters.enable_dispense_warning
enable_level_warning = pet_parameters.enable_level_warning
phone_number = pet_parameters.phone_number

account_sid = "AC896072c13ab71360041195c15c7148dd"
auth_token = "e2abc9840535f491ad56df638c3629a3"

client = TwilioRestClient(account_sid, auth_token)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

FEEDER_MOTOR = 17
WATER_FEED_FILE = "/home/pi/Food_Water_Files/water-feed-status.txt"

# This is the number of seconds to run the feeder motor to
# deliver one serving of food
# This needx to be updated to the actual feeder spec
FEED_SERVING_TIME = 5

# This is the number of servings in a full food reservoir.
# This needs to be updated to match the actual container size in servings.
SERVINGS_PER_CONTAINER = 20

GPIO.setup(FEEDER_MOTOR, GPIO.OUT)

# Get the serving size from the command line
serving = int(sys.argv[1])

print("Serving = " + str(serving))

# Calculate the number seconds the feeding motor needs to be on
feedTime = serving * FEED_SERVING_TIME

# Calculate the percentage of food this will dispense from the container
feedingPercent = float(serving) / SERVINGS_PER_CONTAINER * 100.0

print("feedingPercent" + str(feedingPercent))

# Do the feeding
GPIO.output(FEEDER_MOTOR, on)

time.sleep(feedTime)

GPIO.output(FEEDER_MOTOR, off)

#GPIO.cleanup() #may not need here

# Update the food remaining file

if enable_dispense_warning:
      print("alerting user of a feeding that took place")
      client.messages.create(to="+1" + phone_number,
      from_="+14128880750",
      body="A feeding just occured! To turn off this text warning run the command Settings and set (enable_dispense_warning = false) rather than true")


try:
    #open the file stat has the stored values for % remaining of the food and water reservoirs
    statusFile = open(WATER_FEED_FILE, "r")
    print("file opened")
    food_percent = statusFile.readline()
    water_percent = statusFile.readline()
    statusFile.close()
    
	#get the % remaining in the food reservoir
    foodRemaining = float(food_percent)
    print("foodRemaining = " + str(foodRemaining))
	#calculate the new percent remaining
    foodRemaining = foodRemaining - feedingPercent

    #check if there is no potential food left
    if foodRemaining <= 0: 
         foodRemaining = 0
         print("foodreaming is potentially 0")
    if foodRemaining <= foodWL and enable_level_warning:
         #check if the user set text warning level is active and triggered
         time.sleep(5);
         print("trying to warn")
         client.messages.create(to="+1" + phone_number,
         from_="+14128880750",
         body="your potential food remaining % is " + str(foodRemaining) + " which is below your current warning level of: " + str(foodWL) + "%")   


    print("New foodRemaining = " + str(foodRemaining))
    food_percent = str(foodRemaining) + "\n"
    
	#update the file by writing to it the new values and close it
    statusFile = open(WATER_FEED_FILE, "w")
    statusFile.write(food_percent)
    statusFile.write(water_percent)
    statusFile.close()

except:
    print "ERROR: Cannot update the status file, make sure it is created"


