#!/usr/bin/env python3

from influxdb import InfluxDBClient
import json

influx = InfluxDBClient(host='localhost', port=8086)
influx.switch_database('enviro')

query_pattern = 'select time, value, unit from {:s};'
queries = {
    'humidity': query_pattern.format('humidity'),
    'pressure': query_pattern.format('pressure'),
    'light': query_pattern.format('light'),
    'temperature': query_pattern.format('temperature_corrected')
}

json_body = []
for key in queries:
    result = influx.query(queries[key])
    result_list = list(result.get_points())
    first_result = result_list[0]
    unit = first_result['unit']
    measurement_json = {'measurement': key, 'unit': unit}
    data = []
    for result in result_list:
        time = result['time']
        value = result['value']
        data.append({'time': time, 'value': value})
    measurement_json['data'] = data
    json_body.append(measurement_json)
json = json.dumps(json_body, indent=2)
print(json)
