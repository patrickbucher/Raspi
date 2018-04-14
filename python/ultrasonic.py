#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import statistics

pin_trigger = 18
pin_echo = 24

trigger_time = 0.00001
sonic_speed_mm_per_second = 343000
measurement_interval_millis = 1000

def distance():
    GPIO.output(pin_trigger, True)
    time.sleep(trigger_time)
    GPIO.output(pin_trigger, False)
    while GPIO.input(pin_echo) == 0:
        start = time.time()
    while GPIO.input(pin_echo) == 1:
        stop = time.time()
    diff = stop - start
    distance = (diff * sonic_speed_mm_per_second) / 2 # back and forth
    return distance

def mean_distance(measure_millis):
    if measure_millis < 0:
        raise Exception("measure_millis must be positive, was {}".format(measure_millis))
    start = time.time()
    stop = start + measure_millis / 1000 # time is in seconds
    distances = []
    while time.time() <= stop:
        distances.append(distance())
    return statistics.median(distances)

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_trigger, GPIO.OUT)
    GPIO.setup(pin_echo, GPIO.IN)
    while True:
        print(mean_distance(measurement_interval_millis))
except KeyboardInterrupt:
    print("stopped by user")
except Exception as e:
    print("error:", e)
finally:
    GPIO.cleanup()
