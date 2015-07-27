# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
import os
import subprocess

import params as p
import jsoncalls as j
from request import http_req
from transitions import Machine
from transitions import State


class client(object):
    sleep = False
    queue   = 1 
    obs_id  = 0 
    next_id = 0     
    def check_lock(self):
        subprocess.call(["python","/home/sirius/Downloads/daemon-example.py","start"])
    def check_gw_trig(self):
        while sleep == False:										#System On loop
          current_id = j.getid()
          queue,target_file = http_req()							#Request for new target
          if queue == 1:
              print 'GW trig found!'
              j.create_obj(target_file)
              self.Time_check()
              break
          else:
              return
    def Time_check(self):
       try:	
           json.loadJson(path='/api/change_script',args={'id':'%d' % ID,'c':'C0','s':'for %d { E %d }' % (target.No_exp, target.Exp_time)})
           print 'Target Created At' + time.asctime(time.localtime()) + ' with ID %d' % ID
			
                                      #Checking Constraint

           exp_end = json.loadJson(path='/api/get',args={'d':'C0'})['d']['exposure_end']
		
           if (exp_end == None ):
               print 'Starting Observation for target ID %d at ' % ID + time.asctime(time.localtime())
               json.loadJson(path='/api/cmd',args={'d':'EXEC','c':'now %d' % ID})
               time.asctime(time.localtime())
               self.GW_trig_now()

           elif ((exp_end - time.time()) > 10.0):
               print 'Starting Observation for target ID %d at ' % ID + time.asctime(time.localtime())
               json.loadJson(path='/api/cmd',args={'d':'EXEC','c':'now %d' % ID})
               '''add backup code block here'''
               self.GW_trig_now()

           else:
               self.GW_trig_later()
               time.sleep((exp_end - time.time()))
               print 'Starting Observation for target ID %d at ' % ID + time.asctime(time.localtime())
               json.loadJson(path='/api/cmd',args={'d':'EXEC','c':'now %d' % ID})
           return ID
	
       except:
           e = sys.exc_info()[0]
           print 'Error : %s' % e

obs = client()
machine = Machine(obs)
state_A = State('Telescope_Off')
state_B = State('DND')
state_C = State('Routine_obs')
state_D = State('First_GW_obs')
state_E = State('Last_GW_obs')
machine.add_states([state_A,state_B,state_C,state_D,state_E])
machine.add_transition('DND_end', source='DND', dest='Routine_obs') 
machine.add_transition('Lock_found', source='Routine_obs', dest='DND') ###check for lock
machine.add_transition('Lock_not_found', source='Routine_obs', dest='Routine_obs') ###if lock not found
machine.add_transition('GW_trig_later', source='Routine_obs', dest='Routine_obs') ###if current not cancel
machine.add_transition('GW_trig_now', source='Routine_obs', dest='First_GW_obs') ####right now
machine.add_transition('Final_obs', source='First_GW_obs', dest='Last_GW_obs')
machine.add_transition('Dead', source='*', dest='Telescope_Off')
machine.set_state('Routine_obs')
machine.on_enter_Routine_obs('check_lock')

