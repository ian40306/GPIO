#!/usr/bin/env python
####################################################################
#                                                                  #
#                           7 segments                             #
#                                                                  #
#                        3  5  7 11 13 15                          #
#                        |  |  |  |  |  |                          #
#              +------------------------------------+              #
#              |         3  a  f  2  1  b           |              #
#              |   *****   *****   *****   *****    |              #
#              |   *   *   *   *   *   *   *   *    |              #
#              |   *****   *****   *****   *****    |              #
#              |   *   *   *   *   *   *   *   *    |              #
#              |   ***** * ***** * ***** * ***** *  |              #
#              |         e  d  h  c  g  0           |              #
#              +------------------------------------+              #
#                        |  |  |  |  |  |                          #
#                       12 16 18 22 24 26                          #
#                                                                  #
#//////////////////////////////////////////////////////////////////#
#                                                                  #
#                          sw420_1                                 #
#                          sw420_2                                 #
#                          sw420_3                                 #
#                          sw420_4                                 #
#                                                                  #
#                     +----------------+                           #
#                     |  @@@@@@@@@@@@  |                           #
#                     |                |                           #
#                     |                |                           #
#                     |                |                           #
#                     |                |                           #
#                     |       **       |                           #
#                     |       **       |                           #
#                     |   DO GND VCC   |                           #
#                     +----------------+                           #
#                          |   |   |                               #
#                         29   9   2                               #
#                         31   9   2                               #
#                         33   9   2                               #
#                         35   9   2                               #
#                                                                  #
#//////////////////////////////////////////////////////////////////#
#                                                                  #
#                         button                                   #
#                                                                  #
#                          |  |                                    #
#                       +--------+                                 #
#                       |*      *|                                 #
#                       |   @@   |                                 #
#                       |   @@   |                                 #
#                       |*      *|                                 #
#                       +--------+                                 #
#                          |  |                                    #
#                         39 37                                    #
#                                                                  #
#//////////////////////////////////////////////////////////////////#
#                                                                  #
#                         led_R                                    #
#                         led_L                                    #
#                                                                  #
#                           -                                      #
#                         +   +                                    #
#                        |     |                                   #
#                        |     |                                   #
#                        |     |                                   #
#                        |+   -|                                   #
#                        +-----+                                   #
#                         |   |                                    #
#                         |                                        #
#                      R  9  25                                    #
#                      L 10  25                                    #
#                                                                  #
####################################################################
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
outnumber=0
def segmentsrun(): 
    global score
    global segments
    global digits
    global num
    global outnumber
    global startside
    global who_side
    global step
    while(1):
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            score='0000'
            step=0
            goback=0
            startside=0
            who_side=0
            print('reset')
            GPIO.output(LED_PIN_L,False)
            GPIO.output(LED_PIN_R,False)
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
        
        if(outnumber==1):
            break
    GPIO.cleanup()
        


#sw420
SW420_PIN1 = 5#29 5

SW420_PIN2 = 6#31 6
SW420_PIN3 = 13#33 13
SW420_PIN4 = 19#35 19
SW420_number=0
def my_callback(channel):
    global SW420_number
    global step_time
    if(channel==5):
        SW420_number=1
        print("right move"+"  "+str(step)+"  "+str(startside))
    elif(channel==6):
        SW420_number=-1
        print("left move"+"  "+str(step)+"  "+str(startside))
    if(step_time==0):
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
step_over_time=0
step_time=0
who_side=0
def score_calculate():
    global score
    global step
    global startside
    global SW420_number
    global goback
    global start_time
    global step_over_time
    global step_time
    global who_side
    if(step==0):
        if(startside==0):
            #GPIO.output(LED_PIN_R,True)
            if(SW420_number<0):
                who_side+=1
                if(who_side==2):
                    startside=1
                    who_side=0

                SW420_number=0
                score=str(int(score)+100).zfill(4)  
                step=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_R,False)
                GPIO.output(LED_PIN_L,False)
                goback=0
            else:
                step+=1
                goback=1
                start_time=time.time()
                print("step0: "+str(start_time))
        else:
            #GPIO.output(LED_PIN_L,True)
            if(SW420_number>0):
                who_side+=1
                if(who_side==2):
                    startside=0
                    who_side=0
                SW420_number=0
                score=str(int(score)+1).zfill(4)
                step=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_L,False)
                GPIO.output(LED_PIN_R,False)
                goback=0
            else:
                step+=1
                goback=1
                start_time=time.time()
                print("step0: "+str(start_time))
    elif(step==1):
        if(startside==0):
            if(SW420_number>0):
                who_side+=1
                if(who_side==2):
                    startside=1
                    who_side=0
                SW420_number=0
                score=str(int(score)+100).zfill(4)
                step=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_L,False)
                GPIO.output(LED_PIN_R,False)
                goback=0
            else:
                step+=1
                goback=1
                start_time=time.time()
                print("step1: "+str(start_time))
        else:
            if(SW420_number<0):
                who_side+=1
                if(who_side==2):
                    startside=0
                    who_side=0
                SW420_number=0
                score=str(int(score)+1).zfill(4)
                step=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_L,False)
                GPIO.output(LED_PIN_R,False)
                goback=0
            else:
                step+=1
                goback=1
                start_time=time.time()
                print("step1: "+str(start_time))
    elif(step==2):
        if(startside==0):
            if(SW420_number<0):
                who_side+=1
                if(who_side==2):
                    startside=1
                    who_side=0
                SW420_number=0
                score=str(int(score)+1).zfill(4)
                step=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_L,False)
                GPIO.output(LED_PIN_R,False)
                goback=0
                
            else:
                step+=1
                goback=1
                start_time=time.time()
                print("step2: "+str(start_time))
        else:
            if(SW420_number>0):
                who_side+=1
                if(who_side==2):
                    startside=0
                    who_side=0
                SW420_number=0
                score=str(int(score)+100).zfill(4)
                step=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_L,False)
                GPIO.output(LED_PIN_R,False)
                goback=0
            else:
                step+=1
                goback=1
                start_time=time.time()
                print("step1: "+str(start_time))
    else:
        if(startside==0):
            if(SW420_number>0):
                who_side+=1
                if(who_side==2):
                    startside=1
                    who_side=0
                SW420_number=0
                score=str(int(score)+100).zfill(4)
                step=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_L,False)
                GPIO.output(LED_PIN_R,False)
                goback=0
            else:
                step=2
                goback=1
                start_time=time.time()
                print("step3: "+str(start_time))
        else:
            if(SW420_number<0):
                who_side+=1
                if(who_side==2):
                    startside=0
                    who_side=0
                SW420_number=0
                score=str(int(score)+1).zfill(4)
                step=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_L,False)
                GPIO.output(LED_PIN_R,False)
                goback=0
            else:
                step=2
                goback=1
                start_time=time.time()
                print("step3: "+str(start_time))
