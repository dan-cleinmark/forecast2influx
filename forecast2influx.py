#!./target/bin/python

import numbers
import os

from influxdb import InfluxDBClient
import forecastio

INFLUX_HOST = 'localhost'
INFLUX_PORT = 8086
INFLUX_USER = 'root'
INFLUX_PASS = 'root'
INFLUX_DB = 'forecast_io'

lat = 38.7892
lon = -90.5653


def main():
    influx = InfluxDBClient(INFLUX_HOST, INFLUX_PORT,
                            INFLUX_USER, INFLUX_PASS,
                            INFLUX_DB)
    influx.create_database(INFLUX_DB)

    api_key = os.environ['FORECAST_IO_KEY']
    forecast = forecastio.load_forecast(api_key, lat, lon)
    write_influx(influx, forecast.currently().d)


def tstat_point(data):
    body = []
    for k, v in tstat.tstat['raw'].iteritems():
        if isinstance(v, numbers.Number):
            body.append({
                "measurement": k,
                "tags": {
                  "name": tstat.name['raw']},
                "fields": {
                  "value": v}})
    return body


def write_influx(influx, data):
    influx.write_points(tstat_point(data))    


if __name__ == "__main__":
    main()
