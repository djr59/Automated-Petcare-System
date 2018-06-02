enable_level_warning = False
#setting the above value of either 'True' or 'False' will turn on/off text notifications for when the food and water resevoir 
#go below the Warning level defined below as foodWL and waterWL
#where 'True' means texts will be sent and "False' means texts will not be sent

enable_dispense_warning = False
#setting the above value of either 'True' or 'False' will turn off text notifications for when
#food or water is dispensed
#where 'True' means texts will be sent and "False' means texts will not be sent

foodWL = 30.0
#change the above number to any value followed by a '.' and some any number 0-9
#this value is your food reservoir "Warning Level" percentage
#for example if you want a notice when the reservoir is below 30% input: 30.0 as the number 
#or simply make the line look exactly like this: foodWL = 30.0

waterWL = 25.0
#change the above number to any value followed by a '.' and any number 0-9
#this value is your water reservoir "Warning Level" percentage
#the below green text will give an example on how to set it to your preference:
#for example if you want a notice when the reservoir is below 25.5% input: 25.5 as the number 
#or simply make the line look exactly like this: waterWL = 25.5

phone_number = "4126510478"
#this is where you place the 10-digit phone number that you would like to receive texts on
#simply put your desired phone number in between the "" as above

WATER_FEED_FILE = "/home/pi/Food_Water_Files/water-feed-status.txt"
#used for website to gather information

#negative logic
on = False
off = True

#posetive logic
Ledon = True
Ledoff = False

# GPIO pins used:

LASER   = 22
FORWARD = 17
WATER   = 27
