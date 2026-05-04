from dataclasses import dataclass
from enum import Enum

from external_api.open_meteo.open_meteo_facade import OpenMeteoSimpleWeatherData


class TemperatureCategory(str, Enum):
    Freezing = "Freezing"
    Cold = "Cold"
    Mild = "Mild"
    Warm = "Warm"
    Hot = "Hot"


@dataclass
class WeatherData:
    temperature: float
    temperature_category: TemperatureCategory
    city: str


class WeatherMapper:
    @staticmethod
    def map_open_meteo_to_weather_data(open_meteo_data: OpenMeteoSimpleWeatherData) -> WeatherData:
        temperature = open_meteo_data.temperature_celsius
        city = open_meteo_data.city
        if temperature < 0:
            category = TemperatureCategory.Freezing
        elif temperature <= 10:
            category = TemperatureCategory.Cold
        elif temperature <= 20:
            category = TemperatureCategory.Mild
        elif temperature <= 30:
            category = TemperatureCategory.Warm
        else:
            category = TemperatureCategory.Hot

        return WeatherData(temperature=temperature, temperature_category=category, city=city)
