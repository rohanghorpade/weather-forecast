import json
from pathlib import Path
from datetime import date, datetime


PARENT_DIRECTORY = Path(__file__).parent
RAW_SCHEMA_PATH = Path.joinpath(PARENT_DIRECTORY, "forecastapi_response_schema.json")


class DailyForecastDTO:
    """
    A Data Transfer Object (DTO) for managing data from the Forecast REST API setup at WeatherAPI.

    For simplicity, currently I am storing the data as list of tuples data structure that is required for further processing

    This include any transformations such as array explode, individual field value manipulation etc.
    
    """

    def __init__(self, data, zipcode):
        self.data = data
        self.zipcode = zipcode
        self.schema = self._fetch_schema()
        if not self._validate_schema():
            raise Exception("Weather forecast schema is not valid")

    @staticmethod
    def _fetch_schema():
        """
        method to fetch the schema for the data returned by forecast API

        """
        with open(RAW_SCHEMA_PATH) as f:
            result = json.load(f)

        return result    

    def _validate_schema(self):
        """
        Validate the json data that is returned by forecast API

        """
        try:
            data = json.dumps(self.data)
            json.loads(data)
        except Exception as e:
            return False

        return True        

    @staticmethod
    def _get_daily_forecast(data, zipcode):
        """
        Create and return a tuple with single records at daily forecast level

        """
        batch = ()
        # for d in data:
        batch += (
                zipcode,
                data["date"],
                data["day"]["maxtemp_f"],
                data["day"]["mintemp_f"],
                data["day"]["avgtemp_f"],
                data["day"]["daily_chance_of_rain"],
                data["day"]["daily_chance_of_snow"],
                data["day"]["condition"]["text"],
                data["day"]["condition"]["icon"]
        )

        return batch    

    def get_daily_forecast(self):
        """
        Create and return a list of tuples of all records at daily forecast level

        """

        if not self._validate_schema():
            raise Exception("Weather forecast schema is not valid")
            # except Exception as e: print(e)
        
        forecast_days = []
        for d in self.data["forecast"]["forecastday"]:
            forecast_days.append(self._get_daily_forecast(d, self.zipcode))

        return forecast_days    

    @staticmethod
    def _to_hour(data):
        """
        Changes time to hour number 0-23

        """
        date = datetime.strptime(data, "%Y-%m-%d %H:%M")
        return date.hour

    @staticmethod
    def _get_hourly_forecast(data, zipcode, date):
        """
        Create and return a tuple with single records at hourly forecast level

        """

        batch = ()
        # for d in data:
        batch += (
                zipcode,
                date,
                DailyForecastDTO._to_hour(data["time"]),
                data["temp_f"],
                data["feelslike_f"],
                data["heatindex_f"],
                data["windchill_f"],
                data["humidity"],
                data["cloud"],
                data["chance_of_rain"],
                data["chance_of_snow"],
                data["condition"]["text"],
                data["condition"]["icon"]
        )

        return batch    

    def get_hourly_forecast(self):

        """
        Create and return a list of tuples of all records at hourly forecast level

        """
        
        forecast_hours = []
        for d in self.data["forecast"]["forecastday"]:
            for k in d["hour"]:
                forecast_hours.append(self._get_hourly_forecast(k, self.zipcode, d["date"]))

        return forecast_hours        