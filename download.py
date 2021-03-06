#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import urllib2, urllib
import json
import datetime, time
import logging
import os, errno

import xxutils

DATADIR = "/home/chenyang/Dropbox/bus/data"
APPDIR = "/home/chenyang/opt/bus"
BUSFILE = DATADIR + "/bus.json"

CITY = u"北京"

# cor debug
LINELIST = [
u"运通113(来广营北-吴庄)",
u"运通113(吴庄-来广营北)"
]

def try_line(linename) :
	encode_linename = urllib2.quote(linename.encode("utf8"))
	encode_city = urllib2.quote(CITY.encode("utf8"))
	url = "http://bjgj.aibang.com:8899/bjgj.php?city=" + encode_city + "&linename=" + encode_linename + "&stationNo=31&datatype=json&type=0"
	logger.debug("url : " + url)

	data = xxutils.request_json(url)
	
	if data["root"]["status"] == "200" :
		logger.debug("download data.")
		# prepare data dir
		now = datetime.datetime.now()
		output_path = DATADIR + "/" + now.strftime("%Y%m%d") + "/" + linename
		output_file = output_path + "/" + now.strftime("%Y%m%d_%H%M%S") + ".json"
		xxutils.mkdir_p(output_path)
		# save data to file
		logger.debug("write data to file : " + output_file)
		text_file = open(output_file, "w")
		text_file.write(contents)
		text_file.close()
	elif data["root"]["status"] == "502":
		logger.debug("[%s] : Message : %s", linename, data["root"]["message"])
		logger.debug("[%s] : Reason : Night or line not exist", linename)
	else:
		logger.debug("Unkown error!")

def main():

	LINELIST = []
	jsonfile = open(BUSFILE, "r")
	busdata = json.load(jsonfile)
	for b, v in busdata.items():
		logger.debug("check real time data : %s", b)
		if v["real"] == "False":
			logger.debug("bus dont have real time data")
			continue
		else:
			logger.debug("bus has real time data")
			LINELIST.append(v["real"])

	for ln in LINELIST:
		try_line(ln)
		time.sleep(0.1)

if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig(APPDIR+'/bus/conf/log.conf')

	logger = logging.getLogger(__name__)
	logger.debug('start...')

	main()
