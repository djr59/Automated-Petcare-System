import os

food_hour_array = []
food_min_array = []
food_serving_array = []

Feedings = int(raw_input("how many feedings a day "))
while Feedings < 1 or Feedings > 10:
	print "Invalid feedings per day, must be 1-10"
	Feedings = int(raw_input("how many feedings a day "))

i = 1
#run a loop to get the users input for how many feedings they want a day 
#what times they want those feedings
#and what serving sizes they want dispensed from those feedings
while i <= Feedings:

	number = int(raw_input("Enter feeding hour " + str(i) + ": "))
	while number < 0 or number > 23:
		print "Invalid hour, must be 0 - 23"
		number = int(raw_input("Enter feeding hour " + str(i) + ": "))
	food_hour_array.append(number)

	number = int(raw_input("Enter feeding minute " + str(i) + ": "))
	while number < 0 or number > 59:
		print "Invalid minute, must be 0 - 59"
		number = int(raw_input("Enter feeding minute " + str(i) + ": "))
	food_min_array.append(number)

	number = int(raw_input("Enter feeding serving size " + str(i) + ": "))
	while number < 0 or number > 10:
		print "Invalid serving size, must be 1 - 10"
		number = int(raw_input("Enter feeding serving size " + str(i) + ": "))
	food_serving_array.append(number)

	i = i + 1	 
	
	
	

cronFile = open("/home/pi/Food_Water_Files/Schedule.txt", "w")

#create a cronfile formatted text file that will use cron to run feedings at specified times
i = 0
while i < Feedings:
	cronFile.write(str(food_min_array[i]) + " " + str(food_hour_array[i]) + " * * * python /home/pi/Food_Water_Files/feed.py " + str(food_serving_array[i]) + "\n")
	i = i + 1

cronFile.close()


