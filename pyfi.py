#!/usr/bin/python
import subprocess
import json
import os
import time
#Returns a list of access points
def listWifi(interface):
    out = subprocess.check_output(["iw", interface ,"scan"])
    lines = out.split("\n")
    access_points = []
    for line in lines:
        if("SSID" in line):
            access_points.append(line.replace("\tSSID: ",""))
    return access_points

#Checks if an interface is connected
def checkConnected(interface):
    time.sleep(2)
    out = subprocess.check_output(["iw",interface,"link"])
    print(out)
    if("Not connected" not in out):
        return True
    else:
        return False

#Connect to open wifi point by name
def connectOpen(interface,essid):
    out = subprocess.check_output(["iw","dev",interface,"connect",essid])
    return checkConnected(interface)

#Connect 
def connectWPA(interface,ssid,password):
    # Get current wifi information
    with open("/opt/pyfi/data.json") as data:
        wifi = json.load(data)
        data.close()
    confFile = open("/etc/wpa_supplicant/wpa_supplicant.conf","w")
    confFile.write("country=US\n")
    confFile.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
    confFile.write("update_config=1\n")
    confFile.write("network={\n")
    confFile.write("\tssid=\""+ssid+"\"\n")
    confFile.write("\tpsk=\""+password+"\"\n")
    confFile.write("\tkey_mgmt=WPA-PSK\n")
    confFile.write("}")
    confFile.close()
    #Reconfigure wpa_supplicant
    out = subprocess.check_output(["wpa_cli","-i",interface,"reconfigure"])
    print(out)
    time.sleep(1)
    print(checkConnected(interface))
    #Get ip address via dhclient
    out = subprocess.check_output(["dhclient",interface])
    #If connection was successful. save the config to the json file
    if(checkConnected(interface)==True):
        wifi[ssid] = {"password":password,"encryption":"WPA"}
        with open("/opt/pyfi/data.json","w") as data:
            json.dump(wifi,data)
    return checkConnected(interface)
        

