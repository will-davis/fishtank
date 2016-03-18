#!/usr/bin/env python
config = "/data/config.py"
from config import *
import sys
sys.path.append('/opt/rrdtool-1.4.3/lib/python2.7/site-packages/')
import rrdtool



def createrrd():
    ret = rrdtool.create(rrd_db, "--step", "10", "--start", '0',
                         "DS:ph:GAUGE:600:U:U",
                         "DS:temp:GAUGE:600:U:U",
                         "DS:sump:GAUGE:600:U:U",
                         "RRA:AVERAGE:0.5:1:600",
                         "RRA:AVERAGE:0.5:6:700",
                         "RRA:AVERAGE:0.5:24:775",
                         "RRA:AVERAGE:0.5:288:797",
                         "RRA:MAX:0.5:1:600",
                         "RRA:MAX:0.5:6:700",
                         "RRA:MAX:0.5:24:775",
                         "RRA:MAX:0.5:444:797")
    if ret:
        print rrdtool.error()

createrrd()
