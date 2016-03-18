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

cursor_hist = histconn.execute("SELECT id, time, amount from topoff")
for row in cursor_hist:
    keyid = row[0]
    thetime = row[1]
    duration = row[2]
# print "ID = ", keyid
# print "RECORDED TIME = ", thetime
# print "DURATION = ", duration
thetime = float(thetime)
thetime = round(thetime, 0)
elapsed = currenttime - thetime
timestamp = datetime.datetime.fromtimestamp(
    int(thetime)).strftime('%m-%d-%Y %H:%M:%S')

print "\nTOPOFF INFORMATION"
print "TIMESTAMP", timestamp
print "TIME SINCE LAST TOPOFF = ", str(datetime.timedelta(seconds=elapsed))
print "AMOUNT ADDED (IN SECONDS) = ", round(float(duration), 2)

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
print "\nWATERCHANGE INFORMATION"
print "TIMESTAMP", timestampwc
print "TIME SINCE LAST WATERCHANGE = ", str(datetime.timedelta(seconds=elapsedwc))
print "DURATION (IN SECONDS) = ", round(float(durationwc), 2)
histconn.close()
