#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import rospy

BUTTON_PIN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print('botton')
        time.sleep(0.1)
except KeyboardInterrupt:
    print('close')
finally:
    GPIO.cleanup()