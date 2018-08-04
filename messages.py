#!/usr/bin/python

import os
import json
import urllib
import time

def main():
    while True:
        try:
            url = "http://adamsjacket.ddns.net/messages.json"
            response = urllib.urlopen(url)
            data = json.load(response)
            with open("/opt/interface/notifications.json") as notifications:
                json_data = json.load(notifications)
                for key,value in data.iteritems():
                    json_data[key]=value
                notifications.close()
            with open("/opt/interface/notifications.json","w") as notifications:
                json.dump(json_data,notifications)
            response = urllib.urlopen("http://adamsjacket.ddns.net/clear.php?id=123654")
        except:
            pass
        time.sleep(5)
        
main()
