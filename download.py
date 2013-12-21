#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import urllib2, urllib
import json
import datetime, time
import logging
import os, errno

DATADIR = "/home/chenyang/Dropbox/bus/data"
APPDIR = "/home/chenyang/opt/bus"

CITY = u"北京"

LINELIST = [
u"运通113(来广营北-吴庄)",
u"运通113(吴庄-来广营北)"
]


LINELIST = []
jsonfile = load(DATADIR+"/bus.json", "r")
busdata = json.load(jsonfile)
for b in busdata:
	LINELIST.append(b["aibang"])




def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def try_line(linename) :
	encode_linename = urllib2.quote(linename.encode("utf8"))
	encode_city = urllib2.quote(CITY.encode("utf8"))
	url = "http://bjgj.aibang.com:8899/bjgj.php?city=" + encode_city + "&linename=" + encode_linename + "&stationNo=31&datatype=json&type=0"
	logger.debug("url : " + url)

	request = urllib2.Request(url, headers={"Accept" : "text/html"})
	contents = urllib2.urlopen(request).read()
	data = json.loads(contents)
	
	if data["root"]["status"] == "200" :
		logger.debug("download data.")
		# prepare data dir
		now = datetime.datetime.now()
		output_path = DATADIR + "/" + now.strftime("%Y%m%d") + "/" + linename
		output_file = output_path + "/" + now.strftime("%Y%m%d_%H%M%S") + ".json"
		mkdir_p(output_path)
		# save data to file
		logger.debug("write data to file : " + output_file)
		text_file = open(output_file, "w")
		text_file.write(contents)
		text_file.close()
	else :
		logger.debug( linename + " : night")

def main():

	for ln in LINELIST:
		try_line(ln)
		time.sleep(2)

if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig(APPDIR+'/bus/conf/log.conf')

	logger = logging.getLogger(__name__)
	logger.debug('start...')

	main()
