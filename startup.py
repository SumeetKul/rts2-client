#!/usr/bin/env python


import rts2.json as rts2json
import params as p
import os
import sys
import time


#Create a JSON object:

json = rts2json.JSONProxy(url = p.xmlrpc_url,username = p.rts2_username, password = p.rts2_password, verbose = False, http_proxy=None)

def check_devices():
    Device_list = json.loadJson(path='/api/devices')
    Reqd_devices = ['C0','T0','F0','SD','EXEC']
    if all(x in Device_list for x in Reqd_devices):
        for i in range(len(Reqd_devices)):
            print "Detected", Reqd_devices[i]
            time.sleep(0.1)
        print "All devices available"
    else:    
        for i in Reqd_devices:
            if i in Device_list:
                print "Detected", i
                time.sleep(1.0)
            if not i in Device_list:
                print "Cannot detect", i
        time.sleep(1.0)
        print "Exiting client"
        time.sleep(1.0)
        sys.exit()



        

        


