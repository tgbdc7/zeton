"""
Aplikacja: system żetonowy ucznia/dziecka

"""

from flask import Flask, redirect, render_template
from flask import request, url_for
import json, time
from datetime import datetime, date, timedelta

app = Flask(__name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


@app.route('/')
def hello():
    uczen = wczytaj_dane()
    punkty = uczen["punkty"]
    ban = uczen['ban']
    szkolny_rekord_tygodnia = uczen['szkolny_rekord_tygodnia']
    time_ban_stop = datetime.fromisoformat(uczen['time_ban_stop'])

    return render_template('index.html', punkty=punkty, ban=ban, szkolny_rekord_tygodnia=szkolny_rekord_tygodnia,
                           time_ban_stop=time_ban_stop)


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
            dane = {"punkty": 0, "szkolny_rekord_tygodnia": 0, "ban": False}
            json.dump(dane, plik, default=json_serial)
    return dane


def zapisz_dane(dane):
    """
    zapisuje dane do pliku "dane.json"
    :param dane: dane ucznia - słownik (dictionary)
    :return: None
    """
    try:
        with open('dane.json', 'w') as plik:
            json.dump(dane, plik, default=json_serial)
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
                print("Niestety nie masz wystarczająco duzo punktów na ta nagrodę")
        except:
            pass
        finally:
            return redirect(url_for('hello'))


@app.route("/ban")
def daj_bana(time_ban_start=None):
    """
    Dajemy bana
    :param  time_ban_start: czas dania bana, jeśli nie podany to pobiera aktualny czas
    :return: None,  zapisuje dane ucznia do pliku/ bazy
    """
    uczen = wczytaj_dane()
    if uczen["ban"] is True:
        # # Jeśi jest już dany ban to przedłuża go o 24h
        uczen['time_ban_stop'] = datetime.fromisoformat(uczen['time_ban_stop'])
        uczen['time_ban_stop'] += timedelta(days=1)
        zapisz_dane(uczen)
        return redirect(url_for('hello'))

    if time_ban_start is None:
        time_ban_start = datetime.now()

    uczen['ban'] = True
    uczen['time_ban_start'] = time_ban_start
    uczen['time_ban_stop'] = time_ban_start + timedelta(days=1)
    zapisz_dane(uczen)
    return redirect(url_for('hello'))


def odliczaj_czas_warna(t):
    """
    Funkcja odliczajaca czas warna (minuty:sekundy)
    Dziala, ale nie dodalam jeszcze przekazania liczby sekund do funkcji
    """
    while t:
        minuty, sekundy = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(minuty, sekundy)
        print(timeformat, end="\r")
        time.sleep(1)
        t -= 1
    print("Koniec warna")


if __name__ == '__main__':
    app.run()
