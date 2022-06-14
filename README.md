# weather daily and hourly forecast

## description

Simple app that takes your local zipcode and number of days as input and downloads daily and hourly forecast data relevant to the zipcode and within the number of days.

when run, this app also shows the downloaded data on the localhost: 
    1. http://127.0.0.1:8000/dailyfile for daily forecast data
    2. http://127.0.0.1:8000/hourlyfile for hourly forecast data

## assumption

The host running this app has Python 3.8, pip and Docker installed

## caveats noticed so far

1. WeatherAPI's Forecast API does not return data for more than 3 days even after specific >3 days in the input.
2. Forecast API will sometimes randomly return 502-bad gateway response

## hardcoding

For simplicity, I have currently hardcoded my local zipcode in Seattle area and number of days = 3

## running the app

1. Download the zipped folder sent in the email

2. Unpack and navigate to the folder through your terminal

3. At the root level of the folder, run below command to build docker image
    docker build -t app1 .

4. Once the docker build is complete, run below command to run the docker 
    docker run -d --name weather-forecast --rm -it --network="host" app1

5. You can now inspect the downloaded data. Run below command to navigate into docker's file system. This will either open a new terminal or continue into the existing terminal
    docker exec -it weather-forecast bash

6. Once you are into Docker's file system, run below command to check the csv files:
    cd /output
    cat daily_forecast.csv
    cat hourly_forecast.csv

7. Alternatively, you can execute steps 4-6 on Docker Desktop if you have it installed    

## bonus
1. If your Docker container is still running, go to your web-browser and enter localhost address
    http://127.0.0.1:8000

2. Enter http://127.0.0.1:8000/dailyfile to view contents of daily file

3. Enter http://127.0.0.1:8000/hourlyfile to view contents of hourly file