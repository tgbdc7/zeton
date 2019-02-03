"""
Aplikacja: system żetonowy ucznia/dziecka

"""

from flask import Flask, redirect, render_template
from flask import request, url_for
from datetime import datetime, timedelta
import sys
import os
import sqlite3
from flask import g

from data_access import wczytaj_dane, zapisz_dane

app = Flask(__name__)

"""stworzenie objektu config"""
app.config.update(dict(
    SECRET_KEY='AplikacjaDlaStasia',
    DATABASE=os.path.join(app.root_path, 'db.sqlite'),
    SITE_NAME='Zeton'
))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Zamykanie połączenia z bazą"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_points(user_id):
    query = 'select suma_punktow from punkty_uczniow where id_ucznia = ?'
    result = get_db().cursor().execute(query, (user_id,))
    points = result.fetchone()[0]
    return points


def get_weekly_highscore(user_id):
    # TODO: do dopisania na podstawie funkcji 'get_points()'
    pass


@app.route('/')
def hello():
    uczen = wczytaj_dane()
    ban = uczen['ban']

    punkty = uczen["punkty"]
    szkolny_rekord_tygodnia = uczen['szkolny_rekord_tygodnia']

    # Nadpisuję punkty i ban, danymi z bazy:
    punkty = get_points(user_id=1)
    # szkolny_rekord_tygodnia = get_weekly_highscore(user_id=1)

    python_version = sys.version

    try:
        # datetime.fromisoformat is on > python3.7
        # nasz serwer działa na python 3.6
        # dlatego skorzystamy z datetime.strip
        time_ban_stop = datetime.strptime(uczen['time_ban_stop'], "%Y-%m-%dT%H:%M:%S.%f")

    except (TypeError, KeyError):
        # Gdy nie ma takiej pozycji w pliku
        time_ban_stop = datetime(1969, 10, 29, 22, 30)
    if ban and time_ban_stop < datetime.now():
        ban = False
        uczen['ban'] = ban
        zapisz_dane(uczen)

    return render_template('index.html', punkty=punkty, ban=ban, szkolny_rekord_tygodnia=szkolny_rekord_tygodnia,
                           time_ban_stop=time_ban_stop.strftime("%Y-%m-%d o godzinie: %H:%M:%S"),
                           python_version=python_version)


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
        uczen['time_ban_stop'] = datetime.strptime(uczen['time_ban_stop'], "%Y-%m-%dT%H:%M:%S.%f")
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


if __name__ == '__main__':
    app.run()
