from dotenv import load_dotenv
import requests, sys, os, json
import pprint

# API key
API_KEY = "b249505b7e912e3b3b34821a4533c6f1"

# Input
city = input('City: ')

# Retrieve information
raw_location_data = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}')

location_data = json.loads((raw_location_data.content).decode())
longitude = location_data[0].get('')