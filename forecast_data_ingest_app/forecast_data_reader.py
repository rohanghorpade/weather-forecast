import aiohttp, confuse, sys, json, requests
from pathlib import Path

PROJ_ROOT = Path(__file__).parents[1]
sys.path.append(str(PROJ_ROOT))

from settings import CLIENT_CONFIG_DIRECTORY

CONFIG_MAIN_MOD_NAME = "config"

class ConfigMain(confuse.Configuration):
    def config_dir(self):
        return CLIENT_CONFIG_DIRECTORY

class ConfigManager:
    def __init__(self, client_conf: str):
        conf = ConfigMain("WeatherForecastExtracts", modname=CONFIG_MAIN_MOD_NAME)    
        self.client_conf = conf[client_conf]   

class WeatherForcastReader:
    def __init__(self, uri: str, api_key: str, zipcode: int, days: int):
        self.uri = uri
        self.api_key = api_key
        self.zipcode = zipcode
        self.days = days
        self.params = {"q" : self.zipcode, "key" : self.api_key, "days": self.days}

    def get(self):
        """
        returns data received from forecast API
        
        """
        body = requests.get(self.uri, self.params, verify=False)
        print("Status: ", body.status_code)
        if 400 <= body.status_code < 500:
            raise Exception(body["ExceptionMessage"])

        return body.json()


        