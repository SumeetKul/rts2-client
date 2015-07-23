#!/usr/bin/env python


import rts2.json as rts2json
import params as p
import os
import sys
import time

def query_continue(question):
    prompt = "[y/n]"
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if choice == 'y':
            return
        elif choice == 'n':
            sys.exit()
        else:
            sys.stdout.write("Please respond with 'y' or 'n'.") 

#Create a JSON object:

json = rts2json.JSONProxy(url = p.xmlrpc_url,username = p.rts2_username, password = p.rts2_password, verbose = False, http_proxy=None)

def check_devices():
    json.refresh()
    Device_list = json.loadJson(path='/api/devices')
    Reqd_devices = ['C0','T0','F0','SD','EXEC']
    if all(x in Device_list for x in Reqd_devices):
        for i in range(len(Reqd_devices)):
            print "Detected", Reqd_devices[i]
            time.sleep(0.1)
        print "All devices available"
        return
    else:    
        for i in Reqd_devices:
            if i in Device_list:
                print "Detected", i
                time.sleep(0.2)
            if not i in Device_list:
                print "Cannot detect", i
                time.sleep(0.2)
        query_continue("Do you want to continue?")
    

def check_weather():
    json.refresh()
    w_elements = ['wr_rain', 'wr_wind', 'wr_humidity', 'wr_cloud']
    
    if json.getSingleValue('SD', 'good_weather', refresh_not_found = True) == 1:
        print "Weather conditions are alright"
    
    elif json.getSingleValue('SD', 'good_weather', refresh_not_found = True) == 0:
        for i in w_elements:
            if json.getSingleValue('SD', i, refresh_not_found = False) == 1:
                print "Bad Weather: Unfavourable", i[3:], "conditions"
                time.sleep(0.2)
        query_continue("Do you want to continue?")

                


        
       



        

        


