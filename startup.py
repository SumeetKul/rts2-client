#!/usr/bin/env python


import rts2.json as rts2json
import params as p
import os
import sys
import time
import commands
from datetime import datetime

def query_continue(question):                                      #In case of startup difficulties, provides an option to continue or abort.
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
            print "*Detected", Reqd_devices[i]                       #Prints out a list of devices iff ALL required devices are available.
            time.sleep(0.1)
        print "All devices available\n"
        return
    
    else:    
        for i in Reqd_devices:
            if i in Device_list:
                print "*Detected", i                                 #Prints out all detected devices, followed by any missing devices.
                time.sleep(0.2)                                     
            if not i in Device_list:
                print "*Cannot detect", i
                time.sleep(0.2)
        query_continue("Do you want to continue?")                  #Provides an option to continue
    

def check_weather():
    json.refresh()
    w_elements = ['wr_rain', 'wr_wind', 'wr_humidity', 'wr_cloud']
    
    if json.getSingleValue('SD', 'good_weather', refresh_not_found = False) == 1:
        print "Weather conditions are alright\n"
    
    else:
         if json.getSingleValue('SD', 'good_weather', refresh_not_found = False) == 0:
        
             for i in w_elements:
                 if json.getSingleValue('SD', i, refresh_not_found = False) == 1:
                     print "*Bad Weather: Unfavourable", i[3:], "conditions"
             print "*Bad weather: Cause unknown.\n"
             query_continue("Do you want to continue?")
             
             


def check_time():
    json.refresh()
    print "Time:", time.ctime()
    t = {0:'Day', 1:'Evening', 2:'Dusk', 3:'Night', 4:'Dawn', 5:'Morning', 6:'Soft-Off', 2147483696:'Hard-Off'}
    print "The centrald is in", t[json.getState('centrald')], "state."
    print "Next state:", t[json.getValue('centrald','next_state',refresh_not_found = False)]
    
    fmt = "%H:%M:%S"
    if json.getValue('centrald','next_state',refresh_not_found = False) in [0, 1, 2, 4, 5]:
        d = datetime.strptime(time.ctime(json.getValue('centrald','dark_beginning',refresh_not_found = False)), "%a %b %d %H:%M:%S %Y")
        print "It will get dark at:", d.strftime(fmt), "\n"
        countdown()
        query_continue("Do you want to continue?") 
        
    elif json.getValue('centrald','next_state',refresh_not_found = False) == 2147483696:
        print "hang on..."     
        
      
      
def check_rts2():
    if not 'rts2' in commands.getoutput('ps -A'):
        print "Error: RTS2 has not been initiated. Please start the service and try again"
        sys.exit()
    else:
        pass    
            

def countdown():
    while True:
        json.refresh()
        print '\r', time.ctime(json.getValue('centrald','dark_beginning',refresh_not_found = False) - time.time()),
        sys.stdout.flush()
        time.sleep(1.0)
        


                

        
       



        

        


