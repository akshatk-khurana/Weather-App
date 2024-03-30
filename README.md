# Weather App

## Description
A command line weather app that allows users to get the weather of a certain city in the current moment. It uses the OpenWeatherMap Current Weather API (https://openweathermap.org/current) with the requests module to get weather information. It uses the iso3166 and colorama libraries to enhance user experience.

## Features
This is quite a basic app but has the following enabled:
- Clear interface to direct user to specific commands (which are case-insenstive). Commands are:
  - [I] for help/information about the application
  - [H] for session search history (only valid search options are saved to history)
  - [Q] for quitting the applicaiton and in doing so, clearing the session history
  - [W] for getting the weather for a city in particular

- Allows user to get the weather by city. This includes:
  - Current temperature
  - Daily minimum and maximum temperature
  - Humidity
  - Wind speed and direction
  - Sunset and sunsrise times
    
- Search history allows the user to view what city they got weather for and the information they were given at the time. This is stored in a JSON file which is cleared once the user quits the application.
- Any errors are handled, especially those to do with using an external API. There are checks in place for the response received and deliver an appropriate message or response to the user. e.g 200 is good, 400 is a user error (wrong city typed), 500 is a server error (if the API server crashes)

## Usage
Prior to running the application do the following:
- run ```pip -r install requirements.txt``` in the terminal
- make sure the **history.json** file is in the same directory as **main.py**
- replace the API_KEY variable in **main.py** with your OpenWeatherMap API key.
- Finally, to run the application run ```python main.py``` in the directory of the project.
