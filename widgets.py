
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import RPi.GPIO as GPIO
import time

class menuWidget():
    def __init__(self,xStart,yStart,drawObj,dispItems,title=""):
        #Get Object Variables
        self.x = xStart
        self.y = yStart
        self.draw = drawObj
        self.title = title
        self.length = dispItems
        self.menuItems = []
        self.font = ImageFont.load_default()
        
        #Configure GPIO Pins
        self.L_pin = 27 
        self.R_pin = 23 
        self.C_pin = 4 
        self.U_pin = 17 
        self.D_pin = 22 

        self.A_pin = 5 
        self.B_pin = 6 


        GPIO.setmode(GPIO.BCM) 

        GPIO.setup(self.A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

    def clearItems(self):
        self.menuItems = []
    
    def addItem(self,item):
        self.menuItems.append(item)

    def removeItem(self,index):
        del self.menuItems[index]

    def insertItem(self,index,item):
        self.menuItems.insert(index,item)

    def getIndex(self,item):
        for i in range(len(self.menuItems)-1):
            if(self.menuItems[i] == item):
                return i
        return -1
   
    def getItems(self):
        return self.menuItems

    def getItem(self,index):
        if(index < len(self.menuItems)):
            return self.menuItems[index]
        return "None"

    def processEvents(self):
        #Draw the menu
        if(len(self.menuItems)>0):
            self.draw.text((self.x,self.y),"[" + self.menuItems[0] + "]",font=self.font, fill=255)
        for i in range(1,self.length):
            if(i < len(self.menuItems)):
                self.draw.text((self.x,(self.y+(8*i))),self.menuItems[i],font=self.font,fill=255)
        
        #Menu Scrolling Logic
        if GPIO.input(self.D_pin): # button is released
            self.downPressed = False
        else: # button is pressed:
            if(self.downPressed==False):
                temp = self.menuItems[0]
                del self.menuItems[0]
                self.addItem(temp)
                self.downPressed=True
        if GPIO.input(self.U_pin): # button is released
            self.upPressed = False
        else:
            if(self.upPressed==False):
                temp = self.menuItems[-1]
                self.removeItem(-1)
                self.insertItem(0,temp)
                self.upPressed=True


class inputWidget():
    def __init__(self,drawObj,imageObj,dispObj,title):
        self.title = title
        self.inputStr = ""
        self.draw = drawObj
        self.image = imageObj
        self.disp = dispObj
        self.inputList = []
        self.font = ImageFont.load_default()
        self.index = 0
        self.padding = -2
        self.top = self.padding
        self.x = 0
        self.width = self.disp.width
        self.height = self.disp.height
        self.isVisible = False
        numbers = ["0","1","2","3","4","5","6","7","8","9"]
        lowercase = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        uppercase = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        special = ["!","@","#","$","%","^","&","*","(",")","-","+","-","=","{","}","[","]",":",";","\"","'",",",".","/","<",">","~","\\"," "]
        lowercase.reverse()
        uppercase.reverse()
        self.keyMaps = [numbers,lowercase,uppercase,special]
        self.keyIndex = 0
        self.mapIndex = 0

        #Configure GPIO Pins
        self.L_pin = 27 
        self.R_pin = 23 
        self.C_pin = 4 
        self.U_pin = 17 
        self.D_pin = 22 

        self.A_pin = 5 
        self.B_pin = 6 


        GPIO.setmode(GPIO.BCM) 

        GPIO.setup(self.A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

    def getInput(self):
        self.inputStr = "".join(self.inputList)
        return self.inputStr

    def show(self):
        self.inputStr = ""
        self.inputList = []
        self.isVisible = True
        time.sleep(0.5)
        while self.isVisible==True:
            #Clear the screen
            self.draw.rectangle((0,0,self.width,self.height),outline=0,fill=0)

            #Show Title
            self.draw.text((self.x,self.top),self.title,font=self.font,fill=255)
            #Show text
            self.draw.text((self.x,self.top+16),self.getInput(),font=self.font,fill=255)
            #Highlight current character
            self.draw.text((self.x,self.top+17)," "*self.index+"_",font=self.font,fill=255)
            
            #Set current character
            if(self.index < len(self.inputList)):
                try:
                    self.inputList[self.index]=self.keyMaps[self.mapIndex][self.keyIndex]
                except Exception as e:
                    print(e)
                    print(len(self.inputList))
                    print(self.index)
            else:
                self.inputList.append(self.keyMaps[self.mapIndex][self.keyIndex])
                self.index = len(self.inputList)-1
            

            #Rotate keymap
            if GPIO.input(self.C_pin):
                pass
            elif(self.mapIndex<len(self.keyMaps)-1):
                self.mapIndex+=1
                self.keyIndex=0
                time.sleep(0.1)
            else:
                self.mapIndex=0
                self.keyIndex=0
                time.sleep(0.1)

            #Rotate Character
            if GPIO.input(self.U_pin):
                pass
            elif(self.keyIndex<len(self.keyMaps[self.mapIndex])-1):
                self.keyIndex+=1
                time.sleep(0.1)
            else:
                self.keyIndex=0
                time.sleep(0.1)
            if GPIO.input(self.D_pin):
                pass
            elif(self.keyIndex>0):
                self.keyIndex-=1
                time.sleep(0.1)
            else:
                self.keyIndex = len(self.keyMaps[self.mapIndex])-1

            #Character changing
            if GPIO.input(self.L_pin):
                pass
            elif(self.index>0):
                self.index-=1
                time.sleep(0.1)

            if GPIO.input(self.R_pin):
                pass
            elif(self.index<20):
                self.index+=1
                time.sleep(0.1)

            #Delete current character
            if GPIO.input(self.B_pin):
                pass
            else:
                del self.inputList[self.index]
                self.index = len(self.inputList)-1
                if(self.index<0):
                    self.index=0
                    time.sleep(0.2)
                    return ""
                self.getInput()

            #Submit processing
            if GPIO.input(self.A_pin):
                pass
            else:
                self.isVisible = False
            #Display Screen
            self.disp.image(self.image)
            self.disp.display()
        return self.getInput()


class messageWidget():
    def __init__(self,drawObj,imageObj,dispObj,title,body=None):
        self.title = title
        self.body = body
        self.inputStr = ""
        self.draw = drawObj
        self.image = imageObj
        self.disp = dispObj
        self.inputList = []
        self.font = ImageFont.load_default()
        self.index = 0
        self.padding = -2
        self.top = self.padding
        self.x = 0
        self.width = self.disp.width
        self.height = self.disp.height
        self.isVisible = False
        self.lines = []

        #Configure GPIO Pins
        self.L_pin = 27 
        self.R_pin = 23 
        self.C_pin = 4 
        self.U_pin = 17 
        self.D_pin = 22 

        self.A_pin = 5 
        self.B_pin = 6 


        GPIO.setmode(GPIO.BCM) 

        GPIO.setup(self.A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(self.C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up


    def show(self):
        self.isVisible = True
        time.sleep(0.5)
        while self.isVisible==True:
            #Clear the screen
            self.draw.rectangle((0,0,self.width,self.height),outline=0,fill=0)

            #Show Title
            self.draw.text((self.x,self.top),self.title,font=self.font,fill=255)
            #Show body if there is one, wrapping long strings of text

            if(self.body!=None):
                if(len(self.body)<20 and len(self.lines)<1):
                    self.draw.text((self.x,self.top+8),self.body,font=self.font,fill=255)
                else:
                    while(len(self.body)>0):
                        self.lines.append(self.body[:20])
                        self.body = self.body[20:]
                    for i in range(len(self.lines)):
                        self.draw.text((self.x,self.top+((i+1)*8)),self.lines[i],font=self.font,fill=255)
            #Submit processing
            if GPIO.input(self.A_pin):
                pass
            else:
                self.isVisible = False
                time.sleep(0.2)
            #Scroll if the message is too long
            if GPIO.input(self.U_pin):
                pass
            elif len(self.lines)>7:
                self.lines.insert(0,self.lines[-1])
                del self.lines[-1]
            if GPIO.input(self.D_pin):
                pass
            elif len(self.lines)>7:
                self.lines.append(self.lines[0])
                del self.lines[0]
            #Display Screen
            self.disp.image(self.image)
            self.disp.display()
        time.sleep(0.5)
        self.lines = []
        return
    
    def flash(self):
        self.isVisible=True
        time.sleep(0.5)
        while self.isVisible==True:
            #Clear the screen
            self.draw.rectangle((0,0,self.width,self.height),outline=0,fill=0)

            #Show Title
            self.draw.text((self.x,self.top),self.title,font=self.font,fill=255)
            #Show body if there is one, wrapping long strings of text

            if(self.body!=None):
                if(len(self.body)<20):
                    self.draw.text((self.x,self.top+8),self.body,font=self.font,fill=255)
                else:
                    lines = []
                    while(len(self.body)>=20):
                        lines.append(self.body[:20])
                        self.body = self.body[20:]
                    for i in range(len(lines)-1):
                        self.draw.text((self.x,self.top+(i*8)),lines[i],font=self.font,fill=255)
            self.isVisible = False
            #Display Screen
            self.disp.image(self.image)
            self.disp.display()
        time.sleep(0.5)
        return

