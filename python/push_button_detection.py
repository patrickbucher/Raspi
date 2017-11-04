#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

button_push_threshold = 0.02

pin_button = 27

def pushed_button(channel):
    global time_stamp 
    time_now = time.time()
    if (time_now - time_stamp) >= button_push_threshold:
        print("pushed button", channel)
    time_stamp = time_now

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin_button, GPIO.RISING, callback=pushed_button)
    time_stamp = time.time()

    while (True):
        pass

except KeyboardInterrupt:
    print("program stopped by user");
except Exception as e:
    print("error:", e)
finally:
    GPIO.cleanup()
