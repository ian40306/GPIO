#!/usr/bin/env python
#Using SMA420564
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


#七段顯示器
# GPIO ports for the 7seg pins
segments =  (3,22,25,23,18,4,8,24)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
# GPIO ports for the digit 0-3 pins 
digits = (2,17,27,7)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}
import threading
n='0000'
def segmentsrun(): 
    GPIO.setmode(GPIO.BCM)

    global segments
    global digits
    global n
    global num
    while(1):
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[n[digit]][loop])
            if digit==1:
                GPIO.output(24,1)
            else:
                GPIO.output(24,0)
            GPIO.output(digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit], 1)
    GPIO.cleanup()


#震動感應器
SW420_PIN = 5
def my_callback(channel):
    global n
    n='0111'
    print('move')
GPIO.setup(SW420_PIN, GPIO.IN)
GPIO.add_event_detect(SW420_PIN, GPIO.RISING, callback=my_callback, bouncetime=250)

try:
    starttime=time.time()
    t = threading.Thread(target =segmentsrun)        
    t.start()
    print(' Ctrl-C to stop')
    while(1):
        b=0
        #if(time.time()-starttime>=5):
        #    n='2020'   
    
except KeyboardInterrupt:
    print('close')
#finally:
#    GPIO.cleanup()
