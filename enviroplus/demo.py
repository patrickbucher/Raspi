#!/usr/bin/env python3

import logging
import math
import time
import sys
from subprocess import PIPE, Popen
from datetime import datetime

import ltr559
from bme280 import BME280
from smbus2 import SMBus
from enviroplus import gas

import redis
import numpy as np

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
redis = redis.Redis()

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

        ts = datetime.timestamp(datetime.now())
        redis.zadd('temperature_raw', {ts: t})
        redis.zadd('pressure', {ts: p})
        redis.zadd('humidity', {ts: h})
        redis.zadd('nh3', {ts: n})
        redis.zadd('oxidising', {ts: o})
        redis.zadd('reducing', {ts: r})
        redis.zadd('light', {ts: l})
        redis.zadd('temperature_cpu', {ts: cpu})
        if cpu > t:
            approx = t - (cpu - t) * 0.3
            logging.info('corrected temp={:.1f}°C'.format(approx))
            redis.zadd('temperature_corrected', {ts: approx})

        logging.info('cpu={:.1f}°C'.format(cpu))
        logging.info('temperature={:.1f}°C'.format(t))
        logging.info('pressure={:.1f} HPa'.format(p))
        logging.info('humidity={:.2f}%'.format(h))
        logging.info('nh3 level={:.3f}'.format(n))
        logging.info('oxidising={:.3f}'.format(o))
        logging.info('reducing={:.3f}'.format(r))
        logging.info('light={:.3f} lux'.format(l))

        end = datetime.timestamp(datetime.now())
        diff = end - start
        if diff < 1.0:
            time.sleep(1.0 - diff)

except KeyboardInterrupt:
    sys.exit(0)
