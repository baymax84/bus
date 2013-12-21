#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import urllib2, urllib
import json
import datetime, time
import logging
import os, errno

DATADIR = "/home/chenyang/opt/bus/data"

APIKEY = "f41c8afccc586de03a99c86097e98ccb"

CITY = u"北京"

# data from http://www.arcgis.com/home/item.html?id=e0f8316d91fb43d49a81a76946f9a03c
infile = open(DATADIR+"/../bus/bus.txt")
ALLBUS = infile.read()

BUSLIST = ALLBUS.split(",")

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def try_line(linename) :
	encode_linename = urllib2.quote(linename)#.encode("utf8"))
	encode_city = urllib2.quote(CITY.encode("utf8"))
	url = "http://openapi.aibang.com/bus/lines?app_key=" + APIKEY + "&city=" + encode_city + "&q=" + encode_linename + "&alt=json"
	#logger.debug("url : " + url)

	request = urllib2.Request(url, headers={"Accept" : "text/html"})
	contents = urllib2.urlopen(request).read()
	data = json.loads(contents)
	print data["result_num"]
	offlinedata = {}
	offlinedata[linename] = {}
	offlinedata[linename]["aibang"] = data["lines"]["line"][0]["name"]
	with open(DATADIR+"/bus.json", "w") as outfile:
		json.dump(offlinedata, outfile)

def main():

	try_line(BUSLIST[0])
	#for b in BUSLIST:
	#	try_line(b)
	#	time.sleep(2)

if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('/home/chenyang/opt/bus/bus/conf/log.getofflinedata.conf')

	#logger = logging.getLogger(__name__)
	#logger.debug('start...')

	main()
