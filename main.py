import requests, sys, os, json, time # General utility modules
from datetime import datetime # Work with date time
from iso3166 import countries # To convert country codes to names
from colorama import Fore, init # To add colours to CLI

API_KEY = "" # API key
init() # Initialise colours

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
        print('The server was down. Try again in some time.')
    elif 400 <= status <= 499: # If the user inputs invalid city.
        if status == 401: # If no API key given
            print('\nCheck your API key!')
        else:
            print('\nIncorrect city. Check the name of city you typed in.\n')
    else: 
        return sort_data(raw_weather_data.json())
    return None

def degrees_to_compass(degrees): # Convert degrees to compass directions
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((degrees + 11.25)/22.5) # Calculate direction
    return directions[index % 16] # Access appropriate direction from directions list

def sort_data(data): # Sort out needed values from API data
    info, country = dict(), None 
    try:
        country = ', '+countries.get(data['sys']['country']).name
    except: country = '' # If iso3166 cannot find country of the location typed in.

    # Add selected data to above defined dictionary
    info['place'] = f"{data['name']}{country}"
    info['humidity'] = data['main']['humidity']
    info['temp'], info['feels_like'] = data['main']['temp'], data['main']['feels_like']
    info['max'], info['min'] = data['main']['temp_max'], data['main']['temp_min']
    info['weather'] = data['weather'][0]['description']
    info['sunrise'], info['sunset'] = readable_time(data['sys']['sunrise']), readable_time(data['sys']['sunset'])
    info['wind_speed'], info['wind_direction'] = int(data['wind']['speed'])*3.6, degrees_to_compass(data['wind']['deg'])
    return info

def load_history():
    with open("history.json", "r") as history:
        return json.loads(history.read()) # Return past interactions

def save_history(item):
    with open('history.json', 'r') as read_history:
        # Set key value pair of timestamp and interaction
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
    print(f"{Fore.BLUE}Showing current weather in {data['place']}:\n")
    print(f"The current temperature is {data['temp']}°C and it feels like {data['feels_like']}°C.")
    print(f"The maximum temperature for today is {data['max']}°C and the minimum temperature is {data['min']}°C.")
    print(f"\nHumidity right now is {data['humidity']}%.")
    print(f"Wind direction is {data['wind_direction']} and wind speed is {data['wind_speed']}km/h.\n")
    print(f"The general description of weather today is {data['weather']}.")
    print(f"Sunrise time is {data['sunrise']} and sunset time is {data['sunset']}.")

# Main while loop to keep prompting user
first_time, default = True, Fore.RED+"Press [I] for help, [W] to get weather for a city, [H] for history and [Q] to quit: "
while True:
    choice = input(Fore.RED+"Welcome to CMD Weather! \n" + default if first_time == True else default).strip().lower()
    first_time = False

    # CLI implementation - give user options to choose from
    if choice == 'i':
        print(Fore.GREEN+"\nCommands are case-insensitive. i.e both w and W will work!")
        print("[W] will let you get the weather for a city/place.")
        print("[H] will allow you to scroll through your past history of searches.")
        print("[Q] will exit the application and clear your search history for the session.\n")
    elif choice == 'w':
        city = input('\nWhat city would you like to view weather for?: ').strip()
        try:
            data = get_weather(city)
            if data is not None:
                print(); display(data); print()
                save_history(data)
        except requests.exceptions.ConnectionError:
            print('\nCheck your internet connection!')
    elif choice == 'h':
        clear_screen()
        session_history = load_history()
        
        # Allow user to scroll and view history
        keys = list(session_history.keys()) # Get a list of timestamps to go back and forth through
        if len(keys) > 0: # Check if there is any history
            index = 1
            while True:
                # Show first portion of history
                print(f'{Fore.BLUE}\n------{keys[index-1]}------')
                display(session_history[keys[index-1]])
                print('----------------------\n')

                print(f'SHOWING SEARCH {index} OF {len(keys)}')
                scroll = input('Press [F] to go forward, [B] to go back and [E] to exit scrolling: ').lower()
                clear_screen()
                if scroll == 'b': # Move backwards in history
                    index = index - 1 if index > 1 else index
                elif scroll == 'f': # Move forwards in history
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
    if input(Fore.RED+"\nClear past interactions in the terminal? (y/press any other key): ").lower() == 'y':
        clear_screen()