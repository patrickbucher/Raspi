#!/usr/bin/python3

import RPi.GPIO as gpio
import time

pin_led = 20
pin_button = 21

def pushed_button(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.1:
        print("pushed the button")
        gpio.output(pin_led, gpio.HIGH)
        time.sleep(1.0)
        gpio.output(pin_led, gpio.LOW)
    time_stamp = time_now

try:
    gpio.setmode(gpio.BCM)
    gpio.setup(pin_led, gpio.OUT)
    gpio.setup(pin_button, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.add_event_detect(pin_button, gpio.RISING, callback=pushed_button)
    time_stamp = time.time()
    while True:
        pass
except KeyboardInterrupt:
    print("stopped by user")
except Exception as e:
    print("error:", e)
finally:
    gpio.cleanup()
