#!/usr/bin/env python
import rospy
import RPi.GPIO as gpio
import time
pin=17
gpio.setmode(gpio.BCM)
gpio.setup(pin,gpio.OUT)
print('sos start')
while(True):
    for i in range (3):
        gpio.output(pin,True)
        time.sleep(0.5)
        gpio.output(pin,False)
        time.sleep(0.5)
    for i in range (3):
        gpio.output(pin,True)
        time.sleep(1.5)
        gpio.output(pin,False)
        time.sleep(0.5)
    for i in range (3):
        gpio.output(pin,True)
        time.sleep(0.5)
        gpio.output(pin,False)
        time.sleep(0.5)
    time.sleep(1.5)