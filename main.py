import requests, sys, os, json, time # General utility modules
from datetime import datetime # Work with date time
from iso3166 import countries # To convert country codes to names
from colorama import Fore # To add colours to CLI

API_KEY = "b249505b7e912e3b3b34821a4533c6f1" # API key

# Define formatting colours
RED, GREEN, BLUE = "\033[0;31m", "\033[0;32m", "\033[0;34m"

# Define needed functions
def readable_time(unix): # Convert a UNIX timestamp to a readable one
    return datetime.fromtimestamp(int(unix)).strftime('%H:%M:%S')

def clear_screen(): # Clear screen based off OS 
    os.system('cls' if os.name == 'nt' else "clear") 

def get_weather(city): # Fetch and return data from API
    raw_weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
    status = raw_weather_data.status_code

    # Status code error handling
    if 500 <= status <= 599: # If server errors occur.
        print('The server was down. Try again in some time.'); return None
    elif 400 <= status <= 499: # If the user inputs invalid city.
        print('\nIncorrect city. Check the name of city you typed in.\n'); return None
    else: 
        return sort_data(raw_weather_data.json())

def degrees_to_compass(degrees): # Convert degrees to compass directions
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((degrees + 11.25)/22.5)
    return directions[index % 16]

def sort_data(data): # Sort out needed values
    info = dict() # Define dictionary to contain sorted data

    # Add selected data to above defined dictionary
    info['place'] = f"{data['name']}, {countries.get(data['sys']['country']).name}"
    info['humidity'] = data['main']['humidity']
    info['temp'], info['feels_like'] = data['main']['temp'], data['main']['feels_like']
    info['max'], info['min'] = data['main']['temp_max'], data['main']['temp_min']
    info['weather'] = data['weather'][0]['description']
    info['sunrise'], info['sunset'] = readable_time(data['sys']['sunrise']), readable_time(data['sys']['sunset'])
    info['wind_speed'], info['wind_direction'] = int(data['wind']['speed'])*3.6, degrees_to_compass(data['wind']['deg'])
    return info

def load_history():
    with open("history.json", "r") as history:
        # Return the last n searches and results
        return json.loads(history.read())

def save_history(item):
    with open('history.json', 'r') as read_history:
        # Set key value pair of timestamp and search
        history = json.loads(read_history.read())
        history[datetime.now().strftime('%H:%M:%S')] = item

        # Update the JSON file
        with open('history.json', 'w') as write_history:
            write_history.write(json.dumps(history, indent=4))

def clear_history():
    # Clear the file and replace with an empty JSON object
    with open('history.json', 'w') as write_history:
        write_history.write(json.dumps({}))

def display(data):
    # Display data to the user in a readable format
    print(f"{BLUE}Showing current weather in {data['place']}")
    print(f"The current temperature is {data['temp']}°C and it feels like {data['feels_like']}°C")
    print(f"\nHumidity right now is {data['humidity']}%")
    print(f"Wind is coming from {data['wind_direction']} and wind speed is {data['wind_speed']}km/h.\n")
    print(f"General description of weather today: {data['weather']}")
    print(f"Sunrise time is {data['sunrise']} and sunset time is {data['sunset']}.")

# Main while loop to keep prompting user
first_time, default = True, RED+"Press [I] for help, [W] to get weather for a city, [H] for history and [Q] to quit: "
while True:
    choice = input(RED+"Welcome to CMD Weather! \n" + default if first_time == True else default).strip().lower()
    first_time = False

    # CLI implementation - give user options to choose from
    if choice == 'i':
        print(Fore.GREEN+"\nCommands are [W] to get the weather, [H] for history and [Q] to quit. They are case-insensitive. i.e both w and W will work!")
        print("You will be asked if you want to clear interactions in the terminal after each command.")
        print("History [H] will allow you to scroll through.")
        print("Quiting [Q] will exit the application and clear your search history for the session.\n")
    elif choice == 'w':
        city = input('\nWhat city would you like to view weather for?: ').strip()
        data = get_weather(city)
        if data is not None:
            print(); display(data); print()
            save_history(data)
    elif choice == 'h':
        clear_screen()
        session_history = load_history()
        
        # Allow user to scroll and view history
        keys = list(session_history.keys())
        if len(keys) > 0:
            index = 1
            while True:
                # Show first portion of history
                print(f'{Fore.BLUE}\n------{keys[index-1]}------')
                display(session_history[keys[index-1]])
                print('----------------------\n')

                print(f'SHOWING SEARCH {index} OF {len(keys)}')
                scroll = input('Press [F] to go forwards, [B] to go backwards and [E] to exit history scrolling: ').lower()
                clear_screen()
                if scroll == 'b': # Move backwards
                    index = index - 1 if index > 1 else index
                elif scroll == 'f': # Move forwards
                    index = index + 1 if index < len(keys) else index
                elif scroll == 'e':
                    break # Go back to main loop
        else: 
            print('No past search history.')
    elif choice == 'q': 
        print('Exiting application!'); clear_history(); sys.exit()
    else: 
        print('Unknown command entered.')

    # Ask user if they want to clear their screen
    if input(Fore.RED+"Clear past interactions in the terminal? (y/press any other key): ").lower() == 'y':
        clear_screen()