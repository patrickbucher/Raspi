#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import statistics

pin_trigger = 18
pin_echo = 24

trigger_time = 0.00001
sonic_speed_mm_per_second = 343000
measurement_interval_millis = 1000

lower_limit_mm = 20
upper_limit_mm = 5000

def distance():
    GPIO.output(pin_trigger, True)
    time.sleep(trigger_time)
    GPIO.output(pin_trigger, False)
    start, stop = None, None
    while GPIO.input(pin_echo) == 0:
        start = time.time()
    while GPIO.input(pin_echo) == 1:
        stop = time.time()
    if start is None or stop is None:
        raise ValueError("{} didn't switch from HIGH to LOW".format(pin_echo))
    diff = stop - start
    distance = (diff * sonic_speed_mm_per_second) / 2 # back and forth
    return distance

def median_distance(measure_millis):
    if measure_millis < 0:
        raise Exception("measure_millis negative: {}".format(measure_millis))
    start = time.time()
    stop = start + measure_millis / 1000 # time is in seconds
    distances = []
    while time.time() <= stop:
        distances.append(distance())
    distance_mm = statistics.median(distances)
    if lower_limit_mm < distance_mm < upper_limit_mm:
        return distance_mm
    else:
        raise ValueError("measured {:.0f}mm, out of range".format(distance_mm))

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_trigger, GPIO.OUT)
    GPIO.setup(pin_echo, GPIO.IN)
    while True:
        try:
            dist_cm = median_distance(measurement_interval_millis) / 10
            print('{:.1f}cm'.format(dist_cm))
        except ValueError as e:
            print("no distance:", e)
except KeyboardInterrupt:
    print("stopped by user")
except Exception as e:
    print("error:", e)
finally:
    GPIO.cleanup()
