#!/usr/bin/env python

import requests, os, time, numpy as n, params as p, sys

#tar_dir = "targets/"

def http_req():
	try:
		r = requests.get(p.url)
		if 'target' in r.headers:
			if r.headers['target']:
				filename =  time.strftime("%Y%m%d_%H%M%S") + '.txt'
				n.savetxt(p.tar_dir + filename, [r.content], fmt = '%s')
				print  'Target file detected'
				return 1, filename
			else:
				return 0, r.content
		else:
			return 0, 'Server Error'
	except:
		e = sys.exc_info()
		print e

