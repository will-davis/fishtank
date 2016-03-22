#!/usr/bin/env python


import serial
import os
import glob
import time
import RPi.GPIO as GPIO
import sqlite3
import threading
import subprocess
import sys
sys.path.append('/opt/rrdtool-1.4.3/lib/python2.7/site-packages/')
import rrdtool
config = "/data/config.py"
from config import *
global x
x = 0
print "SENSOR PROGRAM STARTED\n"

usbport = '/dev/ttyAMA0'  # **PH**
ser = serial.Serial(usbport, 9600)  # **PH**
os.system('modprobe w1-gpio')  # **TEMP**
os.system('modprobe w1-therm')  # **TEMP**
base_dir = '/sys/bus/w1/devices/'  # **TEMP**
device_folder = glob.glob(base_dir + '28*')[0]  # **TEMP**
device_file = device_folder + '/w1_slave'  # **TEMP**

GPIO.setmode(GPIO.BCM)  # **DISTANCE**

# turn on the LEDs
ser.write("L,1\r")  # **PH**
ser.write("C,1\r")  # **PH**
global distance  # **DISTANCE*
GPIO.setup(GPIO_OUT_sumptrig, GPIO.OUT)  # **DISTANCE*
GPIO.setup(GPIO_IN_sumpecho, GPIO.IN)  # **DISTANCE*
global phrrd
global temprrd
global sumprrd

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


def cleanup():
    GPIO.cleanup()
    print "GPIO Cleanup"
    hotconn.close()
    print "Database Connection Closed"
    print "Programing Terminated Successfully"


def db_generatetables():
    try:
        cursor_hot = hotconn.cursor()
        time.sleep(1)
        cursor_hot.execute('''
            CREATE TABLE IF NOT EXISTS tank(
                           id INTEGER PRIMARY KEY, 
                           ph TEXT, 
                           temp TEXT, 
                           sump TEXT)
        ''')
        time.sleep(1)
        hotconn.commit()
        print "TABLE TANK COMMITTED IN HOT DATABASE"
    except:
        print "SHITS FUCKED YO - TABLE TANK FAILED TO COMMIT IN HOT DATABASE"
    try:
        # CREATING TOPOFF TABLE
        cursor_hist = histconn.cursor()
        time.sleep(1)
        cursor_hist.execute('''
            CREATE TABLE IF NOT EXISTS topoff(
                           id INTEGER PRIMARY KEY, 
                           time TEXT, 
                           amount TEXT)
        ''')
        # CREATING WATERCHANGE TABLE
        print "TABLE WATERCHANGE COMMITTED IN HOT DATABASE"
        time.sleep(1)
        cursor_hist.execute('''
            CREATE TABLE IF NOT EXISTS waterchange(
                           id INTEGER PRIMARY KEY, 
                           time TEXT, 
                           amount TEXT)
        ''')
        time.sleep(1)
        histconn.commit()
        print "TABLES COMMITTED IN HIST DATABASE"
    except:
        print "SHITS FUCKED YO - TABLES IN HIST DB FAILED TO COMMIT"


time.sleep(1)
db_generatetables()
# cleartable()
time.sleep(1)
cursor_hot = hotconn.cursor()
cursor_hot.execute('''INSERT INTO tank(ph, temp, sump)
                      VALUES(?,?,?)''', ("NULL", "NULL", "NULL"))
hotconn.commit()
time.sleep(1)


def distancesump():
    global sumprrd
    noprint = 0
    while x < 100:
        timeoutstart = time.time()
        timeoutstart = timeoutstart + 5
        GPIO.output(GPIO_OUT_sumptrig, False)
        time.sleep(1)
        GPIO.output(GPIO_OUT_sumptrig, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_OUT_sumptrig, False)
        while GPIO.input(GPIO_IN_sumpecho) == 0:
            pulse_start = time.time()
            if time.time() > timeoutstart:
                break
        while GPIO.input(GPIO_IN_sumpecho) == 1:
            pulse_end = time.time()
            if time.time() > timeoutstart:
                noprint = 1
                break
        pulse_duration = pulse_end - pulse_start
        instantdistance = pulse_duration * 17150
        instantdistance = round(instantdistance, 2)
        distancestring = str(instantdistance)
        try:
            if noprint < 1:
                hotconn.execute(
                    "UPDATE tank SET sump = ? WHERE id = ?", (distancestring, 1))
                hotconn.commit()
                sumprrd = distancestring
            else:
                noprint = 0
        except:
            print "\033[1;31mSUMP DISTANCE WRITE SQL ERROR\033[1;0m"
    return instantdistance


def read_temp_raw():  # **TEMP**
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():  # **TEMP**
    global temprrd
    while x < 100:
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            temp_f = round(temp_f, 1)
            try:
                temp_f = float(temp_f)
                temp_f = str(temp_f)
                hotconn.execute(
                    "UPDATE tank SET temp = ? WHERE id = ?", (temp_f, 1))
                hotconn.commit()
                temprrd = temp_f
            except:
                print "\033[1;31mTEMP WRITE SQL ERROR\033[1;0m"
            time.sleep(1)
    return temp_f


def read_ph():
    global phrrd
    line = ""
    while x < 100:
        time.sleep(2)
        while True:
            data = ser.read()
            if(data == "\r"):
                try:
                    line = float(line)
                    line = str(line)
                    hotconn.execute(
                        "UPDATE tank SET ph = ? WHERE id = ?", (line, 1))
                    hotconn.commit()
                    phrrd = line
                except:
                    print "\033[1;31mPH SQL WRITE ERROR\033[1;0m"
                line = ""
                break
            else:
                line = line + data


def rrdwrite(ph, temp, sump):
    try:
        ph = float(ph)
        ph = str(ph)
        temp = float(temp)
        temp = str(temp)
        sump = float(sump)
        sump = str(sump)
        ret = rrdtool.update(rrd_db, 'N:%s:%s:%s' % (ph, temp, sump))
        time.sleep(.1)
        subprocess.call(
            " python /data/database/creategraphs.py", shell=True)

        if ret:
            print rrdtool.error()
    except Exception as inst:
        print type(inst)
        print ph + " " + temp + " " + sump


def rrdloop():
    time.sleep(5)
    global phrrd
    global temprrd
    global sumprrd
    while True:
        try:
            rrdwrite(phrrd, temprrd, sumprrd)
            time.sleep(10)
        except:
            print "RRDLOOP FAILED"
            time.sleep(10)


if __name__ == "__main__":
    try:
        print "\033[1;32mMAIN SENSOR PROGRAM STARTING...\033[1;0m"
        b = threading.Thread(target=distancesump)
        c = threading.Thread(target=read_temp)
        d = threading.Thread(target=read_ph)
        e = threading.Thread(target=rrdloop)
        b.daemon = True
        c.daemon = True
        d.daemon = True
        e.daemon = True
        b.start()
        c.start()
        d.start()
        e.start()
        while x < 100:
            time.sleep(5)
    except KeyboardInterrupt:
        print "\033[1;31mKEYBOARD INTERRUPT DETECTED - SHUTTING DOWN\033[1;0m"
        cleanup()

cursor_hot = hotconn.execute("SELECT id, ph, temp, sump from tank")
for row in cursor_hot:
    print "ID = ", row[0]
    print "pH = ", row[1]
    print "Temp = ", row[2]
    print "Sump = ", row[3], "\n"


cleanup()
