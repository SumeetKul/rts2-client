#!/usr/bin/env python
#Program asks for targets, creates target and observes.

#Import Necessary packcages
import rts2.json as rts2json, numpy as n, time, os.path, sys

tar_file = sys.argv[1]
tar_dir = 'targets/'

#if (os.path.exists('tar_info.txt')==True):


Target = n.loadtxt(tar_dir + '%s' % tar_file,str)
print 'File read at ' + time.asctime(time.localtime()) + '. \n Moving telescope to given coordinates..'
#create a json object
json = rts2json.JSONProxy(url = 'http://localhost:8889',username = 'sujay', password = 'sujaymate', verbose = False, http_proxy=None)
   
#creating target and setting exposure
json.loadJson(path='/api/cmd',args={'d':'T0', 'c' : ' move %s %s' % (Target[1],Target[2])})

#return True
#else:
#  print 'ERROR : No Target File Found'
