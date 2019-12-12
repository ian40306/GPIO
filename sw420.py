#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
 
SW420_PIN = 5
 
def my_callback(channel):
    print('move')
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW420_PIN, GPIO.IN)
GPIO.add_event_detect(SW420_PIN, GPIO.RISING, callback=my_callback, bouncetime=250)
 
try:
    print(' Ctrl-C to stop')
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('close')
finally:
    GPIO.cleanup()