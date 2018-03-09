#!/usr/bin/python3

import RPi.GPIO as GPIO # pip3 install RPi.GPIO, if missing

pin_button = 21

def pushed_button(channel):
    print("pushed the button")

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin_button, GPIO.RISING, callback=pushed_button)
    while True:
        pass
except KeyboardInterrupt:
    print("stopped by user")
except Exception as e:
    print("error:", e)
finally:
    GPIO.cleanup()
