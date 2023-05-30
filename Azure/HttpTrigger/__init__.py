import json
import logging
import numpy as np
import pandas as pd
import azure.functions as func

# Import frameworks and libraries
import influxdb_client
from datetime import timedelta
from darts import TimeSeries
from darts.models import NaiveSeasonal, NaiveDrift
from utils.constants import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    timestamp = None

    # Retrieving the arguments of the HTTP request
    try:
        timestamp = req.get_json().get('timestamp')
    except ValueError:
            pass

    if not timestamp:
        return func.HttpResponse("Please pass correct argument on function call!", status_code=400)

    # Connecting to the database and create a connector
    client = influxdb_client.InfluxDBClient(
        url=CLDB_URL, 
        token=CLDB_TOKEN,
        org=CLDB_ORG,
        timeout=20000  # 20 seconds
    )
    influx = client.query_api()

    # Retrieving pressure data from the "sensors" bucket
    query = f"""
                from(bucket: "sensors") 
                    |> range(start: 0) 
                    |> filter(fn: (r) =>
                        r._measurement == "climate" and
                        r._field == "temperature" and 
                        r.device == "PiXtend"
                    )
                    |> sort(columns: ["_time"], desc: false)
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
                    |> map(fn: (r) => ({{time:r._time, temperature:r.temperature }}))
            """
    result = influx.query_data_frame(query, org=CLDB_ORG)
    # print(result.head())

    # Conversion of data into Pandas DataFrame
    data = pd.DataFrame(result)

    # Create a TimeSeries, specifying the time and value columns
    series = TimeSeries.from_dataframe(data, value_cols = 'temperature')

    # Set aside the last 30% of the data points as testing data
    last_rows_by_30_percent = int(len(data.index) * 0.3)
    train, val = series[:-last_rows_by_30_percent], series[-last_rows_by_30_percent:]

    # Instantiate the model, K represents the number of time steps in a season
    seasonal_model = NaiveSeasonal(K=10080) # 10080 = 1 week
    drift_model = NaiveDrift()

    # Fit the model to the training data
    seasonal_model.fit(train)
    drift_model.fit(train)

    # Predict the time series, using the model. 
    # I predict for 1 month of data, to be sure to obtain a value lower than the threshold
    seasonal_forecast = seasonal_model.predict(n=43800) # 43800 = 1 month
    drift_forecast = drift_model.predict(n=43800) # 43800 = 1 month

    # Combine the two forecasts
    predictions = drift_forecast + seasonal_forecast - train.last_value()

    # Return the output variable as an HTTP response
    result = {'predictions': predictions}
    return func.HttpResponse(
        json.dumps({'result': result}),
        mimetype='application/json'
    )