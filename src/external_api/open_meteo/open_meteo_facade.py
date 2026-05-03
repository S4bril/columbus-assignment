from dataclasses import dataclass
from urllib.request import Request, urlopen
from urllib.parse import quote

import json


@dataclass
class OpenMeteoSimpleWeatherData:
    temperature_celsius: float
    city: str


class OpenMeteoFacade:
    def __init__(self):
        self.open_meteo_forecast_url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude={lat}&longitude={lon}&current=temperature_2m"
        )

        self.open_meteo_geocoding_url = (
            "https://geocoding-api.open-meteo.com/v1/search?name={city}"
        )

    def __get_open_meteo_forecast_url(self, lat: float, lon: float) -> str:
        return self.open_meteo_forecast_url.format(lat=lat, lon=lon)

    def __get_open_meteo_geocoding_url(self, city: str) -> str:
        return self.open_meteo_geocoding_url.format(city=city)

    def __get_city_coordinates(self, city: str) -> tuple[float, float]:
        safe_city = quote(city)
        request = Request(self.__get_open_meteo_geocoding_url(safe_city))
        with urlopen(request) as response:
            body = response.read().decode('utf-8')
            data = json.loads(body)

        if not data["results"]:
            raise ValueError(f"City '{city}' not found in the geocoding API.")

        first_result = data["results"][0]
        return first_result["latitude"], first_result["longitude"]

    def __get_city_current_temperature(self, lat: float, lon: float) -> float:
        request = Request(self.__get_open_meteo_forecast_url(lat, lon))
        with urlopen(request) as response:
            body = response.read().decode('utf-8')
            data = json.loads(body)

        return data["current"]["temperature_2m"]

    def get_weather(self, city: str) -> OpenMeteoSimpleWeatherData:
        lat, lon = self.__get_city_coordinates(city)
        temperature = self.__get_city_current_temperature(lat, lon)

        return OpenMeteoSimpleWeatherData(temperature_celsius=temperature, city=city)
