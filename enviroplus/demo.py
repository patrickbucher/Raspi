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

def zadd(key, ts, val):
    redis.zadd(key, {val: ts}) # store timestamp as score for lookup

def measure_data(n_measurements, sleep_secs):
    temps = np.array([])
    press = np.array([])
    humid = np.array([])
    light = np.array([])
    nh3 = np.array([])
    oxi = np.array([])
    red = np.array([])
    lux = np.array([])

    for i in range(0, n_measurements):
        temps = np.append(temps, bme280.get_temperature())
        press = np.append(press, bme280.get_pressure())
        humid = np.append(humid, bme280.get_humidity())
        gases = gas.read_all()
        nh3 = np.append(nh3, gases.nh3)
        oxi = np.append(oxi, gases.oxidising)
        red = np.append(red, gases.reducing)
        lux = np.append(lux, ltr559.get_lux())
        time.sleep(sleep_secs)

    temperature_raw = np.median(temps)
    pressure = np.median(press)
    humidity = np.median(humid)
    ammonium = np.median(nh3)
    oxidising = np.median(oxi)
    reducing = np.median(red)
    light = np.median(lux)
    temperature_cpu = get_cpu_temp()
    temperature_corrected = temperature_raw
    if temperature_cpu > temperature_raw:
        temperature_corrected = temperature_raw - (temperature_cpu- temperature_raw) * 0.3

    return {
        'temperature_raw': (temperature_raw, '°C'),
        'temperature_cpu': (temperature_cpu, '°C'),
        'temperature_corrected' : (temperature_corrected, '°C'),
        'pressure': (pressure, 'hPa'),
        'humidity': (humidity, '%'),
        'ammonium': (ammonium, ''),
        'oxidising': (oxidising, ''),
        'reducing': (reducing, ''),
        'light': (light, 'lux')
    }

try:
    while True:
        start = datetime.timestamp(datetime.now())
        ts = datetime.timestamp(datetime.now())
        ts = math.floor(ts * 1000) # store in millis

        measurements = measure_data(10, 0.05)
        for key, value in measurements.items():
            score = value[0]
            unit = value[1]
            logging.info('{}={:.3f} {}'.format(key, score, unit))
            zadd(key, ts, score)

        end = datetime.timestamp(datetime.now())
        diff = end - start
        if diff < 1.0:
            time.sleep(1.0 - diff)

except KeyboardInterrupt:
    sys.exit(0)
