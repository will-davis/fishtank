#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import sqlite3
import os
config = "/data/config.py"
from config import *
global distance



GPIO.setmode(GPIO.BCM)


try:
    hotconn = sqlite3.connect(
        db_location, check_same_thread=False)
    print "CONNECTED TO hot.db"
except:
    print "COULD NOT CONNECT TO HOT DATABASE"
try:
    histconn = sqlite3.connect(
        db_history, check_same_thread=False)
    print "CONNECTED TO history.db"
except:
    print "COULD NOT CONNECT TO HISTORY DATABASE"

GPIO.setup(GPIO_OUT_ROsolenoid, GPIO.OUT)
GPIO.output(GPIO_OUT_ROsolenoid, 1)


def cleanup():
    try:
        GPIO.cleanup()
        print "GPIO Cleanup"
    except:
        print "NO GPIO UTILIZED FOR CLEANING"
    try:
        hotconn.close()
        histconn.close()
        print "DATABASE CONNECTION CLOSED"
        print "PROGRAM TERMINATED SUCCESSFULLY"
    except:
        print "NO DATABASE CONNECTION TO CLOSE"


def sql_getsump():
    try:
        cursor = hotconn.execute("SELECT id, ph, temp, sump from tank")
        for row in cursor:
            sumpdistance = row[3]
        sumpdistance = float(sumpdistance)
    except:
        print "\033[1;31m SQL_SUMP ERROR\033[1;0m"
#        os.system('/bin/echo SQL_SUMP ERROR - SHITS FUCKED YO | wall')
        return 6
    time.sleep(1)
    print sumpdistance
    return sumpdistance


def fillseq():
    global timediff
#    os.system('/bin/echo TOPOFF SEQUENCE STARTING | wall')
    try:
        print "ADDING WATER TO SUMP"
        timestart = time.time()
        while sql_getsump() > INI_distancetofill:
            GPIO.output(GPIO_OUT_ROsolenoid, 0)
            stringholder = sql_getsump()
            stringholder = str(stringholder)
#            os.system(
#                '/bin/echo ' + stringholder + ' CURRENT SUMP LEVEL | wall')
            time.sleep(1)
        GPIO.output(GPIO_OUT_ROsolenoid, 1)
        timeend = time.time()
        timediff = timeend - timestart
    except KeyboardInterrupt:
        print "Keyboard Interrupt Detected - Shutting Down"
        cleanup()


def writetopofftable():
    try:
        cursor_hist = histconn.cursor()
        endtime = time.time()
        cursor_hist.execute('''INSERT INTO topoff(time, amount)
                      VALUES(?,?)''', (endtime, timediff))
        histconn.commit()
        print "SUCCESSFULLY WROTE TO HISTORY DATABASE"
    except:
        print "COULD NOT WRITE TO HISTORY DATABASE"


fillseq()
writetopofftable()
cleanup()
#os.system('/bin/echo TOPOFF SEQUENCE DONE | wall')
