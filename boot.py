#!/usr/bin/python
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import RPi.GPIO as GPIO
import subprocess
import datetime
import os
import widgets
import json
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Input pins:
L_pin = 27 
R_pin = 23 
C_pin = 4 
U_pin = 17 
D_pin = 22 

A_pin = 5 
B_pin = 6 


GPIO.setmode(GPIO.BCM) 

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

#Dictionary of Months for Watch
months = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

#List of menu items
menuItems = []
directory = os.listdir("/opt/interface/Apps")
for item in directory:
    if(os.path.isfile("/opt/interface/Apps/"+item)==True and "boot.py" not in item):
        menuItems.append(item)
menuItems.sort()

# Load default font.
font = ImageFont.load_default()

upPressed = False
downPressed = False
mode = 0
#Create menuWidget object
menu = widgets.menuWidget(x,top+24,draw,3)

for item in menuItems:
    menu.addItem(item)

while True:

    #Get the Current Time to display
    now = datetime.datetime.now()
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    # Write two lines of text.
    if(now.hour>12):
        hour = str(now.hour-12)
        ampm = "PM"
    elif(now.hour==12):
        hour = str(now.hour)
        ampm = "PM"
    else:
        hour = str(now.hour)
        ampm = "AM"
    #Draw the Date and Time at the top of the screen
    if(mode < 2):
        currentTime = str(hour) + ":" + str(now.minute) + ":" + str(now.second) + " " + ampm
        currentDate = months[now.month] + " " + str(now.day) + ", " + str(now.year)
        draw.text((x, top),currentDate,font=font,fill=255)
        draw.text((x, top+8),currentTime,  font=font, fill=255)
    if(mode < 1):
        menu.processEvents()
   
    #Check for notifications
    try:
        with open("/opt/interface/notifications.json") as data:
            notifications = json.load(data)
            data.close()
        if(len(notifications)>0):
            for key,value in notifications.iteritems():
                mesg = widgets.messageWidget(draw,image,disp,key,value)
                mesg.show()
            with open("/opt/interface/notifications.json","w") as data:
                json.dump({},data)
    except:
        pass

    #Running a Program
    if GPIO.input(A_pin):
        pass
    else:
        os.execv("/opt/interface/Apps/" + menu.getItem(0),[""])
    #Switch Display Mode
    if GPIO.input(C_pin):
        pass
    else:
        mode+=1
        if(mode>2):
            mode=0
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
