import requests, sys, os, json, pprint, keyboard
from datetime import datetime
from iso3166 import countries

API_KEY = "b249505b7e912e3b3b34821a4533c6f1" # API key

# Define needed functions
def get_weather(city):
    raw_weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}')
    weather_data = (raw_weather_data.json())
    city_name, country_name = weather_data['name'], countries.get(weather_data['sys']['country']).name
    print(f"Showing current weather in {city_name}, {country_name}")
    return city_name, country_name

# Main while loop to keep prompting user
first_time = True; default = "Press [I] for help, [W] to get weather for a city, [H] for history and [Q] to quit: "
while True:
    choice = input("Welcome to CMD Weather! " + default if first_time == True else default).strip().lower()

    if first_time == True:
        first_time = False

    if choice == 'i':
        print('You pressed help!')
    elif choice == 'w':
        city = input('What city would you like to view weather for?: ').strip()
        try:
            get_weather(city)
        except:
            print('An error, occurred!')
    elif choice == 'h':
        print('Showing history!')
    elif choice == 'q':
        print('Exiting application!')
        sys.exit()
    else:
        print('Unknown command entered.')