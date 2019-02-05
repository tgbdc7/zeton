"""
Aplikacja: system żetonowy ucznia/dziecka

"""

from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime, timedelta
import sys
import os

import data_access
import auth
import db
from data_access import get_points


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='AplikacjaDlaStasia',
        DATABASE=os.path.join(app.root_path, 'db.sqlite'),
        SITE_NAME='Zeton'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(auth.bp)

    return app


app = create_app()


@app.route('/')
def hello():
    db.get_db()

    uczen = data_access.wczytaj_dane()
    ban = uczen['ban']

    punkty = uczen["punkty"]
    szkolny_rekord_tygodnia = uczen['szkolny_rekord_tygodnia']

    # Nadpisuję punkty i ban, danymi z bazy:
    punkty = get_points(user_id=1)
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
        data_access.zapisz_dane(uczen)

    return render_template('index.html', punkty=punkty, ban=ban, szkolny_rekord_tygodnia=szkolny_rekord_tygodnia,
                           time_ban_stop=time_ban_stop.strftime("%Y-%m-%d o godzinie: %H:%M:%S"),
                           python_version=python_version)


@app.route("/dodaj_punkt", methods=['POST', 'GET'])
def dodaj_punkt():
    db.get_db()
    user_id = 1  # TODO: to musi być dynamicznie ustawiane!

    #    mozliwe_punkty = [0, 1, 3]
    if request.method == 'POST':
        try:
            nowe_punkty = int(request.form['liczba_punktow'])
            if nowe_punkty > 0:
                data_access.add_points(user_id, nowe_punkty)
                # uczen = data_access.wczytaj_dane()
                # uczen["punkty"] += nowe_punkty
                # data_access.zapisz_dane(uczen)
        except Exception as e:
            pass

    return redirect(url_for('hello'))



@app.route("/wykorzystanie_punktow", methods=['POST', 'GET'])
def wykorzystaj_punkty():
    if request.method == 'POST':
        try:
            punkty_do_wykorzystania = int(request.form['liczba_punktow'])
            uczen = data_access.wczytaj_dane()
            if uczen["punkty"] >= punkty_do_wykorzystania:
                uczen["punkty"] -= punkty_do_wykorzystania
                data_access.zapisz_dane(uczen)
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
    uczen = data_access.wczytaj_dane()
    if uczen["ban"] is True:
        # # Jeśi jest już dany ban to przedłuża go o 24h
        uczen['time_ban_stop'] = datetime.strptime(uczen['time_ban_stop'], "%Y-%m-%dT%H:%M:%S.%f")
        uczen['time_ban_stop'] += timedelta(days=1)
        data_access.zapisz_dane(uczen)
        return redirect(url_for('hello'))

    if time_ban_start is None:
        time_ban_start = datetime.now()

    uczen['ban'] = True
    uczen['time_ban_start'] = time_ban_start
    uczen['time_ban_stop'] = time_ban_start + timedelta(days=1)
    data_access.zapisz_dane(uczen)
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run()
