#!/usr/bin/env python
config = "/data/config.py"
from config import *
import sqlite3
import time
import datetime
currenttime = round(time.time(), 0)

try:
    histconn = sqlite3.connect(
        db_history, check_same_thread=False)
    # print "CONNECTED TO history.db"
except:
    print "COULD NOT CONNECT TO HISTORY DATABASE"



cursor_hist = histconn.execute("SELECT id, time, amount from waterchange")
for row in cursor_hist:
    keyidwc = row[0]
    thetimewc = row[1]
    durationwc = row[2]
    thetimewc = float(thetimewc)
    thetimewc = round(thetimewc, 0)
    elapsedwc = currenttime - thetimewc
    timestampwc = datetime.datetime.fromtimestamp(
        int(thetimewc)).strftime('%m-%d-%Y %H:%M:%S')
    print "TIMESTAMP: ", timestampwc, "\tDURATION: ", round(float(durationwc), 2)
    time.sleep(.1)

histconn.close()
