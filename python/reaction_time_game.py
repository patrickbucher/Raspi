#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

from random import randint

pin_led_red = 4
pin_led_green = 17
pin_button = 27

def pushed(pin):
    GPIO.wait_for_edge(pin, GPIO.RISING, bouncetime=100)
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_led_red, GPIO.OUT)
    GPIO.setup(pin_led_green, GPIO.OUT)
    GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for i in range(1, 4):
        GPIO.output(pin_led_red, GPIO.HIGH)
        GPIO.output(pin_led_green, GPIO.HIGH)
        time.sleep(0.15)
        GPIO.output(pin_led_red, GPIO.LOW)
        GPIO.output(pin_led_green, GPIO.LOW)
        time.sleep(0.15)

    while (True):
        print("Reaction Time Game")
        print("push button to start")
        pushed(pin_button)

        GPIO.output(pin_led_red, GPIO.HIGH)
        ready = randint(1000, 2000)
        time.sleep(ready / 1000)
        GPIO.output(pin_led_red, GPIO.LOW)
        GPIO.output(pin_led_green, GPIO.HIGH)
        start = time.time()
        pushed(pin_button)
        end = time.time()

        print("reaction time:", int(round(end - start, 3) * 1000), "ms")
        time.sleep(1)
        GPIO.output(pin_led_green, GPIO.LOW)

except KeyboardInterrupt:
    print("program stopped by user");
except Exception as e:
    print("error:", e)
finally:
    GPIO.cleanup()
