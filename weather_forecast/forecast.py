"""
This application queries openweathermap.org's 5-day forecast using requests and prints
a table from the result.
"""

import os
from datetime import datetime
import requests



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

    print(f'Error: Failed GET request. Status Code {response.status_code}')
    exit()

def decode_json(response):
    try:
        data = response.json()
        return data
    except AttributeError:
        print('Error: Failed parsing JSON from response object.')
        exit()


def pull_data(data_chunk):
    """
    Pulls relevant data from response dictionary.
    datetime is local because weather is local.
    """

    utc = str(datetime.fromtimestamp(data_chunk['dt']))
    temp = data_chunk['main']['temp']
    description = data_chunk['weather'][0]['description']
    wind_speed = data_chunk['wind']['speed']

    return utc, temp, description, wind_speed


def print_data(utc, temp, description, wind_speed):
    print(f'{utc:<20} | {temp:<15} | {description:<20} | {wind_speed}')


def iterate_data(data):
    """
    For chunk in data (decoded json), print row of table.
    """
    print_data('Date/Time', 'Temperature (F)', 'Weather Description', 'Wind Speed (MPH)')
    print('-' * 75)
    for chunk in data['list']:
        print_data(*pull_data(chunk))


def main():
    """
    Run all functions
    """
    response = get_open_weather()
    data = decode_json(response)
    iterate_data(data)

# I let the python interpreter raise a KeyError from pull_data() in order to preserve
# the stack trace.


main()
