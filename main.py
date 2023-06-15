from sys_file.openweatherAPI import get_weather
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from flask import Flask
import requests
import time
import json
import os


app = Flask(__name__)


@app.route("/weather/<city_name>", methods=['GET'])
def weather(city_name):
    temp_celsius, feels_like_celsius, wind_speed, humidity, description = get_weather(city_name)
    jsonObj = {
        "City": city_name,
        "Temp_celsius": temp_celsius,
        "Feels_like_celsius": feels_like_celsius,
        "Wind_speed": wind_speed,
        "Humidity": humidity,
        "Description": description
    }
    return json.dumps(jsonObj)


if __name__ == '__main__':
    app.run(debug=True)
    print("API running...")