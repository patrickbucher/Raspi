#!/usr/bin/python3

import io
import RPi.GPIO as gpio
import serial
import time
import threading

led_pin_green = 4
led_pin_yellow = 5
led_pin_red = 6

button_pin = 18

state = gpio.LOW
port, sio = None, None
finished = False

def main():
    global port
    global sio
    global time_stamp
    global finished
    try:
        port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=5.0)
        sio = io.TextIOWrapper(io.BufferedRWPair(port, port))
        gpio.setmode(gpio.BCM)
        gpio.setup(led_pin_green, gpio.OUT)
        gpio.setup(led_pin_yellow, gpio.OUT)
        gpio.setup(led_pin_red, gpio.OUT)
        gpio.setup(button_pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(button_pin, gpio.RISING, callback=pushed_button)
        time_stamp = time.time()
        listener = threading.Thread(target=listen)
        listener.start()
        while True:
            loop()
    except KeyboardInterrupt:
        print("stopped by user")
    except Exception as e:
        print("error:", e)
    finally:
        gpio.cleanup()
        finished = True
        listener.join()
        port.close()

def listen():
    global state
    global finished
    while not finished:
        if port.in_waiting > 0:
            cmd = sio.readline().strip()
            print('read:', cmd)
            if cmd == "pong;":
                state = gpio.HIGH

def loop():
    global state
    if state:
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

def pushed_button(channel):
    global time_stamp
    global state
    time_now = time.time()
    if (time_now - time_stamp) >= 0.1:
        state = gpio.LOW
        sio.write("ping;")
        sio.flush()
        print('push the button')
    time_stamp = time_now

if __name__ == '__main__':
    main()