def testfunction():
    global SW420_number,step,who_side,startside
    SW420_number=1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    SW420_number=-1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    SW420_number=-1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    print("0:1")
    print(score)
    time.sleep(6)
    print("$$$$"+str(time.time()))
    SW420_number=1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    SW420_number=1
    score_calculate()
    print("****"+str(time.time()))
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    print("1:1")
    print(score)
    time.sleep(6)
    SW420_number=-1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    SW420_number=-1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    print("1:2")
    print(score)
    time.sleep(6)
    SW420_number=-1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    SW420_number=1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    SW420_number=-1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    SW420_number=1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    SW420_number=1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    print("2:2")
    print(score)
    time.sleep(6)
    SW420_number=-1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(0.5)
    print("3:2")
    print(score)
    time.sleep(6)
    SW420_number=1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(5)
    print("4:2")
    print(score)
    time.sleep(6)
    SW420_number=-1
    score_calculate()
    print("step:"+str(step)+"  startside:"+str(startside)+"  whoside:"+str(who_side))
    time.sleep(5)
    print("4:3")
    print(score)
    time.sleep(6)
try:
    start_time=time.time()
    t = threading.Thread(target =segmentsrun)        
    t.start()
    #test = threading.Thread(target =testfunction)
    #test.start()
    print(' Ctrl-C to stop')
    while(1):
        time_pass=0
        start_time=time.time()
        step_pass=0
        GPIO.output(LED_PIN_R,True)
        while(1):
            time.sleep(0.1)
            time_now=time.time()
            #time_pass=time.time()-start_time
            step_pass=time_now-step_over_time
            if(step_pass>=5):
                step_time=0
                if(startside==0):
                    GPIO.output(LED_PIN_R,True)
                    GPIO.output(LED_PIN_L,False)
                else:
                    GPIO.output(LED_PIN_L,True)
                    GPIO.output(LED_PIN_R,False)
            else:
                step_time=1
            
            time_pass=time_now-start_time
            if(goback==1 and time_pass>=5):
                print("now"+str(time.time()))
                print(time_pass)
                print("start_time"+str(start_time))
                print("timw_now"+str(time_now))
                if(startside==0):
                    if(step==2):
                        score=str(int(score)+1).zfill(4)
                    else:
                        score=str(int(score)+100).zfill(4)
                    who_side+=1
                    if(who_side==2):
                        startside=1
                        who_side=0
                    step=0
                else:
                    if(step==2):
                        score=str(int(score)+100).zfill(4)
                    else:
                        score=str(int(score)+1).zfill(4)
                    who_side+=1
                    if(who_side==2):
                        startside=0
                        who_side=0
                    step=0
                goback=0
                time_pass=0
                step_over_time=time.time()
                GPIO.output(LED_PIN_L,False)
                GPIO.output(LED_PIN_R,False)
                #break
except KeyboardInterrupt:
    outnumber=1
    print('close')
    
#finally:
#    GPIO.cleanup()
