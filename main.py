import requests, sys, os, json, time
from datetime import datetime
from iso3166 import countries

API_KEY = "b249505b7e912e3b3b34821a4533c6f1" # API key

# Define needed functions
def readable_time(unix): 
    return datetime.fromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')

def get_weather(city): # Fetch and return data from API
    raw_weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
    status = raw_weather_data.status_code

    # Status code error handling
    if 500 <= status <= 599: print('The server was down. Try again in some time.'); return None
    elif 400 <= status <= 499: print('Incorrect city. Check the name of city you typed in.'); return None
    else: return sort_data(raw_weather_data.json())

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
    
    return info

def load_history(n):
    with open("history.json", "r") as history:
        selected = json.loads(history.read())
        keys_list = list(selected.keys())
        if len(keys_list) == 0:
            print('No past history this session.')
            return None

        if n > len(keys_list):
            return selected
        # Return the last n searches and results
        return {i:selected[i] for i in list(selected.keys())[::-1][0:int(n)]}

def save_history(item) -> None:
    with open('history.json', 'r') as read_history:
        # Set key value pair of timestamp and what was looked up at that time
        history = json.loads(read_history.read())
        history[datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = item

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
    print(f"The current temperature is: {data['temp']}°C but it feels like {data['feels_like']}°C")
    print(f"\n")

# Main while loop to keep prompting user
first_time, default = True, "Press [I] for help, [W] to get weather for a city, [H] for history and [Q] to quit: "
while True:
    os.system('clear')
    choice = input("Welcome to CMD Weather! " + default if first_time == True else default).strip().lower()
    first_time = False

    # CLI implementation - give user options to choose from
    if choice == 'i':
        print("""This is a simple application to show the weather.
            Commands are [W] to get the weather, [H] for history and [Q] to quit.
            
            History will get you the last n searches in this session.""")
    elif choice == 'w':
        city = input('What city would you like to view weather for?: ').strip()
        data = get_weather(city)
        display(data); save_history(data)
    elif choice == 'h':
        number = input("Number of previous searches to view: ")
        session_history = load_history(int(number))
        if session_history is not None:
            # Print out requested amount of past searches
            print()
            for k in session_history.keys():
                print(f'****{k}****'); display(session_history[k]); print()
    elif choice == 'q': 
        print('Exiting application!'); clear_history(); sys.exit()
    else:
        print('Unknown command entered.')

    if choice.lower() in ['i', 'w', 'h']: time.sleep(2)