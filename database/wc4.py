#!/usr/bin/env python
config = "/data/config.py"
from config import *
import time
import RPi.GPIO as GPIO
import sys
import sqlite3
import datetime
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


GPIO.setup(GPIO_OUT_drainmotor, GPIO.OUT)
GPIO.setup(GPIO_OUT_ROsolenoid, GPIO.OUT)
GPIO.setup(GPIO_OUT_rightdose, GPIO.OUT)
GPIO.setup(GPIO_OUT_leftdose, GPIO.OUT)
GPIO.output(GPIO_OUT_drainmotor, 1)
GPIO.output(GPIO_OUT_ROsolenoid, 1)
GPIO.output(GPIO_OUT_rightdose, 1)
GPIO.output(GPIO_OUT_leftdose, 1)


def cleanup():
    GPIO.cleanup()
    print "GPIO CLEANED"
    hotconn.close()
    histconn.close()
    print "DATABASE CONNECTION CLOSED"
    print "PROGRAM TERMINATED SUCCESSFULLY"


def sql_getsump():
    try:
        cursor = hotconn.execute("SELECT id, ph, temp, sump from tank")
        for row in cursor:
            sumpdistance = row[3]
        sumpdistance = float(sumpdistance)
    except:
        print "Error in sql_getsump"
        return 7
    time.sleep(1)
    print sumpdistance
    return sumpdistance


def drainseq():
    try:
        print "DRAINING SUMP"
        timestart = time.time()
        startheight = sql_getsump()
        while sql_getsump() < INI_distancetodrain:
            GPIO.output(GPIO_OUT_drainmotor, 0)
        GPIO.output(GPIO_OUT_drainmotor, 1)
        timeend = time.time()
        timediff = timeend - timestart
        timediff = round(timediff, 1)
        endheight = sql_getsump()
        heightdiff = startheight - endheight
        print "TIME TO DRAIN = " + str(timediff) + " SECONDS"
        print "AMOUNT DRAINED = " + str(heightdiff) + "CM"
        rate = heightdiff / timediff
        rate = round(rate, 4)
        print "RATE = " + str(rate) + " CM/SECOND"
    except KeyboardInterrupt:
        print "Keyboard Interrupt Detected - Shutting Down"
        cleanup()


def fillseq():
    try:
        print "ADDING WATER TO SUMP"
        timestart = time.time()
        startheight = sql_getsump()
        while sql_getsump() > INI_distancetofill:
            GPIO.output(GPIO_OUT_ROsolenoid, 0)
        GPIO.output(GPIO_OUT_ROsolenoid, 1)
        timeend = time.time()
        timediff = timeend - timestart
        timediff = round(timediff, 1)
        endheight = sql_getsump()
        heightdiff = startheight - endheight
        print "TIME TO FILL = " + str(timediff) + " SECONDS"
        print "AMOUNT ADDED = " + str(heightdiff) + "CM"
        rate = heightdiff / timediff
        rate = round(rate, 4)
        print "RATE = " + str(rate) + " CM/SECOND"
    except KeyboardInterrupt:
        print "Keyboard Interrupt Detected - Shutting Down"
        cleanup()


def waterchange():
    global timediff
    print "\033[1;31mBEGINING WATER CHANGE\033[1;0m"
    timestart = time.time()
    drainseq()
    print "\033[1;33mPAUSING 2 SECONDS\033[1;0m"
    time.sleep(2)
    fillseq()
    timeend = time.time()
    timediff = timeend - timestart
    timediff = round(timediff, 1)
    print "TOTAL TIME = " + str(timediff) + " SECONDS"
    print "\033[1;32mWATER CHANGE COMPLETE\033[1;0m"


def fert_dose():
    print "ADDING FERTILIZER"
    num = datetime.datetime.today().weekday() + 1
    if num == 1:
        print "MONDAY - ADDING MACROS"
        fert_macros()
    if num == 2:
        print "TUESDAY - ADDING MICROS"
        fert_micros()
    if num == 3:
        print "WEDNESDAY - ADDING MACROS"
        fert_macros()
    if num == 4:
        print "THUSRDAY - ADDING MICROS"
        fert_micros()
    if num == 5:
        print "FRIDAY - ADDING MACROS"
        fert_macros()
    if num == 6:
        print "SATURDAY - ADDING MICROS"
        fert_micros()
    if num == 7:
        print "SUNDAY - ADDING MACROS"
        fert_macros()


def fert_micros():
    print "DOSING PUMP STARTING"
    GPIO.output(GPIO_OUT_rightdose, 0)
    time.sleep(30)
    GPIO.output(GPIO_OUT_rightdose, 1)
    print "MICROS HAVE BEEN ADDED"


def fert_macros():
    print "DOSING PUMP STARTING"
    GPIO.output(GPIO_OUT_leftdose, 0)
    time.sleep(30)
    GPIO.output(GPIO_OUT_leftdose, 1)
    print "MACROS HAVE BEEN ADDED"


def writewctable():
    try:
        cursor_hist = histconn.cursor()
        endtime = time.time()
        cursor_hist.execute('''INSERT INTO waterchange(time, amount)
                      VALUES(?,?)''', (endtime, timediff))
        histconn.commit()
        print "SUCCESSFULLY WROTE TO HISTORY DATABASE"
    except:
        print "COULD NOT WRITE TO HISTORY DATABASE"


waterchange()
fert_dose()
writewctable()
cleanup()
