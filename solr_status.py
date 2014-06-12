#!/bin/env python
# Copyright David Bundgaard (C) 2014
# Email: dapoman@gmail.com
# Made to help out with import and cleaning
# import every 15 minute in cron
# clean every other 15 minute in cron
import httplib
import urllib
import re
import sys
from time import sleep
from datetime import datetime, timedelta
import urllib2
def minutes(minutes):
	return (datetime.utcnow() - timedelta(seconds=60*minutes)).strftime("%Y-%m-%dT%H:%M:%Sz")

def dbnow():
	return (datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%Sz")
	
def fullimport():
	conn = httplib.HTTPConnection('localhost:8082')
	conn.set_debuglevel(9)
	conn.request('GET','/solr3/xplaycms/dataimport?command=full-import&clean=false')
	resp = conn.getresponse()
	print resp.status, resp.reason
	data = resp.read()
	conn.close()
	print data
	
def clean_specific(frome, to=None):
	xml = """<delete><query>index_time_s:[{0} TO {1}]</query></delete>""".format(frome, to)
	params = urllib.urlencode({'commit':'true'})
	headers = {
		'Content-Type':'application/xml', 
		'Content-Length':"%d" % (len(xml)),
	
	}
	conn = httplib.HTTPConnection('localhost:8082')
	conn.set_debuglevel(9)
	conn.request('POST','/solr3/xplaycms/update?commit=true',headers=headers)
	conn.send(xml)
	resp = conn.getresponse()
	print resp.status, resp.reason
	conn.close()

def clean_all():
	xml = "<delete><query>*:*</query></delete>"
#	params = urllib.urlencode({'commit':'true'})
	headers = {
		'Content-Type':'text/xml',
		'Content-Length': "%d" % (len(xml)),
	}
	conn = httplib.HTTPConnection('localhost:8082')
	conn.set_debuglevel(9)
	conn.request('POST', '/solr3/xplaycms/update?commit=true',headers= headers)
	conn.send(xml)
	resp = conn.getresponse()
	print resp.status, resp.reason
	conn.close()

def status():
	conn = httplib.HTTPConnection('localhost:8082')
	conn.request('GET','/solr3/xplaycms/dataimport?command=status')
	resp = conn.getresponse()
#	print resp.status, resp.reason
	data = resp.read()
	conn.close()
#	print data
	pattern = re.compile(r'idle',re.U | re.M)
	match = re.search(pattern,data)
	if match:
		return 0
	else:
		return 1

def loop():
	while True:
		returnCode = status()
		if returnCode == 0:
			print "{0}, done, with dataimport".format(dbnow())
			sys.exit(0)
		sleep(10)

if __name__ == '__main__':
	import getopt
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hfc",["help","fullimport","clean"])
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	if not opts:
		print "Usage: {0} [-h, -f, -c] | [--help, --fullimport, --clean]".format(sys.argv[0])
		sys.exit(5)
	for opt, arg in opts:
		if opt in ('-h','--help'):
			print "Usage: {0} [-h, -f, -c] | [--help, --fullimport, --clean]".format(sys.argv[0])
			sys.exit(3)
		elif opt in ('-f','--fullimport'):
			fullimport()
			loop()
		elif opt in ('-c', '--clean'):
			clean_specific(minutes(30), minutes(15))
			loop()
		else:
			print "No option given"
			sys.exit(4)
#	start = dbnow()
#	print dbnow()
#	#fullimport()
#	clean_specific(minutes(30),minutes(15))
#
#	loop()
