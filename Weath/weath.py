#!/usr/bin/env python3

import requests

def get_current_weather(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&appid=35391bf0e26dc5c88a21b99255729f66&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def main():
    # Enter your OpenWeatherMap API key here
    api_key = "35391bf0e26dc5c88a21b99255729f66"

    # Enter the latitude and longitude of the location you want to get weather data for
    lat = 1.2921  # Example latitude (Nairobi)
    lon = 36.8219  # Example longitude (Nairobi)

    weather_data = get_current_weather(api_key, lat, lon)

    print("Response from API:")
    print(weather_data)  # Print out the entire response data for inspection

    try:
        # Extracting relevant information from the response
        current_weather = weather_data["current"]
        temperature = current_weather["temp"]
        weather_description = current_weather["weather"][0]["description"]

        print(f"Temperature: {temperature}°C")
        print(f"Weather: {weather_description}")
    except KeyError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
