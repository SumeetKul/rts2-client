#!/usr/bin/env python

import time, params as p, jsoncalls as j
from request import http_req

while True:
	sleep = False
	queue   = 1 
	obs_id  = 0 
	next_id = 0 
	
	while sleep == False:										#System On loop
		current_id = j.getid()
		queue,tar_file = http_req()							#Request for new target
	
		if current_id in [obs_id, next_id] and queue == 1:		#Check if current observation is requsted by server		
			next_id = j.queue_tar(tar_file)						#If true, then queue the newly requested target and sleep
			sleep = True	
		
		elif queue == 1:										#Else observe new target
			obs_id = j.observe(tar_file)						
			queue,tar_file = http_req()						#Request for new target
			
			while queue == 1:									 
				next_id = j.queue_tar(tar_file)					#If above request is successful, queue target
				queue,tar_file = http_req()					#Again request for new target, repeat until request returns no target.
				
				while current_id != next_id:
					time.sleep(p.rts2_poll_time)
					current_id = j.getid()
		else:
			tar_file = select_file(p.sms_path)					#If no target from server, check for sms target. If true observe else sleep.
			if tar_file == None:
				sleep = True
			else:
				obs_id = j.observe(tar_file)
	
	time.sleep(p.sleeptime)

