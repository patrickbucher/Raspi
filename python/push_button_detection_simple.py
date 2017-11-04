#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

pin_button = 27

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    time_stamp = time.time()

    print("push the button")
    while (True):
        while (GPIO.input(pin_button) == GPIO.LOW):
            pass
        while (GPIO.input(pin_button) == GPIO.HIGH):
            pass
        print("button pressed")

except KeyboardInterrupt:
    print("program stopped by user");
except Exception as e:
    print("error:", e)
finally:
    GPIO.cleanup()
