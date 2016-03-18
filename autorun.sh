#!/bin/sh
sleep 2
sudo mount -t tmpfs -o size=50M tmpfs /data/database/ramtemp
sleep 1
sudo chmod 777 /data/database/ramtemp
#cd /data
#sudo python creatrrd.py
cd /data/database
sleep 1
sudo python sensors.py &
sleep 8
sudo python program.py &
