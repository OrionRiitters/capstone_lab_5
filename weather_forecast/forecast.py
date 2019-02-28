"""
This application queries openweathermap.org's 5-day forecast using requests and prints a table from the resulting JSON.
"""

import os
import requests
from datetime import datetime


def get_open_weather():
    """
    This method queries the openweathermap API with a key saved in the environment.
    """
    key = os.environ.get('WEATHER_KEY')
    query = {'q': 'minneapolis,us', 'units': 'imperial', 'appid': key}
    url = 'http://api.openweathermap.org/data/2.5/forecast'

    response = requests.get(url, params=query)

    if response.status_code == 200:
        return response
    else:
        raise IOError(response.status_code)

def decode_json(response):
    try:
        data = response.json()
        return data
    except AttributeError:
        raise AttributeError('Error: Failed parsing JSON from response object.')


def pull_data(dict):
    """
    Pulls relevant data from response dictionary.
    datetime is local because weather is local.
    """
    try:
        utc = str(datetime.fromtimestamp(dict['dt']))
        temp = dict['main']['temp']
        description = dict['weather'][0]['description']
        wind_speed = dict['wind']['speed']
    except KeyError:
        raise

    return utc, temp, description, wind_speed

def print_data(utc, temp, description, wind_speed):
    print(f'{utc:<20} | {temp:<15} | {description:<20} | {wind_speed}')


def iterate_data(data):
    print_data('Date/Time', 'Temperature (F)', 'Weather Description', 'Wind Speed (MPH)')
    print('-' * 75)
    try:
        for dict in data['list']:
            print_data(*pull_data(dict))
    except TypeError:
        raise
def main():

    try:
        response = get_open_weather()
        data = decode_json(response)
        iterate_data(data)

# I let the python interpreter raise a KeyError from pull_data() in order to preserve
# the stack trace.
    except IOError as err:
       status_code = err.args[0]
       print(f'Error: Failed GET request. Status Code {status_code}')
    except AttributeError as err:
        print(err.args[0])

main()

