"""
Aplikacja: system żetonowy

"""

from flask import Flask
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World xx!'

def dodaj_punkt(nowe_punkty):
    return nowe_punkty


app.run()