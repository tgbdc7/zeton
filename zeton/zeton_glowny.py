"""
Aplikacja: system żetonowy

"""

from flask import Flask, redirect, render_template
import json

# punkty = 19

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
        nowe_punkty = request.form['liczba_punktow']
    return redirect()


if __name__ == '__main__':
    app.run()
