import json

from external_api.open_meteo.open_meteo_facade import OpenMeteoFacade
from services.weather_mapper import WeatherMapper


def handler(event, context):
    print("Received event: " + str(event))
    query_params = event.get("queryStringParameters") or {}
    city = query_params.get("city") or event.get("city", "Wrocław")

    open_meteo_facade = OpenMeteoFacade()
    open_meteo_data = open_meteo_facade.get_weather(city=city)
    weather_data = WeatherMapper.map_open_meteo_to_weather_data(open_meteo_data)

    print("Mapped weather data: " + str(weather_data))

    return {
        'statusCode': 200,
        'body': json.dumps(weather_data.__dict__)
    }
