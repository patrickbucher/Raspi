#!/usr/bin/env python3

import math
import time
import sys
from subprocess import PIPE, Popen
from datetime import datetime

import ltr559
from bme280 import BME280
from smbus2 import SMBus
from enviroplus import gas

import numpy as np

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

def get_cpu_temp():
    proc = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    out, _err = proc.communicate()
    return float(out[out.index('=') + 1:out.rindex("'")])

try:
    while True:
        start = datetime.timestamp(datetime.now())

        temps = np.array([])
        press = np.array([])
        humid = np.array([])
        light = np.array([])
        nh3 = np.array([])
        oxi = np.array([])
        red = np.array([])
        lux = np.array([])

        for i in range(0, 10):
            temps = np.append(temps, bme280.get_temperature())
            press = np.append(press, bme280.get_pressure())
            humid = np.append(humid, bme280.get_humidity())
            gases = gas.read_all()
            nh3 = np.append(nh3, gases.nh3)
            oxi = np.append(oxi, gases.oxidising)
            red = np.append(red, gases.reducing)
            lux = np.append(lux, ltr559.get_lux())
            time.sleep(0.05)

        t = np.median(temps)
        p = np.median(press)
        h = np.median(humid)
        n = np.median(nh3)
        o = np.median(oxi)
        r = np.median(red)
        l = np.median(lux)
        cpu = get_cpu_temp()

        if cpu > t:
            approx = t - (cpu - t) * 0.3
            print('corrected temp: {:.1f}°C'.format(approx))

        print('cpu={:.1f}°C, temperature={:.1f}°C, pressure={:.1f} HPa, humidity={:.2f}%'.format(cpu, t, p, h))
        print('nh3 level={:.3f}, oxidising={:.3f}, reducing={:.3f}'.format(n, o, r))
        print('light={:.3f} lux'.format(l))

        end = datetime.timestamp(datetime.now())
        diff = end - start
        if diff < 1.0:
            time.sleep(1.0 - diff)

except KeyboardInterrupt:
    sys.exit(0)
