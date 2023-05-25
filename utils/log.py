#!/usr/bin/env python3
# coding=utf-8

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from utils.constants import *

client = InfluxDBClient(
    url=f'http://{TSDB_HOST}:{TSDB_PORT}',
    token=TSDB_TOKEN,
    org=TSDB_ORG
)
influx = client.write_api(write_options=SYNCHRONOUS)

def log(bucket, deviceName, record, userKey='', userId=0):
    try:
        record = record.tag('device', deviceName)
        influx.write(bucket=bucket, org=TSDB_ORG, record=record)
    except Exception as e:
        print(e)
    return