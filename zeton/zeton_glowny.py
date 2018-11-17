
"""
Aplikacja: system żetonowy

"""

from flask import Flask, redirect, render_template
from flask import request, url_for
import json

punkty = None

app = Flask(__name__)


@app.route('/')
def hello():
    global punkty
    try:
        with open('dane.json', 'r') as plik:
            punkty = json.load(plik)
    except FileNotFoundError:
        with open('dane.json', 'w') as plik:
            punkty = 0
            json.dump(punkty, plik)
    return render_template('dodaj_punkty.html', punkty=punkty)


@app.route("/wszystkie-posty", methods=['POST', 'GET'])
def dodaj_punkt():
    if request.method == 'POST':
        try:
            nowe_punkty = int(request.form['liczba_punktow'])
            punkty += nowe_punkty
            with open('dane.json', 'w') as plik:
                json.dump(punkty, plik)
        except:
            pass
        finally:
            return redirect(url_for('hello'))
    

if __name__ == '__main__':
    app.run()
