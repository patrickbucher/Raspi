#!/usr/bin/python3

import serial # apt-get install python3-serial
import time

port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=5.0)
time.sleep(1)

def do(cmd, sleep):
    port.write(cmd.encode('utf-8'))
    time.sleep(sleep)

do('red_on;', 1)
do('green_on;', 1)
do('yellow_on;', 1)
do('blue_on;', 1)
