#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# builtin module

import urllib2, urllib
import json
import datetime, time
import logging
import os, errno
import stat

# custom defined

import check

DATADIR = "/home/chenyang/Dropbox/bus/data"
APPDIR = "/home/chenyang/opt/bus"

APIKEY = "f41c8afccc586de03a99c86097e98ccb"

CITY = u"北京"

# data from http://www.arcgis.com/home/item.html?id=e0f8316d91fb43d49a81a76946f9a03c
infile = open(APPDIR+"/bus/bus.test.txt")
ALLBUS = infile.read()
infile.close()

BUSLIST = ALLBUS.split(",")

G_JSON = {}

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def line_exist(line_obj, all_lines_obj):
	return False

def line2json(line_obj):
	if os.stat(DATADIR+"/bus.json")[stat.ST_SIZE] == 0:
		all_lines_obj = {}
	else:
		try:
			bus_json_file = open(DATADIR+"/bus.json", "r")
			all_lines_obj =  json.load(bus_json_file)
			bus_json_file.close()
		except ValueError:
			all_lines_obj = {}

	if line_obj["name"].encode("utf8") in all_lines_obj:
		logger.debug("line exist in json: " + line_obj["name"].encode("utf8"))
		return False

	# whether the bus line has real time data.
	isreal = "False"
	name = line_obj["name"]
	if check.check_line(name):
		logger.debug("%s has real time data.", name)
		isreal = name
	elif check.check_line(name.replace(u"路", "")):
		logger.debug("%s has real time data.", name.replace(u"路", ""))
		isreal = name.replace(u"路", "")
	elif check.check_line(name.replace(u"线", "")):
		logger.debug("%s has real time data.", name.replace(u"线", ""))
		isreal = name.replace(u"线", "")

	all_lines_obj[line_obj["name"]] = {"real" : isreal}
	logger.debug("write to json: " + line_obj["name"].encode("utf8"))
	#print("write to json: " + line_obj["name"].encode("utf8"))
	#print("write to json: " + line_obj["name"])
	#print(all_lines_obj)
	with open(DATADIR+"/bus.json", "w") as outfile:
		json.dump(all_lines_obj, outfile)#, ensure_ascii = False)

def try_line(query_line) :
	logger.debug("try line, query string is: " + query_line)
	encode_linename = urllib2.quote(query_line)#.encode("utf8"))
	encode_city = urllib2.quote(CITY.encode("utf8"))
	url = "http://openapi.aibang.com/bus/lines?app_key=" + APIKEY + "&city=" + encode_city + "&q=" + encode_linename + "&alt=json"
	#logger.debug("url : " + url)

	request = urllib2.Request(url, headers={"Accept" : "text/html"})
	contents = urllib2.urlopen(request).read()
	data = json.loads(contents)

	for line_id in range(1, int(data["result_num"])):
		line2json(data["lines"]["line"][line_id])
		#offlinedata[query_line]["aibang"] = data["lines"]["line"][0]["name"].encode("utf8")

def main():
	#try_line(BUSLIST[0])
	for idx in range(1, 1000):
		try_line(str(idx))
		time.sleep(1)
	#for b in BUSLIST:
	#	try_line(b)
	#	time.sleep(2)

if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig(APPDIR+'/bus/conf/log.getofflinedata.conf')

	logger = logging.getLogger(__name__)
	logger.debug('start...')

	main()
