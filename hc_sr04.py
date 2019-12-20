import RPi.GPIO as gpio
import time
import rospy

gpio.setmode(gpio.BCM)
TRIGGER_PIN = 27
ECHO_PIN    = 17
gpio.setup(TRIGGER_PIN,  gpio.OUT)
gpio.setup(ECHO_PIN,     gpio.IN)
gpio.output(TRIGGER_PIN, gpio.LOW)
v = 343		# (331 + 0.6*20)

def measure() :
    gpio.output(TRIGGER_PIN, gpio.HIGH)
    time.sleep(0.00001)	# 10uS 
    gpio.output(TRIGGER_PIN, gpio.LOW)
    pulse_start = None
    pulse_end   = None

    while gpio.input(ECHO_PIN) == gpio.LOW:
        pulse_start = time.time()

    while gpio.input(ECHO_PIN) == gpio.HIGH:
        pulse_end = time.time()

    t = pulse_end - pulse_start

    d = t * v
    d = d/2

    return d*100

try :
    while True:
        distance = measure()
        print("Distance: %.1f (cm)" % distance)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")

finally:
    gpio.cleanup()          