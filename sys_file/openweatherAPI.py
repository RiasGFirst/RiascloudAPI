from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import time
import os

#Load Env Variable
load_dotenv()
openweather_url = os.getenv("OPENWEATHER_URL")
openweather_apikey = os.getenv("API_KEY_OPENWEATHER")


# Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius


def get_weather(city_name):
    url = f"{openweather_url}appid={openweather_apikey}&q={city_name}"
    response = requests.get(url).json()

    temp_kelvin = response["main"]["temp"]
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)
    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']

    return temp_celsius, feels_like_celsius, wind_speed, humidity, description

