config = "/data/config.py"
from config import *
import sys
sys.path.append('/opt/rrdtool-1.4.3/lib/python2.7/site-packages/')
import rrdtool
import time

stime = int(time.time()) - 3600
dpoints = 15
etime = int(time.time())



ph_graph = rrdtool.graph(ph_img,
                         '--start', str(etime - (3600)),
                         '--end', str(etime),
                         '--imgformat', 'PNG',
                         '--c', 'CANVAS#000000',
                         '--c', 'FONT#FFFFFF',
                         '--c', 'BACK#000000',
                         '--title', 'pH LEVEL (HOURLY)',
                         '--lower-limit', '7',
#                         '--x-grid', 'MINUTE:10:HOUR:1:HOUR:4:0'
                         'DEF:myspeed=%s:ph:AVERAGE' % rrd_db,
                         'CDEF:mph=myspeed,1,*',
                         'VDEF:msmax=mph,MAXIMUM',
                         'VDEF:msavg=mph,AVERAGE',
                         'VDEF:msmin=mph,MINIMUM',
                         'VDEF:mspct=mph,95,PERCENT',
                         'LINE:mph#40929D:pH',
                         r'GPRINT:msmax:Max\: %6.1lf pH',
                         r'GPRINT:msavg:Avg\: %6.1lf pH',
                         r'GPRINT:msmin:Min\: %6.1lf pH\l',
                         )


temp_graph = rrdtool.graph(temp_img,
                           '--start', str(etime - (3600)),
                           '--end', str(etime),
                           '--imgformat', 'PNG',
                           '--c', 'CANVAS#000000',
                           '--c', 'FONT#FFFFFF',
                           '--c', 'BACK#000000',
                           '--title', 'TEMPERATURE (HOURLY)',
                           '--lower-limit', '75',
                           'DEF:myspeed=%s:temp:AVERAGE' % rrd_db,
                           'CDEF:mph=myspeed,1,*',
                           'VDEF:msmax=mph,MAXIMUM',
                           'VDEF:msavg=mph,AVERAGE',
                           'VDEF:msmin=mph,MINIMUM',
                           'VDEF:mspct=mph,95,PERCENT',
                           'LINE:mph#E8D754:TEMP',

                           r'GPRINT:msmax:Max\: %6.1lf F',
                           r'GPRINT:msavg:Avg\: %6.1lf F',
                           r'GPRINT:msmin:Min\: %6.1lf F\l',
                           )


sump_graph = rrdtool.graph(sump_img,
                           '--start', str(etime - (3600)),
                           '--end', str(etime),
                           '--imgformat', 'PNG',
                           '--c', 'CANVAS#000000',
                           '--c', 'FONT#FFFFFF',
                           '--c', 'BACK#000000',
                           '--title', 'SUMP LEVEL (HOURLY)',
                           '--lower-limit', '6',
                           'DEF:myspeed=%s:sump:AVERAGE' % rrd_db,
                           'CDEF:mph=myspeed,1,*',
                           'VDEF:msmax=mph,MAXIMUM',
                           'VDEF:msavg=mph,AVERAGE',
                           'VDEF:msmin=mph,MINIMUM',
                           'VDEF:mspct=mph,95,PERCENT',
                           'LINE:mph#D15641:SUMP',
                           r'GPRINT:msmax:Max\: %6.1lf SUMP',
                           r'GPRINT:msavg:Avg\: %6.1lf SUMP',
                           r'GPRINT:msmin:Min\: %6.1lf SUMP\l',
                           )
########################DAILY###############################
ph_graph = rrdtool.graph(ph_hr_img,
                         '--start', str(etime - (86400)),
                         '--end', str(etime),
                         '--imgformat', 'PNG',
                         '--c', 'CANVAS#000000',
                         '--c', 'FONT#FFFFFF',
                         '--c', 'BACK#000000',
                         '--title', 'pH LEVEL (DAILY)',
                         '--lower-limit', '7',
                         'DEF:myspeed=%s:ph:AVERAGE' % rrd_db,
                         'CDEF:mph=myspeed,1,*',
                         'VDEF:msmax=mph,MAXIMUM',
                         'VDEF:msavg=mph,AVERAGE',
                         'VDEF:msmin=mph,MINIMUM',
                         'VDEF:mspct=mph,95,PERCENT',
                         'LINE:mph#40929D:pH',
                         r'GPRINT:msmax:Max\: %6.1lf pH',
                         r'GPRINT:msavg:Avg\: %6.1lf pH',
                         r'GPRINT:msmin:Min\: %6.1lf pH\l',
                         )

temp_graph = rrdtool.graph(temp_hr_img,
                           '--start', str(etime - (86400)),
                           '--end', str(etime),
                           '--imgformat', 'PNG',
                           '--c', 'CANVAS#000000',
                           '--c', 'FONT#FFFFFF',
                           '--c', 'BACK#000000',
                           '--title', 'TEMPERATURE (DAILY)',
                           '--lower-limit', '75',
                           'DEF:myspeed=%s:temp:AVERAGE' % rrd_db,
                           'CDEF:mph=myspeed,1,*',
                           'VDEF:msmax=mph,MAXIMUM',
                           'VDEF:msavg=mph,AVERAGE',
                           'VDEF:msmin=mph,MINIMUM',
                           'VDEF:mspct=mph,95,PERCENT',
                           'LINE:mph#E8D754:TEMP',

                           r'GPRINT:msmax:Max\: %6.1lf F',
                           r'GPRINT:msavg:Avg\: %6.1lf F',
                           r'GPRINT:msmin:Min\: %6.1lf F\l',
                           )

sump_graph = rrdtool.graph(sump_hr_img,
                           '--start', str(etime - (86400)),
                           '--end', str(etime),
                           '--imgformat', 'PNG',
                           '--c', 'CANVAS#000000',
                           '--c', 'FONT#FFFFFF',
                           '--c', 'BACK#000000',
                           '--title', 'SUMP LEVEL (DAILY)',
                           '--lower-limit', '6',
                           'DEF:myspeed=%s:sump:AVERAGE' % rrd_db,
                           'CDEF:mph=myspeed,1,*',
                           'VDEF:msmax=mph,MAXIMUM',
                           'VDEF:msavg=mph,AVERAGE',
                           'VDEF:msmin=mph,MINIMUM',
                           'VDEF:mspct=mph,95,PERCENT',
                           'LINE:mph#D15641:SUMP',
                           r'GPRINT:msmax:Max\: %6.1lf SUMP',
                           r'GPRINT:msavg:Avg\: %6.1lf SUMP',
                           r'GPRINT:msmin:Min\: %6.1lf SUMP\l',
                           )