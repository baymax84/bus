#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import urllib2, urllib
import json
import datetime, time
import os, errno

# Equivalent to "mkdir -p" under Linux.
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# notify people that the bus is arrived.
def notify():
    print "notify"

# http://askubuntu.com/questions/108764/how-do-i-send-text-messages-to-the-notification-bubbles
def sendmessage(message):
    import subprocess
    subprocess.Popen(['notify-send', message])
    return
def sendmessage2(title, message):
    import pynotify
    pynotify.init("markup")
    notice = pynotify.Notification(title, message)
    notice.show()
    return

# receive json from url.
def request_json(url):
    request = urllib2.Request(url, headers={"Accept" : "text/html"})
    try:
        contents = urllib2.urlopen(request).read()
    except urllib2.HTTPError, e:
        print "The server couldn\'t fulfill the request."
        print "Error code: %s" % e.code
        return False
    except urllib2.URLError, e:
        print "We failed to reach a server."
        print "Reason: %s" % e.reason
        return False
    else:
        return json.loads(contents)

def check_line(linename) :
    # const define
    CITY = u"北京"

    encode_linename = urllib2.quote(linename.encode("utf8"))
    encode_city = urllib2.quote(CITY.encode("utf8"))
    url = "http://bjgj.aibang.com:8899/bjgj.php?city=" + encode_city + "&linename=" + encode_linename + "&stationNo=31&datatype=json&type=0"
    print "url : %s" % url

    data = xxutils.request_json(url)
    
    time.sleep(0.1)
    
    if data["root"]["status"] == "200" :
        print "bus has real time data"
        return True
    elif data["root"]["status"] == "502":
        print "[%s] : Message : %s" % (linename, data["root"]["message"])
        print "[%s] : Reason : line not exist" % linename
    else:
        print "Unkown error!"

    return False

#EOF
