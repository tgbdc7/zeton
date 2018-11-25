"""
Aplikacja: system żetonowy ucznia/dziecka

"""

from flask import Flask, redirect, render_template
from flask import request, url_for
import json

app = Flask(__name__)


@app.route('/')
def hello():
    uczen = wczytaj_dane()
    punkty = uczen["punkty"]

    return render_template('dodaj_punkty.html', punkty=punkty)


@app.route("/wszystkie-posty", methods=['POST', 'GET'])
def dodaj_punkt():
    # if request.method == 'GET':
    #    mozliwe_punkty = [0, 1, 3]
    if request.method == 'POST':
        try:
            nowe_punkty = int(request.form['liczba_punktow'])
            if nowe_punkty > 0:
                uczen = wczytaj_dane()
                uczen["punkty"] += nowe_punkty
                zapisz_dane(uczen)

        except:
            pass
        finally:
            return redirect(url_for('hello'))


def wczytaj_dane():
    """
    Wczytuje dane z pliku dane.json
    Jeśli nie ma tego pliku to go tworzy z ustawionymi wartościmai na "0"
    :return: dane ucznia
    """
    try:
        with open('dane.json', 'r') as plik:
            dane = json.load(plik)
    except FileNotFoundError:
        with open('dane.json', 'w') as plik:
            dane = {"punkty": 0, "szkolny_rekord_tygodnia": 0}
            json.dump(dane, plik)
    return dane


def zapisz_dane(dane):
    """
    zapisuje dane do pliku "dane.json"
    :param dane: dane ucznia - słownik (dictionary)
    :return: None
    """
    try:
        with open('dane.json', 'w') as plik:
            json.dump(dane, plik)
    except:
        return f'Nie można zapisać dancyh do pliku'


@app.route("/wykorzystanie_punktow", methods=['POST', 'GET'])
def wykorzystaj_punkty():
    if request.method == 'POST':
        try:
            punkty_do_wykorzystania = int(request.form['liczba_punktow'])
            uczen = wczytaj_dane()
            if uczen["punkty"] >= punkty_do_wykorzystania:
                uczen["punkty"] -= punkty_do_wykorzystania
                zapisz_dane(uczen)
            else:
                print("Niestety nie masz wystarczajaco duzo punktow na ta nagrode")
        except:
            pass
        finally:
            return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run()
