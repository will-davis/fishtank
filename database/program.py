#!/usr/bin/env python
config = "/data/config.py"
from config import *
import sys
import sqlite3
import time
import threading
from flask import Flask, Response, redirect, request, url_for
import signal
import subprocess


global conn
try:
    conn = sqlite3.connect(db_location, check_same_thread=False)
    print "CONNECTED TO DATABASE"
except:
    print "FAILED TO CONNECT TO DATABASE!!!!!!!!!!!!!!"

app = Flask(__name__)
global taco1
taco1 = 1
global taco2
taco2 = 1
global taco3
taco3 = 1
global x
global distance
distance = 10
x = 0
y = 0
z = 0
global identity
global ph
global temp
global sump
identiy = 1
ph = "NOT REGISTERED YET"
temp = "NOT REGISTERED YET"
sump = "NOT REGISTERED YET"


def getinfo():
    global identity
    global ph
    global temp
    global sump
    while x < 100:
        try:
            cursor = conn.execute("SELECT id, ph, temp, sump from tank")
            for row in cursor:
                identity = row[0]
                ph = row[1]
                temp = row[2]
                sump = row[3]
            time.sleep(1)
        except KeyboardInterrupt:
            print "CLOSING getinfo"
            conn.close()
            sys.exit()


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def events():
    global identity
    global ph
    global temp
    global sump
    while x < 100:
        try:
            now = "data: " + str(ph) + "%" + str(temp) + \
                "%" + str(sump) + "\n\n"
            time.sleep(1)
            yield now
        except KeyboardInterrupt:
            print "CLOSING events"
            conn.close()
            sys.exit()


events()


@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='index.html'))

if __name__ == "__main__":
    a = threading.Thread(target=getinfo)
    a.daemon = True
    a.start()
    app.run(host='0.0.0.0', port=3000, debug=True,
            use_reloader=False, threaded=True)

conn.close()
