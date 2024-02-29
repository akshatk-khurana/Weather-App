"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('sample.html')

if __name__ == '__main__':
    app.run()
"""

from dotenv import load_dotenv
import requests, sys, os, json

# API key
API_KEY = ""


# Retrieve
# requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q=&limit=1&appid={API_KEY}')
