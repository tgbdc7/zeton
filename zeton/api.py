from flask import Blueprint, session, request, redirect, url_for

import auth
import data_access
import db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route("/dodaj_punkt", methods=['POST'])
@auth.login_required
def dodaj_punkt():
    db.get_db()
    USER_ID = session.get('user_id', None)

    try:
        nowe_punkty = int(request.form['liczba_punktow'])
    except ValueError as ex:
        print(ex)
    else:
        if nowe_punkty > 0:
            data_access.add_points(USER_ID, nowe_punkty)
    finally:
        return redirect(url_for('views.index'))


@bp.route("/wykorzystanie_punktow", methods=['POST', 'GET'])
@auth.login_required
def wykorzystaj_punkty():
    if request.method == 'POST':
        # TODO: zaimplementować wykorzystywanie punktów
        return redirect(url_for('views.index'))


@bp.route("/ban")
@auth.login_required
def daj_bana():
    db.get_db()
    USER_ID = session.get('user_id', None)

    ten_minutes = 10
    data_access.give_ban(USER_ID, ten_minutes)
    return redirect(url_for('views.index'))
