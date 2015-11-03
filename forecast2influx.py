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
    #influx.create_database(INFLUX_DB)

    api_key = os.environ['FORECAST_IO_KEY']
    forecast = forecastio.load_forecast(api_key, lat, lon)
    write_influx(influx, forecast.currently().d, lat, lon)


def forecast_point(data, lat, lon):
    body = []
    for k, v in data.iteritems():
        if isinstance(v, numbers.Number):
            body.append({
                "measurement": k,
                "tags": {
                  "lat": lat,
                  "lon": lon},
                "fields": {
                  "value": round(v, 2)}})
    return body


def write_influx(influx, data, lat, lon):
    influx.write_points(forecast_point(data, lat, lon))    


if __name__ == "__main__":
    main()
