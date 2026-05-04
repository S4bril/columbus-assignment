# Columbus Assignment

## Description

An AWS Lambda function that returns the current temperature and temperature category for a given city. It uses Open-Meteo API as a data source and is exposed via a Lambda Function URL.

## Key Design Decisions

- **`OpenMeteoFacade`** - responsible for using Open-Meteo api. The rest of the code has no knowledge of the API's structure.
- **`WeatherMapper`** - contains all business logic (temperature classification).
- **`handler`** - orchestration: calls the facade, passes the result to the mapper, returns a JSON response.

## Unit Testing Without the Real API

`OpenMeteoFacade` can be replaced with a test double (mock or stub) that returns a hardcoded `OpenMeteoSimpleWeatherData` object.

## Task 3 – Endpoint Exposure

**Endpoint:** `https://vhj5vbigijfft36rxw7fhzdzwe0rdeed.lambda-url.eu-central-1.on.aws/`

**GET parameter:** `city`

**Example request:**

```
GET https://vhj5vbigijfft36rxw7fhzdzwe0rdeed.lambda-url.eu-central-1.on.aws/?city=Helsinki
```

**Example response:**

```json
{
  "temperature": 10.8,
  "temperature_category": "Mild",
  "city": "Helsinki"
}
```

## Task 4 – Design Reflection

Adding a second provider requires only a new facade class. Business logic in `WeatherMapper` does not need to change.

The one limitation is that `WeatherMapper` accepts the concrete `OpenMeteoSimpleWeatherData` type directly.

Given more time, I would introduce a interface for provider data in the services layer, removing this dependency.
