#!/usr/bin/python

import pet_parameters

#used to get the food remaining on the website
statusFile = open(pet_parameters.WATER_FEED_FILE, "r")

food_percent = statusFile.readline()
water_percent = statusFile.readline()
statusFile.close()

print str(food_percent)
