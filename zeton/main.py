"""
Aplikacja: system żetonowy ucznia/dziecka

"""

from flask import Flask, redirect, render_template, request, url_for, session
from datetime import datetime
import os

import data_access
import auth
import db


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
@auth.login_required
def hello():
    db.get_db()
    USER_ID = session.get('user_id', None)
    firstname = data_access.get_firstname(USER_ID)

    ban = data_access.get_last_active_ban(USER_ID)
    points = data_access.get_points(USER_ID)
    weekly_highscore = data_access.get_weekly_highscore(user_id=1)

    context = {"firstname": firstname,
               "points": points,
               "ban": ban,
               "weekly_highscore": weekly_highscore}
    if ban:
        context["time_ban_stop"] = (ban['end'] - datetime.now()).seconds // 60

    return render_template('index.html', **context)


@app.route("/dodaj_punkt", methods=['POST', 'GET'])
@auth.login_required
def dodaj_punkt():
    db.get_db()
    USER_ID = session.get('user_id', None)

    #    mozliwe_punkty = [0, 1, 3]
    if request.method == 'POST':
        try:
            nowe_punkty = int(request.form['liczba_punktow'])
            if nowe_punkty > 0:
                data_access.add_points(USER_ID, nowe_punkty)
                # uczen = data_access.wczytaj_dane()
                # uczen["punkty"] += nowe_punkty
                # data_access.zapisz_dane(uczen)
        except Exception as e:
            pass

    return redirect(url_for('hello'))


@app.route("/wykorzystanie_punktow", methods=['POST', 'GET'])
@auth.login_required
def wykorzystaj_punkty():
    if request.method == 'POST':
        # TODO: zaimplementować wykorzystywanie punktów
        return redirect(url_for('hello'))


@app.route("/ban")
@auth.login_required
def daj_bana():
    db.get_db()
    USER_ID = session.get('user_id', None)

    ten_minutes = 10
    data_access.give_ban(USER_ID, ten_minutes)
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run()
