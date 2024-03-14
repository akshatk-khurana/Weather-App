# Weather App

## Description
A command line weather app that allows users to get the weather of a certain city in the current moment. It uses the OpenWeatherMap Current Weather API (https://openweathermap.org/current) to get weather information. It uses the iso3166 and colorama libraries to enhance user experience.

## Features
This is quite a basic app but has the following enabled:
- Weather by city (Current temperature, daily minimum and maximum, humidity, wind speed and direction, sunset and sunsrise information)
- Search history allows the user to view what city they got weather for and the information they were given at the time. This is stored in a JSON file which is cleared once the user quits the application.
- Error handling; provided an external API is used, there are checks in place to check the response received and deliver an appropriate message or response to the user. e.g 200 is good

## How to run
Prior to running the application run ```pip(3) -r install requirements.txt``` in the terminal.
Also make sure the **history.json** file is in the same directory as **main.py**.
Finally, to run the application run ```python(3) main.py```
>>>>>>> Stashed changes
