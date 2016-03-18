import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

count = 0
var = raw_input("GPIO TO TEST ")
var = int(var)
totaltime = raw_input("HOW MANY SECONDS? ")
print "YOU ENTERED: ", var
print "IT WILL BE ACTIVE FOR: ", totaltime, "SECONDS"

totaltime = int(totaltime)

GPIO.setup(var, GPIO.OUT)


GPIO.output(var, GPIO.LOW)
while count < totaltime:
    time.sleep(1)
    print count, " ", totaltime
    count = count + 1
GPIO.output(var, GPIO.HIGH)


GPIO.cleanup()
