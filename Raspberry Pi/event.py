#!/usr/bin/env python3
# coding=utf-8

from __future__ import print_function

import sys
import time
import socket
import json
import requests

# Import frameworks and libraries
import influxdb_client
from datetime import datetime, timezone

# Import constants and functions
from utils.log import log
from utils.send import send
from utils.constants import *

# Configuration of the connection to InfluxDB
org = TSDB_ORG # CLDB_ORG
client = influxdb_client.InfluxDBClient(
    url=f'http://{TSDB_HOST}:{TSDB_PORT}', # CLDB_URL, 
    token=TSDB_TOKEN, # CLDB_TOKEN,
    org=org
)
influx = client.query_api()

# Loop to retrieve real-time data
def loop():
    while True:

        # Retrieving data from the InfluxDB bucket events
        query = f"""
                    from(bucket: "{CLDB_BUCKET}")
                        |> range(start: -1m)
                        |> filter(fn: (r) =>
                            r._measurement == "YOUR-MESUREMENT" and
                            r._field == "YOUR-FIELD"
                        )
                        |> last()
                """
        
        # Loop trough the results if there is any
        for table in influx.query(query, org=org):
            for record in table.records:
                # print(f'record : {record}')

                # Conversion of the date into a UNIX timestamp
                timestamp = datetime.fromisoformat(str(record.get_time())).timestamp()

                # Sending the HTTP POST request to the Azure Function URL
                input_data = {'timestamp': timestamp}
                response = requests.post(AZURE_FUNCTION_URL, data=json.dumps(input_data))
                # print(f'response : {response.text}')
                
                # Retrieving the output variable from the HTTP response
                result = json.loads(response.text)['result']

                # Notification of predictions 
                send(f'⛽ Predictions : {result["predictions"]}')

        time.sleep(60)

if __name__ == "__main__":
    name = 'event_listener'

    try:
        deviceName = socket.gethostname()

        send('✅ Event listener script ({}) start running...'.format(deviceName))
        log(TSDB_BUCKET, deviceName, influxdb_client.Point('boolean').tag('script', name).field('run', True))

        loop()  # Enter in forever loop
    except Exception as e:
        print('❌ Event listener script ({}) failed with error: {}'.format(deviceName, e))
        send('🛑 Exiting event listener script.')
        log(TSDB_BUCKET, deviceName, influxdb_client.Point('boolean').tag('script', name).field('run', False))
        sys.exit(0)  # Exit the application
