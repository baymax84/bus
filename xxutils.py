#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os, errno

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
import subprocess
def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

import pynotify
def sendmessage2(title, message):
    pynotify.init("markup")
    notice = pynotify.Notification(title, message)
    notice.show()
    return

#EOF
