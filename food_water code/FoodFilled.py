#!/usr/bin/env python

import pet_parameters
import sys

foodWL = pet_parameters.foodWL
WATER_FEED_FILE = "/home/pi/Food_Water_Files/water-feed-status.txt"

# Get the new food fill level
foodLevel = float(sys.argv[1])

#error checking: make sure the user fills the tank more than their warning level
if foodLevel <= foodWL:
   print "You must fill the food to more than " + str(foodWL)
   quit()

#error checking: make sure the user didnt put a value over 100% in the foodlevel
if foodLevel > 100:
   print "WARNING: Food level truncated to 100.0%"
   foodLevel = 100.0

#read and write to the file the updated information then close the file
statusFile = open(WATER_FEED_FILE, "r")
food_percent = statusFile.readline()
water_percent = statusFile.readline()
statusFile.close()
    
food_percent = str(foodLevel) + "\n"
    
statusFile = open(WATER_FEED_FILE, "w")
statusFile.write(food_percent)
statusFile.write(water_percent)
statusFile.close()
