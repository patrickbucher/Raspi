#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

led_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
while (True):
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.5)
