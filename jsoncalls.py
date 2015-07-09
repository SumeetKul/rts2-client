#!/usr/bin/env python
#Program asks for targets, creates target and observes.

#Import Necessary packages
import rts2.json as rts2json, numpy as n, time, os.path, sys, params as p
from tar_info import Target
from socket import error as ConnectionError
import database

#tar_dir = 'targets/'

def observe(tar_file):
	try:
		target = Target()
		target.from_file(p.tar_dir + '%s' % tar_file)
		print 'File read at ' + time.asctime(time.localtime()) + '. \nCreating Target...'
               
                database.create_log(tar_file)
		
		#Create a json object
		
		json = rts2json.JSONProxy(url = p.xmlrpc_url,username = p.rts2_username, password = p.rts2_password, verbose = False, http_proxy=None)
		
		#Creating target and setting exposure
		
		ID = json.loadJson(path='/api/create_target',args={'tn':target.Name,'ra':target.RA,'dec':target.Dec,'type':'l','info':''})['id']
	
	except ConnectionError:
		print 'Error'	
		return
	
	try:	
		json.loadJson(path='/api/change_script',args={'id':'%d' % ID,'c':'C0','s':'for %d { E %d }' % (target.No_exp, target.Exp_time)})
		print 'Target Created At' + time.asctime(time.localtime()) + ' with ID %d' % ID
			
		#Checking Constraint
				
		exp_end = json.loadJson(path='/api/get',args={'d':'C0'})['d']['exposure_end']
		
		if (exp_end == None ):
			print 'Starting Observation for target ID %d at ' % ID + time.asctime(time.localtime())
			json.loadJson(path='/api/cmd',args={'d':'EXEC','c':'now %d' % ID})
			time.asctime(time.localtime())
		
		if ((exp_end - time.time()) < 10.0):
			print 'Starting Observation for target ID %d at ' % ID + time.asctime(time.localtime())
			json.loadJson(path='/api/cmd',args={'d':'EXEC','c':'now %d' % ID})
		else:
			time.sleep((exp_end - time.time()))
			print 'Starting Observation for target ID %d at ' % ID + time.asctime(time.localtime())
			json.loadJson(path='/api/cmd',args={'d':'EXEC','c':'now %d' % ID})
		
                
		return ID
	
	except :
		e = sys.exc_info()[0]
		print 'Error : %s' % e


def queue_tar(tar_file):
	try:
		target = Target()
		target.from_file(p.tar_dir + '%s' % tar_file)
		print 'File read at ' + time.asctime(time.localtime()) + '. \nCreating Target...'
		
		#Create a json object
		json = rts2json.JSONProxy(url = p.xmlrpc_url,username = p.rts2_username, password = p.rts2_password, verbose = False, http_proxy=None)
		
		#Creating target and setting exposure
		ID = json.loadJson(path='/api/create_target',args={'tn':target.Name,'ra':target.RA,'dec':target.Dec,'type':'l','info':''})['id']
		
	except ConnectionError:
		print 'Error'
		return
	
	try:
		json.loadJson(path='/api/change_script',args={'id':'%d' % ID,'c':'C0','s':'for %d { E %d }' % (target.No_exp, target.Exp_time)})
		
		#Queue Target
		json.loadJson(path='/api/cmd',args={'d':'EXEC','c':'now %d' % ID})
		
		return ID
	
	except :
		e = sys.exc_info()[0]
		print 'Error : %s' % e


def getid():
	try:
		json = rts2json.JSONProxy(url = p.xmlrpc_url,username = p.rts2_username, password = p.rts2_password, verbose = False, http_proxy=None)
		
		current_id = json.loadJson(path='/api/get',args={'d':'EXEC'})['d']['obsid']
		
		return current_id
	except:
		e = sys.exc_info()[0]
		print 'Error : %s' % e

