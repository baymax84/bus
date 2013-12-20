import urllib2
import json
import datetime, time
import logging
import os, errno

DATADIR = "/home/chenyang/opt/bus/data"

CITY = "%E5%8C%97%E4%BA%AC"

LINELIST = [
"%E8%BF%90%E9%80%9A113(%E6%9D%A5%E5%B9%BF%E8%90%A5%E5%8C%97-%E5%90%B4%E5%BA%84)",
"%E8%BF%90%E9%80%9A113(%E5%90%B4%E5%BA%84-%E6%9D%A5%E5%B9%BF%E8%90%A5%E5%8C%97)"
]


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def try_line(linename) :
	url = "http://bjgj.aibang.com:8899/bjgj.php?city=" + CITY + "&linename=" + linename + "&stationNo=31&datatype=json&type=0"
	request = urllib2.Request(url, headers={"Accept" : "text/html"})
	contents = urllib2.urlopen(request).read()
	data = json.loads(contents)
	
	if data["root"]["status"] == "200" :
		logger.debug("download data.")
		# prepare data dir
		now = datetime.datetime.now()
		output_path = DATADIR + "/" + now.strftime("%Y%m%d")
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
		time.sleep(5)

if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('/home/chenyang/opt/bus/bus/conf/log.conf')

	logger = logging.getLogger(__name__)
	logger.debug('start...')

	main()
