#!/usr/bin/env python3

import time
import sys

from bme280 import BME280
from smbus2 import SMBus
from enviroplus import gas

import numpy as np

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

try:
    while True:
        temps = np.array([])
        press = np.array([])
        humid = np.array([])
        nh3 = np.array([])
        oxi = np.array([])
        red = np.array([])

        for i in range(0, 10):
            temps = np.append(temps, bme280.get_temperature())
            press = np.append(press, bme280.get_pressure())
            humid = np.append(humid, bme280.get_humidity())

            gases = gas.read_all()
            nh3 = np.append(nh3, gases.nh3)
            oxi = np.append(oxi, gases.oxidising)
            red = np.append(red, gases.reducing)
            time.sleep(0.1)

        t = np.median(temps)
        p = np.median(press)
        h = np.median(humid)
        n = np.median(nh3)
        o = np.median(oxi)
        r = np.median(red)
        print('temperature={:.1f}°C, pressure={:.1f} HPa, humidity={:.2f}%'.format(t, p, h))
        print('nh3 level={:.3f}, oxidising={:.3f}, reducing={:.3f}'.format(n, o, r))

except KeyboardInterrupt:
    sys.exit(0)
