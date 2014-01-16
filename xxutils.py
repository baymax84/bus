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

#EOF