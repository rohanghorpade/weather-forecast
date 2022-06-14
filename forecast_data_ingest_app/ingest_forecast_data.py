from forecast_data_reader import ConfigManager, WeatherForcastReader
from forecast_dto import DailyForecastDTO
import csv

def run(zipcode: int, days: int):
    """
    Main method to read forecast API and write the data to output csv files

    """

    # read config file
    conf_man = ConfigManager("weather_api")

    # create WeatherForecast reader
    forecast_reader = WeatherForcastReader(
        conf_man.client_conf["uri"].get(), 
        conf_man.client_conf["api_key"].get(),
        zipcode,
        days
    )

    result = forecast_reader.get()
    
    dailyDTO = DailyForecastDTO(result, zipcode)

    # create daily forecast data as list of tuples
    daily = dailyDTO.get_daily_forecast()

    # write daily forecast data to csv file
    with open("./output/daily_forecast.csv",'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(["zipcode","date","max_temp","min_temp","avg_temp","chance_of_rain","chance_of_snow","condition_text","condition_icon"])
        for row in daily:
            csv_out.writerow(row)

    # create hourly forecast data as list of tuples
    hourly = dailyDTO.get_hourly_forecast()

    # write hourly forecast data to csv file
    with open("./output/hourly_forecast.csv",'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(["zipcode","date","hour","feelslike_temp","heatindex_temp","windchill_temp","humidity","cloud_cover_percentage","chance_of_rain","chance_of_snow","condition_text","condition_icon"])
        for row in hourly:
            csv_out.writerow(row)       


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--zipcode", required=True, type=int)
    parser.add_argument("--numDays", required=True, type=int)

    args = parser.parse_args()

    run(args.zipcode, args.numDays)

    print("Data ingested successfully!")
    print("check the csv files ./output/daily_forecast.csv and ./output/hourly_forecast.csv")
   
