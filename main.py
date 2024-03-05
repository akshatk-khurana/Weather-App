import requests, sys, os, json, time
from datetime import datetime
from iso3166 import countries

API_KEY = "b249505b7e912e3b3b34821a4533c6f1" # API key

# Define needed functions
def readable_time(unix): 
    return datetime.fromtimestamp(int(unix)).strftime('%H:%M:%S')

def get_forecast():
    raw_forecast_data = requested.get

def get_weather(city): # Fetch and return data from API
    raw_weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
    status = raw_weather_data.status_code

    # Status code error handling
    if 500 <= status <= 599: print('The server was down. Try again in some time.'); return None
    elif 400 <= status <= 499: print('Incorrect city. Check the name of city you typed in.'); return None
    else: return sort_data(raw_weather_data.json())

def degrees_to_compass(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((degrees + 11.25)/22.5)
    return directions[index % 16]

def sort_data(data):
    # Define dictionary to contain sorted data
    info = dict()

    # Add selected data to above defined dictionary
    info['place'] = f"{data['name']}, {countries.get(data['sys']['country']).name}"
    info['humidity'] = data['main']['humidity']
    info['temp'], info['feels_like'] = data['main']['temp'], data['main']['feels_like']
    info['max'], info['min'] = data['main']['temp_max'], data['main']['temp_min']
    info['weather'] = data['weather'][0]['description']
    info['sunrise'], info['sunset'] = readable_time(data['sys']['sunrise']), readable_time(data['sys']['sunset'])
    info['wind_speed'], info['wind_direction'] = int(data['wind']['speed'])*3.6, degrees_to_compass(data['wind']['deg'])
    
    return info

def load_history(n):
    with open("history.json", "r") as history:
        # Return the last n searches and results
        return json.loads(history.read())

def save_history(item) -> None:
    with open('history.json', 'r') as read_history:
        # Set key value pair of timestamp and what was looked up at that time
        history = json.loads(read_history.read())
        history[datetime.now().strftime('%H:%M:%S')] = item

        # Update the JSON file
        with open('history.json', 'w') as write_history:
            write_history.write(json.dumps(history, indent=4))

def clear_history():
    # Clear the file and replace with an empty JSON object
    with open('history.json', 'w') as write_history:
        write_history.write(json.dumps({}))

def display(data, history=False):
    # Display data to the user in a readable format
    print(f"\nShowing current weather in {data['place']}")
    print(f"The current temperature is {data['temp']}°C and it feels like {data['feels_like']}°C")
    print(f"\nHumidity right now is {data['humidity']}%")
    print(f"\nGeneral description of weather today: {data['weather']}")
    print(f"Sunrise time is {data['sunrise']} and sunset time is {data['sunset']}.\n")
    print(f"\nWind direction is {data['wind_direction']} and wind speed is {data['wind_speed']}km/h.\n")

# Main while loop to keep prompting user
first_time, default = True, "Press [I] for help, [W] to get weather for a city, [H] for history and [Q] to quit: "
while True:
    choice = input("Welcome to CMD Weather! " + default if first_time == True else default).strip().lower()
    first_time = False

    # CLI implementation - give user options to choose from
    if choice == 'i':
        print("Commands are [W] to get the weather, [H] for history and [Q] to quit. They are case-insensitive. i.e both w and W will work!")
        print("History [H] will get you the last n searches in this session.")
        print("Quiting [Q] will exit the application and clear your search history for the session.")
    elif choice == 'w':
        city = input('What city would you like to view weather for?: ').strip()
        data = get_weather(city)
        display(data); save_history(data)
    elif choice == 'h':
        number = input("Number of previous searches to view: ")
        session_history = load_history(int(number))
            # Allow user to scroll
        keys = list(session_history.keys())
        while True:
            scroll = input('Press [F] to go forwards, [B] to go backwards and [E] to exit history scrolling: ').lower()
            if scroll == 'b'
        for k in :
            print(f'****{k}****'); display(session_history[k]); print()
    elif choice == 'q': 
        print('Exiting application!'); clear_history(); sys.exit()
    else: print('Unknown command entered.')

    if input("Clear past interactions? (y/n) ").lower() == 'y':
        os.system('cls' if os.name == 'nt' else "clear") 

"""
BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m""""