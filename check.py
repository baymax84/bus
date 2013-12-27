#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import urllib2, urllib
import json
import datetime, time
import logging
import os, errno


def check_line(linename) :
	# const define
	CITY = u"北京"

	encode_linename = urllib2.quote(linename.encode("utf8"))
	encode_city = urllib2.quote(CITY.encode("utf8"))
	url = "http://bjgj.aibang.com:8899/bjgj.php?city=" + encode_city + "&linename=" + encode_linename + "&stationNo=31&datatype=json&type=0"
	print("url : " + url)

	request = urllib2.Request(url, headers={"Accept" : "text/html"})
	contents = urllib2.urlopen(request).read()
	data = json.loads(contents)
	
	if data["root"]["status"] == "200" :
		print("bus has real time data")
		return True
	elif data["root"]["status"] == "502":
		print("[%s] : Message : %s", linename, data["root"]["message"])
		print("[%s] : Reason : Night or line not exist", linename)
	else:
		print("Unkown error!")

	return False

#EOF
