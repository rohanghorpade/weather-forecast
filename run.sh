#!/bin/sh
python3 /app/forecast_data_ingest_app/ingest_forecast_data.py --zipcode 98136 --numDays 3

python3 -m flask run
