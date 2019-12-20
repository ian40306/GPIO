#!/usr/bin/env python
#Using SMA420564
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#button
BUTTON_PIN = 26
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#LED
LED_PIN_R=9
LED_PIN_L=10
GPIO.setup(LED_PIN_R,GPIO.OUT)
GPIO.setup(LED_PIN_L,GPIO.OUT)
GPIO.output(LED_PIN_R,False)
GPIO.output(LED_PIN_L,False)


#7 segments
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
score='0000'
def segmentsrun(): 
    global score
    global segments
    global digits
    global num

    while(1):
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            score='0000'
            step=0
            goback=0
            print('reset')
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[score[digit]][loop])
            if digit==1:
                GPIO.output(24,1)
            else:
                GPIO.output(24,0)
            GPIO.output(digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit], 1)
    GPIO.cleanup()


#sw420
SW420_PIN1 = 5#29
SW420_PIN2 = 6#31
SW420_PIN3 = 13#33
SW420_PIN4 = 19#35
SW420_number=0
def my_callback(channel):
    global SW420_number
    if(channel==5):
        SW420_number=1
        print("right move")
    elif(channel==6):
        SW420_number=-1
        print("left move")
    score_calculate()
GPIO.setup(SW420_PIN1, GPIO.IN)
GPIO.setup(SW420_PIN2, GPIO.IN)
GPIO.add_event_detect(SW420_PIN1, GPIO.RISING, callback=my_callback, bouncetime=250)
GPIO.add_event_detect(SW420_PIN2, GPIO.RISING, callback=my_callback, bouncetime=250)

#score
step=0
startside=0
goback=0
start_time=0

def score_calculate():
    global score
    global step
    global startside
    global SW420_number
    global goback
    global start_time
    if(step==0):
        if(startside==0):
            if(SW420_number<0):
                startside=1
                SW420_number=0
                score=str(int(score)+100).zfill(4)  
                step=0
            else:
                step+=1
                goback=1
                start_time=time.time()
        else:
            if(SW420_number>0):
                startside=0
                SW420_number=0
                score=str(int(score)+1).zfill(4)
                step=0
            else:
                step+=1
                goback=1
                start_time=time.time()
        
    elif(step==1):
        if(startside==0):
            if(SW420_number>0):
                startside=1
                SW420_number=0
                score=str(int(score)+100).zfill(4)
                step=0
            else:
                step+=1
                goback=1
                start_time=time.time()
        else:
            if(SW420_number<0):
                startside=0
                SW420_number=0
                score=str(int(score)+1).zfill(4)
                step=0
            else:
                step+=1
                goback=1
                start_time=time.time()
    elif(step==2):
        if(startside==0):
            if(SW420_number<0):
                startside=0
                SW420_number=0
                score=str(int(score)+1).zfill(4)
                step=0
            else:
                step+=1
                goback=1
                start_time=time.time()
        else:
            if(SW420_number>0):
                startside=1
                SW420_number=0
                score=str(int(score)+100).zfill(4)
                step=0
            else:
                step+=1
                goback=1
                start_time=time.time()
    else:
        if(startside==0):
            if(SW420_number>0):
                startside=1
                SW420_number=0
                score=str(int(score)+100).zfill(4)
                step=0
            else:
                step=2
                goback=1
                start_time=time.time()
        else:
            if(SW420_number<0):
                startside=0
                SW420_number=0
                score=str(int(score)+1).zfill(4)
                step=0
            else:
                step=2
                goback=1
                start_time=time.time()

try:
    global score
    global startside
    global goback
    global start_time
    starttime=time.time()
    t = threading.Thread(target =segmentsrun)        
    t.start()
    print(' Ctrl-C to stop')
    while(1):
        time_pass=0
        start_time=time.time()
        while(1):
            time_pass=time.time()-start_time
            if(goback==1 and time_pass>=5):
                #print(start_time)
                if(startside==0):
                    score=str(int(score)+100).zfill(4)
                else:
                    score=str(int(score)+1).zfill(4)
                goback=0
                #break
                
        #if(time.time()-starttime>=5):
        #    n='2020'   
        #score=str(person[0])+str(person[1])    
except KeyboardInterrupt:
    print('close')
#finally:
#    GPIO.cleanup()
