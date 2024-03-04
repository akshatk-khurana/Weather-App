import requests, sys, os, json, pprint   
from datetime import datetime
from iso3166 import countries

API_KEY = "b249505b7e912e3b3b34821a4533c6f1" # API key

# Define needed functions
def readable_time(unix):
    return datetime.fromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')

def get_weather(city):
    raw_weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
    status = raw_weather_data.status_code

    if 500 <= status <= 599: print('The server was down. Try again in some time.')
    elif 400 <= status <= 499: print('Incorrect city. Check the name of city you typed in.')
    else: return sort_data(raw_weather_data.json())
    return None

def sort_data(data):
    pprint.pprint(data)
    info = dict()
    info['place'] = f"{data['name']}, {countries.get(data['sys']['country']).name}, "
    info['humidity'] = data['main']['humidity']
    info['temp'], info['feels_like'] = data['main']['temp'], data['main']['feels_like']
    info['max'], info['min'] = data['main']['temp_max'], data['main']['temp_min']
    info['weather'] = data['weather'][0]['description']
    info['sunrise'], info['sunset'] = readable_time['sys']['sunrise'], readable_time['sys']['sunset']
    return info

def load_history(number):
    with open("history.json", "r") as history:
        selected = json.loads(history.read())
        return {i:selected[i] for i in list(selected.keys())[0:number]}

def save_history(item):
    pass

def clear_history():
    with open('history.json', 'w') as history: history.write('')

def display(data):
    print(f"Showing current weather in {data['place']}.")
    print(f"Current temperature: {data['temp']} Feels like {data['feels_like']}")

# Main while loop to keep prompting user
first_time, default = True, "Press [I] for help, [W] to get weather for a city, [H] for history and [Q] to quit: "
while True:
    choice = input("Welcome to CMD Weather! " + default if first_time == True else default).strip().lower()
    first_time = False

    if choice == 'i':
        print('This is a simple application to show the weather.\nCommands are [W] to get the weather, [H] for history and [Q] to quit.')
    elif choice == 'w':
        city = input('What city would you like to view weather for?: ').strip()
        display(get_weather(city))
    elif choice == 'h':
        number = input("How many items of your session history would you like to view?: ")
        print('\n'.join(load_history(number)))
        
    elif choice == 'q': print('Exiting application!'); sys.exit()
    else:
        print('Unknown command entered.')