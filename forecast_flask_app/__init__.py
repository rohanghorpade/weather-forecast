from crypt import methods
from flask import Flask

# flask app to expose csv file data (unformatted) to port 8000
app = Flask("weatherforecast_data")

@app.route('/')
def home():
   return "hello this is page will display weather forecast data!"

csv_file_path_daily = "./output/daily_forecast.csv"   
daily_data = ''

try:
    with open(csv_file_path_daily) as f:
        daily_data = f.read()
except Exception:
    print("no file present. will render no data")        

@app.route("/dailyfile", methods=['GET'])
def getDailyFile():
    return daily_data

csv_file_path_hourly = "./output/hourly_forecast.csv"   
hourly_data = ''

try:
    with open(csv_file_path_hourly) as f:
        hourly_data = f.read()
except Exception:
    print("no file present. will render no data")          

@app.route("/hourlyfile", methods=['GET'])
def gethourlyFile():
    return hourly_data    