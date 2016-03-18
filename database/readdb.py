#!/usr/bin/env python
config = "/data/config.py"
from config import *


import sqlite3
import time
conn = sqlite3.connect(db_location, check_same_thread=False)
cursor = conn.execute("SELECT id, ph, temp, sump from tank")
for row in cursor:
   print "ID = ", row[0]
   print "pH = ", row[1]
   print "Temp = ", row[2]
   print "Sump = ", row[3], "\n"

conn.close()
