#!/usr/bin/env python

import pet_parameters
import sys

waterWL = pet_parameters.waterWL
WATER_FEED_FILE = "/home/pi/Food_Water_Files/water-feed-status.txt"

# Get the new water fill level
waterLevel = float(sys.argv[1])

#error checking: make sure the user fills the tank more than their warning level
if waterLevel <= waterWL:
   print "You must fill the water to more than " + str(waterWL)
   quit()

#error checking: make sure the user didnt put a value over 100% in the waterLevel
if waterLevel > 100:
   print "WARNING: Water level truncated to 100.0%"
   waterLevel = 100.0

#read and write to the file the updated information then close the file
statusFile = open(WATER_FEED_FILE, "r")
food_percent = statusFile.readline()
water_percent = statusFile.readline()
statusFile.close()
    
water_percent = str(waterLevel) + "\n"
    
statusFile = open(WATER_FEED_FILE, "w")
statusFile.write(food_percent)
statusFile.write(water_percent)
statusFile.close()
