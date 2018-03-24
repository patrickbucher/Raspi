#!/usr/bin/env python3

import io
from RPi import GPIO as gpio
import serial
import time

led_pin_red = 4
led_pin_yellow = 5
led_pin_green = 6
button_pin = 18

try:
    port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1.0)
    sio = io.TextIOWrapper(io.BufferedRWPair(port, port))

    gpio.setmode(gpio.BCM)
    gpio.setup(led_pin_red, gpio.OUT)
    gpio.setup(led_pin_yellow, gpio.OUT)
    gpio.setup(led_pin_green, gpio.OUT)
    gpio.setup(button_pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)

    time_stamp = time.time()
    def push(channel):
        global time_stamp
        global state
        time_now = time.time()
        if (time_now - time_stamp) >= 0.1:
            print('button pushed')
            state = gpio.LOW
            sio.write('ping;\n')
            sio.flush();
            print('sent ping;')
        time_stamp = time_now

    gpio.add_event_detect(button_pin, gpio.RISING, callback=push)

    state = gpio.LOW
    while True:
        if state == gpio.HIGH:
            gpio.output(led_pin_green, gpio.LOW)
            gpio.output(led_pin_red, gpio.HIGH)
            time.sleep(0.1)
            gpio.output(led_pin_red, gpio.LOW)
            gpio.output(led_pin_yellow, gpio.HIGH)
            time.sleep(0.1)
            gpio.output(led_pin_yellow, gpio.LOW)
            gpio.output(led_pin_green, gpio.HIGH)
            time.sleep(0.1)
        else:
            gpio.output(led_pin_green, gpio.LOW)
            gpio.output(led_pin_yellow, gpio.LOW)
            gpio.output(led_pin_red, gpio.LOW)
        if port.in_waiting > 0:
            if port.in_waiting > 0:
                command = sio.readline().strip()
                print(command)
                if command == "pong;":
                    state = gpio.HIGH
                    sio.flush()

except KeyboardInterrupt:
    print('stopped by user')
finally:
    gpio.cleanup()
