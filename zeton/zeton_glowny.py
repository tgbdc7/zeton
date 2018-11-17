
"""
Aplikacja: system żetonowy

"""

from flask import Flask, redirect, render_template
from flask import request, url_for
import json


app = Flask(__name__)


@app.route('/')
def hello():

    punkty = wczytaj_dane()

    return render_template('dodaj_punkty.html', punkty=punkty)


@app.route("/wszystkie-posty", methods=['POST', 'GET'])

def dodaj_punkt():
    if request.method == 'POST':
        try:
            nowe_punkty = int(request.form['liczba_punktow'])
            punkty = wczytaj_dane()
            punkty += nowe_punkty
            zapisz_dane(punkty)
        except:
            pass
        finally:
            return redirect(url_for('hello'))


def wczytaj_dane():

    try:
        with open('dane.json', 'r') as plik:
            punkty = json.load(plik)
    except FileNotFoundError:
        with open('dane.json', 'w') as plik:
            punkty = 0
            json.dump(punkty, plik)
    return punkty

def zapisz_dane (punkty):

    try:
        with open('dane.json','w') as plik:
            json.dump(punkty,plik)
    except:
        return f'Nie można zapisać dancyh do pliku'



if __name__ == '__main__':
    app.run()
