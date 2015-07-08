import time, params as p, jsoncalls as j, os
from request import http_req
import transitions
from transitions import Machine
from transitions import State

class client(object):
    sleep = False
    queue   = 1 
    obs_id  = 0 
    next_id = 0     
    def check_lock(self):
        while True:
            if 'lock' in os.listdir(p.lock_path):
                self.Lock_found()
            else:
                self.Lock_not_found()
                self.check_gw_trig
        return
        '''actually insert a daemon here'''
    def check_gw_trig(self):
        while sleep == False:										#System On loop
		current_id = j.getid()
		queue,tar_file = http_req()							#Request for new target
        if 
        
        
    
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
machine.add_transition('GW_trig_now', source='Routine_obs', dest='state_D') ####right now
machine.add_transition('Final_obs', source='state_D', dest='state_E')
machine.add_transition('Dead', source='*', dest='state_A')
machine.set_state('Routine_obs')
machine.on_enter_Routine_obs('check_lock')
